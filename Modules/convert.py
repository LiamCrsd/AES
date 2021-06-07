def base16_2_matrix(text):
    matrix = [[0,0,0,0] for _ in range(4)]
    for i in range(0, 16):
        matrix[i%4][i//4] = int(text[(2*i):(2*i)+2], base=16)
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
        elif int(byte, base=16) < 192:
            l = (bytes([194, int(byte, base=16)])).decode()
        else:
            l = (bytes([195, int(byte, base=16) - 64])).decode()
        t += l
    return t

def int_2_utf8(n):
	if n < 128:
		i = bytes([n]).decode()
	elif n < 192:
		i = bytes([194, n]).decode()
	else:
		i = bytes([195, n - 64]).decode()
	return i

def ascii_2_base16(text):
    res = ""
    for lettre in text:
        tmp = hex(ord(lettre))[2:]
        if len(tmp) == 2:
            res += tmp
        else:
            res += "0" + tmp
    while len(res) != 32:
        res += "00"
    return res

def key_2_matrix(text):
    text = ascii_2_base16(text)
    matrix = [[0,0,0,0],[0,0,0,0],[1,7,2,9],[0,0,0,0]]
    for i in range(16):
        matrix[i//4][i%4] = int(text[(2*i):(2*i)+2], base=16)
    return matrix

def ascii_2_matrix(text):
    return base16_2_matrix(ascii_2_base16(text))

def matrix_2_ascii(mat):
    t = ""
    for c in range(16):
        t += int_2_utf8(mat[c%4][c//4])
    return t
