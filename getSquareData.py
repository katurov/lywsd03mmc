#!/opt/homebrew/bin/python3.11

'''
    GET_TEMP_AND_HUMIDITY_ATTRIBUTE_UUID = 'EBE0CCC1-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_BATTERY_ATTRIBUTE_UUID = 'EBE0CCC4-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_OR_SET_UNITS_ATTRIBUTE_UUID = 'EBE0CCBE-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_OR_SET_TIMESTAMP_ATTRIBUTE_UUID = 'EBE0CCB7-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_OR_SET_FIRST_HISTORY_RECORD_IDX_ATTRIBUTE_UUID = 'EBE0CCBA-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_LAST_CALC_AND_NEXT_IDX_ATTRIBUTE_UUID = 'EBE0CCB9-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_HISTORY_DATA_ATTRIBUTE_UUID = 'EBE0CCBC-7A0A-4B0C-8A1A-6FF2997DA3A6'
    GET_LAST_CALC_DATA_ATTRIBUTE_UUID = 'EBE0CCBB-7A0A-4B0C-8A1A-6FF2997DA3A6'

'''

import argparse
import asyncio
import logging
import json

from bleak import BleakClient, BleakScanner

logger = logging.getLogger(__name__)


async def fetchValuesDevice(address, services, characteristics):

    logger.info("starting scan...")

    device = await BleakScanner.find_device_by_address( address, timeout=60.0 )
    if device is None:
        logger.error("could not find device with address '%s'", address)
        return

    logger.info("connecting to device...")

    async with BleakClient( device, services=services ) as client:
        logger.info("connected")
        readvalue = await client.read_gatt_char(characteristics)
        logger.info("disconnecting...")

    logger.info("disconnected")

    return ( readvalue )

def decodeValues ( inputbyte ) :
    try :
        temp = round((inputbyte[0] | inputbyte[1] << 8) * 0.01,  1)
        humd = inputbyte[2]
        batt = round((inputbyte[3] | inputbyte[4] << 8) * 0.001, 2)
        perc = min(int(round((batt - 2.1), 2) * 100), 100)

        return ( temp, humd, batt, perc )
    except :
        logger.error("could not decode bytes")
        return None

if __name__ == "__main__":
    log_level = logging.ERROR # or INFO if you would like to read a lot
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    parser = argparse.ArgumentParser()
    device_group = parser.add_mutually_exclusive_group(required=True)
    device_group.add_argument( "--address", metavar="<address>", help="the address of the bluetooth device to connect to" )
    args = parser.parse_args()

    # address="A093B113-0263-25E8-608D-0A7D3024FAF7"
    r = asyncio.run(fetchValuesDevice( address=args.address, services=["ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6"], characteristics="ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"  ))

    #logger.info( decodeValues(r) )
    stv = decodeValues(r)
    if stv is None :
        print( json.dumps( {"text" : "NaN", "background_color" : "255,0,0,255", "font_color" : "0,0,0,255", "font_size" : 10} ) )
    else :
        print( json.dumps( {"text" : "{}\n{}\n{}  {}%".format(stv[0],stv[1],stv[2],stv[3]), "background_color" : "255,218,185,255", "font_color" : "0,0,0,255", "font_size" : 8} ) )