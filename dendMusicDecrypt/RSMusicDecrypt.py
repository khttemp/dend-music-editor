# -*- coding: utf-8 -*-

import struct

headerList = [
    ["bgm No", 6],
    ["1.08基準\n読み込み", 8],
    ["1.08基準\nBGM名", 8],
    ["BGM\nファイル名", 10],
    ["BGM名", 8],
    ["start", 5],
    ["loop start", 9],
    ["loop end", 7],
    [" ", 3]
]

class RSMusicDecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.headerList = headerList
        self.musicList = []
        self.indexList = []
        self.byteArr = []
        self.error = ""

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            self.decrypt(line)
            self.byteArr = bytearray(line)
            return True
        except Exception as e:
            self.error = str(e)
            return False
    def printError(self):
        f = open("error_log.txt", "w")
        f.write(self.error)
        f.close()
    def decrypt(self, line):
        #self.trainInfoList = []
        #self.indexList = []
        index = 0
        ver = line[index]
        index += 1

        cdCnt = line[index]
        index += 1

        for i in range(cdCnt):
            tcnt = line[index]
            index += 1
            for j in range(tcnt):
                track_time = struct.unpack("<h", line[index:index+2])[0]
                index += 2
            total_time = struct.unpack("<h", line[index:index+2])[0]
            index += 2

        musicCnt = line[index]
        index += 1

        for i in range(musicCnt):
            musicFileNameLen = line[index]
            index += 1
            musicFileName = line[index:index+musicFileNameLen].decode("shift-jis")
            index += musicFileNameLen
            musicNameLen = line[index]
            index += 1
            musicName = line[index:index+musicNameLen].decode("shift-jis")
            index += musicNameLen
            start = struct.unpack("<f", line[index:index+4])[0]
            start = round(start, 4)
            index += 4
            loopStart = struct.unpack("<f", line[index:index+4])[0]
            loopStart = round(loopStart, 4)
            index += 4
            loopEnd = struct.unpack("<f", line[index:index+4])[0]
            loopEnd = round(loopEnd, 4)
            index += 4

    def saveTrain(self):
        try:
            w = open(self.filePath, "wb")
            w.write(self.byteArr)
            w.close()
            return True
        except Exception as e:
            self.error = str(e)
            return False
