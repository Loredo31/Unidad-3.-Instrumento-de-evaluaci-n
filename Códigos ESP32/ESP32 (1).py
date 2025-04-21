import network
from umqtt.simple import MQTTClient
import json
from machine import Pin, ADC, I2C
from time import sleep, ticks_us, ticks_diff
from i2c_lcd import I2cLcd


# Conexión WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("LOREDO LAP", "u55/5B85")
while not wifi.isconnected():
    pass
print("WiFi conectado:", wifi.ifconfig())

# MQTT
client_id = "esp32_sensores"
broker = "broker.emqx.io"# IP de tu servidor/broker MQTT
topic = "kapm/sensores"
cliente = MQTTClient(client_id, broker)
cliente.connect()

# Pines del motor
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(12, Pin.OUT)
IN3 = Pin(13, Pin.OUT)
IN4 = Pin(15, Pin.OUT)

# Botón y LEDs
boton = Pin(19, Pin.IN, Pin.PULL_UP)
led = Pin(23, Pin.OUT)
led2 = Pin(5, Pin.OUT)  # Nuevo LED para segundo sensor

# Fotoresistencia (LDR)
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # Rango de 0 a 4095

# Sensor ultrasónico 1
TRIG1 = Pin(2, Pin.OUT)
ECHO1 = Pin(18, Pin.IN)

# Sensor ultrasónico 2 (nuevo)
TRIG2 = Pin(4, Pin.OUT)
ECHO2 = Pin(16, Pin.IN)

# LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Secuencia del motor
secuencia = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

def mover_motor_derecha(pasos=200, velocidad=1):
    for _ in range(pasos):
        for paso in reversed(secuencia):  # ← secuencia invertida
            IN1.value(paso[0])
            IN2.value(paso[1])
            IN3.value(paso[2])
            IN4.value(paso[3])
            sleep(velocidad / 1000)
    detener_motor()

def detener_motor():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

def medir_distancia(trig, echo):
    trig.off()
    sleep(0.002)
    trig.on()
    sleep(0.01)
    trig.off()

    while echo.value() == 0:
        inicio = ticks_us()
    while echo.value() == 1:
        fin = ticks_us()

    duracion = ticks_diff(fin, inicio)
    distancia = duracion / 58.0
    return distancia

# Inicio del sistema
lcd.clear()
lcd.putstr("Iniciando sistema...")
sleep(2)
lcd.clear()

# Bucle principal
while True:
    distancia1 = medir_distancia(TRIG1, ECHO1)
    distancia2 = medir_distancia(TRIG2, ECHO2)
    luz = ldr.read()

    print("Luz:", luz)
    print("Distancia1:", distancia1, "cm")
    print("Distancia2:", distancia2, "cm")
    
    # Crear diccionario con los datos
    datos = {
    "distancia1": distancia1,
    "distancia2": distancia2,
    "luz": luz
     }

    # Convertir a JSON
    payload = json.dumps(datos)

    # Publicar por MQTT
    cliente.publish(topic, payload)
    print("Publicado:", payload)


    lcd.clear()

    mensaje = ""
    if distancia1 >= 8:
        mensaje += "Falta comida\n"
    if distancia2 >= 10:
        if mensaje:  # Ya hay un mensaje arriba
            mensaje += "    Falta agua\n"
        else:
            mensaje += "Falta agua\n"
    if not mensaje:
        mensaje = "Comida y agua\n OK"

    lcd.putstr(mensaje[:32])  # Para evitar desbordar caracteres

    # Botón
    if boton.value() == 0:
        led.on()
    else:
        led.off()

    # Nuevo LED con sensor 2
    if distancia1 >= 8 or distancia2 >= 10:
       led2.on()
    else:
       led2.off()


    # Activar motor si hay oscuridad
    if luz < 200:
        mover_motor_derecha(200, velocidad=1)

    sleep(1)

