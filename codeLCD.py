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
BalancePercent2 = 0.9

rotateSpeed = 1
threadStop = False

#-------------------------------------

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
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

# referenceUnit = ((212815 + 212716 + 212610)/3) / 500 #1kg bar
referenceUnit = ((-221902 + -221951 + -222027)/3)/1000 #10kg bar
# referenceUnit = 1
brocheDT = 5
brocheSCK = 16

hx = HX711(brocheDT, brocheSCK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")

#-------------------------------------

def getPoids():
    val = hx.get_weight(5)
    print(val)
    
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

def rotateMotor(_poidsMax):
    global rotateSpeed
    global threadStop
    counter = 0;
    threadStop = False
    x = threading.Thread(target=rotateIndefinitely, args=(1,))
    x.start()
    b1 = BalancePercent1
    b2 = BalancePercent2
    
    continueRotate = True;
    # rotateSpeed = 1
    while continueRotate: 
        try :
            _poids = getPoids()
            afficherPoidsActuel(int(_poids))
            # print("GNEUU")
            if (_poids < _poidsMax*BalancePercent1 and rotateSpeed != 1):
                rotateSpeed = 1
            elif(_poids >= _poidsMax*BalancePercent1 and _poids < _poidsMax*BalancePercent2 and rotateSpeed != 2):
                rotateSpeed = 2
            elif (_poids >= _poidsMax*BalancePercent2 and _poids < _poidsMax and rotateSpeed != 3):
                rotateSpeed = 3
            elif (_poids > _poidsMax):
                print("ON S'ARRETE")
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
            
        except (KeyboardInterrupt, SystemExit):
            threadStop = True;
            x.join()
            # GPIO.cleanup()
            # print("Bye!")
            # sys.exit()
    print("On est sortis du while")

def current_milli_time():
    return round(time.time() * 1000)

def start():
    lcd.clear()
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 3)  # 0 = 1Ã¨re ligne / 3 = 4Ã¨me colonne
    lcd.write_string(u' Bienvenue')
    lcd.cursor_pos = (1, 7)  # 1 = 2Ã¨me ligne / 7 = 8Ã¨me colonne
    lcd.write_string(u'EOS')
    time.sleep(1)
    menu()

def menu():
    lcd.clear()
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Mise en sachet')
    lcd.cursor_pos = (1, 1)  # 1 = 2Ã¨me ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Options')

def mise_en_sachet_en_attente():
    lcd.clear()
    lcd.write_string(u'                                ')
    lcd.cursor_pos = (0, 1)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    lcd.write_string(u'Poids : ')
    lcd.cursor_pos = (0, 9)  # 1 = 2Ã¨me ligne / 9 = 10Ã¨me colonne
    lcd.write_string(str(data_options['data']['poids']))
    lcd.cursor_pos = (0, 13)  # 1 = 2Ã¨me ligne / 13 = 14Ã¨me colonne
    lcd.write_string(str(data_options['data']['ordre']))

def options():
    lcd.clear()
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
    lcd.clear()
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
    lcd.clear()
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
    lcd.cursor_pos = (1, 0)  # 0 = 1Ã¨re ligne / 1 = 2Ã¨me colonne
    pdsStr = str(pds) + ' g'
    spaceStr = ' '*(16-len(pdsStr))
    lcd.write_string(u'' + pdsStr + spaceStr)


def button_callback(pin):
    btnNb = pinBtn.index(pin)
    if (current_milli_time() > timeBtn[btnNb] + 100):
        print("BOUTON ", btnNb)
        timeBtn[btnNb] = current_milli_time()
        
        global menuState
        global data_options
        global poids
        
        print("GNEU", menuState)
        if (menuState == "menu"):
            if btnNb == 0:
                menuState = "mise_en_sachet_en_attente"
                mise_en_sachet_en_attente()
            elif btnNb == 1:
                menuState = "options"
                options()
            
        elif (menuState == "mise_en_sachet_en_attente"):
            if btnNb == 0:
                lcd.cursor_pos = (0, 0)
                lcd.write_string(u' Poids actuel:  ')
                pds = data_options['data']['poids'];
                if data_options['data']['ordre'] == "kg":
                    pds = pds * 1000;
                rotateMotor(pds)
                print("FAIRE TOURNER LES SERVIETTES")
                mise_en_sachet_en_attente()
            elif btnNb == 1:
                menuState = "menu"
                menu()
                
            
        elif (menuState == "options"):
            if btnNb == 0:
                menuState = "options_poids"
                options_poids()
            elif btnNb == 1:
                menuState = "options_ordre"
                options_ordre()
            elif btnNb == 2:
                menuState = "menu"
                menu()
            
        elif (menuState == "options_poids"):
            if btnNb == 0:
                data_options['data']['poidsNew'] += 1
                options_poids()
            elif btnNb == 1:
                data_options['data']['poidsNew'] -= 1
                options_poids()
            elif btnNb == 2:
                menuState = "options"
                options()
            elif btnNb == 3:
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

GPIO.add_event_detect(pinBtn[0], GPIO.RISING, callback=button_callback) 
GPIO.add_event_detect(pinBtn[1], GPIO.RISING, callback=button_callback) 
GPIO.add_event_detect(pinBtn[2], GPIO.RISING, callback=button_callback) 
GPIO.add_event_detect(pinBtn[3], GPIO.RISING, callback=button_callback)

try:
    
    start();
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    lcd.write_string(u'                                ')
    GPIO.cleanup()
    print("Cleaning & exit")
    sys.exit();
lcd.write_string(u'                                ')
GPIO.output(STEP, GPIO.LOW)
GPIO.cleanup()
print("Cleaning & exit")