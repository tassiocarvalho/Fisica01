import matplotlib.pyplot as plt
import numpy as np

# Dados da Tabela 2
posicoes = [0.00, 0.16, 0.36, 0.56, 0.76]  # x(m)
incertezas_posicoes = [0.0005, 0.0005, 0.0005, 0.0005, 0.0005]  # δx(m)
tempos = [0.00000, 0.40573, 0.85200, 1.29230, 1.73005]  # t(s)
incertezas_tempos = [0.00005, 0.00536, 0.01104, 0.01647, 0.02179]  # δt(s)

# Criar o gráfico com barras de erro
plt.figure(figsize=(10, 6))

# Plotar os pontos experimentais com barras de erro
plt.errorbar(tempos, posicoes, xerr=incertezas_tempos, yerr=incertezas_posicoes, 
             fmt='o', markersize=8, color='blue', ecolor='red', capsize=5, 
             label='Dados experimentais')

# Ajustar uma curva teórica (para MRUV: x = (1/2)at²)
# Removendo o ponto t=0, x=0 para o ajuste (pode ser problemático)
t_para_ajuste = tempos[1:]
x_para_ajuste = posicoes[1:]

# Ajuste polinomial de grau 2 (parábola)
coefs = np.polyfit(t_para_ajuste, x_para_ajuste, 2)
a, b, c = coefs

# Criar uma função para a curva teórica
def curva_teorica(t, a, b, c):
    return a*t**2 + b*t + c

# Gerar pontos para a curva suave
t_curva = np.linspace(0, max(tempos)*1.05, 100)
x_curva = curva_teorica(t_curva, a, b, c)

# Plotar a curva teórica
plt.plot(t_curva, x_curva, 'r-', 
         label=f'Ajuste: x = {a:.4f}t² + {b:.4f}t + {c:.4f}')

# Calcular a aceleração
aceleracao = 2 * a
print(f"Aceleração calculada: {aceleracao:.4f} m/s²")

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