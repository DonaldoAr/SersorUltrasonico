# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
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

ALARMA = 7
GPIO.setup(ALARMA, GPIO.OUT)
GPIO.output(ALARMA, GPIO.LOW)
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

if(__name__ == '__main__'):
    try:
        while True:
            # APAGAMOS EL ESTROBO 
            GPIO.output(ALARMA, GPIO.LOW)
            distA = distance(TRIGGER1, ECHO1)
            distB = distance(TRIGGER2, ECHO2)
            # -> SOLO PARA MEDIR LA DISTANCIAS <-
            # print("S1: %.1f" % distA, "S2: %.1f" % distB)
            # time.sleep(0.7)
            # SI HAY UNA PERSONA EN MEDIO  
            if((distA < 200 & distA > 10) & (distB >= 190 )):
                # PERSONA CAMINA
                # ENCENDER LA ALARMA
                while(True):
                    GPIO.output(ALARMA, True)
                    print("PRENDE ALARMA")
                    time.sleep(0.7)
                    distA = distance(TRIGGER1, ECHO1)
                    distB = distance(TRIGGER2, ECHO2)
                    # SI PERSONA DEJA DE ESTAR ENFRENTE DEL SENSOR A
                    if(distA >= 190):
                        # ALARMA PERMANECE ENCENDIDA
                        GPIO.output(ALARMA, True)
                        print("PRENDE ALARMA")
                        distA = distance(TRIGGER1, ECHO1)
                        distB = distance(TRIGGER2, ECHO2)
                        if((distA < 200 & distA > 10) & (distB >= 190 )):
                            # DESACTIVAR LA ALARMA 
                            GPIO.output(ALARMA, False)
                            print("APAGAR ALARMA")
                            break
            elif((distB < 200 & distB > 10) & (distA >= 190 )):
                # ENTRA LA PERSONA
                GPIO.output(ALARMA, False)
                while(True):
                    GPIO.output(ALARMA, False)
                    print("SIGUE APAGADA LA ALARMA")
                    time.sleep(0.7)
                    distA = distance(TRIGGER1, ECHO1)
                    distB = distance(TRIGGER2, ECHO2)
                    # SI PERSONA DEJA DE ESTAR ENFRENTE DEL SENSOR DE LA ENTRADA
                    if(distB >= 190):
                        # ALARMA PERMANECE APAGADA
                        GPIO.output(ALARMA, False)
                        print("PRENDE ALARMA")
                        distA = distance(TRIGGER1, ECHO1)
                        distB = distance(TRIGGER2, ECHO2)
                        if((distA >= 190) & (distB >= 190 )):
                            # DESACTIVAR LA ALARMA 
                            GPIO.output(ALARMA, False)
                            print("SE APAGA")
                            break
            print("De vuelta a ciclo infinito")
                        

            
            

                


                        
                
                
            
    # Resetiando
    except KeyboardInterrupt:
        GPIO.cleanup()
