import os
import numpy as np
from keras.models import model_from_json
from keras.optimizers import Adam
import cv2
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

opt = Adam(lr = 0.00001)

path = "/home/pi/tiao"

def load_model():

    json_file = open(path+'/224_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path+'/224_best_model.h5')
    loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    return loaded_model

md_pred = load_model()

def predict(img):

    if img.shape[:2] != (224, 224): img = cv2.resize(img, (224,224))
    
    if img[0][0][0] > 1: img = img / 255.

    prediction = md_pred.predict(img.reshape(1, 224, 224, -1))[0]

    return prediction


if __name__ == "__main__":

    img = cv2.imread('auto_tweet.png')

    res = predict(img)
    print(res, np.argmax(res))
