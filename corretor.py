import nltk
import pandas as pd

def cria_vocabulario(caminho_texto):
    with open(caminho_texto, "r",encoding="utf8") as f:
        artigo = f.read()
    lista_tokens = nltk.tokenize.word_tokenize(artigo)
    lista_palavras = []
    for token in lista_tokens:
        if token.isalpha():
            lista_palavras.append(token)
    lista_normalizada = []
    for palavra in lista_palavras:
        lista_normalizada.append(palavra.lower())
    lista_normalizada
    return lista_normalizada

def probabilidade(palavra_gerada):
    return frequencia[palavra_gerada]/quant_palavras

def insere_letras(fatias):
    novas_palavras = []
    letras = "abcdefghijklmnopqrstuvwxyzáéíóúâêôàçñãõ"
    for E, D in fatias:
        for letra in letras:
            novas_palavras.append(E + letra + D)
    return novas_palavras

def deletando_caracteres(fatias):
    novas_palavras = []
    for E, D in fatias:
        novas_palavras.append(E + D[1:])
    return novas_palavras

def troca_letras(fatias):
    novas_palavras = []
    letras = "abcdefghijklmnopqrstuvwxyzáéíóúâêôàçñãõ"
    for E, D in fatias:
        for letra in letras:
            novas_palavras.append(E + letra + D[1:])
    return novas_palavras

def inverte_letras(fatias):
    novas_palavras = []
    for E, D in fatias:
        if len(D) > 1:
            novas_palavras.append(E + D[1] + D[0] + D[2:])
    return novas_palavras

def gerador_palavras(palavra):
    fatias = []
    for i in range(len(palavra)+1):
        fatias.append((palavra[:i], palavra[i:]))
    palavras_geradas = insere_letras(fatias)
    palavras_geradas += deletando_caracteres(fatias)
    palavras_geradas += troca_letras(fatias)
    palavras_geradas += inverte_letras(fatias)
    return palavras_geradas

def corretor(palavra):
    palavras_geradas = gerador_palavras(palavra)
    palavra_correta = max(palavras_geradas, key=probabilidade)
    return palavra_correta

def avaliador(correta, corrigida):
    numero_palavras = len(corrigida)
    acertou = 0
    desconhecida = 0
    for i in range(numero_palavras):
        if correta[i] == corrigida[i]:
            acertou += 1
        if correta[i] not in vocabulario:
            desconhecida += 1
    taxa_acerto = round(acertou*100/numero_palavras, 2)
    taxa_desconhecida = round(desconhecida*100/numero_palavras, 2)
    print(f"O corretor foi capaz de corrigir {taxa_acerto}% de {numero_palavras} palavras, o quantidade de palavras desconhecidas é {taxa_desconhecida}%")

lista_palavras  = cria_vocabulario("dados/txt-dados.txt")
lista_palavras += cria_vocabulario("dados/txt-artigo-dados.txt")
lista_palavras += cria_vocabulario("dados/artigos.txt")
resposta = str(input("Deseja adicionar outro arquivo txt para que seja adicionado ao vocabulário? [S/N] "))
while resposta not in "nN":
    if resposta in "sS":
        while True:
            try:
                caminho = str(input("Digite o caminho e o nome do arquivo que será adicionado ao vocabulário [C para cancelar]: "))
                if caminho in "Cc":
                    break
                lista_palavras += cria_vocabulario(caminho)
            except FileNotFoundError:
                print("caminho de arquivo inválido, por favor tente novamente...")
    if resposta not in "Ss":
        print("Opção inválida, por favor digite novamente...")
    resposta = str(input("Deseja adicionar outro arquivo txt para que seja adicionado ao vocabulário? [S/N] "))
todas_palavras = lista_palavras
frequencia = nltk.FreqDist(todas_palavras)
quant_palavras = len(todas_palavras)
vocabulario = set(lista_palavras)
palavras_teste = pd.read_table("dados/palavras.txt", sep=" ", names = ["correta", "errada"], header=0)
corretas = palavras_teste["correta"]
erradas = palavras_teste["errada"]
lista_corrigidas = []
for errada in erradas:
    lista_corrigidas.append(corretor(errada))
corrigidas = pd.Series(lista_corrigidas)
avaliador(corretas, corrigidas)

