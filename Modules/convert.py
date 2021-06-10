def base16_2_matrix(text):
    """Fonction convertissant un texte en base 16 en une matrice 4x4 

    Parameters
    ----------
    text : str
        texte composé d'au plus 16 nombres en base 16 chacun écrit à l'aide de 2 chiffres

    Returns
    -------
    list
        Matrice 4x4 contenant les 16 nombres si possible et complétée par des 0 sinon 
    """
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(0,16):
        matrix[i%4][i//4] = int(text[(2*i):(2*i)+2],base=16)
    return matrix

def matrix_2_base16(mat):
    """Fonction convertissant une matrice 4x4 en un texte en base 16

    Parameters
    ----------
    mat : list or np.array
        Matrice 4x4 contenant 16 entiers compris entre 0 et 255

    Returns
    -------
    str
        texte optenu en écrivant consécutivement les 16 entiers en base 16 avec deux chiffres 
    """
    t = ""
    for i in range(16):
        t += hex(mat[i%4][i//4])[2:]
    return t

def base16_2_ascii(b):
    """Fonction convertissant un texte en base 16 en un texte en ascii

    Parameters
    ----------
    b : str
        texte composé de nombres en base 16 chacun écrit à l'aide de 2 chiffres

    Returns
    -------
    str
        texte obtenue en remplaçant chacun des nombres en base 16 par le caractère lui correspond dans le début de l'utf-8 (majoritairement la table ascii)
    """
    t = ""

    for i in range(len(b) // 2):
        byte = b[2*i:2*i+2]
        if int(byte, base=16) < 128:
            i = int(byte, base=16)
            l = bytes([i]).decode()
        elif int(byte, base=16) < 192:
            l = (bytes([194,int(byte, base=16)])).decode()
        else:
            l = (bytes([195,int(byte, base=16) - 64])).decode()
        t += l
    return t

def int_2_utf8(n):
    """Fonction convertissant un entier en un caractère

    Parameters
    ----------
    n : int
        entier entre 0 et 255

    Returns
    -------
    str
        Caractère associé en utf-8
    """
	if n < 128:
		i = bytes([n]).decode()
	elif n < 192:
		i = bytes([194, n]).decode()
	else:
		i = bytes([195, n - 64]).decode()
	return i

def ascii_2_base16(text):
    """Fonction convertissant un texte en ascii en un texte en base 16

    Parameters
    ----------
    text : str
        texte en ascii d'au plus 16 caractères 

    Returns
    -------
    str
        texte optenue en écrivant chaque caractère par sa réprensentation en base 16 avec deux chiffres 
    """
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
    """Fonction convertissant un texte représentant une clé de chiffrement en une matrice 4x4 contenant la clé

    Parameters
    ----------
    text : str
        texte en ascii d'au plus 16 caractères 

    Returns
    -------
    list
        Matrice 4x4 contenant la clé sous forme d'entiers
    """
    text = ascii_2_base16(text)
    matrix = [[0,0,0,0],[0,0,0,0],[1,7,2,9],[0,0,0,0]]
    for i in range(16):
        matrix[i//4][i%4] = int(text[(2*i):(2*i)+2],base=16)
    return matrix

def ascii_2_matrix(text):
    """Fonction convertissant un texte ascii en une matrice 4x4 

    Parameters
    ----------
    text : str
        texte en ascii d'au plus 16 caractères 

    Returns
    -------
    list
        Matrice 4x4 contenant la texte sous forme d'entiers
    """
    return base16_2_matrix(ascii_2_base16(text))

def matrix_2_ascii(mat):
    """Fonction convertissant une matrice 4x4 en un texte ascii

    Parameters
    ----------
    text : list or np.array
        Matrice 4x4 d'entier 

    Returns
    -------
    str
        texte ascii de 16 caractères
    """
    t = ""
    for c in range(16):
        t += int_2_utf8(mat[c%4][c//4])
    return t
    
def matrix_2_data(mat):
    """Fonction convertissant une liste de matrice 4x4 en un texte ascii

    Parameters
    ----------
    text : list 
        liste de matrice 4x4 d'entier 

    Returns
    -------
    str
        texte ascii
    """
	t = ""
	for e in mat:
		t += matrix_2_ascii(e)
	print(len(t))
	return t
