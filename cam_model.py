#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
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

"""
from threading import Thread

def t():
    os.system('bash /home/pi/tiao/run.sh > /home/pi/tiao/server_log.txt 2>&1')

def run():
    t1 = Thread(target=t)
    print('Starting thread')
    t1.start()
"""
#p = psutil.Process(os.getpid())
#p.nice(20)

    #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
path = "/home/pi/tiao"
path_tiao = path+"/tiao"
    
try:

    #run()

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 10) 

 

    min_dog = 3

    #n_2dogs = 0
    n_obj = 0
    n_sacada = 1
    n_tiao = 2

    bark_time = 0.20
    #bark_time = 0.05

    run_time = bark_time + 0.05
    rec_time = 2

    WAIT_TURNS = int(60.0 / run_time)
    #WAIT_TURNS = 60

    SCORE_THRESHOLD = 0.90

    SOUND_THRESHOLD = 0.90
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

        s, img = cam.read()

        if args.a == 'nocam':

            pass

        else:

            cv2.imshow("Cam", img)
            cv2.waitKey(1)

        black = cv2.resize(img, (50,50))
        black = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)

        per = len(np.where(black < 50)[0])/float(2500) * 100

        return img, per

    #from threading import Thread

    #t1 = Thread(target = run_cam)
    #t1.start()

    name = [l for l in string.ascii_uppercase]

    pic_or_gif = "pic"

    while True:

        score = 0
        now = datetime.now()
        time_taken = time()

        
        try:
            sound = aud.R(bark_time)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            with open(path+'/error_audio.txt', 'w') as f:
                f.write('{},{},{},{}'.format(exc_type, e, fname, exc_tb.tb_lineno))
            aud = Audio()
            
        
        img, per = run_cam()

        if per > 75:

            print("Too dark")
            f = open(path + "/last_run.txt","w")
            time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
            f.write("Closed because too dark at: " + time_id+"\n")
            f.close()
            
            cam.release()
            cv2.destroyAllWindows()
     
            while True:
                pass     


        print("Sound:", '{:04f}'.format(sound), "Dark:", int(per))

        time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)

        if sound > SOUND_THRESHOLD:

            if pic_or_gif == "gif":

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

                s, img = cam.read()

            res = predict(img)
            score = res[2]
            pic_id =  str(now.day) +"_"+ str(now.month) +"_"+ str(now.hour) +"_"+ str(now.minute) +"_"+ str(now.second)
            print("Score:", '{:04f}'.format(score), "Sound:", '{:04f}'.format(sound))

            if score > SCORE_THRESHOLD and wait == 0:

                cv2.imwrite(path+"/auto_tweet.png",img)
                print("Salvo em "+path_tiao+"/tiao"+str(pic_id)+".png")
                cv2.imwrite(path_tiao+"/tiao"+str(pic_id)+".png", img)
                wait = WAIT_TURNS

                try:

                    print("Postando foto")

                    if pic_enabled:

                        if pic_or_gif == "pic":

                            pic_or_gif = "gif"
                            post_picture(path+"/auto_tweet.png")

                        else:

                            pic_or_gif = "pic"
                            os.system("python3 "+path+"/gif.py")

                except:

                    print("Corrigir")

            f = open(path + "/report.txt", 'a')
            f.write("W: "+ str(wait).zfill(2) + " " + str(time_id) + " S: " + '{:04f}'.format(score) + " V: " + '{:04f}'.format(sound) + "\n")
            f.close()

        if wait > 0:

            wait -= 1

        command_delay = (command_delay + 1) % loop

        if command_delay == 0:

            try:
                command = get_url()
                if command == "reboot" or command == "Reboot":
                    os.system("reboot")
                elif command == "shutdown" or command == "Shutdown":
                    os.system("shutdown now")
                elif command == "enable" or command == "Enable":
                    pic_enabled = True
                elif command == "disable" or command == "Disable":
                    pic_enabled = False
            except:
                pass

        time_end = time()

        print('{:04f}'.format(time_end - time_taken), "Sec", "Cmd:", command, "-", str(command_delay).zfill(2), "Time:", time_id, "W:", str(wait).zfill(3))

        f = open(path + "/last_run.txt","w")
        f.write(time_id+"\n")
        f.close()

        old_sound = sound
           
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    with open(path+'/error.txt', 'w') as f:
        f.write('{},{},{},{}'.format(exc_type, e, fname, exc_tb.tb_lineno))
    cam.release()
    os.system('python3 /home/pi/tiao/cam_model.py nocam')
