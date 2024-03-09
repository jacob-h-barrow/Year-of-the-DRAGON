from find import Find
from file_ops import openFile
from time import time
from typing import Mapping, MappingView, ItemsView, KeysView, ValuesView
from dataclasses import dataclass

import re

class RegexManager:
    def __init__(self, loc = "./supporting/patterns.txt"):
        self.compiledRegexes = {}
        self.loc = loc

        for line in openFile(self.loc):
            line = line.split(' = ')
            self.add(line[0], line[1])

    def add(self, term, regex, permanent = False):
        try:
            self.compiledRegexes[term] = re.compile(regex)
        except:
            print(f"{term} could not be compiled as a regex: {regex}")

        if permanent:
            with open(self.loc, "a") as appender:
                appender.write(f"{term}~{regex}")

    def remove(self, term):
        lines = openFile(self.loc)
        lineCount = len(lines)
        idx = -1
            
        for lineNo, line in enumerate(lines):
            if term == line.split('~')[0]:
                idx = lineNo
                break

        if idx != -1:
            with open(self.loc, "w") as writer:
                for lineNo in range(lineCount):
                    if lineNo != idx:
                        writer.write(lines[lineNo])
                    if lineNo != (lineCount - 1):
                        writer.write('\n')
        else:
            print(f"Could not find {term} in file provided")

    def checkIfTermExists(self, term):
        if term not in self.compiledRegexes.keys():
            raise Exception("Term does not exist!")

    def searchFile(self, fileLoc, term, findAll = False):
        self.checkIfTermExists(term)
        data = openFile(fileLoc)

        if findAll:
            return self.compiledRegexes[term].findall(data)
        else:
            res = []
            for line in data:
                found = self.compiledRegexes[term].findall(line)
                res.append(found if found != None else [])

            return res

    # write2File = replace file with new contents
    def modifyFile(self, fileLoc, term, option, pattern, write2File = False):
        self.checkIfTermExists(term)
        options = ['split', 'sub', 'subn']
        if option not in options:
            raise Exception(f"Need to choose one of the following options {options}")

        data = openFile(fileLoc, splitLines = False)

        if option == 'split':
            res = self.compiledRegexes[term].split(pattern, data)
        elif option == 'sub':
            res = self.compiledRegexes[term].sub(pattern, data)
        else:
            res = self.compiledRegexes[term].subn(pattern, data)

        return res
        
class File_Handler(Find, RegexManager):
    def __init__(self, search_filename_path, search_filename_patterns = ["^.*[.]py$"]):
        self.find = Find(search_filename_path, patterns=search_filename_patterns,
                        patternThreshold=100, ignoreHidden=True)
        self.regex_manager = RegexManager()
        
        self.find_file_results = self.find()
        self.position = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            filename = self.find_file_results[self.position]
            file_results = self.regex_manager.searchFile(filename)
            self.position += 1
        except IndexError:
            raise StopIteration()
            
        return filename, file_results
        
if __name__ == "__main__":
    for filename, results in File_Handler("/home/kurzi/Desktop/Projects/"):
        print(f'{ filename } found { len(results) }')
        
        if len(results):
            print(results)
