import time
import board
import adafruit_dht
from datetime import datetime
import pandas as pd
import os

path = "/home/pi/tiao"

dhtDevice = adafruit_dht.DHT11(board.D18)   
  
def read_temp():

    now = datetime.now()

    time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
       
    read = False
    
    while not read:
    
        try:
            temp = dhtDevice.temperature
            hum = dhtDevice.humidity
            
            print("{} Temperatura: {}, Humidade {}%".format(time_id, temp,hum))
                            
            if temp is not None:
                read = True
            
                f = open(path + "/temperature.txt", "a")
                f.write("{};{};{}\n".format(time_id, temp, hum))
                f.close()

                f = open(path + "/last_temperature.txt", "w")
                f.write("{};{};{}\n".format(time_id, temp, hum))
                f.close()

        
        except Exception as e:
            print(e)  
            
        time.sleep(1)
        
    dhtDevice.exit()
    
    df = pd.read_csv('/home/pi/tiao/temperature.txt', sep=';', header=None)
    df.rename(columns={0:'date', 1:'temp', 2:'hum'}, inplace=True)
    #df['data'] = pd.to_datetime(df['date'])
    df['data'] = pd.to_datetime(df['date'].iloc[1:]).dt.strftime("%d-%m-%Y %H:%M:%S")
    df['ano'] = pd.to_datetime(df['data']).dt.year
    df['mes'] = pd.to_datetime(df['data']).dt.month
    df['dia'] = pd.to_datetime(df['data']).dt.day
    df['hora'] = pd.to_datetime(df['data']).dt.hour
    
    g = df.groupby(['dia','mes','ano', 'hora'])[['temp', 'hum']].mean().reset_index().sort_values(by=['ano','mes','dia','hora'], ascending=True)
    g['data'] = g['dia'].astype('int').astype(str) + '-' + g['mes'].astype('int').astype(str) + '-' +  g['ano'].astype('int').astype(str) + ' ' + g['hora'].astype('int').astype(str)
    
    g.to_csv('/home/pi/tiao/data.csv', index=False)
    
    os.system('bash /home/pi/tiao/send_file.sh')

    try:
        print("saving to"+ path + "/last_send.txt")
        f = open(path + "/last_send.txt", "w")
        f.write("{}\n".format(time_id))
        f.close()
    except Exception as e:
        print(e)
            
if __name__ == '__main__':

    read_temp()

    
