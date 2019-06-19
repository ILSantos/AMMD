import re
from model import Model

tipos_atributos = ['num', 'cat']


def nome_valido(nome, lista_nomes):
    if re.match("^[A-Za-z0-9_-]*$", nome) and 1 <= len(nome) <= 80 and nome not in lista_nomes:
        return True
    else:
        return False


def coleta_atributos(num_atributos, linhas):
    atributos = []

    for i in range(1, num_atributos + 1):
        linha = linhas[i].split()

        tipo = linha[0]
        nome_atributo = linha[1]
        atributo = dict()

        if nome_valido(nome_atributo, atributos):
            if tipo in tipos_atributos:
                # Se o tipo de atributo for 'num', adiciona no dict
                # o tipo como chave e o nome como valor
                if tipo == tipos_atributos[0]:
                    atributo[tipo] = nome_atributo

                # Se o tipo de atributo for 'cat', cria outro dict com
                # os valores da linha, o nome do atributo como chave e
                # adiciona no dict principal como valor da chave de tipo 'cat'
                elif tipo == tipos_atributos[1]:
                    numValores = int(linha[2])
                    lista_valores = []
                    valores = dict()

                    for j in range(3, numValores + 3):
                        if nome_valido(linha[j], lista_valores):
                            lista_valores.append(linha[j])
                        else:
                            print("Erro de valores de atributo")
                            return

                    valores[nome_atributo] = lista_valores
                    atributo[tipo] = valores

                atributos.append(atributo)
            else:
                print("Erro de tipo de atributo")
                return
        else:
            print("Erro no nome do atributo")
            return

    # print(json.dumps(atributos, indent=2))
    return atributos


def coleta_rotulos(linha_rotulo):
    linha = linha_rotulo.split()
    rotulo = dict()
    if linha[0] == 'cat' and linha[1] == 'classe':
        num_valores = int(linha[2])
        lista_valores = []

        valores = dict()

        for i in range(3, num_valores + 3):
            if nome_valido(linha[i], lista_valores):
                lista_valores.append(linha[i])
            else:
                print("Erro de valores de rotulo")
                return
        valores['classe'] = lista_valores
        rotulo['cat'] = valores

    return rotulo


def coleta_exemplos(indice, linhas, atributos, num_atrr, num_exemplos):
    lista_atributos = atributos
    exemplos = []

    for i in range(1 + indice, 1 + indice + num_exemplos):  # Para cada linha de exemplo
        exemplo = []
        linha = linhas[i].split()

        for j in range(0, len(linha) - 1):
            for key, value in lista_atributos[j].items():
                if key == tipos_atributos[0]:
                    exemplo.append(int(linha[j]))
                elif key == tipos_atributos[1]:
                    for k, v in value.items():
                        if linha[j] in v:
                            exemplo.append(linha[j])

        if len(exemplo) == num_atrr:
            exemplo.append(linha[-1])
            exemplos.append(exemplo)
        else:
            print("Erro na coleta de exemplos")
            break

    return exemplos


def main():
    file = open('./datasets/iris.mini', 'r')

    linhas = file.readlines()

    num_atrr = int(linhas[0])
    atributos = coleta_atributos(num_atrr, linhas)
    num_rotulos = int(linhas[1 + num_atrr])
    rotulos = coleta_rotulos(linhas[2 + num_atrr])

    indice_exemplos = 1 + num_atrr + 2
    num_exemplos = int(linhas[indice_exemplos])
    exemplos = coleta_exemplos(indice_exemplos, linhas, atributos, num_atrr, num_exemplos)

    model = Model(num_atrr, atributos, num_rotulos, rotulos, num_exemplos, exemplos)


if __name__ == "__main__":
    main()