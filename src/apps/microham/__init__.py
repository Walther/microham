import binascii
import os
import time

import display
import machine
import neopixel
import system
import utime
import version
import wifi
import term


from umqtt2.robust2 import MQTTClient

BLOCKING_METHOD = False
SERVER = "test.mosquitto.org"
CLIENT_ID = board_id = "{}".format(
    binascii.hexlify(machine.unique_id()).decode("ascii"))
NICKNAME = machine.nvs_getstr("owner", "name")
# change base_topic to disobey, or clean up one level when we have a custom server
BASE_TOPIC = "walthertest"
CHANNEL = "0"


# print function for the received messages
def sub_cb(topic, msg, retain, dup):
    message = msg.decode('ascii')
    topic = topic.decode('ascii')
    print("{}".format(topic))
    print(message)
    display.drawFill(0x000000)
    display.drawText(0, 0, "microham", 0xFFFFFF, "7x5")
    display.drawText(0, 8, topic, 0xFFFFFF, "7x5")
    display.drawText(0, 16, message, 0xFFFFFF, "7x5")
    display.flush()


def main():

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
        display.drawText(0, 16, "wifi success", 0xFFFFFF, "7x5")
    display.flush()

    # umqtt

    c = MQTTClient(CLIENT_ID, SERVER)
    # Print diagnostic messages when retries/reconnects happens
    c.DEBUG = True
    c.set_callback(sub_cb)
    # Information whether we store unsent messages with the flag QoS==0 in the queue.
    c.KEEP_QOS0 = False
    # Option, limits the possibility of only one unique message being queued.
    c.NO_QUEUE_DUPS = True
    # Limit the number of unsent messages in the queue.
    c.MSG_QUEUE_MAX = 2
    c.set_callback(sub_cb)

    # topic = b"{}/{}/#".format(BASE_TOPIC, CHANNEL)
    topic = b"walthertest/0/#"
    print(topic)

    if not c.connect(clean_session=True):
        print("New MQTT Session")
        display.drawText(0, 24, "New MQTT Session", 0xFFFFFF, "7x5")
        # Wildcard subscribe to channel's topics; subtopics are userIDs
        c.subscribe(topic)

    print("mqtt started")
    display.drawText(0, 24, "mqtt started", 0xFFFFFF, "7x5")
    display.flush()

    SEND_MODE = False

    while True:  # main loop

        while not SEND_MODE:
            utime.sleep_ms(500)
            if c.is_conn_issue():
                c.reconnect()
            c.check_msg()
            c.send_queue()

        while SEND_MODE:
            if c.is_conn_issue():
                c.reconnect()
            term.clear()
            topic = "{}/{}/{}".format(BASE_TOPIC, CHANNEL, NICKNAME)
            display.drawFill(0x000000)
            display.drawText(0, 0, "microham sending to", 0xFFFFFF, "7x5")
            display.drawText(0, 8, topic, 0xFFFFFF, "7x5")
            display.flush()
            # prompt is blocking, waits here instead of looping
            message = term.prompt("Message:", 0, 1)
            if len(message) > 0:
                c.publish(topic, message)
                c.send_queue()
                print("\nMessage sent")
                SEND_MODE = False
            utime.sleep_ms(500)

    # end
    c.disconnect()


if __name__ == '__main__':
    main()
