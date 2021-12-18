# CODIGO PARA DETECTAR UNA ALARMA
# Libraries
import RPi.GPIO as GPIO
import time
from Filtrar_ruido import Filtrar_ruido          # Clase Filtro
# Para usar hilos reciclados
from concurrent.futures import ThreadPoolExecutor
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# # == PINES DE RELEE
rele1 = 12
rele2 = 36
GPIO.setup(rele2, GPIO.IN)
GPIO.setup(rele1, GPIO.IN)

# def tiempoAlarma():
def tiempoAlarma(condicion, t):
    GPIO.output(ALARMA, condicion)
    time.sleep(t)

# ALARMA FUNCIONA EN NORMALMENTE CERRADO
ALARMA = 7
GPIO.setup(ALARMA, GPIO.OUT)
GPIO.output(ALARMA, True)
global contador
contador = 0
if(__name__ == '__main__'):
    executor = ThreadPoolExecutor(max_workers=2)
    try:
        while True:
            print("Vigilando")
            GPIO.output(ALARMA, True)
            rel1 = GPIO.input(rele1)
            rel2 = GPIO.input(rele2)
            if( (rel2 == False) and (rel1 == True) ):
                print("El usuario acaba de entrar de manera incorrecta")
                # executor.submit( tiempoAlarma, False, 5)
                executor.submit( tiempoAlarma(False, 5))
            # == CUANDO LOS USUARIO ENTRA DE MANERA CORRECTA, SE ACTIVA EL SENSOR1 Y SE ENCUENTRA DESACTIVADO EL SENSOR2 ==
            elif( (rel1 == False) and (rel2 == True) ):
                print("El usuario acaba de entrar")
                GPIO.output(ALARMA, True)
                while(True):
                    contador += 1
                    time.sleep(0.01)
                    rel1 = GPIO.input(rele1)
                    rel2 = GPIO.input(rele2)
                    # = EL USARIO ACTIVO EL SENSO2 Y SENSOR1
                    if( (rel1 == True) and (rel2 == False) ):
                        print("El usuario acaba de entrar a la tienda")
                        print(contador/100)
                        if((contador/100)> 60):
                            contador = 10
                            tiempoAlarma(True, 10)
                            contador = 0
                            break
                        else:
                            tiempoAlarma(True, 2*contador/100)
                            print("salio de ciclo")
                            contador = 0
                            break
    # Resetiando
    except KeyboardInterrupt:
        GPIO.cleanup()