import pandas as pd
import numpy as np
from math import sqrt

# Dados da tabela
distancias_cm = [0, 16, 36, 56, 76]  # em cm
distancias_m = [d/100 for d in distancias_cm]  # conversão para metros

# Incerteza tipo B para distância: 0.5 mm = 0.0005 m
incerteza_B_distancia_m = 0.0005  # em metros

# Incerteza tipo B para tempo: 0.00005 s
incerteza_B_tempo = 0.00005  # em segundos

# Tempos de cada medição (em segundos)
tempos = [
    # t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 cm
    [0.42115, 0.43745, 0.41475, 0.39485, 0.38555, 0.4135, 0.37245, 0.4061, 0.38105, 0.3884, 0.37985, 0.4397, 0.399, 0.45135, 0.4089, 0.38975, 0.3714, 0.44395, 0.4156, 0.3998],  # 16 cm
    [0.8835, 0.919, 0.8698, 0.82915, 0.81035, 0.86605, 0.78325, 0.85255, 0.8014, 0.8171, 0.79815, 0.921, 0.83915, 0.9455, 0.8597, 0.8198, 0.7805, 0.9311, 0.87245, 0.84055],  # 36 cm
    [1.3405, 1.39235, 1.3188, 1.2572, 1.23175, 1.30925, 1.1892, 1.292, 1.2168, 1.2403, 1.2116, 1.39405, 1.27425, 1.43135, 1.30515, 1.24475, 1.1851, 1.41095, 1.32485, 1.27575],  # 56 cm
    [1.79395, 1.86105, 1.7655, 1.6839, 1.65275, 1.7486, 1.5928, 1.72855, 1.6304, 1.6606, 1.6222, 1.8645, 1.7069, 1.91235, 1.7486, 1.6684, 1.5881, 1.8899, 1.77535, 1.70655]   # 76 cm
]

# Função para calcular a média
def calcular_media(valores):
    return sum(valores) / len(valores)

# Função para calcular o desvio padrão
def calcular_desvio_padrao(valores):
    media = calcular_media(valores)
    soma_quadrados = sum((x - media) ** 2 for x in valores)
    return sqrt(soma_quadrados / (len(valores) - 1))

# Função para calcular o desvio padrão da média (incerteza tipo A)
def calcular_desvio_padrao_media(valores):
    return calcular_desvio_padrao(valores) / sqrt(len(valores))

# Função para combinar incertezas tipo A e B
def combinar_incertezas(incerteza_A, incerteza_B):
    return sqrt(incerteza_A**2 + incerteza_B**2)

# Calcular média e incerteza dos tempos para cada distância
medias_tempos = []
incertezas_A_tempos = []
incertezas_totais_tempos = []

for i in range(len(distancias_cm)):
    media = calcular_media(tempos[i])
    incerteza_A = calcular_desvio_padrao_media(tempos[i])
    incerteza_total = combinar_incertezas(incerteza_A, incerteza_B_tempo)
    
    medias_tempos.append(media)
    incertezas_A_tempos.append(incerteza_A)
    incertezas_totais_tempos.append(incerteza_total)

# Criar um DataFrame com os resultados
dados_tabela = {
    'x(m)': distancias_m,
    'δx(m)': [incerteza_B_distancia_m] * len(distancias_m),
    't(s)': medias_tempos,
    'δt(s)': incertezas_totais_tempos
}

df = pd.DataFrame(dados_tabela)

# Formatar os valores com precisão adequada
df_formatado = pd.DataFrame({
    'x(m)': [f"{x:.2f}" for x in df['x(m)']],
    'δx(m)': [f"{dx:.4f}" for dx in df['δx(m)']],
    't(s)': [f"{t:.5f}" for t in df['t(s)']],
    'δt(s)': [f"{dt:.5f}" for dt in df['δt(s)']]
})

# Exibir o DataFrame
print("Dados para a Tabela 2:")
print(df_formatado)

# Salvar como CSV
df.to_csv('tabela2_tempo_posicao.csv', index=False)
print("\nDados salvo em 'tabela2_tempo_posicao.csv'")

# Também mostrar os valores numéricos para copiar diretamente
print("\nValores para cópia direta:")
for i in range(len(distancias_m)):
    print(f"Posição {i+1}: x = {distancias_m[i]:.2f} m, δx = {incerteza_B_distancia_m:.4f} m, t = {medias_tempos[i]:.5f} s, δt = {incertezas_totais_tempos[i]:.5f} s")

# Código LaTeX para a tabela
latex_tabela = """
\\begin{table}[htbp]
\\centering
\\caption{Tempo médio para cada posição com as suas respectivas incertezas.}
\\begin{tabular}{|c|c|c|c|}
\\hline
$x(m)$ & $\\delta x(m)$ & $t(s)$ & $\\delta t(s)$ \\\\ \\hline
"""

for i in range(len(distancias_m)):
    x = distancias_m[i]
    dx = incerteza_B_distancia_m
    t = medias_tempos[i]
    dt = incertezas_totais_tempos[i]
    
    latex_tabela += f"{x:.2f} & {dx:.4f} & {t:.5f} & {dt:.5f} \\\\ \\hline\n"

latex_tabela += """\\end{tabular}
\\label{tab:tempos_medios}
\\end{table}
"""

print("\nCódigo LaTeX para a Tabela 2:")
print(latex_tabela)