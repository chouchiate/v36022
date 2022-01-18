#!/usr/bin/env python3

from pathlib import Path
import argparse as ap
import ctypes as ct
import time
import esptool


STR_MAX_SIZE = 64

class FactoryData(ct.Structure):

    _pack_ = 1
    _fields_ = [
        ('sku', ct.c_char * STR_MAX_SIZE),
        ('sn_radar', ct.c_char * STR_MAX_SIZE),
        ('sn_product', ct.c_char * STR_MAX_SIZE),
        ('hw_rev_radar', ct.c_char * STR_MAX_SIZE),
        ('hw_rev_product', ct.c_char * STR_MAX_SIZE),
        ('burn_time', ct.c_char * STR_MAX_SIZE),
    ]


def validate_arg(arg):
    if len(arg) > 32:
        raise ap.ArgumentTypeError(f'exceeded maximum length of 32')
    return arg


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('sku', type=validate_arg, help='SKU (example: WH2BAUS01)')
    parser.add_argument('sn_radar', type=validate_arg, help='SN of radar (example: BLUGBC0Q013S00000000000000000001)')
    parser.add_argument('sn_product', type=validate_arg, help='SN of product (example: VXTAA2013S0000000000000000000001)')
    parser.add_argument('hw_rev_radar', type=validate_arg, help='hardware revision of radar (xxxxxxxxxxxxxxxx (x=0~9, decimal))')
    parser.add_argument('hw_rev_product', type=validate_arg, help='hardware revision of product (xxxxxxxxxxxxxxxx (x=0~9, decimal))')
    args, esptool_args = parser.parse_known_args()

    args = {k: v.encode() for k, v in vars(args).items()}
    factory_data = FactoryData(**args, burn_time=time.asctime().encode())

    factory_data_file = Path(__file__).resolve().parent / 'factory_data.bin'
    factory_data_file.write_bytes(factory_data)
    esptool_cmd = esptool_args + ['write_flash', '0x9000', str(factory_data_file)]
    print(*esptool_cmd)
    esptool.main(esptool_cmd)
    factory_data_file.unlink()
