import smbus
import time
import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
bus=smbus.SMBus(1)
address=0x53 
x_adr=0x32
y_adr=0x34
z_adr=0x36
sensor=[]
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
        params['text'] = '현장에 진동이 감지되었습니다. 안전한 곳으로 대피 후 확인해주세요.' # Message
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
        sys.exit()
        
def init_ADXL345():
    bus.write_byte_data(address,0x2D,0x08)
def measure_acc(adr):
    acc0=bus.read_byte_data(address,adr)
    acc1=bus.read_byte_data(address,adr+1)
    acc=(acc1<<8)+acc0
    if acc>0x1FF:
        acc=(65536-acc)*-1
        acc=acc*3.9/1000
        return acc
try:
    init_ADXL345()
    while 1:
        x_acc=measure_acc(x_adr)
        y_acc=measure_acc(y_adr)
        z_acc=measure_acc(z_adr)
        print(x_acc,y_acc,z_acc)
        if x_acc!=None or y_acc!=None or z_acc!=None:
            sms()
            break
        time.sleep(0.5)
        
except KeyboardInterrupt:
    pass
