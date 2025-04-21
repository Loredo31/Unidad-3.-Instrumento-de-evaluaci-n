from machine import Pin, ADC
from time import sleep
from network import WLAN, STA_IF
from urequests import post

# Pines del joystick
joystick_x = ADC(Pin(34))  # Eje X
joystick_y = ADC(Pin(35))  # Eje Y
joystick_sw = Pin(32, Pin.IN, Pin.PULL_UP)  # Botón

joystick_x.atten(ADC.ATTN_11DB)
joystick_y.atten(ADC.ATTN_11DB)

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzMHwz7b0uqCux_5XhaJXw5BgNeiLIQdzpsLC8l5yVN7SXoX1MTTuNQEy6YIIJUHsYG3g/exec"

def connect_wifi():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect("CGA2121_eax2rVq", "888ERmCpQHzMkNddBq")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWIFI-OK")

def send_to_sheets(x, y, sw):
    data = {
        "x": x,
        "y": y,
        "sw": sw
    }

    try:
        response = post(WEBAPP_URL, json=data)
        print("Respuesta:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar a Sheets:", e)

connect_wifi()

while True:
    x_val = joystick_x.read()
    y_val = joystick_y.read()
    sw_val = 0 if joystick_sw.value() == 0 else 1  # 0 si está presionado

    print(f"X: {x_val} | Y: {y_val} | Botón: {'Presionado' if sw_val == 0 else 'Libre'}")
    print("-" * 20)

    send_to_sheets(x_val, y_val, sw_val)
    sleep(1)
