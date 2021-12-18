#Libraries
import RPi.GPIO as GPIO
import time
from Filtrar_ruido import Filtrar_ruido
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# == PINES DE SENSOR 
TRIGGER1 = 32
ECHO1 = 36
GPIO.setup(TRIGGER1, GPIO.OUT)
GPIO.output(TRIGGER1, GPIO.LOW)
GPIO.setup(ECHO1, GPIO.IN)

TRIGGER2 = 38
ECHO2 = 40
GPIO.setup(TRIGGER2, GPIO.OUT)
GPIO.output(TRIGGER2, GPIO.LOW)
GPIO.setup(ECHO2, GPIO.IN)

# senal_ruido2 = Filtrar_ruido(0.32, 0.32, 0.01)

def distance(T, E):
    # set Trigger to HIGH
    GPIO.output(T, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(T, False)
    StartTime = time.time()
    StopTime = time.time()
    # Guarda tiempo de inicio
    while GPIO.input(E) == 0:
        StartTime = time.time()
    # Guarda tiempo de regreso de pulso
    while GPIO.input(E) == 1:
        StopTime = time.time()
        delta = StopTime - StartTime
        # if(delta > 0.0233):
        if(delta > 0.0104): # Para 180
            break
    # Delta tiempo
    Dt = StopTime - StartTime
    # Multiplicando velocidad de sonido (34300 cm/s)
    distancia = (Dt * 34300) / 2
    return distancia

if __name__ == '__main__':
    try:
        while True:
            print("inicio")
            dist1 = int(distance(TRIGGER1, ECHO1))
            # print ("Distancia calculada = %.1f cm" % dist1)
            # time.sleep(1)
            # fin = int( senal_ruido2.Estimador_Kalman( distance(TRIGGER2, ECHO2) ) )
            dist2 = int(distance(TRIGGER2, ECHO2))
            # print ("Distancia calculada = %.1f cm" % dist2)
            print ("S1: %.1f" %dist1,"S2: %.1f" %dist2 )
            time.sleep(0.5)
    # Resetiando
    except KeyboardInterrupt:
        GPIO.cleanup() 