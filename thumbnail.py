import json
import os
from PIL import Image

team = {}


def thumbnail(file, path):
    if not os.path.exists(file):
        return
    im = Image.open(file)
    im.thumbnail((350, 350))
    im.save(path)


def main():
    with open('AzuGoal/records.json', 'r') as f:
        records = json.load(f)

    for i in list(records.keys()):
        team = i.split('+')[3]
        file = "Azugoal/png/"+str(records[i])+".png"
        if not os.path.exists("AzuGoal/thumbnail"):
            os.mkdir("AzuGoal/thumbnail")
        path = "AzuGoal/thumbnail/" + team

        if not os.path.exists(path):
            print('Generating ' + path)
            os.mkdir(path)

        thumbnail(file, path+'/'+str(records[i])+".png")


if __name__ == '__main__':
    main()
