import sys,os

normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","54":"/","55":"*","56":"-","57":"+","58":"<ENTER>","59":"1","5a":"2","5b":"3","5c":"4","5d":"5","5e":"6","5f":"7","60":"8","61":"9","62":"0","63":"."}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":"\"","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","54":"/","55":"*","56":"-","57":"+","58":"<ENTER>","59":"1","5a":"2","5b":"3","5c":"4","5d":"5","5e":"6","5f":"7","60":"8","61":"9","62":"0","63":"."}


def extract_data(types,filename):
    presses = []
    type_dicts = {"capdata": "usb.capdata", "usbhid": "usbhid.data","bluetooth":"btatt.value"}
    mytype = type_dicts[types]

    os.system(f'tshark.exe -r "{filename}" -T fields -e {mytype}  > usb.dat')
    with open("usb.dat", "r") as f:
        for line in f:
            presses.append(line[0:-1])
    result = ""
    result_data = []
    for press in presses:
        if press == '':
            continue
        if ':' in press:
            Bytes = press.split(":")
        else:
            Bytes = [press[i:i+2] for i in range(0, len(press), 2)]
        if Bytes[0] == "00":
            if Bytes[2] != "00" and normalKeys.get(Bytes[2]):
                result += normalKeys[Bytes[2]]
                result_data.append(normalKeys[Bytes[2]])
        elif int(Bytes[0],16) & 0b10 or int(Bytes[0],16) & 0b100000:
            if Bytes[2] != "00" and normalKeys.get(Bytes[2]):
                result += shiftKeys[Bytes[2]]
                result_data.append(shiftKeys[Bytes[2]])
        else:
            pass

    return result,result_data

#以下是对提取的键盘流量进行加工
def process_data(res):
    datas = []
    delete_data = []
    temp_del = []
    not_last_del = False
    CAP = 0
    for data in res:
        if(data == '<CAP>'):
            CAP ^= 1
        elif(data == '<DEL>'):
            try:
                temp_del.append(datas.pop())
            except:
                pass
            not_last_del = True
        elif(data == '<SPACE>'):
            if(not_last_del):
                delete_data += temp_del[::-1]
                temp_del = []
            datas.append(' ')
            not_last_del = False
        else:
            if(not_last_del):
                delete_data += temp_del[::-1]
                temp_del = []
            if(CAP == 0 or not data.isalpha()):
                datas.append(data)
            else:
                key = [k for k, v in normalKeys.items() if v == data][0]
                corresponding_value_in_shiftKeys = shiftKeys.get(key)
                datas.append(corresponding_value_in_shiftKeys)
            not_last_del = False

    datas = ''.join(datas)
    delete_data = ''.join(delete_data)
    return datas,delete_data
