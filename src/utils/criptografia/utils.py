import hashlib
import random
import string

def gerar_codigo_hash_aleatorio(tamanho=32):
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(tamanho))
    codigo_hash = hashlib.sha256(codigo.encode()).hexdigest()
    return codigo_hash