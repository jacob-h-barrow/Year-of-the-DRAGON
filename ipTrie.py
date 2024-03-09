from time import time

"""
A modified Trie data structure is provided as a way to store all connection histories associated with a system.

- `Trie()`: Modified to store objects (IP connection history) across the lifetime of the device.
"""

# Class code was modified from https://www.tutorialspoint.com/implement-trie-prefix-tree-in-python
class Trie(object):
   def __init__(self):
      self.child = {}
   def insert(self, word, obj = 1):
      current = self.child
      for l in word:
         if l not in current:
            current[l] = {}
         current = current[l]
      if "#" in current.keys():
          current["#"].insert(0, [obj,time()])
      else:
          current['#']=[[obj,time()]]

   def search(self, word):
      current = self.child
      for l in word:
         if l not in current:
            return False
         current = current[l]

      if "#" in current:
          return current['#']
      else:
          return False

   def startsWith(self, prefix):
      current = self.child
      for l in prefix:
         if l not in current:
            return False
         current = current[l]
      return True
