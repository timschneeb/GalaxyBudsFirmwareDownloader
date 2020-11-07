# License: GPL-3.0
# Author: @ThePBone
# 11/07/2020

import requests
import xmltodict
import argparse
import re

sm_r140 = {
    "retail": ["FOTA", "Production"],
    "qa": ["FOTA-QA", "Quality assurance"],
    "cradle": ["CRADLE", "Retail cradle"],
}

sm_r17x = {
    "retail": ["FOTA", "Production"],
    "qa": ["FOTA-QA", "Quality assurance"],
    "dummy": ["FOTA-DUMMY", "Dummy XML response"],
}


def get_types(device):
    types = {}
    if device == "sm-r140":
        types = sm_r140
    elif device == "sm-r170" or device == "sm-r175":
        types = sm_r17x
    else:
        print("Unknown hardware ID")
        exit(1)
    return types


def list_types(args):
    types = get_types(str(args.device[0]).lower())
    print("Available firmware types for {}:".format(str(args.device[0]).upper()))
    for key, value in types.items():
        print("  {} ({})".format(key, value[1]))


def build_url(device, fw_type):
    types = get_types(device.lower())
    return "https://wsu-dms.samsungdm.com/common/support/firmware/downloadUrlList.do?prd_mdl_name={}{}&loc=global".format(
        device.upper(), types[fw_type][0])


def entrypoint():
    parser = argparse.ArgumentParser(description='Download firmware images for Buds(+) device from Samsung\'s update '
                                                 'servers')
    parser.add_argument('device', metavar='device', type=str, nargs=1,
                        help='Device hardware ID (SM-R140 = IconX, SM-R170 = Buds, SM-R175 = Buds+)')
    parser.add_argument('-t', '--type', type=str, help="Select firmware type (default = retail)")
    parser.add_argument('-l', '--list-types', action='store_true', help="Print available types for a specific device")
    args = parser.parse_args()

    if args.list_types:
        list_types(args)
        exit(0)

    types = get_types(str(args.device[0]).lower())
    if not args.type in types:
        print("Unknown firmware type. You can list all available types using -l")
        exit(1)

    xml_url = build_url(args.device[0], args.type)
    resp = requests.get(xml_url)

    if "XML file not found" in str(resp.content):
        print("Server error: No firmware found")
        exit(1)

    try:
        xml_data = xmltodict.parse(resp.content)
        root = xml_data["FirmwareInfo"]
        fw_version = root["FWVersion"]
        fw_url = root["DownloadURL"]

        raw_changelog = root["Description"].partition("<ENG>")[2].partition("</ENG>")[0]
        if "<ENG>" in raw_changelog or raw_changelog == "":
            changelog = str(root["Description"]).replace("<![CDATA[", "").replace("]]>", "")
        else:
            changelog = raw_changelog.lstrip()

        print("Found firmware: {}".format(fw_version))
        print("Changelog:\n{}".format(changelog))

        raw_filename = re.search('&file=(.*).bin', fw_url)
        if raw_filename is None:
            filename = fw_version
        else:
            filename = raw_filename.group(1)

        if args.type != "retail":
            filename += "_" + str(args.type).upper()
        filename += ".bin"

        raw_fw = requests.get(fw_url)
        with open(filename, 'wb') as f:
            f.write(raw_fw.content)

        print("Firmware image written to '{}'".format(filename))
    except:
        print("Failed to parse XML data. Dumping server response:")
        print(resp.content)
        exit(1)


if __name__ == '__main__':
    entrypoint()
