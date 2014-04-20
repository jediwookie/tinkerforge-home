##!/usr/bin/env python
# -*- coding: utf-8 -*-  

import socket
import sys
import time
import math
import os
import datetime


# tfile= open("/sys/bus/w1/devices/10-00080277ad52/w1_slave")


HOST1 = "192.168.2.157" # MasterBrick Flur mit Ethernet
HOST2 = "192.168.2.156" # MasterBrick Esszimmer mit Wireless LAN
PORT = 4223 # Port von den Bricks
UID_L = "9LY" # Change to your UID
UID_B = "jXQ" #Barometer inkl. Temperatur
UID_A = "jxV"
UID_M = "68USSm" #MasterBrick 1
UID_T1 = "Temp1" # Temperatur Aussen
UID_T2 = "dUj" # Temperatur Flur 
UID_F = "ka6"


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_20x4 import LCD20x4
from tinkerforge.bricklet_barometer import Barometer
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.brick_master import Master
from tinkerforge.bricklet_temperature import Temperature
from tinkerforge.bricklet_humidity import Humidity


if __name__ == "__main__":
    ipcon1 = IPConnection() # Create IP connection
    ipcon2 = IPConnection() # Create IP connection
    lcd = LCD20x4(UID_L, ipcon1) # Create device object
    b = Barometer(UID_B, ipcon2) # Create device object
    temp1 = Temperature(UID_T1, ipcon2)
    temp2 = Temperature(UID_T2, ipcon1)
    al = AmbientLight(UID_A, ipcon1) # Create device object
    h = Humidity(UID_F, ipcon2) # Create device object
    master = Master(UID_M, ipcon2) # Create device object
    ipcon1.connect(HOST1, PORT) # Connect to brickd
    ipcon2.connect(HOST2, PORT) 

    while True:
        air_pressure = b.get_air_pressure()/1000.0
        altitude = b.get_altitude()/100.0
        illuminance = al.get_illuminance()/10.0
        bartemp = b.get_chip_temperature()/100.0
        esszimm = temp1.get_temperature()/100.0
        flur = temp2.get_temperature()/100.0
        voltage = master.get_stack_voltage()
        current = master.get_stack_current()
        wifi = master.get_wifi_configuration()
        wifistatus = master.get_wifi_status()
        wifipower = master.get_wifi_power_mode()
        wifihost = master.get_wifi_hostname()
        usbvoltage = master.get_usb_voltage()
        masterid = master.get_identity()
        feuchte = h.get_humidity()/10.0

        os.system('clear')
        
        luxwert = 10
        
         
        print "Or like this: " ,datetime.datetime.now().strftime("%d.%m.%y - %H:%M")

        
        # Werte in die Konsole schreiben
        print ('Display Ein/Aus Schalten')
        print ('Ist: ' + str(illuminance) + ' LUX')
        print ('Soll: ' + str(luxwert) + ' LUX')
        print ('')
        
        # Luxwert abfragen und Wert in die Konsole schreiben
        if (illuminance >= luxwert): 
            # print ('' + str(illuminance) + 'grosser als' + str(luxwert))
            print ('Display ist EIN')
            lcd.backlight_on()
        if (illuminance <= luxwert):  
            # print ('' + str(illuminance) + 'ist kleiner als' +str(luxwert))
            print ('Display ist AUS')
            lcd.backlight_off()
        print('')
        
        ts = 10 # Sleeptime wert

        print('Tinkerforge Brick1+2')
        print('========================================')
        print(' Luftdr.: ' + str(air_pressure) + ' mbr')
        print(' Feuchte: ' + str(feuchte) + ' %')
        print('   Licht: ' + str(illuminance) + ' Lux')
        print('========================================')
        print('  Aussen: ' + str(esszimm) + '°C')
        print('   Buero: ' + str(21.82) + ' °C')
        print('    Flur: ' + str(flur) + ' °C')
        print('   EssZi: ' + str(bartemp) + ' °C')
        print('========================================')
        print(' Heizung: --- ')
        print('   Pumpe: ---')
        print(' Vorlauf: --.-- °C')
        print('Rucklauf: --.-- °C')
        print('========================================')
        
        
        lcd.clear_display()
        lcd.write_line(0,0, '')
        lcd.write_line(1,0,  datetime.datetime.now().strftime('        %H:%M    '))
        lcd.write_line(2,0,  datetime.datetime.now().strftime('      %d.%m.%Y   '))
        lcd.write_line(3,0, '')
        time.sleep(8)
        
        # Starten von dem Display
        lcd.clear_display()
        lcd.write_line(0, 0, 'Luftdr.: ' + str(air_pressure) + '')
        lcd.write_line(0, 15, ' mbr')
        lcd.write_line(1, 0, 'Feuchte: ' + str(feuchte) + '')
        lcd.write_line(1, 15, ' %')
        lcd.write_line(2, 0, '  Licht: ' + str(illuminance) + '')
        lcd.write_line(2, 15, ' Lux')
        lcd.write_line(3, 0, '  ' + str() + '')
        lcd.write_line(3, 13, ' ')
        time.sleep(8)    

        lcd.clear_display()
        lcd.write_line(0, 0, 'Futterautom.: ---')
        lcd.write_line(0, 19, '')
        lcd.write_line(1, 0, '  Futterzeit: 16:00')
        lcd.write_line(1, 19, '')
        lcd.write_line(2, 0, ' Stop: Taste 2')
        lcd.write_line(2, 19, '')
        lcd.write_line(3, 0, 'Start: Taste 3')
        lcd.write_line(3, 19, '')
        time.sleep(8)
    
        lcd.clear_display()
        lcd.write_line(0, 0, ' Heizung: --- ')
        lcd.write_line(1, 0, '   Pumpe: ---')
        lcd.write_line(2, 0, ' Vorlauf: --.-- \xdfC')
        lcd.write_line(3, 0, 'Rucklauf: --.-- \xdfC')
        time.sleep(8)

        lcd.clear_display()
        lcd.write_line(0, 0, 'Master 1: EIN')
        lcd.write_line(1, 0, 'Master 2: EIN')
        lcd.write_line(2, 0, '  RasbPi: EIN')
        lcd.write_line(3, 0, '  433MHz: EIN')
        time.sleep(8)
        
        lcd.clear_display()
        lcd.write_line(0, 0, 'Aussen: ' + str(esszimm) + '')
        lcd.write_line(0, 13, ' \xdfC')
        lcd.write_line(1, 0, ' Buero: ' + str(21.82) + '')
        lcd.write_line(1, 13, ' \xdfC')
        lcd.write_line(2, 0, '  Flur: ' + str(flur) + '')
        lcd.write_line(2, 13, ' \xdfC')
        lcd.write_line(3, 0, ' EssZi: ' + str(bartemp) + '')
        lcd.write_line(3, 13, ' \xdfC')
        time.sleep(8)
        




