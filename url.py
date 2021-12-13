#
# read the data from the URL and print it
#
import urllib.request
# open a connection to a URL using urllib

def get_url():

    webUrl  = urllib.request.urlopen("http://www.dontpad.com/ocaotiao", timeout=1)

    data = str(webUrl.read()).split('id="text">')[1].split('</textarea>')[0]
    return data
    #return "Enable"
