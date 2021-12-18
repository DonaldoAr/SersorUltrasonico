from flask import Flask
from flask import request
from flask.json import jsonify
app = Flask(__name__)
import json
import RPi.GPIO as GPIO
import time
from concurrent.futures import ThreadPoolExecutor
# from FunUltra import 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pins=[2,4,15,22]
GPIO.setup(pins,GPIO.OUT)
GPIO.output(pins,GPIO.HIGH)

#  == PINES PARA SENSORES ==
rele1 = 18
rele2 = 16
ALARMA = 4
GPIO.setup(rele2, GPIO.IN)
GPIO.setup(rele1, GPIO.IN)
executor = ThreadPoolExecutor(max_workers=2)

contador = 0

# == PARA REVISAR ==
def tiempoAlarma(condicion, t):
    GPIO.output(ALARMA, condicion)
    time.sleep(t)

def checkAlarma():
    global contador
    try:
        while True:
            print("Vigilando")
            GPIO.output(ALARMA, True)
            rel1 = GPIO.input(rele1)
            rel2 = GPIO.input(rele2)
            if( (rel2 == False) and (rel1 == True) ):
                print("El usuario acaba de entrar de manera incorrecta")
                executor.submit( tiempoAlarma(False, 5))
            # == CUANDO LOS USUARIO ENTRA DE MANERA CORRECTA, SE ACTIVA EL SENSOR1 Y SE ENCUENTRA DESACTIVADO EL SENSOR2 ==
            elif( (rel1 == False) and (rel2 == True) ):
                print("El usuario acaba de entrar")
                GPIO.output(ALARMA, True)
                while(1):
                    estado = GPIO.input(22)
                    contador += 1
                    time.sleep(0.01)
                    rel1 = GPIO.input(rele1)
                    rel2 = GPIO.input(rele2)
                    # = EL USARIO ACTIVO EL SENSO2 Y SENSOR1
                    if( (rel1 == True) and (rel2 == False) ):
                        print("El usuario acaba de entrar a la tienda")
                        print(contador/100)
                        if( int(contador/100) > 60):
                            print("Se supero los 60seg, se espera 30 segundo solo para pasar")
                            contador = 30
                            tiempoAlarma(True, contador)
                            contador = 0
                            break
                        else:
                            tiempoAlarma(True, 2*contador/100)
                            print("salio de ciclo")
                            contador = 0
                            break
                    elif(estado):
                        break
    # Resetiando
    except KeyboardInterrupt:
        pass

# == ROUTES ===

# antes de una ruta
@app.before_first_request
def middleware():
    # print('Hello first Middleware')
    checkAlarma()

# Despues de un ruta
@app.teardown_request
def middleware():
    # print('Hello teardown_request')
    checkAlarma()

@app.before_request
def middleware():
    # print('Hello Middleware')
    checkAlarma()

@app.route('/on', methods = ['POST'])
def on():
        GPIO.output(4, GPIO.LOW)
        x = '{"led":"on"}'
        y = json.loads(x)
        checkAlarma()
        return y
	
@app.route('/off', methods = ['POST'])
def off():
        GPIO.output(4, GPIO.HIGH)
        x = '{"led":"off"}'
        y = json.loads(x)
        checkAlarma()
        return y
        
	
@app.route('/door', methods = ['POST'])
def door():
        open = request.json
        GPIO.output(15, GPIO.LOW)
        GPIO.output(2,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(2,GPIO.HIGH)
        time.sleep(6.5)
        GPIO.output(22,GPIO.HIGH)
        checkAlarma()
        # open = json.loads(open)
        return jsonify({"status": "ok"})
        # return open
	
if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, port=8000)
    