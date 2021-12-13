import streamlit as st
import matplotlib.pyplot as plt
from time import sleep
import os
from PIL import Image
from read import read_inputs

from datetime import datetime


path = "/home/pi/sensor/sensor_agua/"



pl = st.empty()
t = st.empty()

sensors = read_inputs()

while True:

    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    inputs = read_inputs()

    if input != sensors:

        img = Image.open(path + str(sum(inputs)) + '.png')
        pl.image(img)
	
        sensors = inputs
    
    t.text(date_time)

    sleep(1)
    
"""
fig = plt.figure()

plt.imshow(Image.open(path + str(sum(inputs)) + '.png'))
plt.axis("off")

st.pyplot(fig)

  
"""

