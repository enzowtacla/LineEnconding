CARACTERES_VALIDOS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÂÊÔÃÕÇabcdefghijklmnopqrstuvwxyzáéíóúâêôãõç0123456789 .,!?'

def string_to_binario(texto):

    seq_binaria = ""

    for char in texto:
        decimal = ord(char)
        binario = format(decimal, '08b')

        seq_binaria += binario

    return seq_binaria.strip()


def codifica_amipseudo(seq_binaria):

    sinal_amipseudo = []
    polaridade_ultimo_um = -1

    for bit in seq_binaria:       #'0' é 0 e '1' alterna entre -V e +V
        if bit == '0':
            sinal_amipseudo.append(0)
        elif bit == '1':
            nova_polaridade = -polaridade_ultimo_um
            sinal_amipseudo.append(nova_polaridade)
            polaridade_ultimo_um = nova_polaridade
    return sinal_amipseudo

def decodifica_amipseudo(sinal_amipseudo):
    seq_decodificada = ""
    for pulso in sinal_amipseudo:
        if pulso == 0:
            seq_decodificada += '0'
        else:
            seq_decodificada += '1'
    return seq_decodificada


def criptografar(texto, deslocamento):
    texto_criptografado = ""
    tam = len(CARACTERES_VALIDOS)
    for char in texto:
        posicao_original = CARACTERES_VALIDOS.find(char)

        if posicao_original != -1:
            posicao_nova = (posicao_original + deslocamento) % tam
            texto_criptografado += CARACTERES_VALIDOS[posicao_nova]
        else:
            texto_criptografado += char
            
    return texto_criptografado

def descriptografar(texto_criptografado, deslocamento):
    return criptografar(texto_criptografado, -deslocamento)

texto = "Olá, mundo!"
print(f"Texto original: {texto}")

criptografado = criptografar(texto, 3)
print(f"Texto criptografado: {criptografado}")

seq_binaria = string_to_binario(texto)
print(f"Sequencia binaria: {seq_binaria}")

sinal_amipseudo = codifica_amipseudo(seq_binaria)
print(f"Sinal AMI Pseudo: {sinal_amipseudo}")

seq_decodificada = decodifica_amipseudo(sinal_amipseudo)
print(f"Sequencia decodificada: {seq_decodificada}")

descriptografado = descriptografar(criptografado, 3)
print(f"Texto descriptografado: {descriptografado}")