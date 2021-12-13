import imageio
import os
from tweet import post_picture
from datetime import datetime

print("Criando gif")

path = "/home/pi/tiao"

filenames = os.listdir(path + "/gif/")
filenames.sort()

images = []

for filename in filenames:

    print(filename)
    images.append(imageio.imread(path + "/gif/" + filename))

imageio.mimsave(path + "/auto_output.gif", images)


print("Postando gif")

try:

    post_picture(path + "/auto_output.gif")

except Exception as e:

    print(e)
