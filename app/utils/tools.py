import random

def gerar_codigo(tamanho=6):
    return f"{random.randint(10**(tamanho-1), 10**tamanho - 1)}"