#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
import psutil
from tweet import post_picture
from time import sleep, time
from datetime import datetime
from audio import Audio
from url import get_url
#from model import predict
from model_224 import predict
import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument("a", nargs='?', default="empty")
args = parser.parse_args()

p = psutil.Process(os.getpid())
p.nice(20)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

cam = cv2.VideoCapture(0)
#cam.set(5,10)

path = "/home/felipe/backup"
path_tiao = path+"/tiao"

min_dog = 3

#n_2dogs = 0
n_obj = 0
n_sacada = 1
n_tiao = 2

bark_time = 0.20
#bark_time = 0.05

run_time = bark_time + 0.05

WAIT_TURNS = int(60.0 / run_time)
#WAIT_TURNS = 60

SCORE_THRESHOLD = 0.90

SOUND_THRESHOLD = 0.50
#SOUND_THRESHOLD = -100

pic_enabled = True
#pic_enabled = False

time_init = time()

wait = 0

time_end = 0
old_sound = 0
command_delay = 0
command = "Init"
loop = int(20. / run_time)

aud = Audio()

def run_cam():

    #while True:
    
    print("Debug image get")

    s, img = cam.read()

    if args.a == 'nocam':

        pass

    else:

        cv2.imshow("Cam", img)
        cv2.waitKey(1)

    black = cv2.resize(img, (50,50))
    black = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)

    per = len(np.where(black < 50)[0])/float(2500) * 100
    
    print("Debug image read")

    return img, per

#from threading import Thread

#t1 = Thread(target = run_cam)
#t1.start()

name = [l for l in string.ascii_uppercase]

pic_or_gif = "pic"

while True:

    print("Debug antes do datetime")
    score = 0
    now = datetime.now()
    time_taken = time()

    print("Debug antes do audio")
    try:
        sound = aud.R(bark_time)
    except Exception as e:
        print(e)
        aud = Audio()

    print("Debug antes de pegar imagem")
    img, per = run_cam()

    if per > 75:

        print("Too dark")
        #f = open(path + "/last_run.txt","w")
        #time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
        #f.write("Closed because too dark at: " + time_id+"\n")
        #f.close()
        #break
        sleep(1800)


    print("Sound:", '{:04f}'.format(sound), "Dark:", int(per))

    time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)

    print("Debug antes de testar o som")
    if sound > SOUND_THRESHOLD:

        if pic_or_gif == "gif":
            print("Debug gif")
            for frame in range(10):

                s, im = cam.read()

            for frame in range(17):

                t = time()
                s, im = cam.read()

                if frame == 8:

                    img = im

                cv2.imwrite(path+"/gif/"+name[frame] + ".png", cv2.resize(im, (480,360)))

                while (time()) - t < 0.100:

                    pass

                print(frame, time() - t)

        else:
            print("Debug pic")
            s, img = cam.read()


        print("Debug predict")
        res = predict(img)
        score = res[2]
        pic_id =  str(now.day) +"_"+ str(now.month) +"_"+ str(now.hour) +"_"+ str(now.minute) +"_"+ str(now.second)
        print("Score:", '{:04f}'.format(score), "Sound:", '{:04f}'.format(sound))

        print("Debug teste score")
        if score > SCORE_THRESHOLD and wait == 0:

            print("Debug salvar imgs")
            cv2.imwrite(path+"/auto_tweet.png",img)
            print("Salvo em "+path_tiao+"/tiao"+str(pic_id)+".png")
            cv2.imwrite(path_tiao+"/tiao"+str(pic_id)+".png", img)
            wait = WAIT_TURNS

            try:

                print("Debug postar foto")
                print("Postando foto")

                if pic_enabled:

                    if pic_or_gif == "pic":

                        print("Debug postar pic")
                        pic_or_gif = "gif"
                        post_picture(path+"/auto_tweet.png")

                    else:
                        print("Debug postar gif")
                        pic_or_gif = "pic"
                        os.system("python3 "+path+"/gif.py")

            except:

                print("Corrigir")

        #f = open(path + "/report.txt", 'a')
        #f.write("W: "+ str(wait).zfill(2) + " " + str(time_id) + " S: " + '{:04f}'.format(score) + " V: " + '{:04f}'.format(sound) + "\n")
        #f.close()

    if wait > 0:

        wait -= 1


    time_end = time()

    print('{:04f}'.format(time_end - time_taken), "Sec", "Cmd:", command, "-", str(command_delay).zfill(2), "Time:", time_id, "W:", str(wait).zfill(3))

    print("Debug log")
    f = open(path + "/last_run.txt","w")
    f.write(time_id+"\n")
    f.close()

    old_sound = sound
