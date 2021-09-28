import tensorflow.keras
import numpy as np
import cv2
import pygame
import time

import requests
import json
import datetime

import time



import RPi.GPIO as GPIO

capture = cv2.VideoCapture(-1)


GPIO.setmode(GPIO.BCM)
#


pirPin = 7

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)
te=0
#te=1
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.
while True:
    while True:

        if GPIO.input(pirPin) == GPIO.LOW or te==1:

            print('Loading...please wait..')


            nothing=0
            p=0
            vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"

        service_key = "SFSY0mKiqLyTTowHERC3S793ldcq6nzSp0m5i%2B8Qae8W38rwL3naLNa3fur6ci9LlyUtXQ7UDhDLwsQEVgxYdg%3D%3D"

        today = datetime.datetime.today()
        base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜
        base_time = "0800" # 날씨 값

        nx = "100"
        ny = "76"

        payload = "serviceKey=" + service_key + "&" +\
            "dataType=json" + "&" +\
            "base_date=" + base_date + "&" +\
            "base_time=" + base_time + "&" +\
            "nx=" + nx + "&" +\
            "ny=" + ny

        # 값 요청
        res = requests.get(vilage_weather_url + payload)

        items = res.json().get('response').get('body').get('items')
        #{'item': [{'baseDate': '20200214',
        #   'baseTime': '0500',
        #   'category': 'POP',
        #   'fcstDate': '20200214',
        #   'fcstTime': '0900',
        #   'fcstValue': '0',
        #   'nx': 60,
        #   'ny': 128},
        #  {'baseDate': '20200214',
        #   'baseTime': '0500',
        #   'category': 'PTY',
        #   'fcstDate': '20200214',
        #   'fcstTime': '0900',
        #   'fcstValue': '0',
        #   'nx': 60,
        #   'ny': 128},
        #      'ny': 128},
        #     {'baseDate': '20200214'

        #폭염은 33도
        data = dict()
        data['date'] = base_date

        weather_data = dict()
        for item in items['item']:
            # 기온
            if item['category'] == 'T3H':
                weather_data['tmp'] = item['fcstValue']
    
            # 기상상태
            if item['category'] == 'PTY':
        
                weather_code = item['fcstValue']
        
                if weather_code == '1':
                    weather_state = '비'
                elif weather_code == '2':
                    weather_state = '비/눈'
                elif weather_code == '3':
                    weather_state = '눈'
                elif weather_code == '4':
                    weather_state = '소나기'
                else:
                    weather_state = '없음'
        
                weather_data['code'] = weather_code
                weather_data['state'] = weather_state





    
        data['weather'] = weather_data
        data['weather']

        tmp=int(weather_data['tmp'])
        

        # 모델 위치
        model_filename='/home/pi/Desktop/keras_model.h5'

        # 케라스 모델 가져오기
        model = tensorflow.keras.models.load_model(model_filename)

        # 카메라를 제어할 수 있는 객체
        



        # 카메라 길이 너비 조절
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        # 이미지 처리하기

        def preprocessing(frame):
            #frame_fliped = cv2.flip(frame, 1)
            # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
            size = (224,224)
            frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
            # 이미지 정규화
            # astype : 속성
            frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

            # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
            # keras 모델에 공급할 올바른 모양의 배열 생성
            frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
            #print(frame_reshaped)
            return frame_reshaped

        # 예측용 함수
        def predict(frame):
            prediction = model.predict(frame)
            return prediction
        test=0    
        
        while test==0:
            
            ret, frame = capture.read()
            

            if cv2.waitKey(100) > 0: 
                break

            
            time.sleep(2)
            preprocessed = preprocessing(frame)
            prediction = predict(preprocessed)
            cv2.imshow("VideoFrame", frame)

            ret, frame = capture.read()

            if cv2.waitKey(100) > 0: 
                break

            preprocessed = preprocessing(frame)
            prediction = predict(preprocessed)
            cv2.imshow("VideoFrame", frame)
            
            if (prediction[0,0] < prediction[0,1]):
                print("hello")
                wav=pygame.mixer.Sound("hello3.wav")
                wav.play()
                time.sleep(4)
                import requests
                import json
                import datetime
                nothing=0
                no=0
                ph=[]
                # This example is a hello world example
                # for using a keypad with the Raspberry Pi

                import RPi.GPIO as GPIO
                import time
                phone_num=[]
                pa=0

                d=''
                ne=0

                L1 = 5
                L2 = 6
                L3 = 13
                L4 = 19

                C1 = 12
                C2 = 16
                C3 = 20
                C4 = 21

                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(L1, GPIO.OUT)
                GPIO.setup(L2, GPIO.OUT)
                GPIO.setup(L3, GPIO.OUT)
                GPIO.setup(L4, GPIO.OUT)

                GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

                def readLine(line, characters):
                    global d
                    global ne
                    GPIO.output(line, GPIO.HIGH)
                    if(GPIO.input(C1) == 1):
                        d+=characters[0]
                        print(characters[0])
        
            
        
                    if(GPIO.input(C2) == 1):
        
                        d+=characters[1]
                        print(characters[1])    
                    if(GPIO.input(C3) == 1):
                        d+=characters[2]
                        print(characters[2])
                    if(GPIO.input(C4) == 1):
                        d+=characters[3]
                        print(characters[3])
                    if d.count('A')>0:
                        print('p')
                        d=d.replace('A','')
                        phone_num.append(d)
                        d=''
                    if d.count('D')>0:
                        print('e')
                        ne=1

                    if d.count('C')>0:
                        print('r')
                        d=''
                    GPIO.output(line, GPIO.LOW)

    
        


                while ne==0:
    
                    readLine(L1, ["1","2","3","A"])
                    readLine(L2, ["4","5","6","B"])
                    readLine(L3, ["7","8","9","C"])
                    readLine(L4, ["*","0","#","D"])
                    time.sleep(0.28)
                print(phone_num)   
    
                ph=list(phone_num)

            elif (prediction[0,0] > prediction[0,1]):
                print("hello")
                wav=pygame.mixer.Sound("hello2.wav")
                wav.play()
                time.sleep(4)
                import requests
                import json
                import datetime
                nothing=0
                no=0
                ph=[]
                # This example is a hello world example
                # for using a keypad with the Raspberry Pi

                import RPi.GPIO as GPIO
                import time
                phone_num=[]
                pa=0

                d=''
                ne=0

                L1 = 5
                L2 = 6
                L3 = 13
                L4 = 19

                C1 = 12
                C2 = 16
                C3 = 20
                C4 = 21

                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(L1, GPIO.OUT)
                GPIO.setup(L2, GPIO.OUT)
                GPIO.setup(L3, GPIO.OUT)
                GPIO.setup(L4, GPIO.OUT)

                GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

                def readLine(line, characters):
                    global d
                    global ne
                    GPIO.output(line, GPIO.HIGH)
                    if(GPIO.input(C1) == 1):
                        d+=characters[0]
                        print(characters[0])
        
            
        
                    if(GPIO.input(C2) == 1):
        
                        d+=characters[1]
                        print(characters[1])    
                    if(GPIO.input(C3) == 1):
                        d+=characters[2]
                        print(characters[2])
                    if(GPIO.input(C4) == 1):
                        d+=characters[3]
                        print(characters[3])
                    if d.count('A')>0:
                        print('p')
                        d=d.replace('A','')
                        phone_num.append(d)
                        d=''
                    if d.count('D')>0:
                        print('e')
                        ne=1

                    if d.count('C')>0:
                        print('r')
                        d=''
                    GPIO.output(line, GPIO.LOW)

    
        


                while ne==0:
    
                    readLine(L1, ["1","2","3","A"])
                    readLine(L2, ["4","5","6","B"])
                    readLine(L3, ["7","8","9","C"])
                    readLine(L4, ["*","0","#","D"])
                    time.sleep(0.28)
            break

        
        print(phone_num)   
    
        ph=list(phone_num)
        
        
        # 모델 위치
        model_filename='/home/pi/Desktop/CSSC.h5'

        # 케라스 모델 가져오기
        model = tensorflow.keras.models.load_model(model_filename)

        # 카메라를 제어할 수 있는 객체
        



        # 카메라 길이 너비 조절
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        # 이미지 처리하기

        def preprocessing(frame):
            #frame_fliped = cv2.flip(frame, 1)
            # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
            size = (224,224)
            frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
            # 이미지 정규화
            # astype : 속성
            frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

            # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
            # keras 모델에 공급할 올바른 모양의 배열 생성
            frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
            #print(frame_reshaped)
            return frame_reshaped

        # 예측용 함수
        def predict(frame):
            prediction = model.predict(frame)
            return prediction


        while True:
            
            ret, frame = capture.read()
            

            if cv2.waitKey(100) > 0: 
                break

            

            preprocessed = preprocessing(frame)
            prediction = predict(preprocessed)
            cv2.imshow("VideoFrame", frame)

            ret, frame = capture.read()

            if cv2.waitKey(100) > 0: 
                break

            preprocessed = preprocessing(frame)
            prediction = predict(preprocessed)
            cv2.imshow("VideoFrame", frame)
            
            if p!=0:
                ret, frame = capture.read()

                if cv2.waitKey(100) > 0: 
                    break

                preprocessed = preprocessing(frame)
                prediction = predict(preprocessed)
                cv2.imshow("VideoFrame", frame)

    

                if (prediction[0,0] < prediction[0,1]):
                    print('helmet on')
                    cv2.putText(frame, 'helmet on', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                    tmp=int(weather_data['tmp'])
                    cv2.imshow("VideoFrame", frame)
                    ret, frame = capture.read()

                    if cv2.waitKey(100) > 0: 
                            break

                    preprocessed = preprocessing(frame)
                    prediction = predict(preprocessed)
                    cv2.imshow("VideoFrame", frame)
           
                    import sys
                    if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
                        from Tkinter import *
                    else:
                        from tkinter import *
    
                    root = Tk()
                    noth=0

                    root.attributes("-fullscreen", True)

                    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

                    #center position
                    positionRight = root.winfo_screenwidth()/2 
                    positionDown = root.winfo_screenheight()/2
 
                    #set image
                    if weather_code=='1' or weather_code=='2' or weather_code=='3':
            
                        tk_image1 = PhotoImage(file='/home/pi/Desktop/rain.png')

                    elif weather_code=='4':
                        tk_image1 = PhotoImage(file='/home/pi/Desktop/snow.png')
                    else:
                        noth+=1
            
                    if tmp>=33:
                        tk_image1 = PhotoImage(file='/home/pi/Desktop/high.png')

                    elif tmp<=-17:
                        tk_image1 = PhotoImage(file='/home/pi/Desktop/low.png')

                    else:
                        noth+=1
                    if noth==2:
                        tk_image1 = PhotoImage(file='/home/pi/Desktop/png/nothing.png')
        
                    label = Label(image=tk_image1, bg='black')
                    label.place(x=positionRight,y=positionDown,anchor=CENTER)
 
                    #background color
                    root.configure(bg='black')

                    #root.mainloop()
                    root.update()
                    

                    
                    if weather_code=='1' or weather_code=='2' or weather_code=='4':
                        print("rain")
                        pygame.mixer.init()
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)

                        wav=pygame.mixer.Sound("Rain0.wav")
                        wav.play()
                        time.sleep(7)
    
                        cv2.imshow("VideoFrame", frame)
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)
                    elif weather_code=='3':
    
                        print("snow")
                        pygame.mixer.init()
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)

                        wav=pygame.mixer.Sound("Snow0.wav")
                        wav.play()
                        time.sleep(9)
    
                
                    else:
                        print("nothing(weather)")
                        nothing+=1
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)
    


                    cv2.imshow("VideoFrame", frame)
                    ret, frame = capture.read()

                    if cv2.waitKey(100) > 0: 
                        break

                    preprocessed = preprocessing(frame)
                    prediction = predict(preprocessed)
                    cv2.imshow("VideoFrame", frame)

                    if tmp>=33:
                        print("high")
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)
                        pygame.mixer.init()


                        wav=pygame.mixer.Sound("High0.wav")
                        wav.play()
                        time.sleep(10)
            
                    elif tmp<=-12:
                        print("low")
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)
                        pygame.mixer.init()
                        wav=pygame.mixer.Sound("Low0.wav")
                        wav.play()
                        time.sleep(8)
            
                    else:
                        print("nothing(tmp)")
                        nothing+=1
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)
                        cv2.imshow("VideoFrame", frame)
                        ret, frame = capture.read()

                        if cv2.waitKey(100) > 0: 
                            break

                        preprocessed = preprocessing(frame)
                        prediction = predict(preprocessed)
                        cv2.imshow("VideoFrame", frame)
                    if nothing==2:


                        pygame.mixer.init()
                        wav=pygame.mixer.Sound("Go_1.wav")
                        wav.play()
                        time.sleep(5)
                    break

                else:
                    cv2.putText(frame, 'helmet off', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                    print('helmet off')
                    ret, frame = capture.read()

                    if cv2.waitKey(100) > 0: 
                        break

                    preprocessed = preprocessing(frame)
                    prediction = predict(preprocessed)
                    cv2.imshow("VideoFrame", frame)
                    ret, frame = capture.read()

                    if cv2.waitKey(100) > 0: 
                            break

                    preprocessed = preprocessing(frame)
                    prediction = predict(preprocessed)
                    cv2.imshow("VideoFrame", frame)
                    ret, frame = capture.read()

                    if cv2.waitKey(100) > 0: 
                        break

                    preprocessed = preprocessing(frame)
                    prediction = predict(preprocessed)
                    cv2.imshow("VideoFrame", frame)
                    pygame.mixer.init()
                    pls=pygame.mixer.Sound("Helmetpls.wav")
                    pls.play()
                    #time.sleep(0.5)
                    ret, frame = capture.read()

                    if cv2.waitKey(100) > 0: 
                            break

                    preprocessed = preprocessing(frame)
                    prediction = predict(preprocessed)
                    cv2.imshow("VideoFrame", frame)
            p+=1
        
        root.attributes("-fullscreen", False)
        root.destroy()
        time.sleep(2)

        while True:
            vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"

            service_key = "SFSY0mKiqLyTTowHERC3S793ldcq6nzSp0m5i%2B8Qae8W38rwL3naLNa3fur6ci9LlyUtXQ7UDhDLwsQEVgxYdg%3D%3D"

            today = datetime.datetime.today()
            base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜
            base_time = "0800" # 날씨 값

            nx = "100"
            ny = "76"

            payload = "serviceKey=" + service_key + "&" +\
            "dataType=json" + "&" +\
            "base_date=" + base_date + "&" +\
            "base_time=" + base_time + "&" +\
            "nx=" + nx + "&" +\
            "ny=" + ny

            # 값 요청
            res = requests.get(vilage_weather_url + payload)

            items = res.json().get('response').get('body').get('items')
            #{'item': [{'baseDate': '20200214',
            #   'baseTime': '0500',
            #   'category': 'POP',
            #   'fcstDate': '20200214',
            #   'fcstTime': '0900',
            #   'fcstValue': '0',
            #   'nx': 60,
            #   'ny': 128},
            #  {'baseDate': '20200214',
            #   'baseTime': '0500',
            #   'category': 'PTY',
            #   'fcstDate': '20200214',
            #   'fcstTime': '0900',
            #   'fcstValue': '0',
            #   'nx': 60,
            #   'ny': 128},
            #      'ny': 128},
            #     {'baseDate': '20200214'

            #폭염은 33도
            data = dict()
            data['date'] = base_date

            weather_data = dict()
            for item in items['item']:
                # 기온
                if item['category'] == 'T3H':
                    weather_data['tmp'] = item['fcstValue']
    
                # 기상상태
                if item['category'] == 'PTY':
        
                    weather_code = item['fcstValue']
        
                    if weather_code == '1':
                        weather_state = '비'
                    elif weather_code == '2':
                        weather_state = '비/눈'
                    elif weather_code == '3':
                        weather_state = '눈'
                    elif weather_code == '4':
                        weather_state = '소나기'
                    else:
                        weather_state = '없음'
        
                    weather_data['code'] = weather_code
                    weather_data['state'] = weather_state


            tmp=int(weather_data['tmp'])
            prt=''
            if weather_code=='1' or weather_code=='2' or weather_code=='4':
                prt="비가 올 예정이니 감전사고 또는 붕괴사고에 유의하세요."
    

    
    

            elif weather_code=='3':
                prt="눈이 올 예정이니 작업 발판과 안전 난간을 정비하고, 미끄럼 사고에 주의하세요."
    
    
    

    
    
    

            else:
                print("nothing(weather)")
                nothing+=1
    




            if tmp>=33:
                prt="폭염이 예상되니 충분한 수분을 섭취하시고 1시간 주기로 휴식을 취하여 온열질환에 유의하세요."
    
    

            elif tmp<=-12:
                prt="기온이 낮으니 방한 장구를 착용하시고, 한랭질환에 유의하세요."
    

            else:
                print("nothing(tmp)")
                nothing+=1


            if nothing==2:
                no=1
            #prt="비가 올 예정이니 감전사고 또는 붕괴사고에 유의하세요."    
            #no=0
            g=input("다음 사람이 있으면 r를 누르고 enter를 누르고, 다음 사람이 없으면 n을 누르고 eneter를 눌러주세요.")

            if g=='r':
                break
            
            #no=0
            #prt='test'
            while True:
                if no==0:
                    for i in ph:    
                        if __name__ == "__main__":
                            import sys
 
                            from sdk.api.message import Message
                            from sdk.exceptions import CoolsmsException
                            # set api key, api secret
                            api_key = "NCSUQC7X8QD6JT1M"
                            api_secret = "G9BYFAOQ7CXYJ5KC6ZCY2QY0SGGITPTR"
                            ## 4 params(to, from, type, text) are mandatory. must be filled
                            params = dict()
                            params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
                            params['to'] = str(i) # Recipients Number '01000000000,01000000001'
                            params['from'] = str(i) # Sender number
                            params['text'] = str(prt) # Message
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

                    time.sleep(7200)
    else:

        print("No motion")

