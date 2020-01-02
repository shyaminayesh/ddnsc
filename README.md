# ddnsc v1.0.0

Just another simple & lightweight client to update DNS dynamically. Written in python with easy way of supporting new service providers with REST API.


## Requirements

 - Python v3 or later
   - python-systemd
   - python-requests


## Supported Services

|     NAME     |  SITE                      |         STATUS        |
|--------------|:--------------------------:|:----------------------|
| CloudFlare   |  [LINK](//cloudflare.com)  |  :large_blue_circle:  |
| DreamHost    |  [LINK](//dreamhost.com)   |  :red_circle:         |


## Installation

ddnsc support few linux package managers to make it easy to install.

| DISTRO         |  REPO                                          |  VERSION  |
|----------------|------------------------------------------------|:---------:|
|  Arch          | [aur](//aur.archlinux.org/packages/ddnsc)      | v1.0.0    |

## Configuration

Multiple DNS providers, domains, and hosts/subdomains are supported. The configuration file has the following format:

```
[global]
intervel=300
use=web

[example.com]
provider=LuaDNS
email=EMAIL
key=KEY
hosts=@,blah,bazz
ttl=200

[bar.com]
provider=LuaDNS
email=EMAIL
key=KEY
hosts=@,foo
ttl=600
```

The `global` section is required, and an arbitrary number of subsequent sections after that are supported where each section title is the zone/domain to update. Hosts/subdomains to update are listed under each section. The `@` denotes updating the zone/domain itself. If the `@` were omitted from the `[example.com]` section in the example above, then only the A records for blah.example.com and bazz.example.com would be updated, and the A record for `example.com` would *not* be updated.
