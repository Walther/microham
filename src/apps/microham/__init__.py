import binascii
import os
import time

import buttons
import display
import machine
import neopixel
import system
import utime
import version
import wifi
import term


# the badge has the umqtt.robust2 library renamed in this way
# to keep the support for legacy umqtt some apps depend on
from umqtt2.robust2 import MQTTClient

SERVER = "test.mosquitto.org"
CLIENT_ID = board_id = "{}".format(
    binascii.hexlify(machine.unique_id()).decode("ascii"))
NICKNAME = machine.nvs_getstr("owner", "name")
# change base_topic to disobey, or clean up one level when we have a custom server
BASE_TOPIC = "walthertest"
CHANNEL = 0


class microham:
    """microham: a virtual amateur radio client, using MQTT"""

    def __init__(self):
        """Initialize the microham client. Connect wifi, connect MQTT, subscribe to default channel."""
        display.drawFill(0x000000)
        display.drawText(0, 0, "microham starting", 0xFFFFFF, "7x5")
        display.drawText(0, 8, CLIENT_ID, 0xFFFFFF, "7x5")
        display.flush()

        # wifi connection
        wifi.connect()
        if not wifi.wait():
            print("wifi error")
            display.drawText(0, 16, "wifi error", 0xFFFFFF, "7x5")
        else:
            print("wifi connected")
            display.drawText(0, 16, "wifi connected", 0xFFFFFF, "7x5")
        display.flush()

        # umqtt client
        self.client = MQTTClient(CLIENT_ID, SERVER)
        self.client.DEBUG = True
        self.client.set_callback(self.sub_cb)
        self.client.KEEP_QOS0 = False
        self.client.NO_QUEUE_DUPS = True
        self.client.MSG_QUEUE_MAX = 2
        self.client.set_callback(self.sub_cb)

        self.channel = CHANNEL  # Channel number, int
        # Wildcard subscribe to channel's topics; subtopics are userIDs
        self.topic = b"{}/{}/#".format(BASE_TOPIC, self.channel)

        if not self.client.connect(clean_session=True):
            self.client.subscribe(self.topic)

        print("mqtt started")
        display.drawText(0, 24, "mqtt started", 0xFFFFFF, "7x5")
        display.flush()
        utime.sleep_ms(1000)
        self.clear()

    def channel_up(self, pressed=True):
        """Switch the channel to one number higher. Causes a reconnect to the MQTT server."""
        if pressed:
            self.channel = self.channel + 1
            self.exclusive_subscribe()
            self.clear()

    def channel_down(self, pressed=True):
        """Switch the channel to one number lower. Causes a reconnect to the MQTT server."""
        if pressed:
            self.channel = self.channel - 1
            self.exclusive_subscribe()
            self.clear()

    def exclusive_subscribe(self):
        """Manually disconnect, connect, and subscribe. Workaround for the library not supporting unsubscribe."""
        self.topic = b"{}/{}/#".format(BASE_TOPIC, self.channel)
        self.client.disconnect()
        self.client.connect(clean_session=True)
        self.client.subscribe(self.topic)

    def sub_cb(self, topic, msg, retain, dup):
        """Handle an incoming message from the MQTT server, format and display it."""
        message = msg.decode('ascii')
        topic = topic.decode('ascii')
        # walthertest/channelname/username, and add colon
        username = topic.split("/")[2] + ':'
        print(username)
        print(message)
        self.clear()
        display.drawText(0, 8, username, 0xFFFFFF, "7x5")
        display.drawText(0, 16, message, 0xFFFFFF, "7x5")  # TODO: wrap/scroll?
        display.flush()

    def clear(self):
        """Clear the screen and draw the current channel number."""
        display.drawFill(0x000000)
        display.drawText(0, 0, "microham channel {}".format(
            self.channel), 0xFFFFFF, "7x5")
        display.flush()
        print("microham channel {}".format(self.channel))

    def send_message(self, pressed=True):
        """Blocking call. Prompt for a message via serial input, send the message to MQTT server"""
        if pressed:
            if self.client.is_conn_issue():
                self.client.reconnect()
            term.clear()
            self.clear()
            topic = "{}/{}/{}".format(BASE_TOPIC, self.channel, NICKNAME)
            display.drawText(0, 8, "transmitting...", 0xFFFFFF, "7x5")
            display.flush()
            # prompt is a blocking call, waits here for the message
            message = term.prompt("message:", 0, 1)
            if len(message) > 0:
                self.client.publish(topic, message)
                self.client.send_queue()
                print("\nmessage sent")
                display.drawText(0, 16, "message sent", 0xFFFFFF, "7x5")
            # wait and clear
            utime.sleep_ms(500)
            self.clear()

    def main(self):
        """The main refresh loop for microham."""
        while True:
            utime.sleep_ms(500)
            if self.client.is_conn_issue():
                self.client.reconnect()
            self.client.check_msg()
            self.client.send_queue()

        # end
        self.client.disconnect()


m = microham()
buttons.attach(buttons.BTN_A, m.send_message)
buttons.attach(buttons.BTN_UP, m.channel_up)
buttons.attach(buttons.BTN_DOWN, m.channel_down)
m.main()
