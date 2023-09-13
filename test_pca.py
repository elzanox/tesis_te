# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60
onn = 65535 
off = 0

def maju():
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

def mundur():
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

def kiri():
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

def kanan():
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

def berhenti():
    pca.channels[0].duty_cycle = off
    pca.channels[1].duty_cycle = off

    pca.channels[2].duty_cycle = off
    pca.channels[3].duty_cycle = off

    pca.channels[4].duty_cycle = off
    pca.channels[5].duty_cycle = off
    
    pca.channels[6].duty_cycle = off
    pca.channels[7].duty_cycle git= off
    
    pca.channels[8].duty_cycle = off
    pca.channels[9].duty_cycle = off
    
    pca.channels[10].duty_cycle = off
    pca.channels[11].duty_cycle = off
# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of 
while True:
    berhenti()
    