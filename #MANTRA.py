
import random
import numpy as np
def main():
    print("入力Integral特性：aaaacc~c")                                        ####　変更
    ROUND = int( input("何段分のintegral特性を求めますか？　：") )
    ATEMPT = 100000 #段鍵、平文のランダム設定の回数

    #出力部のIntegral特性　0で初期化
    output_integral=0x0000000000000000
    
    for a in range(ATEMPT):
        #平文をランダムに設定 64bits
        plain_text = random.randint(0x0000000000000000,0xffffffffffffffff)
        #段鍵をランダムに設定 128bits
        key = random.randint(0x00000000000000000000000000000000,0xffffffffffffffffffffffffffffffff)

        total=0
        #Integral特性 aacccc の計算
        for delta_p in range(2**4):                                            ### 変更
            cryptgram = mantra(plain_text ^ (delta_p<<60) ,key,ROUND)
            #print( "0b"+format(cryptgram, '06b'))#暗号文を0埋め6桁2進数で出力
            
            row=[]
            for i in range(64):
                row=np.append(row,(cryptgram>>(63-i))&1)
            total+=row
        #print(total)
        tem_result=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for j in range(64):
            if total[j]==0 or total[j]==2**4:
                tem_result[j]='c'
            elif total[j]%2==0:
                tem_result[j]='b'
            else:
                tem_result[j]='u'
        #print(tem_result)
        #print(" ")
        if a==0:    
            result=tem_result
        else:
            for l in range(64):
                if result[l]=='c'and tem_result[l]=='c':
                    pass
                elif (result[l]=='b' and tem_result[l]=='b') or (result[l]=='c'and tem_result[l]=='b')or(result[l]=='b'and tem_result[l]=='c'):
                    result[l]='b'
                else:
                    result[l]='u'
                #print(result)
    result=''.join(map(str,result))
    print(ROUND,"段の出力結果",result)

#####暗号器####
#sbox
def sbox(p):

    s=[0x2,0x5,0xd,0xa,0xf,0x3,0x4,0x9,0xb,0x0,0x6,0xc,0x8,0xe,0x1,0x7]
    pts=[]
    for i in range(4):
        y=(p>>(i*4))&0xf
        pts.insert(0,y)
        pts[0]=s[pts[0]]
    ###ビット列になおす###
    a=pts[3]
    b=pts[2]<<4
    c=pts[1]<<8
    d=pts[0]<<12
    psb=a^b^c^d
    return psb

## F1 function
def func1(pt2,pt1,i,rk1):
    p3=((pt1<<3)&0xffff)^(pt1>>13) #巡回シフトを実現 shift 3 bit
    ps=sbox(pt2)
    pt3=ps^p3^rk1[i]
    return pt3,pt2

## F2 funcion
def func2(pt3,pt2,i,rk2):
    p8=(pt2>>8)^((pt2<<8)&0xffff)
    ps=sbox(pt3)
    pt4=ps^p8^rk2[i]
    pf=(pt4<<16)^pt3
    return pf

##全体##
def mantra(plaintext,key,round):

    pl=(plaintext>>32)&0xffffffff #32bit
    pr=plaintext&0xffffffff #32bit

##keyschedule
    rk1=[]
    rk2=[]
    s=[0x2,0x5,0xd,0xa,0xf,0x3,0x4,0x9,0xb,0x0,0x6,0xc,0x8,0xe,0x1,0x7]
    for i in range(round):
        rkey1=(key>>16)&0xffff #16bits
        rk1.append(rkey1)
        rkey2=key&0xffff #16bits
        rk2.append(rkey2)
        key=((key<<27)&0xffffffffffffffffffffffffffffffff)^(key>>101)  ###27shift
        a=key&0xf
        b=s[a]
        c=(key>>4)&0xf
        d=s[c]
        e=key^(i<<66)
        f=(e>>8)<<8 ##sboxの結果を反映させるために8bit0埋めに
        key=(f^b)^(d<<4)##sboxの結果反映


    for i in range(round):
        pt1=pl&0xffff
        pt2=(pl>>16)&0xffff
        pt3,pt2=func1(pt2,pt1,i,rk1)
        #print("pt3=",hex(pt3),"pt2=",hex(pt2))
        pf=func2(pt3,pt2,i,rk2)

        #print("pf=",hex(pf))
        px=pr^pf ###xor
        #print("px=",hex(px))
        pr=pl
        pl=px
        #print(i,"pl=",hex(pl),"pr=",hex(pr))
    ct=(pl<<32)^pr
    return ct

#c = mantra(0x0000000000000000,0x0123456789abcdef0123456789abcdef,32)
#print("出力:",hex(c))




if __name__=="__main__":
    main()