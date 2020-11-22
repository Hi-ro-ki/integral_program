#anu2
plaintext=0000000000000000000000000000000000000000000000000000000000000000 #64bit

###pt_msb pt_lsb
ptm=(plaintext>>32)&0xffffffff
ptl=plaintext&0xffffffff

# sbox
def sbox(p):
    s=[0xe,0x4,0xb,0x1,0x7,0x9,0xc,0xa,0xd,0x2,0x0,0xf,0x8,0x5,0x3,0x6]
    pt=[] #4bit単位でリストに格納（最上位がindex0になるよう）
    for i in range(8):
        y=(p>>(i*4))&0xf
        pt.insert(0,y)
        pt[0]=s[pt[0]]
    ###リストからビット列になおす###
    a=pt[7]
    b=pt[6]<<4
    c=pt[5]<<8
    d=pt[4]<<12
    e=pt[3]<<16
    f=pt[2]<<20
    g=pt[1]<<24
    h=pt[0]<<28
    ps=a^b^c^d^e^f^g^h
    return ps
"""
#shift
def shift(p):
    ps2=((p<<2)&0xffffffff)^(p>>30) #巡回シフトを実現　  <<<2
    ps7=(p>>7)^((p<<25)&0xffffffff)                  # >>>7
    #plaintext after shift
    psh=ps2^ps7
    return psh
"""

#key schedule
key=0x00000000000000000000000000000000
rk1=[]
rk2=[]
s=[0xe,0x4,0xb,0x1,0x7,0x9,0xc,0xa,0xd,0x2,0x0,0xf,0x8,0x5,0x3,0x6]

for i in range(25):
    rkey1=key&0xffffffff #32bits
    rk1.append(rkey1)
    rkey2=(key>>32)&0xffffffff #32bits
    rk2.append(rkey2)
    key=((key<<13)&0xffffffffffffffffffffffffffffffff)^(key>>115)  ###31shift
    a=key&0xf
    b=s[a]
    c=(key>>4)&0xf
    d=s[c]
    e=key^(i<<59)
    f=(e>>8)<<8 ##sboxの結果を反映させるために8bit0埋めに
    key=(f^b)^(d<<4)##sboxの結果反映




def main (p1,p0):
    for i in range(25):
        pps=sbox(p1)
        #print("pps=",hex(pps))
        p3=(p0>>3)^((p0<<29)&0xffffffff)
        p1x=pps^p3^rk1[i]
        p10=((p1x<<10)&0xffffffff)^(p1x>>22)
        #print("pf=",bin(pf))
        p0x=p10^p0^rk2[i]
        p0=p1x
        p1=p0x
        #print(i,"pm=",hex(p1),"pl=",hex(p0))
    return p1,p0

p0_out,p1_out = main(ptm,ptl)
print(hex(p0_out),hex(p1_out))