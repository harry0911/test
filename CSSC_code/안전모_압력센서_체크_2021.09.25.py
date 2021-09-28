#!/usr/bin/env python
import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException



import spidev
import time
import os
def sms():
    ## @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
    if __name__ == "__main__":
        # set api key, api secret
        api_key = "NCSUQC7X8QD6JT1M"
        api_secret = "G9BYFAOQ7CXYJ5KC6ZCY2QY0SGGITPTR"
        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = '01086031048' # Recipients Number '01000000000,01000000001'
        params['from'] = '01086031048' # Sender number
        params['text'] = '1번 작업자가 안전모를 미착용했습니다.' # Message
        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])
        
            if "error_list" in response:
                print("Error List : %s" % response['error_list'])
        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
        
Vcc = 5.0
R1 = 1000
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Calculate fsr402 registor value
def fsr420_Registor(voltage):
    R = (R1 * Vcc)/voltage - R1
    return R
 
def ReadChannel(channel):
#  adc = spi.xfer2([1,(8+channel)<<4,0])
    adc = spi.xfer([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
 
# Define sensor channels(SS01)
mcp3008_channel = 0
 
# Define delay between readings
delay = 0.01
f = open('fsr402-2.dat', 'w') 
index = 0
 
try: 
    while True:
        analog_level = ReadChannel(mcp3008_channel)
        Vout = analog_level * Vcc / 1024.0
        if(Vout < 2.2):
            Vout = 0.001
            Rfsr = 5000000
            analog_level = 100
        else:
            Rfsr = fsr420_Registor(Vout)
        #print("Digital:", analog_level, " Voltage:", Vout, " R(K Ohm):", Rfsr / 1000.0)
        data = "{} {} {} {}\n".format(index, analog_level, Vout, Rfsr / 1000.0)
        f.write(data)
        time.sleep(delay)
        index += 1

        if analog_level==100:
            print("helmet on")

        else:
            print("helmet off")
            sms()
 
except KeyboardInterrupt:   
    print("Now Exit")
    f.close()
