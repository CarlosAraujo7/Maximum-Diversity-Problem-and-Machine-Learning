import os
import pandas as pd

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
            
            # Inicializando a lista de adjacência
            lista_adjacencia = [[] for _ in range(n_vertices)]
            
            # Preenchendo a lista de adjacência com base nas arestas
            for linha in linhas[1:]:
                vertice1, vertice2, peso = linha.strip().split()
                vertice1 = int(vertice1)
                vertice2 = int(vertice2)
                peso = float(peso)
                
                # Adicionando a aresta para ambos os vértices (grafo não direcionado)
                lista_adjacencia[vertice1].append((vertice2, peso))
                lista_adjacencia[vertice2].append((vertice1, peso))
            
            # Obtendo o nome da instância
            nome_instancia = os.path.splitext(arquivo)[0]
            
            # Procurando as informações de vértices selecionados no CSV
            vertices_selecionados_str = df_selecionados.loc[df_selecionados['Instância'] == nome_instancia, 'Vértices Selecionados'].values[0]
            vertices_selecionados = list(map(int, vertices_selecionados_str.strip('[]').split(',')))
            
            # Preparando os dados para o DataFrame
            dados = []
            for i in range(n_vertices):
                adjacentes = '; '.join([f"{vizinho}({peso})" for vizinho, peso in lista_adjacencia[i]])
                conjunto = 2 if i in vertices_selecionados else 1
                dados.append({
                    'Vértice': i,
                    'Adjacentes': adjacentes,
                    'Conjuntos': conjunto
                })
            
            # Criando o DataFrame
            df_grafo = pd.DataFrame(dados)
            
            # Salvando o dataframe resultante em um arquivo CSV
            nome_arquivo_saida = os.path.join(pasta_saida, f'{nome_instancia}_lista_adjacencia.csv')
            df_grafo.to_csv(nome_arquivo_saida, index=False)
            print(f'Salvo: {nome_arquivo_saida}')

# Exemplo de uso
pasta_grafos = 'New Instances Carlos/uniformes inteiras'
arquivo_csv = 'New Instances Carlos/great_values_uniforme.csv'
pasta_saida = 'New Instances Carlos/Uniformes Inteiros Lista Adj'

processar_grafos_e_adicionar_conjuntos(pasta_grafos, arquivo_csv, pasta_saida)
