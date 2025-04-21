from machine import Pin, ADC
from time import sleep
from network import WLAN, STA_IF
from urequests import post

# LDR conectada al pin analógico 34
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # Rango 0 - 4095 (0 a 3.3V)

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwJDS7EIIVz77-mJ3XtlUcLgQgCcbcJfE12k1uX7wiK9WxuEYy4KAlOb0r6zzeI4EqKmw/exec"

def connect_wifi():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect("CGA2121_eax2rVq", "888ERmCpQHzMkNddBq")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWIFI-OK")

def send_to_sheets(luz):
    data = {
        "luz": luz
    }

    try:
        response = post(WEBAPP_URL, json=data)
        print("Respuesta:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar a la hoja de cálculo:", e)

connect_wifi()

while True:
    luz = ldr.read()  # Valor entre 0 (mucha luz) y 4095 (poca luz)
    print(f"Intensidad de luz: {luz}")
    print("-" * 20)

    send_to_sheets(luz)
    sleep(2)
