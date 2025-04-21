# Unidad3. Instrumento de evaluación

# Alimentador automatico para mascotas

## Descripción General

**Alimentador automatico para mascotas** es un sistema de automatización diseñado para la alimentación rapida y eficiente para las mascotas mediante sensores y actuadores conectados a través de una red de microcontroladores **ESP32**. Este aparato inteligente se coordina mediante **Node-RED**, e incluye visualización gráfica, control manual y almacenamiento de datos en **SQLite**.

El sistema combina sensores de ambiente con controladores mecánicos para realizar acciones automáticas como:
- Suministra alimento y/o agua en los recipientes
- Calcula el nivel de agua y/o comida en el almacenamiento
- Da aviso a los usuarios si alguno de estos dos recursos es escaso

---

## Objetivos del Proyecto

- Automatizar procesos de alimentación para las mascotas.
- Diseñar una solución IoT descentralizada basada en múltiples ESP32.
- Visualizar datos en tiempo real y guardar el histórico en una base de datos SQLite.
- Proporcionar control manual del aparato.

---

## Tecnologías Utilizadas

| Tecnología       | Uso Principal                                   |
|------------------|--------------------------------------------------|
| ESP32            | Microcontroladores para manejar sensores/actuadores |
| Node-RED         | Plataforma de control |
| Raspberry Pi     | Máquina virtual que aloja Node-RED y SQLite  |
| PostgreSQL       | Base de datos relacional para almacenamiento de datos |
| MQTT             | Protocolo de mensajería entre nodos ESP32 y Node-RED |
| Impresión 3D     | Estructuras físicas y mecanismos personalizados   |

---

## Arquitectura del Sistema

El sistema está distribuido en **2 placas ESP32**, cada una encargada de distintos sensores y actuadores. La comunicación entre ellas se realiza mediante **MQTT**, utilizando **Node-RED** como broker.
```
        [ESP32-1] ---> Motor Paso, Sensores ultrasonicos, Sensor de fotoresistencia, LEDs, Pantalla LCD, Boton
        [ESP32-2] ---> Bomba de agua, Relevador, Sensor de agua

                      ↕  MQTT
                    [Node-RED]
                        ↕
                    [SQLite]
```

## **Tabla de Actuadores**

| **Nombre**             | **Tipo**                | **Uso**                                                                 | **Imagen** |
|------------------------|-------------------------|--------------------------------------------------------------------------|------------|
| **Pantalla LCD**       | Actuador de Salida      | Muestra si la comida o agua estan por terminarse del almacen                          | <img src="https://github.com/user-attachments/assets/4bf088ba-d3d1-4aea-aab1-8bd3dd8c1f48" width="100"> |
| **Motor Paso a Paso**  | Actuador de Movimiento  | Gira en pasos precisos para dispensar alimento          | <img src="https://github.com/user-attachments/assets/e7c641b1-ff37-40ef-8c2c-9576ee7891ee" width="100"> |
| **LEDs**               | Actuador Visual         | Se iluminan si hay una advertencia de agua u comida por terminarce, se enciende para iluminar el sensor LDR y funcione el motor a pasos     | <img src="https://github.com/user-attachments/assets/b0d5934c-12ae-4927-8a38-046f7a9b8195" width="100"> | 
| **Bomba de Agua**      | Actuador Hidráulico     | Permite el flujo de agua cuando se necesita llenar el plato | <img src="https://github.com/user-attachments/assets/91f4d8e3-f0b5-48ed-8f20-d4d5a3c5ff39" width="100"> |
| **Relevador**          | Actuador de Control     | Activa o desactiva la bomba de agua | <img src="https://github.com/user-attachments/assets/c78ab39c-ad4f-4a0a-8305-45acbcc570a1" width="100"> |

---

## **Tabla de Sensores**

| **Nombre**             | **Tipo**             | **Uso**                                                         | **Imagen** |
|------------------------|----------------------|------------------------------------------------------------------|------------|
| **Sensor Ultrasónico** | Sensor de Distancia  | Detecta la el espacio vacio en el recipiente para enviar la alerta                | <img src="https://github.com/user-attachments/assets/05caa13a-5f45-4a04-9b6f-37066208a5b7" width="100"> |
| **Sensor LDR**         | Sensor de Luz        | Detecta el nivel de luz para activar o desarctivar el motor a pasos                              | <img src="https://github.com/user-attachments/assets/ec8c293e-8974-4bfc-8ced-33b1ee464d63" width="100"> |
| **Sensor de Agua**     | Sensor de Líquido    | Detecta el nivel de agua en el recipiente para encender o apagar la bomba                            | <img src="https://github.com/user-attachments/assets/2eb8b9fd-3866-428c-86ac-03362d4e61a0" width="100"> |
| **Botón (Pulsador)** | Sensor de Entrada | Enciende un led para activar el sensor LDR | <img src="https://github.com/user-attachments/assets/21aa5846-a403-48c8-a9c4-9c2dc77a3084" width="100"> |

---

## 🛠 Funcionalidad del Sistema

### Servidor de agua
Cuando el **sensor de agua** detecta que el agua en el plato es baja, enciende la **bomba de agua**, lanzara el agua al recipiente hasta que el nivel de agua sea adecuado.

### Servidor de comida
El **boton** enciende un **LED** el cual omitira luz para que lo detecte el **sensor LDR**. Si el sensor detecta la luz el **motor a pasos** comenzara a girar sacando comida, cuando se deje de oprimir el **boton** el **LED** se apagara y dejara de mandar comida.

### Alerta de comida y/o agua
El **sensor ultrasonico** medira la distancia entre este mismo y la comida o agua en los recimientes, si estos tinen una distancia superior a 10 cm, se encenderan dos **LEDs** rojos y la **pantalla LCD** enviara un mensaje de comida o agua insuficientes segun sea el caso.

---

## Prototipo

El prototipo fue creada con materiales comunes como madera, papel cascaron, frascos y un dispensador impreso en 3D (sirve la comida).

**Imágenes del prototipo**
<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 20px;"> <img src="https://github.com/user-attachments/assets/de32992b-8a7d-4899-8230-848be7ca8ab6" alt="Imagen 1" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/b4b91a90-7ace-4e10-aaad-5c82f6dfd937" alt="Imagen 2" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/60b443d1-6dc9-4596-83cf-43bcc734d5c9" alt="Imagen 3" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/aa25aa33-ce80-45d5-9357-a65053784ac4" alt="Imagen 4" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/787a2090-2863-40fb-82d7-a46705006e7d" alt="Imagen 4" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> <img src="https://github.com/user-attachments/assets/1d419685-e435-44d6-a40f-6aefd6ca231a" alt="Imagen 4" style="width: 300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"> </div>

---
## Diagramas de las placas

**Placa 1 (Motor Paso, Sensores ultrasonicos, Sensor de fotoresistencia, LEDs, Pantalla LCD, Boton)**
<br>

Link: https://app.cirkitdesigner.com/project/03323c64-a62a-40d1-a593-d0e92c2792ca

<img src="https://github.com/user-attachments/assets/0051de63-2881-4f79-bf67-e2398111643c">
<br> 
**Placa 2 (Bomba de agua, Relevador, Sensor de agua)**
<br>

Link: https://app.cirkitdesigner.com/project/03323c64-a62a-40d1-a593-d0e92c2792ca

<img src="https://github.com/user-attachments/assets/9dfb0382-4bc0-4bb8-bb5a-41dc03d36fcc">
<br>
---

## Base de Datos y Almacenamiento

El sistema guarda todos los datos generados por los sensores en una base de datos **SQLite** permitindo un control eficiente ademas de poder consultar los datos ya registradoe.

<img src="https://github.com/user-attachments/assets/d0cd7f99-5050-43dc-bf88-2a5003a70c41">

---


## Videos explicando el funcionamiento de cada placa

Link a videos

https://drive.google.com/drive/folders/1FzxKbiOTlkNObt1a5S4nrsO6X3wCQRds?usp=sharing

## Videos explicando el funcionamiento general del prototipo

Link a videos

https://drive.google.com/drive/folders/1FzxKbiOTlkNObt1a5S4nrsO6X3wCQRds?usp=sharing

---

## Ejecicios de Clase

Link a videos

https://drive.google.com/drive/folders/1nj32m4lo2pFC3ACGYva-95rT2RvLLuux?usp=sharing

## Coevaluación

https://docs.google.com/document/d/1jDS9AxsSn1z5lsY4fK3YzhkUiO5Kk1glECyVzDjCRfc/edit?usp=sharing

---

## ✍️ Autores

- **Nombre del equipo**: Alimentador automatico para mascotas GDS0651 y GDS0653
- **Integrantes**:
  - Padrón Martínez Karen Anahí
  - Loredo Melendez Jose de Jesus

---
