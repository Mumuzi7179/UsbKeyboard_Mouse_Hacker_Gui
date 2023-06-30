import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def extract_data(types,choise,filename):
    posX, posY = 0, 0
    X, Y = [], []
    type_dicts = {"capdata": "usb.capdata", "usbhid": "usbhid.data"}
    mytype = type_dicts[types]
    choise_dicts = {"左键": "L", "右键": "R","无按键" : "N" ,"所有" : "ALL"}
    mychoise = choise_dicts[choise]
    os.system(f'tshark.exe -r "{filename}" -T fields -e {mytype}  > usb.dat')
    data = []

    result = open('result.txt', 'w')

    with open('usb.dat', "r") as f:
        for line in f:
            data.append(line[0:-1])

    for i in data:
        Bytes = bytes.fromhex(i)
        if(len(Bytes) == 8):
            horizontal = 2
            vertical = 4
            key = 1
        elif(len(Bytes) == 6):
            horizontal = 2
            vertical = 3
            key = 1
        elif(len(Bytes) == 4):
            horizontal = 1
            vertical = 2
            key = 0
        else:
            continue
        offsetX = Bytes[horizontal]
        offsetY = Bytes[vertical]
        if offsetX > 127:
            offsetX -= 256
        if offsetY > 127:
            offsetY -= 256
        posX += offsetX
        posY += offsetY
        if Bytes[key] == 1:
            if mychoise == "L":
                X.append(posX)
                Y.append(-posY)
                result.write(str(posX) + ' ' + str(-posY) + '\n')
        elif Bytes[key] == 2:
            if mychoise == "R":
                X.append(posX)
                Y.append(-posY)
                result.write(str(posX) + ' ' + str(-posY) + '\n')
        elif Bytes[key] == 0:
            if mychoise == "N":
                X.append(posX)
                Y.append(-posY)
                result.write(str(posX) + ' ' + str(-posY) + '\n')
        else:
            pass
        if mychoise == "ALL":
            X.append(posX)
            Y.append(-posY)
            result.write(str(posX) + ' ' + str(-posY) + '\n')
    result.close()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(X, Y, c='r', marker='o')
    return plt

