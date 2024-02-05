# Xiaomi Thermometers (lywsd03mmc)

Reading Xiaomi Thermometers data using BLE to use in something else.

![picture](LYWSD03MMC.jpg)

Where I start:
  * [This video](https://youtu.be/ExFxuvfCbAU?si=BxsuaZ9HShyMFUsc) give me an Idea
  * [His example](https://github.com/VolosR/XiaomiBLE) can explain how to convert from bytes to readable values (temperature, humidity, battery and its percentage)
  * [This project](https://github.com/keks51/lywsd03mmc-client) is very good in expaining of how to get values, but on my MacBook 2020 M1 Pro it is always run to **segmentation fault**
  * [Bleak](https://github.com/hbldh/bleak/tree/master) itself: I've used its examples to locate my device

## Quick start

Use [discover.py](https://github.com/hbldh/bleak/blob/master/examples/discover.py) from ```bleak/examples``` to locate all available devices around you. You will get something like this:
```
A093B113-0263-25E8-608D-0A7D3024FAF7: LYWSD03MMC
------------------------------------------------
AdvertisementData(local_name='LYWSD03MMC', service_data={'0000fe95-0000-1000-8000-00805f9b34fb': b'0X[\x05GG\xa9\xbc8\xc1\xa4\x08'}, rssi=-71)
```

Now use ```python3 service_explorer.py --address A093B113-0263-25E8-608D-0A7D3024FAF7 --services ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6``` with [service_explorer.py](https://github.com/hbldh/bleak/blob/master/examples/service_explorer.py); where ```--address``` is quite the same as you get before and ```--services``` are the key I get from ESP32 example. Please, note that devices have names started with "LYWSD0..." (saw it in YT-video). The result will be like this:
```
2024-02-04 22:58:22,571 __main__ INFO: starting scan...
2024-02-04 22:58:30,957 __main__ INFO: connecting to device...
2024-02-04 22:58:34,103 __main__ INFO: connected
2024-02-04 22:58:34,103 __main__ INFO: [Service] ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 33): Unknown
2024-02-04 22:58:34,133 __main__ INFO:   [Characteristic] ebe0ccb7-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 34): Unknown (read,write), Value: bytearray(b'i\xef\r\x03')
2024-02-04 22:58:34,207 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 36): Characteristic User Description, Value: bytearray(b'Time')
2024-02-04 22:58:34,238 __main__ INFO:   [Characteristic] ebe0ccb9-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 37): Unknown (read), Value: bytearray(b'\x997\x00\x00\x9b\x0e\x00\x00')
2024-02-04 22:58:34,268 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 39): Characteristic User Description, Value: bytearray(b'Data Count')
2024-02-04 22:58:34,298 __main__ INFO:   [Characteristic] ebe0ccba-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 40): Unknown (read,write), Value: bytearray(b'\x00\x00\x00\x00')
2024-02-04 22:58:34,328 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 42): Characteristic User Description, Value: bytearray(b'Index')
2024-02-04 22:58:34,358 __main__ INFO:   [Characteristic] ebe0ccbb-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 43): Unknown (read), Value: bytearray(b'\x997\x00\x00\xa0\xe5\r\x03\xef\x00,\xee\x00,')
2024-02-04 22:58:34,388 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 45): Characteristic User Description, Value: bytearray(b'Data Read')
2024-02-04 22:58:34,388 __main__ INFO:   [Characteristic] ebe0ccbc-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 46): Unknown (notify)
2024-02-04 22:58:34,418 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 48): Characteristic User Description, Value: bytearray(b'Data Notify')
2024-02-04 22:58:34,448 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 49): Client Characteristic Configuration, Value: bytearray(b'')
2024-02-04 22:58:34,478 __main__ INFO:   [Characteristic] ebe0ccbe-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 50): Unknown (read,write), Value: bytearray(b'\x00')
2024-02-04 22:58:34,508 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 52): Characteristic User Description, Value: bytearray(b'Temperature Uint')
2024-02-04 22:58:34,538 __main__ INFO:   [Characteristic] ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 53): Unknown (read,notify), Value: bytearray(b'Y\t+\x9a\n')
2024-02-04 22:58:34,598 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 55): Characteristic User Description, Value: bytearray(b'Temperature and Humidity')
2024-02-04 22:58:34,628 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 56): Client Characteristic Configuration, Value: bytearray(b'\x00')
2024-02-04 22:58:34,658 __main__ INFO:   [Characteristic] ebe0ccc4-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 57): Unknown (read), Value: bytearray(b'd')
2024-02-04 22:58:34,688 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 59): Characteristic User Description, Value: bytearray(b'Batt')
2024-02-04 22:58:34,688 __main__ INFO:   [Characteristic] ebe0ccc8-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 60): Unknown (write)
2024-02-04 22:58:34,718 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 62): Characteristic User Description, Value: bytearray(b'disconnect')
2024-02-04 22:58:34,718 __main__ INFO:   [Characteristic] ebe0ccd1-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 63): Unknown (write)
2024-02-04 22:58:34,748 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 65): Characteristic User Description, Value: bytearray(b'clear data')
2024-02-04 22:58:34,778 __main__ INFO:   [Characteristic] ebe0ccd7-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 66): Unknown (read,write), Value: bytearray(b'\x8c\nl\x07U\x14')
2024-02-04 22:58:34,838 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 68): Characteristic User Description, Value: bytearray(b'comfortable temp and humi')
2024-02-04 22:58:34,838 __main__ INFO:   [Characteristic] ebe0ccd8-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 69): Unknown (write)
2024-02-04 22:58:34,868 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 71): Characteristic User Description, Value: bytearray(b'set conn interval')
2024-02-04 22:58:34,868 __main__ INFO:   [Characteristic] ebe0ccd9-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 72): Unknown (write,notify)
2024-02-04 22:58:34,898 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 74): Characteristic User Description, Value: bytearray(b'para_value_get')
2024-02-04 22:58:34,928 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 75): Client Characteristic Configuration, Value: bytearray(b'')
2024-02-04 22:58:34,958 __main__ INFO:   [Characteristic] ebe0cff1-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 76): Unknown (read,write), Value: bytearray(b'\x00')
2024-02-04 22:58:34,988 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 78): Characteristic User Description, Value: bytearray(b'fun switch')
2024-02-04 22:58:34,988 __main__ INFO: disconnecting...
2024-02-04 22:58:34,990 __main__ INFO: disconnected
```
_In case of changing UUID of the service, you can always find it by remove --services parameter and read long output to find values_

Actually we need only one: ```[Characteristic] ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6 (Handle: 53): Unknown (read,notify), Value: bytearray(b'Y\t+\x9a\n')``` which can be translated with easy:
```
temp = round((inputbyte[0] | inputbyte[1] << 8) * 0.01,  1)
humd = inputbyte[2]
batt = round((inputbyte[3] | inputbyte[4] << 8) * 0.001, 2)
perc = min(int(round((batt - 2.1), 2) * 100), 100)
```

And this is all.

## Battery during testing

I think this IS **the big problem** if you want to request values friequently - the batter will die very fast (a month maybe). So use 10 minutes or so between requests. 

## Timeouts

Each request have to wait up to a minute to receive values so think about timeout of the operation.
