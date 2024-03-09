from ipstat import IpStatHandler
from ipTrie import Trie
from multiprocessing import Lock
import os

class ConnTrack:
    systemInsertionLock = Lock()
    systemLookupLock  = [Lock() for i in range(os.cpu_count())]
    system = Trie()

    def __init__(self): # option to add data later!!!
        self.system = Trie()

    def refreshIpStat(self):
        lockAll = [l.acquire() for l in self.systemLookupLock]
        with self.systemInsertionLock:
            try:
                for conn in IpStatHandler():
                    self.addConn(conn)
            except Exception as e:
                print("Exception refreshing")
                print(e)

            releaseAll = [l.release() for l in self.systemLookupLock]

    def addConn(self, conn):
        self.system.insert(conn.remoteAddr.split(":")[0], conn.localAddr.split(":")[0])

    def retrieveIpInfo(self, ip: str):
        for i in range(len(self.systemLookupLock)):
            aq = self.systemLookupLock[i].acquire(block=False)
            if aq:
                ret = self.system.search(ip)
                if ret == False:
                    if ip == "0.0.0.0":
                        return f"Your system probably uses a hosts file to exchange the 0.0.0.0 address"
                    else:
                        return f"User/system has not connected to {ip} before!"
                self.systemLookupLock[i].release()
                return ret
        
        return False

    def retrieveIpInfo_LastN(self, ip: str, amount: int = 5):
        infoRetrieved = self.retrieveIpInfo(ip)
        
        if infoRetrieved == False:
            return f"User/system has not connected to {ip} before!"

        length = len(infoRetrieved)

        if amount <= length:
            return infoRetrieved[:amount]
        else:
            return infoRetrieved[:length]

    def __repr__(self):
        ret = "This is your Connection Handler\nThe current connections are:\n"

        for conn in IpStatHandler():
            ret += str(conn) + "\n"

        return ret

class ConnTrackHandler:
    count = 0
    
    def __init__(self):
        pass

    def __enter__(self):
        # Python 3.11 return self 
        # Before 3.11
        self.count += 1
        return ConnTrack()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.count -= 1
        if isinstance(exc_value, IndexError):
            # Handle IndexError here...
            print(f"An exception occurred in your with block: {exc_type}")
            print(f"Exception message: {exc_value}")
            return True

    def __del__(self):
        print("Goodbye friend!")

'''if __name__ == "__main__":
    with ConnTrackHandler() as handler:
        print(handler)
        for i in range(3):
            handler.refreshIpStat()
        print(handler.retrieveIpInfo("35.244.181.201"))'''
