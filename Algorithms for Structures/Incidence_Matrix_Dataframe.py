import os
import pandas as pd
import numpy as np

def processar_grafos_matriz_incidencia(pasta_grafos, arquivo_csv, pasta_saida):
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
            
            # Lista para armazenar as arestas
            lista_arestas = []
            
            # Preenchendo a lista de arestas com base nas arestas do arquivo
            for linha in linhas[1:]:
                vertice1, vertice2, peso = map(float, linha.strip().split())
                lista_arestas.append((int(vertice1), int(vertice2), peso))
            
            n_arestas = len(lista_arestas)
            
            # Criando uma matriz de incidência de tamanho [n_vertices x n_arestas]
            matriz_incidencia = np.zeros((n_vertices, n_arestas))
            
            # Preenchendo a matriz de incidência
            for i, (vertice1, vertice2, peso) in enumerate(lista_arestas):
                matriz_incidencia[int(vertice1), i] = 1
                matriz_incidencia[int(vertice2), i] = 1
            
            # Convertendo a matriz de incidência para um DataFrame
            df_matriz_incidencia = pd.DataFrame(matriz_incidencia, columns=[f'Aresta_{i}' for i in range(n_arestas)])
            
            # Obtendo o nome da instância
            nome_instancia = os.path.splitext(arquivo)[0]
            
            # Procurando as informações de vértices selecionados no CSV
            vertices_selecionados_str = df_selecionados.loc[df_selecionados['Instância'] == nome_instancia, 'Vértices Selecionados'].values[0]
            vertices_selecionados = list(map(int, vertices_selecionados_str.strip('[]').split(',')))
            
            # Criando a coluna 'Conjuntos' para os vértices
            conjuntos_coluna = [2 if i in vertices_selecionados else 1 for i in range(n_vertices)]
            
            # Adicionando a coluna 'Conjuntos' ao DataFrame de vértices
            df_matriz_incidencia['Conjuntos'] = conjuntos_coluna
            
            # Salvando o dataframe de matriz de incidência resultante em um arquivo CSV
            nome_arquivo_saida_incidencia = os.path.join(pasta_saida, f'{nome_instancia}_matriz_incidencia.csv')
            df_matriz_incidencia.to_csv(nome_arquivo_saida_incidencia, index=False)
            print(f'Salvo: {nome_arquivo_saida_incidencia}')

# Exemplo de uso
pasta_grafos = 'instances'
arquivo_csv = 'resultados_valores_otimos.csv'
pasta_saida = 'dataframes_matriz_incidencia'

processar_grafos_matriz_incidencia(pasta_grafos, arquivo_csv, pasta_saida)
