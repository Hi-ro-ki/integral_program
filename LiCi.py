#lici
"""plaintext=0000000000000000000000000000000000000000000000000000000000000000 #64bit

###pt_msb pt_lsb
ptm=(plaintext>>32)&0xffffffff
ptl=plaintext&0xffffffff
"""
"""#key schedule
key=0xffffffffffffffffffffffffffffffff
rk1=[]
rk2=[]
s=[0x3,0xf,0xe,0x1,0x0,0xa,0x5,0x8,0xc,0x4,0xb,0x2,0x9,0x7,0x6,0xd]
for i in range(31):
    rkey1=key&0xffffffff #32bits
    rk1.append(rkey1)
    rkey2=(key>>32)&0xffffffff #32bits
    rk2.append(rkey2)
    key=((key<<13)&0xffffffffffffffffffffffffffffffff)^(key>>115)  ###13shift
    a=key&0xf
    b=s[a]
    c=(key>>4)&0xf
    d=s[c]
    e=key^(i<<59)
    f=(e>>8)<<8 ##sboxの結果を反映させるために8bit0埋めに
    key=(f^b)^(d<<4)##sboxの結果反映
"""
#sbox
def sbox(p):
    s=[0x3,0xf,0xe,0x1,0x0,0xa,0x5,0x8,0xc,0x4,0xb,0x2,0x9,0x7,0x6,0xd]
    pts=[]
    for i in range(8):
        y=(p>>(i*4))&0xf
        pts.insert(0,y)
        pts[0]=s[pts[0]]
    ###ビット列になおす###
    a=pts[7]
    b=pts[6]<<4
    c=pts[5]<<8
    d=pts[4]<<12
    e=pts[3]<<16
    f=pts[2]<<20
    g=pts[1]<<24
    h=pts[0]<<28
    psb=a^b^c^d^e^f^g^h
    return psb



def whole_process(pm,pl,round,rk1,rk2):
    for i in range(round):
        ps=sbox(pm)
        pkl=ps^pl^rk1[i]
        #print("rk1",bin(rk1[i]))
        #print("pkl=",bin(pkl))
        p3=(pkl<<3)&0xffffffff^(pkl>>29) #巡回シフトを実現
        #print("p3=",bin(p3))
        pkm=ps^p3^rk2[i]
        #print("rk2=",bin(rk2[i]))
        #print("pkm=",bin(pkm))
        p7=(pkm>>7)^((pkm<<25)&0xffffffff)
        pm=p3
        pl=p7
        print(i,hex(p7),hex(p3))
    pl_out,pm_out = pm,pl
    ct=(pl_out<<32)^pm_out
    ct=format(ct,'x')
    return ct


#print("出力: ",main(ptm,ptl))



def lici(plaintext,key,round):


    ###pt_msb pt_lsb
    ptm=(plaintext>>32)&0xffffffff
    ptl=plaintext&0xffffffff
    ###key schedule

    rk1=[]
    rk2=[]
    s=[0x3,0xf,0xe,0x1,0x0,0xa,0x5,0x8,0xc,0x4,0xb,0x2,0x9,0x7,0x6,0xd]
    for i in range(round):
        rkey1=key&0xffffffff #32bits
        rk1.append(rkey1)
        rkey2=(key>>32)&0xffffffff #32bits
        rk2.append(rkey2)
        key=((key<<13)&0xffffffffffffffffffffffffffffffff)^(key>>115)  ###13shift
        a=key&0xf
        b=s[a]
        c=(key>>4)&0xf
        d=s[c]
        e=key^(i<<59)
        f=(e>>8)<<8 ##sboxの結果を反映させるために8bit0埋めに
        key=(f^b)^(d<<4)##sboxの結果反映
    ciphertext=whole_process(ptm,ptl,round,rk1,rk2)
    return ciphertext

print(lici(0x0000000000000000,0xffffffffffffffffffffffffffffffff,31))