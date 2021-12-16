# CODIGO PARA DETECTAR UNA ALARMA
# Libraries
import RPi.GPIO as GPIO
import time
from Filtrar_ruido import Filtrar_ruido          # Clase Filtro
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# # == PINES DE RELEE
# rele1 = 38
# rele2 = 40
rele1 = 12
rele2 = 36
GPIO.setup(rele2, GPIO.IN)
GPIO.setup(rele1, GPIO.IN)

# ALARMA FUNCIONA EN NORMALMENTE CERRADO
ALARMA = 7
GPIO.setup(ALARMA, GPIO.OUT)
GPIO.output(ALARMA, True)

if(__name__ == '__main__'):
    try:
        while True:
            GPIO.output(ALARMA, True)
            rel1 = GPIO.input(rele1)
            rel2 = GPIO.input(rele2)
            time.sleep(0.3)
            # PRUGUNTAMOS SI EN EL SENSOR DE "FIN" HAY ALGUIEN senFinQ ?
            senFinQ = (rel2 == True)
            # PREGUNTAMOS SI EN EL SENSOR DE INICIO NO HAY NADIE
            senIniQ = (rel1 == False)
            # CUANDO EL USUARIO SALE DE MANERA INCORRECTA
            if(senFinQ and senIniQ):
                print("= Se detecto a alguien =")
                GPIO.output(ALARMA, False)
                time.sleep(5)
                while(True):
                    rel1 = GPIO.input(rele1)
                    rel2 = GPIO.input(rele2)
                    print("= El usuario tiene que salir (Esperando salida) =")
                    if( (rel1 == True) and (rel2 == False) ):
                        print("Hay alguien por dentro pero activando el sensor 1")
                        # ENTONCES TODAVIA HAY ALGUIEN, SE SIGUE PRENDIENDO LA ALARMA
                        # GPIO.output(ALARMA, False)
                        # time.sleep(1)
                    elif( (rel1 == False) and (rel2 == False) ):
                        print("Hay alguien entre los dos sensores")
                        # ENTONCES TODAVIA HAY ALGUIEN, SE SIGUE PRENDIENDO LA ALARMA
                        # GPIO.output(ALARMA, False)
                        # time.sleep(1)
                    elif( (rel1 == True) and (rel2 == True) ):
                        print("Hay alguien activando los sensores")
                        # ALARMA ACTIVA SIGUE ACTIVA 
                        # GPIO.output(ALARMA, False)
                    elif( (rel1 == False) and (rel2 == True) ):
                        print("El usuario activo el sensor ultimo para regresar, sedesactia alarma")
                        # PERSONA SE SALIO 
                        GPIO.output(ALARMA, True)
                        break
            # == CUANDO LOS USUARIO ENTRA DE MANERA CORRECTA, SE ACTIVA EL SENSOR1 Y SE ENCUENTRA DESACTIVADO EL SENSOR2 ==
            elif( (rel1 == True) and (rel2 == False) ):
                print("El usuario acaba de entrar")
                GPIO.output(ALARMA, True)
                while(True):
                    rel1 = GPIO.input(rele1)
                    rel2 = GPIO.input(rele2)
                    # = EL USARIO ACTIVO EL SENSO2 Y SENSOR1
                    if( (rel1 == False) and (rel2 == True) ):
                        print("El usuario acaba de entrar a la tienda")
                        GPIO.output(ALARMA, True)
                        break
                    # == SE ACTIVO SENSOR1 Y SENSOR2 ==
                    elif( (rel1 == True) and (rel2 == True) ):
                        print("Los usuarios activaron los dos sensores, hay mucha gente")
                    # == SENSOR1 Y SENSOR2 DESACTIVADOS ==
                    elif( (rel1 == False) and (rel2 == False) ):
                        print("El usuario se encuentra entre los dos sensore, pero sensores en 0")
                    # == SENSOR1 Y SENSOR2 DESACTIVADOS ==
                    elif( (rel1 == True) and (rel2 == False) ):
                        print("El usuario encuentra en la entrada todavia")
    # Resetiando
    except KeyboardInterrupt:
        GPIO.cleanup()