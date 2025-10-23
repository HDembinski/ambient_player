# Ambient-Player

## Setup on the RaspberryPI

### Systemd Service

Replace in `ambient_player.service`

- USER with your username
- PATH to this project path
- USERID with your user ID (`id -u USER`)

Copy the file `ambient_player.service` to `/etc/systemd/system/`

Reload systemd to recognize the new service:

```sh
sudo systemctl daemon-reload
```

Enable the service to start on boot:

```sh
sudo systemctl enable ambient_player.service
```

Start the service now:

```sh
sudo systemctl start ambient_player.service
```

Check the status:

```sh
sudo systemctl status ambient_player.service
```

### Bluetooth connection

```sh
sudo apt-get update
sudo apt-get install bluez pulseaudio pulseaudio-module-bluetooth
```

```sh
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```

```sh
bluetoothctl
```

Once inside `bluetoothctl`, run these commands:

1. Power on the Bluetooth adapter:

```sh
   power on
```

2. Enable the agent and set it as default:

```sh
   agent on
   default-agent
```

3. Turn on discovery mode:

```sh
   scan on
```

4. Wait for your speaker to appear. You'll see output like:

```sh
   [NEW] Device AA:BB:CC:DD:EE:FF Speaker Name
```

Note the MAC address (AA:BB:CC:DD:EE:FF).

5. Stop scanning:

```sh
   scan off
```

6. Pair with the device:

```sh
   pair AA:BB:CC:DD:EE:FF
```

7. Trust the device (so it auto-connects in the future):

```sh
   trust AA:BB:CC:DD:EE:FF
```

8. Connect to the device:

```sh
   connect AA:BB:CC:DD:EE:FF
```

9. Exit bluetoothctl:

```sh
   exit
```

10. Set audio device as default sink for pulse-audio:

```sh
# get list of sinks
pactl list short sinks
# set the default sink
pactl set-default-sink <sink_name>
```

11. Speaker test

```sh
speaker-test -t wav -c 2
```
