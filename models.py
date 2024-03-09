from dataclasses import dataclass

@dataclass
class Connection:
    proto: str
    connectionId: str
    uid: str
    localAddr: str
    remoteAddr: str
    state: str
    pid: str
    exeName: str

    def getVals(self):
        return f'Proto {self.proto}, connection id {self.connectionId}, uid {self.uid}, local address {self.localAddr}, remote address {self.remoteAddr}, state {self.state}, pid {self.pid}, execution name {self.exeName}'

    def __str__(self):
        return f'{self.proto}, {self.connectionId}, {self.uid}, {self.localAddr}, {self.remoteAddr}, {self.state}, {self.pid}, {self.exeName}'
    
    def getPort(self):
        try:
            return int(self.remoteAddr[self.remoteAddr.rfind(':')+1:])
        except:
            pass
        
        return 65536 # one greater than 65535
            
    def __lt__(self, nxt):
        return self.getPort() < nxt.getPort()

@dataclass
class PacketSocket:
    proto: str
    pid: str
    exeName: str

    def __str__(self):
        return f'{self.proto}, {self.pid}, {self.exeName}'

    def getVals(self):
        return f'Proto {self.proto}, pid {self.pid}, execution name{self.exeName}'
