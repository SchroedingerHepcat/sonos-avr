import requests
import xml.etree.ElementTree as ElementTree

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

    def getPowerState(self):
        root = self.retrieveStateXml()
        if root[2][0].text == 'ON':
            return True
        else:
            return False

    def getCurrentInput(self):
        root = self.retrieveStateXml()
        return root[17][0].text

    def retrieveStateXml(self):
        url = 'http://' + self.ip + '/goform/formMainZone_MainZoneXml.xml'
        response = requests.get(url)
        if response.status_code == 200:
            root = ElementTree.fromstring(response.text)
            return root
        else:
            print('Could not retrieve status xml.')
            return response
