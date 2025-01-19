import os
import pandas as pd
import numpy as np

def processar_grafos_e_adicionar_conjuntos(pasta_grafos, arquivo_csv, pasta_saida):
    # Lendo o CSV que contém as informações dos vértices selecionados
    df_selecionados = pd.read_csv(arquivo_csv)
    
    # Iterando sobre os arquivos da pasta de grafos
    for arquivo in os.listdir(pasta_grafos):
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(pasta_grafos, arquivo)
            
            # Lendo o arquivo de grafo
            with open(caminho_arquivo, 'r') as f:
                linhas = f.readlines()
            
            # Obtendo a quantidade de vértices e o tamanho do conjunto de diversidade máxima
            primeira_linha = linhas[0].strip().split()
            n_vertices = int(primeira_linha[0])
            tamanho_conjunto_div_max = int(primeira_linha[1])
            
            # Criando uma matriz de adjacência (inicialmente com zeros)
            matriz_adjacencia = np.zeros((n_vertices, n_vertices))
            
            # Preenchendo a matriz de adjacência com base nas arestas
            for linha in linhas[1:]:
                vertice1, vertice2, peso = map(float, linha.strip().split())
                matriz_adjacencia[int(vertice1)][int(vertice2)] = peso
                matriz_adjacencia[int(vertice2)][int(vertice1)] = peso  # Para grafos não direcionados
            
            # Convertendo a matriz de adjacência para um dataframe
            df_grafo = pd.DataFrame(matriz_adjacencia, columns=[f'Vértice_{i+1}' for i in range(n_vertices)])
            
            # Obtendo o nome da instância
            nome_instancia = os.path.splitext(arquivo)[0]
            
            # Procurando as informações de vértices selecionados no CSV
            vertices_selecionados_str = df_selecionados.loc[df_selecionados['Instância'] == nome_instancia, 'Vértices Selecionados'].values[0]
            vertices_selecionados = list(map(lambda x: int(x), vertices_selecionados_str.strip('[]').split(',')))

            # Garantindo que a indexação dos vértices esteja correta
            df_grafo['Conjuntos'] = [2 if i in vertices_selecionados else 1 for i in range(n_vertices)]

            # Salvando o dataframe resultante em um arquivo CSV
            nome_arquivo_saida = os.path.join(pasta_saida, f'{nome_instancia}_matriz_adjacencia.csv')
            df_grafo.to_csv(nome_arquivo_saida, index=False)
            print(f'Salvo: {nome_arquivo_saida}')

# Exemplo de uso
pasta_grafos = 'New Instances Carlos/euclidianas'
arquivo_csv = 'New Instances Carlos/great_values_euclidianas.csv'
pasta_saida = 'New Instances Carlos/Euclidianas Matriz Adj'

processar_grafos_e_adicionar_conjuntos(pasta_grafos, arquivo_csv, pasta_saida)
