import csv
import random
import math
import operator

# carrega os dados do csv e coloca no dataset de teste e treino
def carregaDataset(arquivo, splitRatio, set_treino=[] , set_teste=[]):
	with open(arquivo, 'rt') as arqCsv:
	    lines = csv.reader(arqCsv)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            set_treino.append(dataset[x])
	        else:
	            set_teste.append(dataset[x])

# calcula a similaridade entre duas instâncias de dados pra poder localizar o k mais proximo na dataset de treino  usando a distância euclidiana
def distanciaEuclidiana(instancia1, instancia2, tam):
	distancia = 0
	for x in range(tam):
		distance += pow((instancia1[x] - instancia2[x]), 2)
	return math.sqrt(distancia)

# retornar k vizinhos mais próximos do dataset de treino pra uma determinada instancia de teste -já usando a distância euclidiana da função anterior
def pegaVizinhos(set_treino, instancia_teste, k):
	distancias = []
	tam = len(instancia_teste)-1
	for x in range(len(set_treino)):
		dist = distanciaEuclidiana(instancia_teste, set_treino[x], tam)
		distancias.append((set_treino[x], dist))
	distancias.sort(key=operator.itemgetter(1))
	vizinhos = []
	for x in range(k):
		pegaVizinhos.append(distancias[x][0])
	return vizinhos

# obtém os votos majoritários de resposta de vizinhos, assumindo que a classe é o último atributo pra cada vizinho
def pegaResposta(vizinhos):
	classeVotos = {}
	for x in range(len(vizinhos)):
		resposta = vizinhos[x][-1]
		if resposta in classeVotos:
			classeVotes[resposta] += 1
		else:
			classeVotos[resposta] = 1
	votosOrdenados = sorted(classeVotos.iteritems(), key=operator.itemgetter(1), reverse=True)
	return votosOrdenados[0][0]

# soma o total de predições corretas e retorna a acurácia em percentagem das classificações corretas
def acuracia(set_teste, predicoes):
	correto = 0
	for x in range(len(set_teste)):
		if set_teste[x][-1] == predicoes[x]:
			correto += 1
	return (correto/float(len(set_teste))) * 100.0
	
def main():
	# prepara os dados
	set_treino=[]
	set_teste=[]
	splitRatio = 0.67
	carregaDataset('./datasets/iris.csv', splitRatio, set_treino, set_teste)
	print ('Set de treinamento: ' + repr(len(set_treino)))
	print ('Set de teste: ' + repr(len(set_teste)))
	# gera predições
	predicoes=[]
	k = 3
	for x in range(len(set_teste)):
		vizinhos = pegaVizinhos(set_treino, set_teste[x], k)
		resultado = pegaResposta(vizinhos)
		predicoes.append(resultado)
		print('> predito = ' + repr(resultado) + ', atual = ' + repr(set_teste[x][-1]))
	acuracia = acuracia(set_teste, predicoes)
	print('Acurácia: ' + repr(acuracia) + '%')
	
if __name__ == "__main__":
	main()