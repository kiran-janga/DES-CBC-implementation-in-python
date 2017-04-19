#This code takes the text message from message.txt, encrypts it and stores the encrypted message in encryptedFile.txt 
#Further it takes the encrypted message from encryptedFile.txt and decrypts it and stores the decrypted message to decryptedFile.txt

import numpy as np
import bitarray

CPTable = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]

EPTable = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]
 
IPTable = [57, 49, 41, 33, 25, 17, 9,  1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6
	]
FPTable = [
		39,  7, 47, 15, 55, 23, 63, 31,
		38,  6, 46, 14, 54, 22, 62, 30,
		37,  5, 45, 13, 53, 21, 61, 29,
		36,  4, 44, 12, 52, 20, 60, 28,
		35,  3, 43, 11, 51, 19, 59, 27,
		34,  2, 42, 10, 50, 18, 58, 26,
		33,  1, 41,  9, 49, 17, 57, 25,
		32,  0, 40,  8, 48, 16, 56, 24
	]
 
SOPTable = [
		15, 6, 19, 20, 28, 11,
		27, 16, 0, 14, 22, 25,
		4, 17, 30, 9, 1, 7,
		23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10,
		3, 24
	]
S1Table1 = np.array([[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
                     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
                     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
                     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]])
S1Table2 = np.array([[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
                     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
                     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
                     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]])
S1Table3 = np.array([[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
                     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
                     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
                     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]])
S1Table4 = np.array([[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
                     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
                     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
                     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]])
S1Table5 = np.array([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		          [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		          [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])
S1Table6 = np.array([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		          [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            	    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            	    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])
S1Table7 = np.array([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])
S1Table8 = np.array([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])

STableList = [S1Table1,S1Table2,S1Table3,S1Table4,S1Table5,S1Table6,S1Table7,S1Table8]

def generateKeys(key):
    
    keyList = []
    
    inputKey = key
    subKey = [None] * 48
    newInputKey = [None] * 56
    
    for i in range(16):
        
        newInputKey1 = [None] * 28
        newInputKey2 = [None] * 28
        
        newInputKey1[0:27] = inputKey[1:28]
        newInputKey1[27] = inputKey[0]
        
        newInputKey2[0:27] = inputKey[29:56]
        newInputKey2[27] = inputKey[28]

        newInputKey = newInputKey1 + newInputKey2
        
        for index,value in enumerate(CPTable):
            subKey[index] = newInputKey[value-1]
        
        keyList.append(subKey)
        inputKey = newInputKey
    return keyList
    
def DES_encryption_box(message1,message2,keyList):
    
    m1 = message1
    m2 = message2
        
    for i in range(16):
        
        Em2 = permute(m2,EPTable)
        Em2xor = xor(Em2,keyList[i])
        Sm2 = sbox(Em2xor)
        Pm2 = permute(Sm2,SOPTable)
        Pm2xor = xor(Pm2,m1)
        m1 = m2
        m2 = Pm2xor
        
    return m1+m2
    

def DES_decryption_box(emessage1,emessage2,keyList):
       
#Initial permutation and Final permutation for message in DES are not implemented.

    c1 = emessage1
    c2 = emessage2
    
    for i in range(16):
        
        Ec1 = permute(c1,EPTable)
        Ec1xor = xor(Ec1,keyList[15-i])
        Sc1 = sbox(Ec1xor)
        Pc1 = permute(Sc1,SOPTable)
        Pc1xor = xor(Pc1,c2)
        c2 = c1
        c1 = Pc1xor
        
    return c1+c2
        
def xor(l1,l2):
    
    outputlist = [None] * len(l1)
    
    for i in range(len(l1)):
        
        if l1[i] == l2[i]:
            outputlist[i] = 0
        else:
            outputlist[i] = 1
            
    return outputlist        
        
def permute(key,Table):
    newKey = [None] * len(Table)
    for index,value in enumerate(Table):
        newKey[index] = key[value-1]
    return newKey

def sbox(key):
    
    newKey = []
    for i in range(0,8):
        subKey = key[6*i:6*(i+1)]
        row = int(str(subKey[0])+str(subKey[5]),2)
        column = int(str(subKey[1])+str(subKey[2])+str(subKey[3])+str(subKey[4]),2)
        newKey += list(map(int,list("{0:04b}".format(STableList[i][row,column])))) 
    
    return newKey
    
def encrypt(message,key):
    
    
    bitString = bitarray.bitarray()
    bitString.fromstring(message)
    
    initialBitArray = list(map(int,list(bitString)))
    
    r = len(initialBitArray) % 64
    if r != 0:
        bitArray = initialBitArray + [0] * (64 - r)
    
    keys = generateKeys(key)
    encryptedBitArray = []

    output = DES_encryption_box(bitArray[0:32],bitArray[32:64],keys)
    
    encryptedBitArray += output
    
    i = 64
    while i < len(bitArray):
        outputxor = xor(output,bitArray[i:i+64])
        output = DES_encryption_box(outputxor[0:32],outputxor[32:64],keys)
        encryptedBitArray += output
        i += 64
        
    return encryptedBitArray
    
def decrypt(encryptedBitArray,key):
    
    keys = generateKeys(key)

    decryptedBitArray = []
    
    output = DES_decryption_box(encryptedBitArray[0:32],encryptedBitArray[32:64],keys)
    decryptedBitArray += output
    
    i = 64
    while i < len(encryptedBitArray):       
        output = DES_decryption_box(encryptedBitArray[i+0:i+32],encryptedBitArray[i+32:i+64],keys)
        outputxor = xor(output,encryptedBitArray[i-64:i])
        decryptedBitArray += outputxor
        i += 64
 
    o = bitarray.bitarray(decryptedBitArray).tostring()
    return o

keyText = "Crypto Project"
baKey = bitarray.bitarray()
baKey.fromstring("Crypto Project")
key = list(map(int,list(baKey)))[0:56]

#.............................................FOR ENCRYPTION..........................................

#textFile = open("message.txt", "r")
#f1 = textFile.read()
#textFile.close()
#  
#message = f1
#el = encrypt(message,key)
#es = " ".join(list(map(str,el)))
#print ("Encrypted Bits\n","Stored in encryptedFile.txt\n",el)
#encryptedFile = open("encryptedFile.txt","w+")
#encryptedFile.write(es)
#encryptedFile.close()


#....................................FOR DECRYPTION.................................................

textFile2 = open("encryptedFile.txt", "r")
f2 = textFile2.read()
textFile2.close()

el2 = list(map(int,f2.split(" ")))
dm = decrypt(el2,key)
decryptedFile = open("decryptedFile.txt","w+")
decryptedFile.write(dm)
decryptedFile.close()
print (dm)


