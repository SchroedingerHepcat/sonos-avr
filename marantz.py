import requests

class Marantz:
    def __init__(self, ip):
        self.ip = ip
    
    def sendCommand(self, command, zone='MainZone'):
        url  = 'http://' + self.ip + '/'
        url += zone + '/'
        url += 'index.put.asp'
        payload = {'cmd0': command}
        requests.get(url, payload)

    def powerOn(self):
        command = 'PutZone_OnOff/ON'
        self.sendCommand(command)
    
    def powerOff(self):
        command = 'PutZone_OnOff/OFF'
        self.sendCommand(command)
    
    def changeInput(self, inputName):
        command = 'PutZone_InputFunction/' + inputName
        self.sendCommand(command)

    def cd(self):
        self.changeInput('CD')
    
    def tv(self):
        self.changeInput('TV')
