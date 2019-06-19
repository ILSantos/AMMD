import csv
import random
import math
import re

def carregaCsv(arquivo, header=False):
    linhas = csv.reader(open(arquivo, 'rt'))
    dataset = list(linhas)
    if header:
        # remove a header
        dataset = dataset[1:]
    for i in range(len(dataset)):
        dataset[i] = [float(x) if re.search('\d', x) else x for x in dataset[i]]
    return dataset

# divide o dataset 
def divDataset(dataset, splitRatio):
    tam_treino = int(len(dataset) * splitRatio)
    set_treino = []
    copia = list(dataset)
    while len(set_treino) < tam_treino:
        index = random.randrange(len(copia))
        set_treino.append(copia.pop(index))
    return [set_treino, copia]

def separaPorClasse(dataset):
    separado = {}
    for i in range(len(dataset)):
        vetor = dataset[i]
        if (vetor[-1] not in separado):
            separado[vetor[-1]] = []
        separado[vetor[-1]].append(vetor)
    return separado

def media(num):
    resultado = sum(num) / float(len(num))
    return resultado

def desvioPadrao(num):
    avg = media(num)
    variancia = sum([pow(x-avg, 2) for x in num])/float(len(num)-1)
    return math.sqrt(variancia)

def sumariza(dataset):
    sumarios = [(media(atributo), desvioPadrao(atributo)) for atributo in zip(*dataset)]
    del sumarios[-1]
    return sumarios

def sumarizaPorClasse(dataset):
    separado = separaPorClasse(dataset)
    sumarios = {}
    for valorClasse, instancias in separado.items():
        sumarios[valorClasse] = sumariza(instancias)
    return sumarios

def calculaProbabilidade(x, media, desvioPadrao):
    expoente = math.exp(-(math.pow(x-media, 2)/(2*math.pow(desvioPadrao, 2))))
    return (1 / (math.sqrt(2*math.pi) * desvioPadrao)) * expoente

def calculaProbabilidadeClasses(sumarios, vetor_entrada):
    probabilidades = {}
    for valorClasse, sumariosClasse in sumarios.items():
        probabilidades[valorClasse] = 1
        for i in range(len(sumariosClasse)):
            media, desvioPadrao = sumariosClasse[i]
            x = vetor_entrada[i]
            probabilidades[valorClasse] *= calculaProbabilidade(x, media, desvioPadrao)
    return probabilidades

def predicao(sumarios, vetor_entrada):
    probabilidades =  calculaProbabilidadeClasses(sumarios, vetor_entrada)
    melhorRotulo, melhorProb = None, -1
    for valorClasse, probabilidade in probabilidades.items():
        if melhorRotulo is None or probabilidade > melhorProb:
            melhorProb = probabilidade
            melhorRotulo = valorClasse
    return melhorRotulo

def pegaPredicoes(sumarios, set_teste):
    predicoes = []
    for i in range(len(set_teste)):
        resultado = predicao(sumarios, set_teste[i])
        predicoes.append(resultado)
    return predicoes

def acuracia(set_teste, predicoes):
    correto = 0
    for i in range(len(set_teste)):
        if set_teste[i][-1] == predicoes[i]:
            correto += 1
    return (correto/float(len(set_teste))) * 100.0

def main():
    arquivo = (r'./datasets/wine.csv')
    slipRatio = 0.67
    dataset = carregaCsv(arquivo, header=True)
    set_treino, set_teste = divDataset(dataset, slipRatio)
    print("Usando %s linhas pra treinamento e %s linhas pra teste" % (len(set_treino),(len(set_teste))))
    # prepara modelo
    sumarios = sumarizaPorClasse(set_treino)
    # testa modelo
    predicoes = pegaPredicoes(sumarios, set_teste)
    acc = acuracia(set_teste, predicoes)
    print("Acurácia: %.3f" % acc)

if __name__ == "__main__":
    main()