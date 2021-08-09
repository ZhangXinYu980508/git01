# coding:utf-8
import socket


class Server:
    # comandict = {"1": "AA 00 01 00 00 00 00 DD", "2": "AA 00 02 00 00 00 00 DD", "3": "AA 00 03 00 01 ",
    #              "4": "AA 00 03 00 01 "}
    comandict = {"1": "AA 00 01 01", "2": "AA 00 02 01 01", "3": "AA 00 03 01 01 01 ",
                 "4": "AA 00 03 00 01 "}

    def __init__(self, ip="192.168.0.201", port=10000):
        self.ip = ip
        self.port = port
        self.serversocket = None

    # 创建socket 对象
    def createSocket(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置端口监听客户端数量
    def setSocket(self, listennumber=10):
        if self.serversocket:
            self.serversocket.bind((self.ip, self.port))
            self.serversocket.listen(listennumber)

    def startServer(self):
        self.createSocket()
        self.setSocket()
        while True:
            print("服务端已启动等待客户端的连接")
            client, address = self.serversocket.accept()
            print("客户端IP地址: %s, 端口  %s " % (address[0], address[1]))
            self.handle(client)

    # 解析接收指令
    def handle(self, client):
        while True:
            command = input("请输入：\n"
                            "1. 音量增加 "
                            "2. 音量减少 "
                            "3. 复位 "
                            "4. 静音"
                            "\n")
            if not int(command) > 0 and int(command) < 5:
                print("输入错误, 请重新输入\n")
                continue

            value = 0
            # if command == "3" or command == "4":
            if command == "3":
                value = 128

            if not (command == "3" or command == "4"):
                while True:
                    value = input("请输入增加/减少音量值：\n")
                    if not int(value) >= 0 and int(value) < 256:
                        print("输入音量值错误,请重新输入")
                        continue
                    else:
                        break

            self.executeComand(client, command, value)

    # 解析操作指令
    def executeComand(self, client, command, value):
        comandstr = self.getCommand(command, value)
        self.sendComand(client, comandstr)

    # 发送16 进制数
    def sendComand(self, client, hexcode):
        client.send(bytes.fromhex(hexcode))
        # self.recv(client)
        # client.close()

    def getCommand(self, command, value):
        comandvalue = Server.comandict.get(command, "")
        if command in ["1", "2","3"]:
            hexValue = self.changHex(value)
            return comandvalue + " " + hexValue + " 00 DD"+ " 0D 0A"
        else:
            return comandvalue+ " 0D 0A"

    # 转成十六进制数
    def changHex(self, value):
        return hex(int(value))[2:].rjust(2, "0")

    def recv(self, client):
        currentData = ''
        while True:
            bytedata = client.recv(1024)
            flagbit = bytedata.hex()[-2:]
            if flagbit != 'dd':
                currentData += bytedata.hex()
                continue
            else:
                currentData += bytedata.hex()    # 字符串拼接字节异常
                print(currentData)
                currentData = ''
                break


if __name__ == '__main__':
    ser = Server()
    ser.startServer()
