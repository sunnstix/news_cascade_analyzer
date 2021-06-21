import math
import sys

#Create a Progress Bar to Illustrate Progress of Different Things - Modular and Reusable
class ProgressBar:
    def __init__(self,totalActions,bar_char='▱',bar_len = 20):
        self.bar_char = bar_char
        self.bar_len = bar_len
        self.totalActions = totalActions
        self.doneActions = 0
    def update(self):
        displayLen = math.floor((self.doneActions/self.totalActions)*self.bar_len)
        displayedBar = self.bar_char * displayLen + ' ' * (self.bar_len - displayLen)
        percentage = str(math.floor(self.doneActions/self.totalActions*100))
        sys.stdout.write('\r\tProgress: {}% ({}/{}) Complete [{}]'.format(percentage,str(self.doneActions),str(self.totalActions),displayedBar))
        sys.stdout.flush()
    def iterate(self):
        if self.doneActions<self.totalActions:
            self.doneActions+=1
    def complete(self):
        displayedBar = self.bar_char * self.bar_len
        sys.stdout.write('\r\tProgress: {}% ({}/{}) Complete [{}]\n'.format('100',str(self.totalActions),str(self.totalActions),displayedBar))
        sys.stdout.flush()