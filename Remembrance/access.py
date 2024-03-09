from models import Connection, PacketSocket
import os
import re
import pwd
import glob
from typing import Union

def openFile(file_location, split_lines = True, option = "r", new_text = ""):
    if option not in ["r", "a", "w"]:
        raise Exception("File option not supported")

    if option == "r":
        try:
            with open(file_location) as reader:
                data = reader.read().strip()
                if split_lines:
                    return data.split("\n")
                else:
                    return data
        except:
            raise Exception("Could not open file: {fileLoc}!")
    else:
        try:
            with open(file_location, option) as writer:
                writer.write(new_text)
        except:
            raise Exception("Could not modify file: {fileLoc}!")
            
class Netstat:
    procTcp4 = "/proc/net/tcp"
    procTcp6 = "/proc/net/tcp6"
    procUdp = "/proc/net/udp"
    procUdp6 = "/proc/net/udp6"
    procPacket = "/proc/net/packet"

    tcpStates = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

    def __init__(self):
        pass

    def hex2dec(self, val: str) -> str:
        return str(int(val,16))

    def getIp(self, val: str) -> str:
        return ".".join([(self.hex2dec(val[6:8])),(self.hex2dec(val[4:6])),(self.hex2dec(val[2:4])),(self.hex2dec(val[0:2]))])

    def getIp6(self, val: str) -> str:
        return ":".join([val[6:8],val[4:6],val[2:4],val[0:2],val[12:14],val[14:16],val[10:12],val[8:10],val[22:24],val[20:22],val[18:20],val[16:18],val[30:32],val[28:30],val[26:28],val[24:26]])

    def removeEmpty(self, array: list) -> list:
        return [x for x in array if x != '']

    def convertIpv4Port(self, array: list):
        host, port = array.split(':')
        return self.getIp(host), self.hex2dec(port)

    def convertIpv6Port(self, array: list) :
        host, port = array.split(':')
        return self.getIp6(host), self.hex2dec(port)

    def getTcp4(self) -> list:
        '''
        Function to return a list with status of tcp connections on Linux systems.
        Please note that in order to return the pid of a network process running on the
        system, this script must be ran as root.
        '''

        tcpresult = []
        for line in openFile(self.procTcp4)[1:]:
            line_array = self.removeEmpty(line.split(' '))     # Split lines and remove empty spaces.
            l_host,l_port = self.convertIpv4Port(line_array[1]) # Convert ipaddress and port from hex to decimal.
            r_host,r_port = self.convertIpv4Port(line_array[2])
            tcp_id = line_array[0][:-1]
            state = self.tcpStates[line_array[3]]
            uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID.
            inode = line_array[9]                           # Need the inode to get process pid.
            pid = self.getPidOfInode(inode)                  # Get pid prom inode.
            try:                                            # try read the process name.
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None

            tcpresult.append(Connection("TCP", tcp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, state, pid, exe)) #[tcp_id, uid, l_host+':'+l_port, r_host+':'+r_port, state, pid, exe]
        return tcpresult

    def getTcp6(self) -> list:
        '''
        This function returns a list of tcp connections utilizing ipv6. Please note that in order to return the pid of of a
        network process running on the system, this script must be ran as root.
        '''
        tcpresult = []
        for line in openFile(self.procTcp6)[1:]:
            line_array = self.removeEmpty(line.split(' '))
            l_host,l_port = self.convertIpv6Port(line_array[1])
            r_host,r_port = self.convertIpv6Port(line_array[2])
            tcp_id = line_array[0][:-1]
            state = self.tcpStates[line_array[3]]
            uid = pwd.getpwuid(int(line_array[7])) [0]
            inode = line_array[9]
            pid = self.getPidOfInode(inode)
            try:                                            # try read the process name.
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None

            #nline = [tcp_id, uid, l_host+':'+l_port, r_host+':'+r_port, state, pid, exe]
            tcpresult.append(Connection("TCPv6", tcp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, state, pid, exe))
        return tcpresult

    def getUdp4(self) -> list:
        '''
        Function to return a list with status of udp connections on Linux systems. Please note that UDP is stateless, so
        state will always be blank. Please note that in order to return the pid of of a network process running on the
        system, this script must be ran as root.
        '''
        udpresult = []
        for line in openFile(self.procUdp)[1:]:
            line_array = self.removeEmpty(line.split(' '))
            l_host,l_port = self.convertIpv4Port(line_array[1])
            r_host,r_port = self.convertIpv4Port(line_array[2])
            udp_id = line_array[0][:-1]
            udp_state ='Stateless' #UDP is stateless
            uid = pwd.getpwuid(int(line_array[7]))[0]
            inode = line_array[9]
            pid = self.getPidOfInode(inode)
            try:
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None

            #nline = [udp_id, uid, l_host+':'+l_port, r_host+':'+r_port, udp_state, pid, exe]
            udpresult.append(Connection("UDP", udp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, udp_state, pid, exe))
        return udpresult

    def getUdp6(self) -> list:
        '''
        Function to return a list of udp connection utilizing ipv6. Please note that UDP is stateless, so state will always
        be blank. Please note that in order to return the pid of of a network process running on the system, this script
        must be ran as root.
        '''
        udpresult = []
        for line in openFile(self.procUdp6)[1:]:
            line_array = self.removeEmpty(line.split(' '))
            l_host,l_port = self.convertIpv6Port(line_array[1])
            r_host,r_port = self.convertIpv6Port(line_array[2])
            udp_id = line_array[0][:-1]
            udp_state ='Stateless' #UDP is stateless
            uid = pwd.getpwuid(int(line_array[7]))[0]
            inode = line_array[9]
            pid = self.getPidOfInode(inode)
            try:
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None

            #nline = [udp_id, uid, l_host+':'+l_port, r_host+':'+r_port, udp_state, pid, exe]
            udpresult.append(Connection("UDPv6", udp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, udp_state, pid, exe))
        return udpresult

    def getPacketSocket(self) -> list:
        '''
        Function to return a list of pids and process names utilizing packet sockets.
        '''

        packetresult = []
        for line in openFile(self.procPacket)[1:]:
            line_array = self.removeEmpty(line.split(' '))
            inode = line_array[8].rstrip()
            pid = self.getPidOfInode(inode)
            try:
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None

            #nline = [pid, exe]
            packetresult.append(PacketSocket("Socket Packet", pid, exe))
        return packetresult

    def getPidOfInode(self, inode: str) -> Union[str, None]:
        '''
        To retrieve the process pid, check every running process and look for one using
        the given inode.
        '''
        for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
            try:
                if re.search(inode,os.readlink(item)):
                    return item.split('/')[2]
            except:
                pass
        return None

'''if __name__ == "__main__":
    netstat = Netstat()
    print("\nLegend: Connection ID, UID, localhost:localport, remotehost:remoteport, state, pid, exe name")
    print("\nTCP (v4) Results:\n")
    for conn_tcp in netstat.getTcp4():
        print(conn_tcp)
    print("\nTCP (v6) Results:\n")
    for conn_tcp6 in netstat.getTcp6():
        print(conn_tcp6)
    print("\nUDP (v4) Results:\n")
    for conn_udp in netstat.getUdp4():
        print(conn_udp)
    print("\nUDP (v6) Results:\n")
    for conn_udp6 in netstat.getUdp6():
        print(conn_udp6)
    print("\nPacket Socket Results:\n")
    for pack_sock in netstat.getPacketSocket():
        print(pack_sock)
'''
