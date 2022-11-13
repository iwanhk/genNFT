import json
import os
from PIL import Image

team = {}


def thumbnail(file, path):
    im = Image.open(file)
    im.thumbnail((80, 80))
    im.save(path)


def main():
    with open('HotoDoge/records.json', 'r') as f:
        records = json.load(f)

    for i in list(records.keys()):
        team = i.split('+')[2][6:]
        file = "HotoDoge/png/"+str(records[i])+".png"
        path = "HotoDoge/thumbnail/" + team

        if not os.path.exists(path):
            print('Generating ' + path)
            os.mkdir(path)

        thumbnail(file, path+'/'+str(records[i])+".png")


if __name__ == '__main__':
    main()
