#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sounddevice as sd
from datetime import datetime
import soundfile as sf
import os
import numpy as np
from time import time, sleep


class Audio():

    def __init__(self):
    
        self.id = self.get_id()
        self.device = sd.query_devices()[self.id]
        self.fs = int(self.device["default_samplerate"])    
       

    def get_time(self):

        now = datetime.now()
        time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
        return time_id


    def audio_id(self):

        now = datetime.now()
        pic_id =  str(now.day) +"_"+ str(now.month) +"_"+ str(now.hour) +"_"+ str(now.minute) +"_"+ str(now.second)

        return pic_id


    def get_id(self):

        dev = sd.query_devices()
        dev_list = [dev[i]["name"] for i in range(len(dev))]
        for i in range(len(dev_list)):

            if "USB" in dev_list[i]:

                return i

        print("Nenhum dispositivo foi encontrado")
        return -1
        

    def R(self, duration=0.25):
                
        rec = sd.rec(int((duration * self.fs)), samplerate = self.fs, channels=1, blocking=True)
        #sd.wait()
        #sleep(duration)

        return rec.max()
        
        

if __name__ == "__main__":

    sound = Audio()
    mx = sound.R()
    print(mx)



