import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

# Dados da tabela
distancias_cm = [0, 16, 36, 56, 76]  # em cm
distancias_m = [d/100 for d in distancias_cm]  # conversão para metros

# Incerteza tipo B para distância: 0.5 mm = 0.0005 m
incerteza_B_distancia_m = 0.0005  # em metros

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
incertezas_totais_tempos = []

for i in range(len(distancias_cm)):
    media = calcular_media(tempos[i])
    incerteza_A = calcular_desvio_padrao_media(tempos[i])
    incerteza_total = combinar_incertezas(incerteza_A, 0.00005)  # 0.00005 é a incerteza tipo B do tempo
    
    medias_tempos.append(media)
    incertezas_totais_tempos.append(incerteza_total)

# Criar um DataFrame com os resultados
dados = {
    'x(m)': distancias_m,
    'δx(m)': [incerteza_B_distancia_m] * len(distancias_m),
    't(s)': medias_tempos,
    'δt(s)': incertezas_totais_tempos
}

df = pd.DataFrame(dados)

# Mostrar os dados da tabela
print("Dados para o gráfico:")
print(df)

# Plotar o gráfico de x versus t com barras de erro
plt.figure(figsize=(10, 6))
plt.errorbar(df['t(s)'], df['x(m)'], 
             xerr=df['δt(s)'], yerr=df['δx(m)'],
             fmt='o', markersize=8, color='blue', 
             ecolor='red', capsize=5, label='Dados experimentais')

# Ajustar uma curva teórica (para MRUV: x = (1/2)at²)
def ajuste_polinomial(x, y):
    # Para um MRUV, ajustamos uma parábola: x = x0 + v0*t + (1/2)a*t²
    # Como x0 = 0 e assumindo v0 = 0, temos x = (1/2)a*t²
    coefs = np.polyfit(x, y, 2)
    return coefs

# Removendo o ponto t=0, x=0 para o ajuste (pode ser problemático)
t_para_ajuste = df['t(s)'].values[1:]  # excluindo o primeiro ponto
x_para_ajuste = df['x(m)'].values[1:]  # excluindo o primeiro ponto

coefs = ajuste_polinomial(t_para_ajuste, x_para_ajuste)
a, b, c = coefs

# Criar uma função para a curva teórica
def curva_teorica(t, a, b, c):
    return a*t**2 + b*t + c

# Gerar pontos para a curva suave
t_curva = np.linspace(0, max(df['t(s)'])*1.05, 100)
x_curva = curva_teorica(t_curva, a, b, c)

# Plotar a curva teórica
plt.plot(t_curva, x_curva, 'r-', label=f'Ajuste: x = {a:.4f}t² + {b:.4f}t + {c:.4f}')

# Calcular a aceleração
aceleracao = 2 * a
print(f"\nAceleração calculada: {aceleracao:.4f} m/s²")

# Adicionar rótulos e título
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Posição (m)', fontsize=12)
plt.title('Gráfico de Posição versus Tempo', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Adicionar informações do ajuste no gráfico
plt.annotate(f'Aceleração: {aceleracao:.4f} m/s²', 
             xy=(0.05, 0.9), xycoords='axes fraction',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

# Salvar o gráfico
plt.savefig('grafico_posicao_vs_tempo.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como 'grafico_posicao_vs_tempo.png'")

# Mostrar o gráfico
plt.tight_layout()
plt.show()

# Também vamos fazer o gráfico de x versus t²
plt.figure(figsize=(10, 6))

# Calcular t² e sua incerteza
t_quadrado = [t**2 for t in df['t(s)']]
# A propagação de incerteza para t² é: δ(t²) = 2t·δt
delta_t_quadrado = [2*t*dt for t, dt in zip(df['t(s)'], df['δt(s)'])]

# Plotar x versus t² com barras de erro
plt.errorbar(t_quadrado, df['x(m)'], 
             xerr=delta_t_quadrado, yerr=df['δx(m)'],
             fmt='o', markersize=8, color='blue', 
             ecolor='red', capsize=5, label='Dados experimentais')

# Ajustar uma reta para x versus t²
# Para MRUV, esperamos x = (1/2)a·t², ou seja, x é linearmente proporcional a t²
def ajuste_linear(x, y):
    # Ajustando uma reta: y = mx + b
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

# Excluindo o ponto (0,0) para o ajuste linear
t2_para_ajuste = t_quadrado[1:]
x_para_ajuste = df['x(m)'].values[1:]

slope, intercept = ajuste_linear(t2_para_ajuste, x_para_ajuste)

# Gerar pontos para a reta de ajuste
t2_curva = np.linspace(0, max(t_quadrado)*1.05, 100)
x_curva = slope*t2_curva + intercept

# Plotar a reta de ajuste
plt.plot(t2_curva, x_curva, 'r-', label=f'Ajuste: x = {slope:.4f}t² + {intercept:.4f}')

# Calcular a aceleração a partir do coeficiente angular
aceleracao_linear = 2 * slope
print(f"\nAceleração calculada (do ajuste linear x vs t²): {aceleracao_linear:.4f} m/s²")

# Adicionar rótulos e título
plt.xlabel('Tempo² (s²)', fontsize=12)
plt.ylabel('Posição (m)', fontsize=12)
plt.title('Gráfico de Posição versus Tempo²', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Adicionar informações do ajuste no gráfico
plt.annotate(f'Aceleração: {aceleracao_linear:.4f} m/s²', 
             xy=(0.05, 0.9), xycoords='axes fraction',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

# Salvar o gráfico
plt.savefig('grafico_posicao_vs_tempo_quadrado.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como 'grafico_posicao_vs_tempo_quadrado.png'")

# Mostrar o gráfico
plt.tight_layout()
plt.show()