# Put all of the functional codecs here
from abc import ABC, abstractmethod

import json

class Translator(ABC):
    @abstractmethod
    def process_bind(self, data: dict, indent: int):
        pass
    
    @abstractmethod
    def process_return(self, data: str):
        pass
        
class JsonTranslator(Translator):
    def __init__(self):
        pass
    
    def process_bind(self, data: dict, indent: int):
        return json.dumps(data, indent=indent)
    
    def process_return(self, data: str):
        return json.loads(data)
        
class DataTranslation:
    def __init__(self, factory = None):
        self.factories = {}
        
    def register_factor(self, name, factory):
        self.factories[name] = factory()
        
    def serialize(self, name, data: dict, indent: int = 4):
        try:
            return self.factories[name].process_bind(data, indent)
        except Exception as e:
            return e
        
    def deserialize(self, name, data: str):
        try:
            return self.factories[name].process_return(data)
        except Exception as e:
            return e
        
info_translations = DataTranslation()

info_translations.register_factor('json', JsonTranslator)
if __name__ == "__main__":

    weather_ex = {'timestamp': '06-27-23 14:04:28', 'temperature': 86.47, 'pressure': 1005, 'humidity': 63, 'wind_speed': 11.5, 'wind_degree': 280, 'sunrise': 1687859284, 'sunset': 1687912085}

    print('Trying Json!')
    json_string = info_translations.serialize('json', weather_ex)
    print(info_translations.deserialize('json', json_string))
