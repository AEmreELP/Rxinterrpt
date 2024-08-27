
import serial
import select
import time

testList=[]
crc=0
indexTrack=-1
dn=0

def interpretation(byte):
    global testList
    global dataLenght
    global crc
    global indexTrack
    global dn

    # print(f" Header is:{data[0]}")

    if str(byte) > "7F":
        print(f"Our Header is : {byte}")
        y = int(byte) & 7
        indexTrack = 0
        testList.append(byte)
    elif indexTrack > 2:
        if (indexTrack > int(dataLenght, 16) + 2):
            crc = byte
            print(f"Our CRC is : {byte}")
            print("Data Geldi")
            dn=0
        else:
            testList.append(byte)
            indexTrack = indexTrack + 1
            dn = dn + 1
            print(f"Our {dn}.data is : {byte}")

    elif indexTrack == 2:
        print(f"Our Data Lenght is : {byte}")
        dataLenght = byte
        testList.append(byte)
        indexTrack = 3

    elif indexTrack == 1:
        print(f"Our command is : {byte}")
        komut = byte
        testList.append(byte)
        indexTrack = 2

    elif indexTrack == 0:
        print(f"Our K is : {byte}")
        k = byte
        n = ((0 * 128) + int(k, 16))
        indexTrack = 1
        testList.append(byte)


    #return myList;



if __name__ == '__main__':
    testList = ['0A','80' ,'07' ,'0A' ,'06' ,'0B' ,'0B' ,'0B' ,'0B' ,'0B' ,'0B','02']
    crc = 0
    indexTrack = -1
    dn = 0
    dataLenght=-5

    for byte in testList:
        interpretation(byte)




