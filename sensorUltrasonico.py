#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# == PINES DE SENSOR 
TRIGGER1 = 20
ECHO1 = 21
GPIO.setup(TRIGGER1, GPIO.OUT)
GPIO.output(TRIGGER1, GPIO.LOW)
GPIO.setup(ECHO1, GPIO.IN)

TRIGGER2 = 12
ECHO2 = 16
GPIO.setup(TRIGGER2, GPIO.OUT)
GPIO.output(TRIGGER2, GPIO.LOW)
GPIO.setup(ECHO2, GPIO.IN)


# def distance():
#     # set Trigger to HIGH
#     GPIO.output(TRIGGER, True)
#     # set Trigger after 0.01ms to LOW
#     time.sleep(0.00001)
#     GPIO.output(TRIGGER, False)
#     StartTime = time.time()
#     StopTime = time.time()
#     # Guarda tiempo de inicio
#     while GPIO.input(ECHO) == 0:
#         StartTime = time.time()
#     # Guarda tiempo de regreso de pulso
#     while GPIO.input(ECHO) == 1:
#         StopTime = time.time()
#     # Delta tiempo
#     Dt = StopTime - StartTime
#     # Multiplicando velocidad de sonido (34300 cm/s)
#     distancia = (Dt * 34300) / 2
#     return distancia

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
    # Delta tiempo
    Dt = StopTime - StartTime
    # Multiplicando velocidad de sonido (34300 cm/s)
    distancia = (Dt * 34300) / 2
    return distancia

if __name__ == '__main__':
    try:
        while True:
            dist1 = distance(TRIGGER1, ECHO1)
            # print ("Distancia calculada = %.1f cm" % dist1)
            # time.sleep(1)

            dist2 = distance(TRIGGER2, ECHO2)
            # print ("Distancia calculada = %.1f cm" % dist2)
            # time.sleep(1)
            print ("S1: %.1f" %dist1, "S2: %.1f" %dist2 )
    # Resetiando
    except KeyboardInterrupt:
        GPIO.cleanup()