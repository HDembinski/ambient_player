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

Speaker test:

```sh
speaker-test -t wav -c 2
```
