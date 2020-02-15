# microham

**Virtual amateur radio for the Disobey 2020 badge.**

When you start up `microham`, the badge connects to a virtual radio service. On startup, it joins the channel 0. You can switch channels with the `UP` and `DOWN` buttons.

Pressing the `A` button gets you into transmission mode. Currently, this requires USB Serial connection to be present. You are presented with a prompt to type your message into. When you press enter, the message will be sent.

Any badges that are listening on the same channel will display the sender's nickname and message. Your own badge will also display the message you just sent.

The messaging service is ephmeral, kind of like amateur radio. If you are not on a specific channel, you cannot see the backlog of messages by joining later.

Please note that there is zero expectation of privacy, security or trust on the service. Please also note that there are no challenges, flags or targets on the virtual amateur radio service, it is provided for visitor amusement and convenience only.

## Implementation details

- MQTT server: currently using `disobey.hilla.io`
- Channels are implemented with topics: topic topology is `[channelnumber]/[nickname]`
- By default, the badges subscribe to the topic `0/#` (note the wildcard!)
- When a badge sends a message, it gets sent to a subtopic with the nickname
- This subtopic is then used to show the nickname of the sender of the message

## Development

- You'll need the Disobey 2020 badge
- You'll need a regular micro-USB cable with data pins available (a charging cable will not work)
- Dev env setup: <https://lemariva.com/blog/2019/08/micropython-vsc-ide-intellisense>
- The directory structure is intentional for IDE & badge integration purposes
  - The `src/apps/microham` directory contains all the actual application code
- Connect your badge to your computer via usb. Find where the serial port is abailable at - is it a `/dev/tty`, is it a `/dev/cu.usbserial`, or something else?
- Edit the `pymakr.conf` of your IDE integration to make sure it can connect to the badge

## TODO

- [x] Connect to a test MQTT server
- [x] Receive messages sent to a topic
- [x] Send messages to a topic
- [x] Switch the topic you're subscribed to
- [x] Serial interface / UI for text chat instead of audio
- [ ] Audio messages from/to the badge
- [x] Set up Disobey MQTT server
- [x] Clean up the topic channel levels
- [ ] Better error handling and user-friendly output on the display

