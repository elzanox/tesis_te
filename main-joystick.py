# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.
import time
import paho.mqtt.client as mqtt
dev = 0
if dev != 1:    
    from board import SCL, SDA
    import busio

    from adafruit_pca9685 import PCA9685 # Import the PCA9685 module.
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)

    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)
    # Set the PWM frequency to 60hz.
    pca.frequency = 60
    print(dev)

# MQTT broker configuration
# broker_address = "103.150.93.184"
broker_address = "localhost"
port = 1883
topicc = "control"

# MQTT client setup
client = mqtt.Client()
client.connect(broker_address, port)



# //65535
onn = 60000  
off = 0

def maju():
    print("maju bray")
    pca.channels[0].duty_cycle = off
    pca.channels[1].duty_cycle = onn

    pca.channels[2].duty_cycle = off
    pca.channels[3].duty_cycle = onn

    pca.channels[4].duty_cycle = off
    pca.channels[5].duty_cycle = onn
    
    pca.channels[6].duty_cycle = off
    pca.channels[7].duty_cycle = onn
    
    pca.channels[8].duty_cycle = off
    pca.channels[9].duty_cycle = onn
    
    pca.channels[10].duty_cycle = off
    pca.channels[11].duty_cycle = onn
    time.sleep(1)
def mundur():
    print("mundur bray")
    pca.channels[0].duty_cycle = onn
    pca.channels[1].duty_cycle = off

    pca.channels[2].duty_cycle = onn
    pca.channels[3].duty_cycle = off

    pca.channels[4].duty_cycle = onn
    pca.channels[5].duty_cycle = off
    
    pca.channels[6].duty_cycle = onn
    pca.channels[7].duty_cycle = off
    
    pca.channels[8].duty_cycle = onn
    pca.channels[9].duty_cycle = off
    
    pca.channels[10].duty_cycle = onn
    pca.channels[11].duty_cycle = off
    time.sleep(1)
def kiri():
    print("kiri bray")
    pca.channels[0].duty_cycle = off
    pca.channels[1].duty_cycle = onn

    pca.channels[2].duty_cycle = onn
    pca.channels[3].duty_cycle = off

    pca.channels[4].duty_cycle = off
    pca.channels[5].duty_cycle = onn
    
    pca.channels[6].duty_cycle = onn
    pca.channels[7].duty_cycle = off
    
    pca.channels[8].duty_cycle = off
    pca.channels[9].duty_cycle = onn
    
    pca.channels[10].duty_cycle = onn
    pca.channels[11].duty_cycle = off

def kanan():
    print("kanan bray")
    pca.channels[0].duty_cycle = onn
    pca.channels[1].duty_cycle = off

    pca.channels[2].duty_cycle = off
    pca.channels[3].duty_cycle = onn

    pca.channels[4].duty_cycle = onn
    pca.channels[5].duty_cycle = off
    
    pca.channels[6].duty_cycle = off
    pca.channels[7].duty_cycle = onn
    
    pca.channels[8].duty_cycle = onn
    pca.channels[9].duty_cycle = off
    
    pca.channels[10].duty_cycle = off
    pca.channels[11].duty_cycle = onn

def berhenti():
    print("berhenti bray")
    pca.channels[0].duty_cycle = off
    pca.channels[1].duty_cycle = off

    pca.channels[2].duty_cycle = off
    pca.channels[3].duty_cycle = off

    pca.channels[4].duty_cycle = off
    pca.channels[5].duty_cycle = off
    
    pca.channels[6].duty_cycle = off
    pca.channels[7].duty_cycle = off
    
    pca.channels[8].duty_cycle = off
    pca.channels[9].duty_cycle = off
    
    pca.channels[10].duty_cycle = off
    pca.channels[11].duty_cycle = off
# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of 
# Callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to MQTT topics here
    client.subscribe(topicc)
    
# Inisialisasi variabel payload_sebelumnya
payload_sebelumnya = None
# Callback for when a message is received from the MQTT broker
def on_message(client, userdata, message):
    global payload_sebelumnya  # Menggunakan payload_sebelumnya sebagai variabel global
    global state_maju, state_berhenti, state_kanan, state_kiri, state_mundur
    payload = message.payload.decode("utf-8")
    print("Received message '" + payload + "' on topic '" + message.topic + "'")

    # Memeriksa apakah payload sama dengan payload_sebelumnya
    if payload != payload_sebelumnya:
        # Payload berbeda, maka lakukan tindakan
        if payload == "UP":
            state_maju = 1
            state_mundur = 0
            state_kiri = 0
            state_kanan = 0
            state_berhenti = 0
            # maju()
        elif payload == "DOWN":
            state_maju = 0
            state_mundur = 1
            state_kiri = 0
            state_kanan = 0
            state_berhenti = 0
        elif payload == "LEFT":
            state_maju = 0
            state_mundur = 0
            state_kiri = 1
            state_kanan = 0
            state_berhenti = 0
        elif payload == "RIGHT":
            state_maju = 0
            state_mundur = 0
            state_kiri = 0
            state_kanan = 1
            state_berhenti = 0
        elif payload == "null":
            state_maju = 0
            state_mundur = 0
            state_kiri = 0
            state_kanan = 0
            state_berhenti = 1
    else:
        # Payload sama dengan yang sebelumnya, tidak lakukan apa-apa
        # print("Payload sama dengan sebelumnya, tidak ada tindakan yang diambil.")
        pass

    # Setel payload_sebelumnya ke payload saat ini
    payload_sebelumnya = payload

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message
state_maju = None
state_mundur = None
state_kiri = None
state_kanan = None
state_berhenti = None

# Start the MQTT client loop
client.loop_start()
# while True:
    # maju()
    # berhenti()

# Don't forget to handle exceptions and clean up when your script exits
# For example, you can use a try-except block to gracefully exit the script:
try:
    while True:
        if state_maju == True:
            maju()
        elif state_mundur == True:
            mundur()
        # # elif state_kiri == True:
        # #     kiri()
        # # elif state_kanan == True:
        # #     kanan()
        elif state_berhenti== True:
            berhenti()
        # berhenti()
        # maju()
        pass
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from MQTT broker")
    