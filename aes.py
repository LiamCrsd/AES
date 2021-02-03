import aes_dec as dec
import aes_enc as enc

def text2matrix(text):
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(0,16):
        matrix[i%4][i//4] = int(text[(2*i):(2*i)+2],base=16)
    return matrix

def key2matrix(text):
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(16):
        matrix[i//4][i%4] = int(text[(2*i):(2*i)+2],base=16)
    return matrix

def matrix2text(mat):
    t = ""
    for i in range(16):
        t += hex(mat[i%4][i//4])[2:]
    return t

def bizarre2text(b):
    t = ""
    for i in range(len(b) // 2):
        byte = b[2*i:2*i+2]
        i = int(byte, base=16)
        l = bytes([i]).decode()
        t += l
    return t

def text2bizarre(text):
	res = ''
	for lettre in text:
		res += hex(ord(lettre))[2:]
	while len(res) != 32:
		res += '00'
	return res

def encrypt(text, key):
    mat_text = text2matrix(text2bizarre(text))
    mat_key = key2matrix(text2bizarre(key))
    res = enc.AES(mat_text, mat_key)
    return res

def decrypt(mat_text, key):
    mat_key = key2matrix(text2bizarre(key))
    res = dec.InvAES(mat_text,mat_key)
    return bizarre2text(matrix2text(res))
