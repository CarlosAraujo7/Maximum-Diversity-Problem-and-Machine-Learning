import os
import pandas as pd

def processar_grafos_lista_arestas(pasta_grafos, arquivo_csv, pasta_saida):
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
                lista_arestas.append([int(vertice1), int(vertice2), peso])
            
            # Convertendo a lista de arestas para um DataFrame
            df_grafo = pd.DataFrame(lista_arestas, columns=['Vértice_1', 'Vértice_2', 'Peso'])
            
            # Obtendo o nome da instância
            nome_instancia = os.path.splitext(arquivo)[0]
            
            # Procurando as informações de vértices selecionados no CSV
            vertices_selecionados_str = df_selecionados.loc[df_selecionados['Instância'] == nome_instancia, 'Vértices Selecionados'].values[0]
            vertices_selecionados = list(map(int, vertices_selecionados_str.strip('[]').split(',')))
            
            # Criando a coluna 'Conjuntos' com base em se qualquer um dos vértices da aresta faz parte do conjunto de diversidade máxima
            df_grafo['Conjuntos'] = df_grafo.apply(
                lambda row: 2 if row['Vértice_1'] in vertices_selecionados or row['Vértice_2'] in vertices_selecionados else 1,
                axis=1
            )
            
            # Salvando o dataframe resultante em um arquivo CSV
            nome_arquivo_saida = os.path.join(pasta_saida, f'{nome_instancia}_lista_arestas.csv')
            df_grafo.to_csv(nome_arquivo_saida, index=False)
            print(f'Salvo: {nome_arquivo_saida}')

# Exemplo de uso
pasta_grafos = 'instances'
arquivo_csv = 'resultados_valores_otimos.csv'
pasta_saida = 'dataframes_lista_arestas'

processar_grafos_lista_arestas(pasta_grafos, arquivo_csv, pasta_saida)
