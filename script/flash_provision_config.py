#!/usr/bin/env python3

from pathlib import Path
import argparse as ap
import json
import esptool


CWD = Path(__file__).resolve().parent


def flash_provision_config(json_cfg_path):
    esptool_cmd = ['write_flash', '0xa000', str(json_cfg_path)]
    print(*esptool_cmd)
    esptool.main(esptool_cmd)


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('json_cfg', type=Path, help='path/to/json/config')
    args = parser.parse_args()
    flash_provision_config(args.json_cfg)
