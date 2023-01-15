# -*- coding: utf-8 -*-

import struct
import os

headerList = [
    ["No", 40],
    ["1.02基準 BGMリスト", 200],
    ["BGM ファイル名", 200],
    ["BGM名", 200],
    ["start", 120],
    ["loop start", 120]
]

ver102Music = {
    "RAIL001.BIN": "OPのレール(BGMはダミー)",
    "RAIL002.BIN": "架空 〜Going My Way〜",
    "RAIL003.BIN": "Power-running",
    "RAIL004.BIN": "FullNotch",
    "RAIL005.BIN": "Rail-Roader's shooting star",
    "RAIL006.BIN": "Sands of Time",
    "RAIL007.BIN": "r90",
    "RAIL008.BIN": "Missin",
    "RAIL010.BIN": "ダミー",
    "RAIL011.BIN": "電D沿線 阪急宝塚線",
    "RAIL012.BIN": "電D沿線 阪急京都線",
    "RAIL013.BIN": "電D沿線 京津線",
    "RAIL020.BIN": "二人バトル 阪急宝塚線",
    "RAIL021.BIN": "二人バトル 阪急京都線",
    "RAIL022.BIN": "二人バトル 京津線"
}


class LSMusicDecrypt():
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
        self.musicList = []
        self.indexList = []
        index = 0

        index = 16
        header = line[0:index]
        if header != b'DEND_MAP_VER0100' and header != b'DEND_MAP_VER0101':
            self.error = "LSのMapではありません"
            return

        # Model
        readModelCnt = line[index]
        index += 1
        for i in range(readModelCnt):
            modelNameLen = line[index]
            index += 1
            # modelName
            line[index:index + modelNameLen].decode("shift-jis")
            index += modelNameLen
            for j in range(2):
                index += 1
            cnt = line[index]
            if cnt != 0xFF:
                index += 1
                for j in range(cnt):
                    for k in range(2):
                        index += 2
            else:
                index += 1

        # Music
        self.indexList.append(index)
        musicArr = []

        file_name = os.path.basename(self.filePath)
        if file_name in ver102Music:
            musicArr.append(ver102Music[file_name])
        else:
            musicArr.append("-")

        readMusicNameLen = line[index]
        index += 1
        musicName = line[index:index + readMusicNameLen].decode("shift-jis")
        musicArr.append(musicName)
        index += readMusicNameLen

        readMusicFileLen = line[index]
        index += 1
        musicFile = line[index:index + readMusicFileLen].decode("shift-jis")
        musicArr.append(musicFile)
        index += readMusicFileLen

        start = struct.unpack("<f", line[index:index + 4])[0]
        start = round(start, 4)
        index += 4
        musicArr.append(start)

        loopStart = struct.unpack("<f", line[index:index + 4])[0]
        loopStart = round(loopStart, 4)
        index += 4
        musicArr.append(loopStart)

        self.musicList.append(musicArr)
        self.indexList.append(index)

    def saveMusic(self):
        try:
            newByteArr = bytearray(self.byteArr[0:self.indexList[0]])
            for i in range(len(self.musicList)):
                for j in range(2, len(headerList)):
                    if headerList[j][0] in ["start", "loop start", "loop end"]:
                        time = struct.pack("<f", self.musicList[i][j - 1])
                        for n in time:
                            newByteArr.append(n)
                    else:
                        name = self.musicList[i][j - 1].encode("shift-jis")
                        nameLen = len(name)
                        newByteArr.append(nameLen)

                        for n in name:
                            newByteArr.append(n)

            newByteArr.extend(self.byteArr[self.indexList[-1]:])
            w = open(self.filePath, "wb")
            w.write(newByteArr)
            w.close()
            return True
        except Exception as e:
            self.error = str(e)
            return False
