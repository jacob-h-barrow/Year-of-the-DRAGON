from access import Netstat

class IpStatHandler:
    allowedProtos = ["udp", "udp6", "tcp", "tcp6"]

    # sort by localAddr, destinationAddr or proto later, right now only localAddr and custom
    def __init__(self, protos = ["udp", "udp6", "tcp", "tcp6"], sort: bool = True, sortBy: str = "custom"):
        for proto in protos:
            if proto not in self.allowedProtos:
                raise Exception("Library doesnt work with that protocol yet!")

        self.protos = protos
        self.connections = []
        self.ptr = 0

        self.getIpStat()

        if sort:
            try:
                if sortBy == "localAddr":
                    self.connections = sorted(self.connections, key = lambda x: x.localAddr)
                elif sortBy == "custom":
                    self.connections = sorted(self.connections, key = lambda x: [x.proto, x.localAddr, x.remoteAddr, x.uid])
            except:
                raise Exception("That wasn't a sorting option!")

        self.amount = len(self.connections)

    def addConnections(self, connectionList: list) -> None:
        for conn in connectionList:
            self.connections.append(conn)
        
    def getIpStat(self):
        netstat = Netstat()
        
        for proto in self.protos:
            if proto == "udp":
                self.addConnections(netstat.getUdp4())
            elif proto == "udp6":
                self.addConnections(netstat.getUdp6())
            elif proto == "tcp":
                self.addConnections(netstat.getTcp4())
            elif proto == "tcp6": # in case more protos are added
                self.addConnections(netstat.getTcp6())

    def __iter__(self):
        return self

    def __next__(self):
        if self.ptr < self.amount:
            self.ptr += 1
            return self.connections[self.ptr-1]
        else:
            raise StopIteration()

if __name__ == "__main__":    
    for connection in IpStatHandler():
        print(connection)
