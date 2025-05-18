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

# Definição das incertezas do tipo B
incerteza_B_distancia = 0.5/10  # 0.5 mm em cm (dividido por 10 para converter mm para cm)
incerteza_B_tempo = 0.00005  # em segundos

# Converter distâncias para metros (cm -> m)
distancias_m = [d/100 for d in distancias]
incerteza_B_distancia_m = incerteza_B_distancia/100  # Convertendo para metros

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

for i in range(len(distancias)):
    media = calcular_media(tempos[i])
    incerteza_A = calcular_desvio_padrao_media(tempos[i])
    incerteza_total = combinar_incertezas(incerteza_A, incerteza_B_tempo)
    
    medias_tempos.append(media)
    incertezas_A_tempos.append(incerteza_A)
    incertezas_totais_tempos.append(incerteza_total)

print("Médias dos tempos (s):", [round(t, 5) for t in medias_tempos])
print("Incertezas tipo A dos tempos (s):", [round(inc, 5) for inc in incertezas_A_tempos])
print("Incertezas tipo B dos tempos (s):", [round(incerteza_B_tempo, 5) for _ in range(len(distancias))])
print("Incertezas totais dos tempos (s):", [round(inc, 5) for inc in incertezas_totais_tempos])

# Calcular velocidade média para cada distância
velocidades = []
incertezas_A_velocidades = []
incertezas_totais_velocidades = []

for i in range(1, len(distancias)):
    delta_s = distancias_m[i] - distancias_m[0]  # Distância em relação ao ponto inicial
    delta_t = medias_tempos[i] - medias_tempos[0]  # Tempo em relação ao ponto inicial
    
    # Velocidade em m/s
    v = delta_s / delta_t
    
    # Cálculo da incerteza tipo A da velocidade usando propagação de erros
    incerteza_A_v = v * (incertezas_A_tempos[i] / delta_t)
    
    # Cálculo da incerteza total da velocidade considerando incertezas tipo A e B
    # Para a velocidade v = s/t, a incerteza propaga como:
    # σv/v = √[(σs/s)² + (σt/t)²]
    incerteza_relativa_s = incerteza_B_distancia_m / delta_s
    incerteza_relativa_t = incertezas_totais_tempos[i] / delta_t
    incerteza_relativa_v = sqrt(incerteza_relativa_s**2 + incerteza_relativa_t**2)
    incerteza_total_v = v * incerteza_relativa_v
    
    velocidades.append(v)
    incertezas_A_velocidades.append(incerteza_A_v)
    incertezas_totais_velocidades.append(incerteza_total_v)

print("\nVelocidades médias (m/s):")
for i, v in enumerate(velocidades):
    print(f"Distância {distancias[i+1]} cm:")
    print(f"  Valor: {v:.4f} m/s")
    print(f"  Incerteza tipo A: ±{incertezas_A_velocidades[i]:.4f} m/s")
    print(f"  Incerteza total (A+B): ±{incertezas_totais_velocidades[i]:.4f} m/s")

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
incerteza_A_aceleracao = 2 * s_b_s_t2

# Calculando a incerteza total da aceleração
# Considerando incerteza tipo B nas medições de distância
# Como a = 2 * (coef_angular), a incerteza propaga linearmente
incerteza_total_aceleracao = aceleracao * sqrt((incerteza_A_aceleracao/aceleracao)**2 + (incerteza_B_distancia_m/distancias_m[1])**2)

print(f"\nResultados do ajuste s vs t²:")
print(f"Equação: s = {a_s_t2:.4f} + {b_s_t2:.4f} * t²")
print(f"Coeficiente de correlação: {r_s_t2:.4f}")
print(f"Aceleração:")
print(f"  Valor: {aceleracao:.4f} m/s²")
print(f"  Incerteza tipo A: ±{incerteza_A_aceleracao:.4f} m/s²")
print(f"  Incerteza total (A+B): ±{incerteza_total_aceleracao:.4f} m/s²")

# Plotar o gráfico de s vs t
plt.figure(figsize=(10, 6))
plt.errorbar(medias_tempos[1:], distancias_m[1:], xerr=incertezas_totais_tempos[1:], yerr=[incerteza_B_distancia_m]*len(distancias_m[1:]), fmt='o', label='Dados experimentais')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição vs Tempo')
plt.grid(True)
plt.legend()

# Plotar o gráfico de s vs t²
plt.figure(figsize=(10, 6))
plt.errorbar(t_quadrado, distancias_m[1:], yerr=[incerteza_B_distancia_m]*len(distancias_m[1:]), fmt='o', label='Dados experimentais')
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
plt.savefig('grafico_s_vs_t2_com_incertezas.png')
print("\nGráficos gerados e salvos como 'grafico_s_vs_t2_com_incertezas.png'")

# Calcular velocidade instantânea para cada ponto (derivada da posição)
# Para um MRUV: v = v0 + a*t
# Se v0 = 0, então v = a*t

velocidades_instantaneas = [aceleracao * t for t in medias_tempos[1:]]
incertezas_A_vi = [sqrt((incerteza_A_aceleracao/aceleracao)**2 + (incertezas_A_tempos[i+1]/medias_tempos[i+1])**2) * velocidades_instantaneas[i] for i in range(len(velocidades_instantaneas))]
incertezas_totais_vi = [sqrt((incerteza_total_aceleracao/aceleracao)**2 + (incertezas_totais_tempos[i+1]/medias_tempos[i+1])**2) * velocidades_instantaneas[i] for i in range(len(velocidades_instantaneas))]

print("\nVelocidades instantâneas (m/s):")
for i, v in enumerate(velocidades_instantaneas):
    print(f"Tempo {medias_tempos[i+1]:.4f} s:")
    print(f"  Valor: {v:.4f} m/s")
    print(f"  Incerteza tipo A: ±{incertezas_A_vi[i]:.4f} m/s")
    print(f"  Incerteza total (A+B): ±{incertezas_totais_vi[i]:.4f} m/s")

# Análise estatística adicional
# Teste de consistência do modelo MRUV

# Calcular qui-quadrado (chi-squared)
qui_quadrado = sum(((distancias_m[i+1] - (a_s_t2 + b_s_t2 * medias_tempos[i+1]**2)) / (b_s_t2 * 2 * medias_tempos[i+1] * incertezas_totais_tempos[i+1]))**2 for i in range(len(distancias_m)-1))
graus_liberdade = len(distancias_m) - 1 - 2  # número de pontos - 1 - número de parâmetros ajustados

print(f"\nTeste de Qui-quadrado:")
print(f"χ² = {qui_quadrado:.4f}")
print(f"Graus de liberdade = {graus_liberdade}")
print(f"χ²/graus de liberdade = {qui_quadrado/graus_liberdade if graus_liberdade > 0 else 'N/A':.4f}")

# Resumo dos resultados
print("\n======== RESUMO DOS RESULTADOS ========")
print("Valores das grandezas físicas e suas incertezas:")
print(f"1. Aceleração:")
print(f"   Incerteza tipo A: ±{incerteza_A_aceleracao:.4f} m/s²")
print(f"   Incerteza tipo B (proveniente da medida de distância): ±{incerteza_B_distancia_m:.6f} m")
print(f"   Incerteza total (A+B): ±{incerteza_total_aceleracao:.4f} m/s²")
print(f"   Incerteza percentual: {100*incerteza_total_aceleracao/aceleracao:.2f}%")

print(f"\n2. Velocidades médias (m/s):")
for i, v in enumerate(velocidades):
    print(f"   Distância {distancias[i+1]} cm: {v:.4f} ± {incertezas_totais_velocidades[i]:.4f} m/s")
    print(f"   Incerteza percentual: {100*incertezas_totais_velocidades[i]/v:.2f}%")

print(f"\n3. Coeficiente de determinação (R²): {r_s_t2**2:.4f}")