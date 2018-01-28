# Lantern

## Description

Asyncio TCP-client for lantern with 3 commands: ON, OFF and COLOR.

Also there is a simple [server](https://github.com/pomidoroshev/lantern/blob/master/lantern_tcp/server.py)

## Requirements

- Python 3.6
- [xtermcolor](https://github.com/broadinstitute/xtermcolor) (included in package)

## Installation

```
$ pip install git+https://github.com/pomidoroshev/lantern.git
```

## Usage

```
$ lantern -h
usage: lantern [-h] [host] [port]

Lantern TCP Client

positional arguments:
  host        Server host, default is 127.0.0.1
  port        Server port, default is 9999

optional arguments:
  -h, --help  show this help message and exit
```

You can also test lantern behavior with demo-server, just run it in another terminal window:

```
$ lantern_server -h
usage: lantern_server [-h] [host] [port]

Lantern TCP Server

positional arguments:
  host        Server host, default is 127.0.0.1
  port        Server port, default is 9999

optional arguments:
  -h, --help  show this help message and exit
```

## Screenshot
![Lantern](https://github.com/pomidoroshev/lantern/blob/master/screenshot.png)

## Adding new commands

If you want to add a new external command, e.g. `BLINK` with `type = 0x30`, you should add a method to [`LanternProtocol`](https://github.com/pomidoroshev/lantern/blob/master/lantern_tcp/lantern.py) decorated with `@cmd`:

```python
@cmd(0x30)
def blink(self):
    ...
```
