# microham

Virtual amateur radio for Disobey 2020 badge.

## Development

- Dev env setup: <https://lemariva.com/blog/2019/08/micropython-vsc-ide-intellisense>
- Directory structure is intentional for IDE & badge integration purposes
  - The `src/apps/microham` directory contains all the actual application code
  - The `server` directory contains an optional dev server for local development purposes
- You probably need to edit the `pymakr.conf` - check which address your badge is available at


## Scratchpad

- Final goal: cross-badge ham radio with voice channels
- Test server: using `test.mosquitto.org`
- Channel topology with the topics: `walthertest/[channelnumber]/[nickname]`.
- By default, the badges listen to topic `walthertest/0/#` wildcard, and they see nicknames as subtopics.

- [x] Connect to a test MQTT server
- [x] Receive messages sent to a topic
- [x] Send messages to a topic
- [ ] Switch the topic you're subscribed to
- [ ] Serial interface / UI for text chat instead of audio
- [ ] Audio messages from the badge
- [ ] Set up Disobey MQTT server
- [ ] Clean up the topic channel levels