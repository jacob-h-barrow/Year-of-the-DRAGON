from .signalDecorator import timeout
from functools import wraps
from abc import ABC, abstractmethod
from time import time
# Later from apiRateDeco import ApiRateDeco

import requests
import json
import subprocess
import multiprocessing as mp
import os

class API(ABC):
    @abstractmethod
    def get(self, url, headers):
        pass

class vtClient(API):
    def __init__(self, apiKey, timeouts = 2):
        self.key = apiKey
        self.headers = {"x-apikey": self.key}
        self.vtUrl = "http://www.virustotal.com/api/v3/"
        self.timeouts = timeouts
        
        self.nproc = os.cpu_count()
    
    def get(self, url, headers):
        return json.loads(requests.get(url, headers=headers).text)

    @timeout(2)
    def getIpRep(self, ip, strict=True):
        response = self.get(self.vtUrl + f'ip_addresses/{ip}', headers=self.headers)
        
        try:
            response = response['data']['attributes']['last_analysis_results']
        except:
            return 'Quota Reached!'
            
        total = 0
        harmless = 0
        compareList = ['harmless'] if strict == True else ['harmless', 'undetected']

        for key, value in response.items():
            if value['category'] in compareList:
                    harmless += 1
            total += 1

        return {"ip": ip, "total": total, "harmless": True if harmless/total > 0.90 else False, "timestamp": int(time()), "result": f'VirusTotal polled the community regarding {ip} and got {total} votes, but only {harmless} harmless votes'}

    def bulkGetIpRep(self, ipList: list, strictList: list):
        if len(ipList) != len(strictList):
            return -1

        with mp.Pool(self.nproc) as pool:
            processes = [pool.apply_async(self.getIpRep, args=(ipList[idx], strictList[idx], )) for idx in range(len(ipList))]
            result = [p.get() for p in processes]
            return result

if __name__ == "__main__":
    with open("vtKey.txt", "r") as _file:
        vt = vtClient(_file.read().strip())
    
    print(vt.getIpRep('8.8.8.8'))
    print(vt.getIpRep('8.8.8.8', strict=False))
        
    from GenerateIPv4Addresses import generateIPv4Addresses
    
    for ip in generateIPv4Addresses(5):
        print(f'Testing {ip}')
        print(vt.getIpRep(ip, strict=False))
    
