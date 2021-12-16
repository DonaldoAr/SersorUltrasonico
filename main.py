# CODIGO PARA DETECTAR UNA ALARMA
# Libraries
import RPi.GPIO as GPIO
import time
from Filtrar_ruido import Filtrar_ruido          # Clase Filtro
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

senal_ruido1 = Filtrar_ruido(0.32, 0.32, 0.01)
senal_ruido2 = Filtrar_ruido(0.32, 0.32, 0.01)

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
        print("Esperando a que el pulso regrese")
        StopTime = time.time()
    # Delta tiempo
    Dt = StopTime - StartTime
    # Multiplicando velocidad de sonido (34300 cm/s)
    distancia = (Dt * 34300) / 2
    return distancia

if(__name__ == '__main__'):
    try:
        while True:
            GPIO.output(ALARMA, True)
            ini = int( senal_ruido1.Estimador_Kalman( distance(TRIGGER1, ECHO1) ))
            fin = int( senal_ruido2.Estimador_Kalman( distance(TRIGGER2, ECHO2) ) )
            # ini = int(distance(TRIGGER1, ECHO1))
            # fin = int(distance(TRIGGER2, ECHO2))
            print("Fin: %.1f" % fin, "Ini: %.1f" % ini)

            # PRUGUNTAMOS SI EN EL SENSOR DE "FIN" HAY ALGUIEN senFinQ ?
            senFinQ = (fin < 200 and fin > 10)
            # PREGUNTAMOS SI EN EL SENSOR DE INICIO NO HAY NADIE
            senIniQ = (ini > 190)

            # PARA EL ELIF DENTRO DEL MAIL CUANDO ENTRA UNA PERSONA
            senFinOk = (fin > 190)
            # PREGUNTAMOS SI EN EL SENSOR DE INICIO NO HAY NADIE
            senIniOk = (ini < 200 and ini > 10)
            if(senFinQ and senIniQ):
                print("= Se detecto a alguien =")
                # PRENDER ALARMA
                GPIO.output(ALARMA, False)
                # ESPERAMOS 0.8seg
                time.sleep(1)
                while(True):
                    ini = int(distance(TRIGGER1, ECHO1))
                    fin = int(distance(TRIGGER2, ECHO2))
                    # PREGUNTAMO SI EN EL SENSOR FINAL NO HAY NADIE EN TAL CASO EL SENSOR MEDIRA MAS DE 190cm
                    senFinQ = (fin > 190)
                    # PREGUNTAMOS SI HAY ALGUIEN EN EL SENSOR INICIAL EN TAL CASO DEBE MEDIR ENTRE MAYOR A 10 Y MENOR A 200CM
                    senIniQ = (ini < 200 and ini > 10)
                    
                    # == CONDICIONES PARA EL ELIF 1 ==
                    # PREGUNTAMO SI EN EL SENSOR DE FIN SE ENCUENTRA DESACTIVADO
                    senFinQ2 = (fin > 190)
                    # PREGUNTAMOS SI EN EL SENSOR DE INICIO SE ENCUENTRA DESACTIVADO
                    senIniQ2 = (ini > 190)

                     # == CONDICIONES PARA EL ELIF 2 ==
                    # PREGUNTAMO SI EN EL SENSOR DE FIN SE ENCUENTRA ACTIVADO
                    senFinQ3 = (fin < 200 and fin > 10)
                    # PREGUNTAMOS SI EN EL SENSOR DE INICIO SE ENCUENTRA ACTIVADO
                    senIniQ3 = (ini < 200 and ini > 10)

                    # == CONDICIONES PARA ELIF 3 == 
                    # PREGUNTAMO SI EN EL SENSOR DE FIN SE ENCUENTRA ACTIVADO, EN TAL CASO LA PERSONAL VOLVIO A ENTRAR DENTRO DE LA SUCURSAL
                    senFinQ4 = (fin < 200 and fin > 10)
                    # PREGUNTAMOS SI EN EL SENSOR DE INICIO SE ENCUENTRA DESACTIVADO YA NO SE NADIE
                    senIniQ4 = (ini > 190)

                    if(senFinQ and senIniQ):
                        print("SE DETECTO ALGUIEN QUE PASO DEL SENSOR FIN AL SENSOR INI")
                        # ENTONCES TODAVIA HAY ALGUIEN, SE SIGUE PRENDIENDO LA ALARMA
                        GPIO.output(ALARMA, False)
                        time.sleep(1)
                    elif(senFinQ2 and senIniQ2):
                        # ENTONCES TODAVIA HAY ALGUIEN, SE SIGUE PRENDIENDO LA ALARMA
                        GPIO.output(ALARMA, False)
                        time.sleep(1)
                    elif(senFinQ3 and senIniQ3):
                        # ALARMA ACTIVA SIGUE ACTIVA 
                        GPIO.output(ALARMA, False)
                    elif(senFinQ4 and senIniQ4):
                        # PERSONA SE SALIO 
                        GPIO.output(ALARMA, True)
                        break
            # == CUANDO LOS USUARIO ENTRA DE MANERA CORRECTA ==
            elif(senIniOk and senFinOk):
                # SE MANTIENE APAGADA LA ALARMA
                GPIO.output(ALARMA, True)
                # ESPERAMOS 0.8seg
                time.sleep(1)
                while(True):
                    ini = int(distance(TRIGGER1, ECHO1))
                    fin = int(distance(TRIGGER2, ECHO2))
                    # PREGUNTAMO SI EN EL SENSOR DE INICIO NO DETECTA NADA
                    senIniOk = (ini > 190)
                    # PREGUNTAMOS SI HAY ALGUIEN EN EL SENSOR DE FIN
                    senFinOk = (ini < 200 and ini > 10)
                    if(senIniOk and senFinOk):
                        # SE MANTIENE APAGADA LA ALARMA Y VOLVEMOS AL CICLO WHILE PRINCIPAL
                        GPIO.output(ALARMA, True)
                        time.sleep(1)
                        break

    # Resetiando
    except KeyboardInterrupt:
        GPIO.cleanup()