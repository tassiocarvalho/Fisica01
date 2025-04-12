import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

# Dados da tabela
distancias = [0, 16, 36, 56, 76]  # em cm

# Tempos de cada medição (em segundos)
tempos = [
    # t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 cm
    [0.42115, 0.43745, 0.41475, 0.39485, 0.38555, 0.4135, 0.37245, 0.4061, 0.38105, 0.3884, 0.37985, 0.4397, 0.399, 0.45135, 0.4089, 0.38975, 0.3714, 0.44395, 0.4156, 0.3998],  # 16 cm
    [0.8835, 0.919, 0.8698, 0.82915, 0.81035, 0.86605, 0.78325, 0.85255, 0.8014, 0.8171, 0.79815, 0.921, 0.83915, 0.9455, 0.8597, 0.8198, 0.7805, 0.9311, 0.87245, 0.84055],  # 36 cm
    [1.3405, 1.39235, 1.3188, 1.2572, 1.23175, 1.30925, 1.1892, 1.292, 1.2168, 1.2403, 1.2116, 1.39405, 1.27425, 1.43135, 1.30515, 1.24475, 1.1851, 1.41095, 1.32485, 1.27575],  # 56 cm
    [1.79395, 1.86105, 1.7655, 1.6839, 1.65275, 1.7486, 1.5928, 1.72855, 1.6304, 1.6606, 1.6222, 1.8645, 1.7069, 1.91235, 1.7486, 1.6684, 1.5881, 1.8899, 1.77535, 1.70655]   # 76 cm
]

# Converter distâncias para metros (cm -> m)
distancias_m = [d/100 for d in distancias]

# Função para calcular a média
def calcular_media(valores):
    return sum(valores) / len(valores)

# Função para calcular o desvio padrão
def calcular_desvio_padrao(valores):
    media = calcular_media(valores)
    soma_quadrados = sum((x - media) ** 2 for x in valores)
    return sqrt(soma_quadrados / (len(valores) - 1))

# Função para calcular o desvio padrão da média
def calcular_desvio_padrao_media(valores):
    return calcular_desvio_padrao(valores) / sqrt(len(valores))

# Calcular média e incerteza dos tempos para cada distância
medias_tempos = []
incertezas_tempos = []

for i in range(len(distancias)):
    media = calcular_media(tempos[i])
    incerteza = calcular_desvio_padrao_media(tempos[i])
    medias_tempos.append(media)
    incertezas_tempos.append(incerteza)

print("Médias dos tempos (s):", [round(t, 5) for t in medias_tempos])
print("Incertezas dos tempos (s):", [round(inc, 5) for inc in incertezas_tempos])

# Calcular velocidade média para cada distância
# v = Δs/Δt
velocidades = []
incertezas_velocidades = []

for i in range(1, len(distancias)):
    delta_s = distancias_m[i] - distancias_m[0]  # Distância em relação ao ponto inicial
    delta_t = medias_tempos[i] - medias_tempos[0]  # Tempo em relação ao ponto inicial
    
    # Velocidade em m/s
    v = delta_s / delta_t
    
    # Cálculo da incerteza da velocidade usando propagação de erros
    # σv = v * sqrt((σs/s)^2 + (σt/t)^2)
    # Como distância não tem incerteza (valores fixos), apenas consideramos a incerteza do tempo
    incerteza_v = v * (incertezas_tempos[i] / delta_t)
    
    velocidades.append(v)
    incertezas_velocidades.append(incerteza_v)

print("\nVelocidades médias (m/s):")
for i, v in enumerate(velocidades):
    print(f"Distância {distancias[i+1]} cm: {v:.4f} ± {incertezas_velocidades[i]:.4f} m/s")

# Ajuste linear para encontrar a aceleração (a = 2*coef_angular)
# Sabendo que s = s0 + v0*t + (1/2)*a*t^2
# Se s0 = 0 e v0 = 0, então s = (1/2)*a*t^2
# Portanto, plotando s vs t^2, o coeficiente angular será a/2

# Calcular t^2 para o ajuste
t_quadrado = [t**2 for t in medias_tempos[1:]]  # Excluindo t=0

# Implementação manual do método dos mínimos quadrados para o ajuste linear
def ajuste_linear(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi**2 for xi in x)
    
    # Coeficientes da reta y = a + b*x
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    a = (sum_y - b * sum_x) / n
    
    # Coeficiente de correlação
    numerador = n * sum_xy - sum_x * sum_y
    denominador = sqrt((n * sum_x2 - sum_x**2) * (n * sum(yi**2 for yi in y) - sum_y**2))
    r = numerador / denominador if denominador != 0 else 0
    
    # Cálculo da incerteza de b
    s_y = sqrt(sum((yi - (a + b * xi))**2 for xi, yi in zip(x, y)) / (n - 2))
    s_b = s_y / sqrt(sum((xi - sum_x/n)**2 for xi in x))
    
    return a, b, r, s_b

# Ajuste para s vs t²
a_s_t2, b_s_t2, r_s_t2, s_b_s_t2 = ajuste_linear(t_quadrado, distancias_m[1:])

# A aceleração é 2 vezes o coeficiente angular
aceleracao = 2 * b_s_t2
incerteza_aceleracao = 2 * s_b_s_t2

print(f"\nResultados do ajuste s vs t²:")
print(f"Equação: s = {a_s_t2:.4f} + {b_s_t2:.4f} * t²")
print(f"Coeficiente de correlação: {r_s_t2:.4f}")
print(f"Aceleração: {aceleracao:.4f} ± {incerteza_aceleracao:.4f} m/s²")

# Plotar o gráfico de s vs t
plt.figure(figsize=(10, 6))
plt.errorbar(medias_tempos[1:], distancias_m[1:], xerr=incertezas_tempos[1:], fmt='o', label='Dados experimentais')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição vs Tempo')
plt.grid(True)
plt.legend()

# Plotar o gráfico de s vs t²
plt.figure(figsize=(10, 6))
plt.errorbar(t_quadrado, distancias_m[1:], fmt='o', label='Dados experimentais')
# Linha de ajuste
t2_range = np.linspace(min(t_quadrado), max(t_quadrado), 100)
s_ajuste = a_s_t2 + b_s_t2 * t2_range
plt.plot(t2_range, s_ajuste, 'r-', label=f's = {a_s_t2:.4f} + {b_s_t2:.4f}*t²')
plt.xlabel('Tempo² (s²)')
plt.ylabel('Posição (m)')
plt.title('Posição vs Tempo² (Determinação da Aceleração)')
plt.grid(True)
plt.legend()

# Salvar os gráficos
plt.savefig('grafico_s_vs_t2.png')
print("\nGráficos gerados e salvos como 'grafico_s_vs_t2.png'")

# Calcular velocidade instantânea para cada ponto (derivada da posição)
# Para um MRUV: v = v0 + a*t
# Se v0 = 0, então v = a*t

velocidades_instantaneas = [aceleracao * t for t in medias_tempos[1:]]
incertezas_vi = [sqrt((incerteza_aceleracao/aceleracao)**2 + (incertezas_tempos[i+1]/medias_tempos[i+1])**2) * velocidades_instantaneas[i] for i in range(len(velocidades_instantaneas))]

print("\nVelocidades instantâneas (m/s):")
for i, v in enumerate(velocidades_instantaneas):
    print(f"Tempo {medias_tempos[i+1]:.4f} s: {v:.4f} ± {incertezas_vi[i]:.4f} m/s")

# Análise estatística adicional
# Teste de consistência do modelo MRUV

# Calcular qui-quadrado (chi-squared)
qui_quadrado = sum(((distancias_m[i+1] - (a_s_t2 + b_s_t2 * medias_tempos[i+1]**2)) / (b_s_t2 * 2 * medias_tempos[i+1] * incertezas_tempos[i+1]))**2 for i in range(len(distancias_m)-1))
graus_liberdade = len(distancias_m) - 1 - 2  # número de pontos - 1 - número de parâmetros ajustados

print(f"\nTeste de Qui-quadrado:")
print(f"χ² = {qui_quadrado:.4f}")
print(f"Graus de liberdade = {graus_liberdade}")
print(f"χ²/graus de liberdade = {qui_quadrado/graus_liberdade if graus_liberdade > 0 else 'N/A':.4f}")

# Resumo dos resultados
print("\n======== RESUMO DOS RESULTADOS ========")
print(f"Aceleração: {aceleracao:.4f} ± {incerteza_aceleracao:.4f} m/s²")
print(f"Coeficiente de determinação (R²): {r_s_t2**2:.4f}")
print("Velocidades médias (m/s):")
for i, v in enumerate(velocidades):
    print(f"  Distância {distancias[i+1]} cm: {v:.4f} ± {incertezas_velocidades[i]:.4f} m/s")