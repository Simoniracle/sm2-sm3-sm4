import re
SboxTable = [
            0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
            0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
            0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
            0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
            0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
            0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
            0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
            0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
            0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
            0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
            0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
            0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
            0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
            0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
            0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
            0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
        ]

Roundk=[]
Ck=[]

def xor(str1, str2):  # 异或运算
    r = ''
    for i in range(len(str1)):
        t = int(str1[i]) ^ int(str2[i])
        if (int(t) == 1):
            r += '1'
        else:
            r += '0'
    return r

def str2bits(str):
    r = ''
    for i in str:
        t = bin(ord(i))[2:]
        for j in range(0, 8 - len(t)):
            t = '0' + t  # 把输出的b给去掉
        r += t
    return (r)

def bin2str(bin_str):
    r = ""
    tmp = re.findall(r'.{8}', bin_str)
    for i in tmp:
        r+= chr(int(i, 2))
    return r


def int2bit(x,n): #十进制转为n位2进制
    r=bin(x)[2:]
    while(len(r)<n):
        r='0'+r
    return r

def move(k, n):  # 循环移位
    return k[n:]+k[:n]      #移位数在长度之内，未做溢出判断

def T(x):  #x:32bits,
    B=''                        #B:32bits
    for i in range(0,8,2):    #分为四组
        B+=int2bit(SboxTable[int(x[i*4:(i+1)*4],2)*16+int(x[(i+1)*4:(i+2)*4],2)],8) #高四位为排，低四位为列。
    C=xor(B,xor(move(B,2),xor(move(B,10),xor(move(B,18),move(B,24)))))
    return C

def TT(x):
    B = ''  # B:32bits
    for i in range(0, 8, 2):  # 分为四组
        B+=int2bit(SboxTable[int(x[i*4:(i+1)*4],2)*16+int(x[(i+1)*4:(i+2)*4],2)],8)  # 高四位为排，低四位为列。
    C = xor(B,xor(move(B,13),move(B,23)))
    return C

def f(x):  #   Rk:32bits
    t = ''
    x=str2bits(x)       #字符串转为比特
    #x=int2bit(int('0x0123456789abcdeffedcba9876543210',16),128)
    for j in range(32):
        t = xor(x[j*32:(j+1) * 32], T(xor(x[(j+1) * 32:(j+2) * 32], xor(x[(j+2) * 32:(j+3) * 32], xor(Roundk[j], x[(j+3) * 32:(j+4) * 32])))))  #x128bits，分为四组进行异或操作。
        x+=t
    return  x[35*32:36*32]+ x[34* 32:35* 32] +x[33* 32:34* 32]+x[32*32:33 * 32]       #倒序输出


def ff(x):
    t = ''
    for j in range(32):
        t = xor(x[j*32:(j+1) * 32], T(xor(x[(j+1) * 32:(j+2) * 32], xor(x[(j+2) * 32:(j+3) * 32], xor(Roundk[j], x[(j+3) * 32:(j+4) * 32])))))  ##x128bits，分为四组进行异或操作。
        x+=t
    return  x[35*32:36*32]+ x[34* 32:35* 32] +x[33* 32:34* 32]+x[32*32:33 * 32]      # 倒序输出

def set_Ck():   #Ck[i]:32bits
    for i in range(32):
        t=''
        for j in range(4):
            t+=int2bit(7*(4*i+j)%256,8)
        Ck.append(t)

def RoundKey():  #key:128bits
    key=str2bits(input('请输入16字节密钥：'))
    #key=int2bit(int('0x0123456789abcdeffedcba9876543210',16),128)
    K=[]
    FK1, FK2, FK3, FK4 = 0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc
    K.append(xor(int2bit(FK1,32),key[0:32]))    #k0
    K.append(xor(int2bit(FK2,32),key[32:64]))   #k1
    K.append(xor(int2bit(FK3,32),key[64:96]))   #k2
    K.append(xor(int2bit(FK4,32),key[96:128]))  #k3
    for i in range(32):
        t=xor(K[i],TT(xor(K[i+1],xor(K[i+2],xor(K[i+3],Ck[i])))))
        K.append(t) #K[4]-K[35]
        Roundk.append(t)    #加入轮密钥


def encrypt():
    r=''
    set_Ck()
    RoundKey()
    m=input('请输入明文(输入#结束)：')
    if m == '0x0123456789abcdeffedcba9876543210':
            r+=f(int2bit(int(m,16),128))
            print(hex(int(r,2)))
    else:
        while(len(m)%16!=0):
            m+='0'
        for i in range(0,len(m),16):
            r+=f(m[i:i+16])                         #分组加密|m为字符串
        print('密文：'+r)

def decrypt():
    r=''
    set_Ck()
    RoundKey()
    Roundk.reverse()        #解密密钥是加密密钥的逆序
    m = input('请输入密文')
    for i in range(0,len(m),128):
        r+=ff(m[i:i+128])
    r=bin2str(r)
    for i in range(len(r) - 1, 0, -1):
        if r[i] == "#":
            r = r[0:i]
            break
    print('明文：' + r)

option=int(input('请选择：1、加密   2、解密\n'))
if option==1:
    encrypt()
else:
    decrypt()
