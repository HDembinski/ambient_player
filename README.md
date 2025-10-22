# Ambient-Player

## Setup on the RaspberryPI

Replace the USER to your username and PATH in `ambient_player.service` to this project path.

Copy the file `ambient_player.service` to `/etc/systemd/system/`

Reload systemd to recognize the new service:

```sh
sudo systemctl daemon-reload
```

Enable the service to start on boot:

```sh
sudo systemctl enable mywebserver.service
```

Start the service now:

```sh
sudo systemctl start mywebserver.service
```

Check the status:

```sh
sudo systemctl status mywebserver.service
```
