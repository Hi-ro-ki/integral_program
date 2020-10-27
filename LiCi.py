
import random
import numpy as np
def main():
    print("入力Integral特性：aaaacc~c")                                        ####　変更
    ROUND = int( input("何段分のintegral特性を求めますか？　：") )
    ATEMPT = 10 #段鍵、平文のランダム設定の回数

    #出力部のIntegral特性　0で初期化
    output_integral=0x0000000000000000
    # print(lici(0x0000000000000000,0xffffffffffffffffffffffffffffffff,31))
    
    for a in range(ATEMPT):
        
        #平文をランダムに設定 64bits
        plain_text = random.randint(0x0000000000000000,0xffffffffffffffff)
        #鍵をランダムに設定 128bits
        key = random.randint(0x00000000000000000000000000000000,0xffffffffffffffffffffffffffffffff)

        #xor_sum=0x0000000000000000#初期化
        total=0
        #Integral特性 aacccc の計算
        for delta_p in range(2**4):                                            ### 変更
            cryptgram = lici(plain_text ^ (delta_p<<60) ,key,ROUND)
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
        print(tem_result)
        print(" ")
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
    """        xor_sum ^= cryptgram
            print(format(cryptgram,'064b'))
        
        output_integral = output_integral | xor_sum #output_integralにxor総和をOR演算して代入　最後まで0が続いたビットがxor総和０ってこと
    
    output_integral = format(output_integral, '064b')
    print(ROUND,"段: 出力Integral特性：" + output_integral.replace('0', 'b').replace('1', 'u'))
    """
#6bitFeistel暗号の暗号器
#plain_text:64bits平文、key：128bits鍵、ROUND：暗号器の段数
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
        #print(i,hex(p7),hex(p3))
    pl_out,pm_out = pm,pl
    ct=(pl_out<<32)^pm_out
    #ct=format(ct,'x')
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



if __name__=="__main__":
    main()