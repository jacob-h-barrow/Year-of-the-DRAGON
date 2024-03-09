import asyncio

from access_async import Netstat, get_one_from_queue
from rich.console import Console
from rich.table import Table
from rich.live import Live

####################################
####  Async Ip Netstat Handler  ####
####################################
#########################################
####  Protocols - udp4/6 and tcp4/6  ####
#########################################
class IpStatHandlerAsync:    
    def __init__(self, protocols: dict[str, int] = {"udp":1, "udp6":1, "tcp":1, "tcp6":1}, sleep_timer: int = 1):
        self.sleep_timer = sleep_timer
        self.slept = False
        self.protocols = protocols
        self.producer = Netstat()
        
        for key in self.protocols.keys():
            if key == 'udp':
                asyncio.create_task(self.producer.getUdp4())
            if key == 'udp6':
                asyncio.create_task(self.producer.getUdp6())
            if key == 'tcp':
                asyncio.create_task(self.producer.getTcp4())
            if key == 'tcp6':
                asyncio.create_task(self.producer.getTcp6())
        
    def __aiter__(self):
        return self
        
    # Could make class Queue to yield
    async def __anext__(self):
        if self.sleep_timer > 0 and not self.slept:
            await asyncio.sleep(self.sleep_timer)
            
        while sum(self.protocols.values()) > 0:
            for protocol in self.protocols.keys():
                connection = await get_one_from_queue(self.producer, protocol)
                
                if connection == False:
                    self.protocols[protocol] = 0
                else:
                    self.protocols[protocol] = 1
                    return protocol, connection
        
        raise StopAsyncIteration

async def doctest_connection_handler_async():
    async with ConnectionHandlerAsync(['udp', 'tcp']) as connections_handler:
        async for protocol, connection in connections_handler.get_all_protocol_connections():
            pass

        async for protocol, connection in connections_handler.get_protocol_connections('udp'):
            pass
            
class ConnectionHandlerAsync:
    """Test the number of iterator pulls!
    
    >>> asyncio.run(doctest_connection_handler_async())
    Entering the context manager
    Thank you! We served you 2 during this context!
    """
    iterator_pulls = 0
    
    def __init__(self, protocols: list[str], sleep_timer: int = 1): 
        self.protocols = protocols
        self.sleep_timer = sleep_timer
    
    async def __aenter__(self):
        print("Entering the context manager")
        return self
        
    async def get_protocol_connections(self, protocol: str):
        self.iterator_pulls += 1
        
        async for protocol, connection in IpStatHandlerAsync(protocols = {protocol: 1}, sleep_timer = self.sleep_timer):
            yield protocol, connection
        
    async def get_all_protocol_connections(self):
        self.iterator_pulls += 1
        async for protocol, connection in IpStatHandlerAsync(protocols = {protocol: 1 for protocol in self.protocols}, sleep_timer = self.sleep_timer):
            yield protocol, connection

    async def __aexit__(self, exc_type, exc, tb):
        print(f"Thank you! We served you {self.iterator_pulls} during this context!")
        
def display_connections(connections: list, table_name: str = "Active Connections", columns: list[str] = ["Protocol", "Connection Id", "UID", "Local Address", "Remote Address", "State", "PID", "Execution Name"]):
    table = Table(title=table_name)
    colors = ['magenta', 'cyan', 'blue', 'green', 'red']
    colors_ptr = 0
    
    for column in columns:
        color = colors[colors_ptr % len(colors)]
        colors_ptr += 1
        
        table.add_column(column, justify="center", style=color)
    
    for connection in connections:
        table.add_row(connection.proto, connection.connectionId, connection.uid, connection.localAddr, connection.remoteAddr, connection.state, connection.pid, connection.exeName)
        
    # console = Console()
    # console.print(table)
    return table
    
async def display_continuous_connections():
    connections = []
    
    async for protocol, connection in IpStatHandlerAsync():
        connections.append(connection)
        
    return display_connections(connections)
        
if __name__ == "__main__":
    async def main():
        print("Testing the iteratorable object first!")
        
        async for protocol, connection in IpStatHandlerAsync():
            print(f"Protocol {protocol} produced the following connection: {connection}") 
        print("\nTrying connection handler now")
        
        async with ConnectionHandlerAsync(['udp', 'tcp']) as connections_handler:
            
            print("Trying all protocols provided!")
            print(connections_handler)

            async for protocol, connection in connections_handler.get_all_protocol_connections():
                print(f"{protocol} {connection}")
                
            print("\nTrying only the udp protocol")
            
            async for protocol, connection in connections_handler.get_protocol_connections('udp'):
                print(connection)
        
        """
        connections = []
        
        async for protocol, connection in IpStatHandlerAsync():
            connections.append(connection)
            
        display_connections(connections)
        """
        
        # Not asynchronous, would either need to modify my code or theirs!!!
        """
        async with Live(display_continuous_connections(), refresh_per_second=5) as live:
            for _ in range(40):
                time.sleep(0.4)
                live.update(await display_continuous_connections())
        """
    asyncio.run(main())
            
            
    
