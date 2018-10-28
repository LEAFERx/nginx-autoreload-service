# Nginx Autoreload Service

## Prerequisites

- OS support systemd
- Python 3
- [pyinotify](https://pypi.org/project/pyinotify/) installed

## Usages

- change paths in nginx-autoreload.py and nginx-autoreload.service and make configurations
- copy nginx-autoreload.service to `/etc/systemd/system/`
- run command
  ```sh
  sudo systemctl daemon-reload
  sudo systemctl start nginx-autoreload.service
  ```