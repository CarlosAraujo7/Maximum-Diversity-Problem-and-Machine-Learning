import os
import pandas as pd
from collections import defaultdict

def processar_grafos_lista_adjacencia(pasta_grafos, arquivo_csv, pasta_saida):
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
            
            # Criando uma lista de adjacência (usando defaultdict para listas)
            lista_adjacencia = defaultdict(list)
            
            # Preenchendo a lista de adjacência com base nas arestas
            for linha in linhas[1:]:
                vertice1, vertice2, peso = map(float, linha.strip().split())
                lista_adjacencia[int(vertice1)].append((int(vertice2), peso))
                lista_adjacencia[int(vertice2)].append((int(vertice1), peso))  # Para grafos não direcionados
            
            # Convertendo a lista de adjacência para um DataFrame
            df_grafo = pd.DataFrame(dict(lista_adjacencia)).fillna(0)
            
            # Reindexando para garantir que todos os vértices estejam presentes
            df_grafo = df_grafo.reindex(range(n_vertices), fill_value=0)
            
            # Obtendo o nome da instância
            nome_instancia = os.path.splitext(arquivo)[0]
            
            # Procurando as informações de vértices selecionados no CSV
            vertices_selecionados_str = df_selecionados.loc[df_selecionados['Instância'] == nome_instancia, 'Vértices Selecionados'].values[0]
            vertices_selecionados = list(map(int, vertices_selecionados_str.strip('[]').split(',')))
            
            # Criando a coluna 'Conjuntos' de uma vez só, usando pd.concat para eficiência
            conjuntos_coluna = pd.Series([2 if i in vertices_selecionados else 1 for i in range(n_vertices)])
            df_grafo = pd.concat([df_grafo, conjuntos_coluna.rename('Conjuntos')], axis=1)
            
            # Salvando o dataframe resultante em um arquivo CSV
            nome_arquivo_saida = os.path.join(pasta_saida, f'{nome_instancia}_lista_adjacencia.csv')
            df_grafo.to_csv(nome_arquivo_saida, index=False)
            print(f'Salvo: {nome_arquivo_saida}')

# Exemplo de uso
pasta_grafos = 'instances'
arquivo_csv = 'resultados_valores_otimos.csv'
pasta_saida = 'dataframes_lista'

processar_grafos_lista_adjacencia(pasta_grafos, arquivo_csv, pasta_saida)
