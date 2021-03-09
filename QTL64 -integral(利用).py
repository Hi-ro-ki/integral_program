#QTL 64
from __future__ import print_function
import random

#CON
"""
CON1=[0x01,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x10,0x11,0x12,0x13]
CON2=[0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f,0x23,0x24,0x25,0x26,0x27]
"""
CON1=[0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f]
CON2=[0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f]

#sbox
s1=[0xc,0x5,0x6,0xb, 0x9,0x0,0xa,0xd, 0x3,0xe,0xf,0x8, 0x4,0x7,0x1,0x2]
s2=[0x4,0xf,0x3,0x8, 0xd,0xa,0xc,0x0, 0xb,0x5,0x7,0xe, 0x2,0x6,0x1,0x9]


#permutation layer
def permutation(x):
    #input x is 16bit int
    per_table=[0 ,4 ,8 ,12 ,1 ,5 ,9 ,13, 2 ,6 ,10, 14 ,3, 7, 11, 15]

    y=0
    for i in range(16):
        bit=(x>>i)&1#
        y=y^(bit<<per_table[i])
    #y is 16 bit int
    return y


def s_layer(x,i):
    if i==1:
        s=s1#
    elif i==2:
        s=s2#
    else:
        print("errorrrrrrr")
        import sys
        sys.exit()

    y=0
    for j in range(4):
       y^=s[(x>>4*j)&0xf]<<4*j

    return y

def Func(x,i):
    #x is 16bit int
    a=s_layer(x,i)

    b=permutation(a)#c is 4 length list
    
    c=s_layer(b,i)

    return c

def pri(X,r):
        print("r : ",end="")
        print(r)
        for i in range(4):
            print(format(X[i],"04x")," ",end="")
        print("\n")
def main():
    #key=[0xffff,0xffff,0xffff,0xffff]
    #key=[0x0000,0x0000,0x0000,0x0000]
    #key=[0x3995,0x48C2,0x7529,0x023F]

    
    
    #p=[0x0000,0x0000,0x0000,0x0000]
    #p=[0xffff,0xffff,0xffff,0xffff]
    #p=[0x36E6,0x5AAE,0x2BC1,0x17D8 ]
    
    
                          #X¨X0||X1||X2||X3]

    totaljud=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#64bit
    jud=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#64bit
    for trial in range(20):#
        hdadd=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#64bit

        key=[random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff)]
        k0=key[0]
        k1=key[1]
        k2=key[2]
        k3=key[3]

        base=[random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff),random.randint(0,0xffff)]
        
        for i in range(2**4):#
            X=[base[0],base[1],base[2],base[3]]
            X[0]^=i<<0###################################A‚ÌˆÊ’uˆÚ“®
            for r in range(16):
                #pri(X,r)
               
                a=X[1]^Func(X[0]^k0^(CON1[r]<<8),1)#
                b=X[0]^Func(a^k2^(CON1[r]<<8),1)#
                c=X[3]^Func(X[2]^k1^(CON2[r]<<8),2)#
                d=X[2]^Func(c^k3^(CON2[r]<<8),2)#

                if r ==15:
                    X[0],X[1],X[2],X[3] = a,b,c,d
                    #pri(X,r)
                    break
                X[0],X[1],X[2],X[3] = c,b,a,d

                if r==1:#  ###########################Round”•ÏX
                    for j in range(64):
                        hdadd[j]+=(X[int(j/16)]>>(j%16))&1

        for i in range(64):
            if(hdadd[i]==0 or hdadd[i]==16):
                jud[i]='C'
            elif(hdadd[i]%2==0 ):
                jud[i]='B'
            else:
                jud[i]='O'
                
            if(trial==0):
                totaljud[i]=jud[i]#

            else:
                if(totaljud[i]==jud[i] or totaljud[i]=='U'):
                    pass#
                elif(jud[i]!='O' and totaljud[i]!='O'):
                    totaljud[i]='B'
                else:
                    totaljud[i]='U'

                #
                #
    print(totaljud)
    







if __name__=="__main__":
    main()
