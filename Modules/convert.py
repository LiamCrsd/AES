def base16_2_matrix(text):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(0,16):
        matrix[i%4][i//4] = int(text[(2*i):(2*i)+2],base=16)
    return matrix

def matrix_2_base16(mat):
    t = ""
    for i in range(16):
        t += hex(mat[i%4][i//4])[2:]
    return t

def base16_2_ascii(b):
    t = ""

    for i in range(len(b) // 2):
        byte = b[2*i:2*i+2]
        if int(byte, base=16) < 128: 
            i = int(byte, base=16)
            l = bytes([i]).decode()
        elif: int(byte, base=16) < 192:
            l = ("\xc2" + str(bytes([int(byte, base=16)]))[3:-1]).decode()
        t += l
    return t

def ascii_2_base16(text):
	res = ''
	for lettre in text:
		res += hex(ord(lettre))[2:]
	while len(res) != 32: #If the text is not 16 characters long, it is completed with empty characters represented by the value 0 in ascii.
		res += '00'
	return res

def key_2_matrix(text):
    text = ascii_2_base16(text)
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(16):
        matrix[i//4][i%4] = int(text[(2*i):(2*i)+2],base=16)
    return matrix

def ascii_2_matrix(text):
    return base16_2_matrix(ascii_2_base16(text))

def matrix_2_ascii(mat):
    return base16_2_ascii(matrix_2_base16(mat))

