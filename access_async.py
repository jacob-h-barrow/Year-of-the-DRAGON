import sys
import os
import re
import pwd
import glob
import asyncio

from typing import Union
from .models import Connection, PacketSocket

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
        self.connections_queues = {protocol: asyncio.Queue() for protocol in ["udp", "udp6", "tcp", "tcp6"]}

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

    async def getTcp4(self):

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
                
            await self.connections_queues["tcp"].put(Connection("TCP", tcp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, state, pid, exe))

    async def getTcp6(self):
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

            await self.connections_queues["tcp6"].put(Connection("TCPv6", tcp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, state, pid, exe))

    async def getUdp4(self):
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

            await self.connections_queues['udp'].put(Connection("UDP", udp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, udp_state, pid, exe))

    async def getUdp6(self):
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

            await self.connections_queues['udp6'].put(Connection("UDPv6", udp_id, uid, l_host + ":" + l_port, r_host + ":" + r_port, udp_state, pid, exe))

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
        
async def get_one_from_queue(queue: Netstat, protocol: str):
    try:
        if not queue.connections_queues[protocol].qsize():
            return False
        connection = await queue.connections_queues[protocol].get()
        #print(f"Testing connection here first: {connection}")
        return connection
    except Exception as e:
        print(e)
        
async def consumer(queue: Netstat, sleep_timer: int = 1, protocols: dict[str, int] = {"udp":1, "udp6":1, "tcp":1, "tcp6":1}):
    if sleep_timer:
        await asyncio.sleep(sleep_timer)
        
    results = {protocol: [] for protocol in protocols}
    
    while sum(protocols.values()) > 0:
        for protocol in protocols.keys():
            connection = await get_one_from_queue(queue, protocol)
            
            if connection == False:
                protocols[protocol] = 0
            else:   
                protocols[protocol] = 1
                results[protocol].append(connection)
    
    return results
            
if __name__ == "__main__":                  
    async def main():
        producer =  Netstat()
        asyncio.create_task(producer.getUdp4())
        asyncio.create_task(producer.getUdp6())
        asyncio.create_task(producer.getTcp4())
        asyncio.create_task(producer.getTcp6())
        
        results = await consumer(producer)
        
        print(results)
                    
    asyncio.run(main())
    
"""
async def main2():
    producer =  Netstat()
    asyncio.create_task(producer.getUdp4())
    asyncio.create_task(producer.getUdp6())
    asyncio.create_task(producer.getTcp4())
    asyncio.create_task(producer.getTcp6())
    
    await asyncio.sleep(2)
    protocols = {"udp":1, "udp6":1, "tcp":1, "tcp6":1}
    
    for protocol in protocols:
        producer.connections_queues[protocol].qsize()
    
    # Potential infinite loop if data is infinite... it's not
    while sum(protocols.values()) > 0:
        for protocol in protocols.keys():
            connection = await get_one_from_queue(producer, protocol)
            
            if connection == False:
                protocols[protocol] = 0
            else:
                protocols[protocol] = 1
                print(connection)
                
async def producer(netstat_obj: Netstat, protocols: list[str] = ['udp', 'udp6', 'tcp', 'tcp6']):
    for protocol in protocols:
        if protocol == 'udp':
            asyncio.create_task(netstat_obj.getUdp4())
        elif protocol == 'udp6':
            asyncio.create_task(netstat_obj.getUdp6())
        elif protocol == 'tcp':
            asyncio.create_task(netstat_obj.getTcp4())
        elif protocol == 'tcp6':
            asyncio.create_task(netstat_obj.getTcp6())
        else:
            raise Exception(f"{protocol} not supported here!")
                
async def main():
    producer =  Netstat()
    asyncio.create_task(producer.getUdp4())
    asyncio.create_task(producer.getUdp6())
    asyncio.create_task(producer.getTcp4())
    asyncio.create_task(producer.getTcp6())
    
    results = await consumer(producer)
    
    print(results)
"""

