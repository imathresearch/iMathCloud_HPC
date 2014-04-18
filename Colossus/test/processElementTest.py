'''
Created on Nov 14, 2013

@author: iMath
'''
import sys
import csv
import time
from Colossus.core.constants import CONS
from scipy.stats.stats import pearsonr

def trim(str):
    if (str[len(str)-1]=='\n'):
        return str[0:len(str)-1]
    return str

if __name__ == '__main__':
    CONS = CONS()
    
    done = False
    while not done:
        firstToken = sys.stdin.readline()
        if firstToken == CONS.ENDPROCESS:
            done=True
        else:
            if firstToken == CONS.BEGINTOKEN_PROCESSELEM:
                i0 = sys.stdin.readline()
                i0 = int(trim(i0))
                i1 = sys.stdin.readline()
                i1 = int(trim(i1))
                start_time = time.time()
                i2 = sys.stdin.readline()
                i3 = sys.stdin.readline()
                endToken = sys.stdin.readline()
                if endToken!=CONS.ENDTOKEN_PROCESSELEM:
                    raise NameError('Expected END TOKEN:' + CONS.ENDTOKEN)
                
                i2 = i2[1:len(i2)-2]    # Trim is implicit with the -2
                i3 = i3[1:len(i3)-2]    # Trim is implicit with the -2
                
                x = i2.split(",")
                y = i3.split(",")
    
                for i in range(0,len(x)):
                    x[i] = int(x[i])
                    y[i] = int(y[i])
                r = pearsonr(x, y)
                sys.stdout.write('#' + str(i0) + ',' + str(i1) + ',' + str(r[0]) + '\n')
                sys.stdout.flush()
                
            else:
                if firstToken == CONS.BEGINTOKEN_MERGE:
                    out1 = trim(sys.stdin.readline())
                    out2 = trim(sys.stdin.readline())
                    endToken = sys.stdin.readline()
                    if endToken!=CONS.ENDTOKEN_MERGE:
                        raise NameError('Expected END TOKEN:' + CONS.ENDTOKEN_MERGE + ' got: ' + endToken)
                
                    sys.stdout.write(out1 + out2 + '\n')    
                    sys.stdout.flush()
                else:
                    if len(firstToken)!=0:
                        sys.stderr.write('size: ' + str(len(firstToken)))
                        raise NameError('Expected BEGIN TOKEN:' + CONS.BEGINTOKEN + ' or END PROCESS TOKEN:' + CONS.ENDPROCESS + '. Found:' + firstToken)

'''
    path = "/media/ipinyol/DATA/workspace3/iMathCloud_Plugin/Colossus/test/"
    with open(path+'test.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            x.append(int(row[i0]))
            y.append(int(row[i1]))
    '''