'''
Created on Nov 14, 2013

@author: iMath
'''
import sys
from Colossus.core.constants import CONS

if __name__ == '__main__':
    CONS = CONS()
    
    done = False
    while not done:
        firstToken = sys.stdin.readline()
        
        if firstToken == CONS.ENDPROCESS:
            done=True
        else:
            if firstToken == CONS.BEGINTOKEN_MERGE:
                out1 = sys.stdin.readline()
                out2 = sys.stdin.readline()
                endToken = sys.stdin.readline()
                if endToken!=CONS.ENDTOKEN_MERGE:
                    raise NameError('Expected END TOKEN:' + CONS.ENDTOKEN_MERGE)
                
                sys.stdout.write(out1 + out2 + '\n')
                sys.stdout.flush()
                
            else:
                raise NameError('Expected BEGIN TOKEN:' + CONS.BEGINTOKEN_MERGE + ' or END PROCESS TOKEN:' + CONS.ENDPROCESS)
            