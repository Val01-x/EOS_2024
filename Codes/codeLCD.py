#!/usr/bin/python

from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time
import json
import sys
from hx711 import HX711
import threading

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=17, pin_e=27, pins_data=[22, 23, 24, 25])

pinBtn = [6, 13, 19, 26]
stateBtn = [False, False, False, False]
timeBtn = [0, 0, 0, 0]

menuState = "menu"
with open('data.json') as json_data:
    data_options = json.load(json_data)
    data_options["data"]['poids']
    data_options["data"]['poidsNew'] = data_options["data"]['poids']

GPIO.setup((pinBtn[0], pinBtn[1], pinBtn[2], pinBtn[3]), GPIO.IN, pull_up_down=GPIO.PUD_UP)


poidsMax = 548;

speedMax = 4
speedMed = 16
speedMin = 64

BalancePercent1 = 0.8
BalancePercent2 = 0.95

rotateSpeed = 1
threadStop = False
continueRotate = True
stopRotation = False;
tmpPdsMax = 0;
#-------------------------------------

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 0     # Clockwise Rotation
CCW = 1    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CCW)
GPIO.output(STEP, GPIO.LOW)

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['1/32'])
step_count = SPR * 32
delay = .0208 / (32*3)

#-------------------------------------

referenceUnit1 = ((-273360 + -272796 + -272141)/3) / 250 #1kg bar
referenceUnit10 = ((-221902 + -221951 + -222027)/3)/1000 #10kg bar

# data_options["data"]['referenceUnitState'] = True

# referenceUnit = 1
brocheDT = 5
brocheSCK = 16

hx = HX711(brocheDT, brocheSCK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit10)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")

#-------------------------------------

def getPoids():
    val = hx.get_weight(5)
    # print(val)
    
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    return val

def rotate(_delay):
    # for x in range(step_count):
    # print("rotate")
    GPIO.output(STEP, GPIO.HIGH)
    time.sleep(_delay)
    GPIO.output(STEP, GPIO.LOW)
    time.sleep(_delay)

def rotateIndefinitely(_):
    etatMotor = 0
    while not threadStop:
        # print  ("RotateSpeed", rotateSpeed)
        sT = 0;
        if rotateSpeed == 1:
            sT = delay * speedMax
        elif rotateSpeed == 2:
            sT = delay  * speedMed
        elif rotateSpeed == 3:
            sT = delay * speedMin
        if (sT > 0):
            rotate(sT)

def threadRotate(_):
    global rotateSpeed
    global threadStop
    global continueRotate;
    global stopRotation
    global tmpPdsMax
    global menuState
    counter = 0;
    x = threading.Thread(target=rotateIndefinitely, args=(1,))
    x.start()
    b1 = BalancePercent1
    b2 = BalancePercent2
    
    stopRotation = False;
    continueRotate = True;
    threadStop = False;
    
    while continueRotate: 
        try :
            _poids = getPoids()
            afficherPoidsActuel(int(_poids))
            if (_poids < tmpPdsMax*BalancePercent1 and rotateSpeed != 1):
                rotateSpeed = 1
            elif(_poids >= tmpPdsMax*BalancePercent1 and _poids < tmpPdsMax*BalancePercent2 and rotateSpeed != 2):
                rotateSpeed = 2
            elif (_poids >= tmpPdsMax*BalancePercent2 and _poids < tmpPdsMax and rotateSpeed != 3):
                rotateSpeed = 3
            elif (_poids > tmpPdsMax):
                threadStop = True;
                x.join()
                rotateSpeed = 0
                continueRotate = False;
            time.sleep(0.1)
            counter +=1;
            if counter >= 5:
              GPIO.output(DIR, CW)
              time.sleep(0.3)
              GPIO.output(DIR, CCW)
              counter = 0
            # print("pds Max:",tmpPdsMax)
            # print("thread stopRotation:",stopRotation)
            # print("thread threadStop:", threadStop)
            # print("thread continueRotate:", continueRotate)
            if stopRotation == True:
                # print("ON STOP LA ROTATION")
                # stopRotation = False;
                threadStop = True
                x.join()
                continueRotate = False;
            
        except (KeyboardInterrupt, SystemExit):
            threadStop = True;
            x.join()
            continueRotate = False;
    if threadStop == False or stopRotation == True:
        threadStop = True
        x.join()
    
    stopRotation = False;
    continueRotate = True;
    threadStop = False;
    menuState = "mise_en_sachet_en_attente"
    mise_en_sachet_en_attente()

def rotateMotor():
    x = threading.Thread(target=threadRotate, args=(1,))
    x.start()

def current_milli_time():
    return round(time.time() * 1000)

def start():
    # lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 3)  # 0 = 1Ã¨re ligne / 3 = 4Ã¨me colonne
    lcd.write_string(u' Bienvenue')
    lcd.cursor_pos = (1, 7)  # 1 = 2Ã¨me ligne / 7 = 8Ã¨me colonne
    lcd.write_string(u'EOS')
    time.sleep(1)
    menu()

def menu():
    # lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Mise en sachet')
    lcd.cursor_pos = (1, 1)  # 1 = 2Ã¨me ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Options')

def mise_en_sachet_en_attente():
    # print("Fct mise en sachet en attente")
    # lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Poids : ')
    lcd.cursor_pos = (0, 9)  # 1 = 2Ã¨me ligne / 9 = 10Ã¨me colonne
    lcd.write_string(str(data_options['data']['poids']))
    lcd.cursor_pos = (0, 13)  # 1 = 2Ã¨me ligne / 13 = 14Ã¨me colonne
    lcd.write_string(str(data_options['data']['ordre']))

def options():
    # lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Poids : ')
    lcd.cursor_pos = (0, 9)  # 0 = 1Ã¨re ligne / 9 = 10Ã¨me colonne
    lcd.write_string(str(data_options['data']['poids']))
    lcd.cursor_pos = (1, 1)  # 1 = 2Ã¨me ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Ordre')
    lcd.cursor_pos = (1, 9)  # 1 = 2Ã¨me ligne / 9 = 10Ã¨me colonne
    lcd.write_string(str(data_options['data']['ordre']))

def options_poids():
    pds = data_options['data']['poidsNew']
    # lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Nouveau poids')
    lcd.cursor_pos = (0, 15)  # 0 = 1Ã¨re ligne / 15 = 16Ã¨me colonne
    lcd.write_string(u'+')
    lcd.cursor_pos = (1, 6)  # 1 = 2Ã¨me ligne / 6 = 7Ã¨me colonne
    lcd.write_string(str(pds))
    lcd.cursor_pos = (1, 15)  # 1 = 2Ã¨me ligne / 15 = 16Ã¨me colonne
    lcd.write_string(u'-')

def options_ordre():
    # lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Nouvel ordre')
    lcd.cursor_pos = (0, 13)  # 0 = 1Ã¨re ligne / 13 = 14Ã¨me colonne
    lcd.write_string(u'KG')
    lcd.cursor_pos = (1, 14)  # 1 = 2Ã¨me ligne / 14 = 15Ã¨me colonne
    lcd.write_string(u'G')

def enregistrer():
    with open('data.json') as doc:
        # json.dump(data_options, doc)
        print(data_options)

def afficherPoidsActuel(pds):
    # lcd.clear()
    # lcd.write_string(u'                                ')
    print("POIDS:", pds)
    lcd.cursor_pos = (1, 0)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    if pds == 0:
        pdsStr = "0 g"
    else :
        pdsStr = str(pds) + ' g'
    spaceStr = ' '*(16-len(pdsStr))
    lcd.write_string(u'' + pdsStr + spaceStr)


def button_callback(pin):
    btnNb = pinBtn.index(pin)
    global menuState
    global data_options
    # global poids
    global stopRotation
    global tmpPdsMax
    # global referenceUnitState
    
    if (current_milli_time() > timeBtn[btnNb] + 100):
        # print("BOUTON ", btnNb)
        # print(menuState)
        timeBtn[btnNb] = current_milli_time()
        
        if (menuState == "menu"):
            if btnNb == 0:
                hx.tare()
                menuState = "mise_en_sachet_en_attente"
                mise_en_sachet_en_attente()
            elif btnNb == 1:
                menuState = "options"
                options()
            """
            elif btnNb == 3:
                # referenceUnit1
                # referenceUnit10
                data_options["data"]['referenceUnitState']  = not data_options["data"]['referenceUnitState'] 
                enregistrer()
                
                lcd.write_string(u'                                ')
                lcd.cursor_pos = (0, 1) 
                lcd.write_string(u'Cellule switch')
                lcd.cursor_pos = (1, 1) 
                
                # lcd.write_string(u'LOL')
                if data_options["data"]['referenceUnitState'] :
                    hx.set_reference_unit(referenceUnit1)
                    lcd.write_string(u'1  kg')
                else:
                    hx.set_reference_unit(referenceUnit10)
                    lcd.write_string(u'10 kg')
                hx.reset()
                hx.tare()
                print("TARE FAITE")
                
                time.sleep(2.5)
                
                lcd.cursor_pos = (0, 0)
                lcd.write_string(u'                                ')
                lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
                lcd.write_string(u'Mise en sachet')
                lcd.cursor_pos = (1, 1)  # 1 = 2Ã¨me ligne / 1 = 2Ã¨me colonne
                lcd.write_string(u'Options')
            """
        elif (menuState == "mise_en_sachet_en_attente"):
            if btnNb == 2:
                menuState = "mise_en_sache_en_cours"
                lcd.cursor_pos = (0, 0)
                lcd.write_string(u' Poids actuel:  ')
                tmpPdsMax = data_options['data']['poids'];
                if data_options['data']['ordre'] == "kg":
                    tmpPdsMax = tmpPdsMax * 1000;
                stopRotation = False;
                rotateMotor()
                # mise_en_sachet_en_attente()
            elif btnNb == 3:
                menuState = "menu"
                menu()
                
        elif (menuState == "mise_en_sache_en_cours"):
            if btnNb == 3:
                stopRotation = True;
                # print("event:", stopRotation)
                menuState = "mise_en_sachet_en_attente"
                mise_en_sachet_en_attente()
                
        elif (menuState == "options"):
            if btnNb == 0:
                menuState = "options_poids"
                options_poids()
            elif btnNb == 1:
                menuState = "options_ordre"
                options_ordre()
            elif btnNb == 3:
                menuState = "menu"
                menu()
            
        elif (menuState == "options_poids"):
            if btnNb == 0:
                data_options['data']['poidsNew'] += 1
                options_poids()
            elif btnNb == 1:
                data_options['data']['poidsNew'] -= 1
                options_poids()
            elif btnNb == 3:
                menuState = "options"
                options()
            elif btnNb == 2:
                menuState = "options"
                data_options['data']['poids'] = data_options['data']['poidsNew']
                enregistrer()
                options()
        elif (menuState == "options_ordre"):
            if btnNb == 0:
                menuState = "options"
                data_options['data']['ordre'] = 'kg'
                enregistrer()
                options()
            elif btnNb == 1:
                menuState = "options"
                data_options['data']['ordre'] = 'g'
                enregistrer()   
                options()
            elif btnNb == 3:
                menuState = "options"  
                options()

GPIO.add_event_detect(pinBtn[0], GPIO.RISING, callback=button_callback) 
GPIO.add_event_detect(pinBtn[1], GPIO.RISING, callback=button_callback) 
GPIO.add_event_detect(pinBtn[2], GPIO.RISING, callback=button_callback) 
GPIO.add_event_detect(pinBtn[3], GPIO.RISING, callback=button_callback)

try:
    
    start();
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    lcd.cursor_pos = (0, 0)
    lcd.write_string(u'                                ')
    GPIO.cleanup()
    print("Cleaning & exit")
    sys.exit();
lcd.cursor_pos = (0, 0)
lcd.write_string(u'                                ')
GPIO.output(STEP, GPIO.LOW)
GPIO.cleanup()
print("Cleaning & exit")
