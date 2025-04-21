from machine import Pin, ADC
from time import sleep
from network import WLAN, STA_IF
from urequests import post

# Sensor de nivel de agua (ej: humedad de suelo) en pin analógico 34
agua_sensor = ADC(Pin(34))
agua_sensor.atten(ADC.ATTN_11DB)  # Rango completo de 0 a 3.3V (0-4095)

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzXFPLyNaB0OA_SsRK_t6JnHRozb4Lj3pkxK3i1EMB1Mk5n1huVFaD-xGcB9M4IiI6uYw/exec"

def connect_wifi():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect("CGA2121_eax2rVq", "888ERmCpQHzMkNddBq")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWIFI-OK")

def send_to_sheets(agua):
    data = {
        "agua": agua
    }

    try:
        response = post(WEBAPP_URL, json=data)
        print("Respuesta:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar a la hoja de cálculo:", e)

connect_wifi()

while True:
    try:
        agua = agua_sensor.read()  # Valor entre 0 y 4095
        print(f"Nivel de agua: {agua}")
        print("-" * 20)

        send_to_sheets(agua)

    except Exception as e:
        print("Error al leer el sensor de agua:", e)

    sleep(2)
