# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 01:30:18 2021

@author: Anmole
"""
class multiple(object):
    x=0
    y=0
    READ_MODE = 'r'
    APPEND_MODE = 'a'
    WRITE_MODE= 'w'
    PROMPT_SPLITTER = ':'
    OUTPUT_FILE = './outputPS13.txt'
    
    def __init__(self):
        outputFile = open(self.OUTPUT_FILE, self.WRITE_MODE)
        outputFile.close()
    
    def runInputFile(self, inputFile):
        inputFile = open(inputFile, self.READ_MODE)
        lines = inputFile.readlines()
        for line in lines:
            word = line.strip()
            inputLine = word.split(self.PROMPT_SPLITTER)
            
            if(inputLine[0].strip()=='Number 1'):
                self.x=inputLine[1].strip()
                
            if(inputLine[0].strip()=='Number 2'):
                self.y=inputLine[1].strip()
              
        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write('---------------------------\n')
        outputFile.close()
        m=self.multiplyNum(self.x,self.y)
        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write("\n Result:> "+ str(self.x)+" x "+str(self.y)+" = "+str(m))
        outputFile.close()
        
            
    def multiplyNum(self,x ,y):
        """Multiply two integers using Karatsuba's algorithm."""
        #convert to strings for easy access to digits
        x = str(x)
        y = str(y)
        #base case for recursion
        if len(x) == 1 and len(y) == 1:
            return int(x) * int(y)
        if len(x) < len(y):
            x = self.zeroPad(x, len(y) - len(x))
        elif len(y) < len(x):
            y = self.zeroPad(y, len(x) - len(y))
        n = len(x)
        j = n//2
        #for odd digit integers
        if (n % 2) != 0:
            j += 1    
        BZeroPadding = n - j
        AZeroPadding = BZeroPadding * 2
        a = int(x[:j])
        b = int(x[j:])
        c = int(y[:j])
        d = int(y[j:])
        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write("1st number, x:"+str(x)+" \n2nd number, y: "+str(y)+"\nIntermediate Values of A, B after partition:\nx:"+str(x)+"  a : "+str(a)+" b : "+str(b)+"\ny: "+str(y)+" c : "+str(c)+" d : "+str(d)+"\n---------------------------\n")
        outputFile.close()
        #recursively calculate
        ac = self.multiplyNum(a, c)
        bd = self.multiplyNum(b, d)
        k = self.multiplyNum(a + b, c + d)
        A = int(self.zeroPad(str(ac), AZeroPadding, False))
        B = int(self.zeroPad(str(k - ac - bd), BZeroPadding, False))
        intmul=A+B+bd
        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write("Intermediate Product: "+str(x)+" x "+str(y)+" = "+str(intmul)+"\n-----------------\n")
        outputFile.close()
        return intmul
    
    def zeroPad(self,numberString, zeros, left = True):
        """Return the string with zeros added to the left or right."""
        for i in range(zeros):
            if left:
                numberString = '0' + numberString
            else:
                numberString = numberString + '0'
        return numberString      

if __name__ == '__main__':
    multiple = multiple()
    multiple.runInputFile('./inputPS13.txt')
    
