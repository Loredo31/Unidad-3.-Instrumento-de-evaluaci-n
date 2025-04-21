from machine import Pin, time_pulse_us
from time import sleep
from network import WLAN, STA_IF
from urequests import post

# Pines del sensor ultrasónico
TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwwGcT_h-AmIpMb_FjCmjQiM2bQKi6e9rxN4nVZ2SHfyjhHNupdNf4fbbN7ybE4Fgqg/exec"

def connect_wifi():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect("CGA2121_eax2rVq", "888ERmCpQHzMkNddBq")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWIFI-OK")

def medir_distancia():
    TRIG.off()
    sleep(0.000002)
    TRIG.on()
    sleep(0.00001)
    TRIG.off()

    try:
        duracion = time_pulse_us(ECHO, 1, 30000)  # espera hasta 30ms
        distancia = (duracion / 2) / 29.1  # Convertir a cm
        return round(distancia, 2)
    except OSError as e:
        print("Error al medir:", e)
        return -1

def send_to_sheets(distancia):
    data = {
        "distancia": distancia
    }

    try:
        response = post(WEBAPP_URL, json=data)
        print("Respuesta:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar a la hoja de cálculo:", e)

connect_wifi()

while True:
    distancia = medir_distancia()
    if distancia != -1:
        print(f"Distancia medida: {distancia} cm")
        send_to_sheets(distancia)
    else:
        print("No se pudo medir la distancia")

    print("-" * 20)
    sleep(2)
