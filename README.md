# Firmware Downloader
Download firmware images for Buds(+) devices from Samsung's official servers

## Prerequisites

You need to install a few python dependencies:
```
sudo pip install requests xmltodict
```

## Usage

Currently supports IconX (SM-R140), Buds (SM-R170) and Buds+ (SM-R175).

Available parameters:
```
❯ python fw_downloader.py --help
usage: fw_downloader.py [-h] [-t TYPE] [-l] device

Download firmware images for Buds(+) device from Samsung's update servers

positional arguments:
  device                Device hardware ID (SM-R140 = IconX, SM-R170 = Buds, SM-R175 = Buds+)

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  Select firmware type (default = retail)
  -l, --list-types      Print available types for a specific device
```

List available firmware types for Buds+ devices:
```
❯ python fw_downloader.py --list-types sm-r175
Available firmware types for SM-R175:
  retail (Production)
  qa (Quality assurance)
  dummy (Dummy XML response)
```

Download the default retail firmware image for Buds+ devices:
```
❯ python fw_downloader.py --type retail sm-r175
Found firmware: R175XXU0ATH7
Changelog:
• Improved system stability and reliability

Firmware image written to 'FOTA_R175XXU0ATH7.bin'
```
