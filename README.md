# Aprendizado de Máquina e Mineração de Dados

## Trabalho Prático 1

__Objetivo:__ implementar o Mini Weka, contendo seus próprios algoritmos para induzir e empregar os modelos de classificação estudados em aula. Os indutores e classificadores devem ser um ou mais programas de linha de comando.

__Entrada:__ os indutores devem ler arquivos de dados no formato ARFF ou MiniARFF, especificados neste documento. Os classificadores devem ler arquivos de dados no formato ARFF ou MiniARFF, bem como arquivos que representam os modelos induzidos, em formato especificado pelos autores.

__Saída:__ os indutores devem gerar arquivos em formato especificado pelos autores do trabalho. Os classificadores devem escrever na saída padrão.

        PYTHON: print()
        C: printf()
        C++: std::count

__Restrições:__ não é permitido utilizar bibliotecas que implementem partes que são objetos de avaliação do trabalho. Por exemplo, pode-se utilizar *NumPy* ou outra biblioteca para realizar operações de álgebra linear, mas __não__ pode utilizar uma biblioteca que encontre os vizinhos mais próximos, que implemente diretamente uma função de ganho de informação ou calcule automaticamente a distância entre o exemplo de teste e os vetores de suporte. É permitido utilizar *pickles* ou outro formato automático de serialização.

__Indutores implementados:__

1. Modelo probabilístico Naive Bayes (atributos categóricos e numéricos)
2. Árvores de decisão (mínimo: ID3, ganho de informação e atributos categóricos)
3. Regras (algoritmo de cobertura estudado em aula para atributos categóricos)
4. Vizinhança (k-NN; deve ser possível utilizar distância euclidiana, Manhattan e Chebyshev)
