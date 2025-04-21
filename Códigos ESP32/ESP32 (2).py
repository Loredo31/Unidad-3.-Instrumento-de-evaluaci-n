from machine import ADC, Pin
import time

# ---------------------- Sensor de nivel de agua (ADC) ----------------------
sensor = ADC(Pin(34))  
sensor.atten(ADC.ATTN_11DB)  # Rango hasta ~3.3V
sensor.width(ADC.WIDTH_12BIT)  # Resolución de 12 bits (0-4095)

# ---------------------- Bomba de agua ----------------------
bomba = Pin(2, Pin.OUT)
nivel_objetivo = 1000  # Nivel mínimo requerido para apagar la bomba

# ---------------------- Bucle principal infinito ----------------------
while True:
    nivel = sensor.read()
    print("Nivel actual de agua (ADC):", nivel)

    # Control de la bomba según nivel de agua
    if nivel < nivel_objetivo:
        print("Nivel bajo. Activando bomba...")
        bomba.on()
    else:
        bomba.off()
        print("Nivel adecuado. Bomba apagada.")

    time.sleep(2)
