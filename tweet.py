import tweepy
from datetime import datetime

path = "/home/pi/tiao"
deg = u"\N{DEGREE SIGN}"

def post_picture(image_path, msg=None):

    # personal details
    consumer_key =""
    consumer_secret =""
    access_token ="-"
    access_token_secret =""

    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    now = datetime.now()
    time_id = '{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
    
    
    temp,hum = open(path + '/last_temperature.txt', 'r').read().split(';')[1:]

    if msg is not None:
            tweet = msg
    else:
            tweet = "Olar ("+ time_id + " - " + temp + deg + "C" + ")" # toDo
    #image_path ="path of the image" # toDo

    # update the status
    status = api.update_with_media(image_path, tweet)
    api.update_status(status)


if __name__ == "__main__":
    
    post_picture(path + '/auto_tweet.png')
