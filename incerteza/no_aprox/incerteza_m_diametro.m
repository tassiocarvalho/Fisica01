% Algoritmo para calcular média, desvio padrão e variância de um vetor com 10 elementos

% Vetor com os valores fornecidos
vetor = [27.3 28.5 27.7 27.0 27.0 27.2 27.7 28.4 27.5 27.0];

% Cálculo da média do vetor
media_valor = mean(vetor);

% Cálculo da variância do vetor
variancia_valor = var(vetor);

% Cálculo do desvio padrão do vetor
desvio_padrao_valor = std(vetor);

% Exibir os resultados
fprintf('Vetor: ');
fprintf('%d ', vetor);
fprintf('\n');
fprintf('Média: %.2f\n', media_valor);
fprintf('Variância: %.6f\n', variancia_valor);
fprintf('Desvio Padrão: %.6f\n', desvio_padrao_valor);

% Alternativa: implementando manualmente os cálculos
% Cálculo manual da média
soma = 0;
for i = 1:length(vetor)
    soma = soma + vetor(i);
end
media_manual_valor = soma / length(vetor);

% Cálculo manual da variância
soma_quadrados = 0;
for i = 1:length(vetor)
    soma_quadrados = soma_quadrados + (vetor(i) - media_manual_valor)^2;
end
variancia_manual_valor = soma_quadrados / length(vetor);

% Cálculo manual do desvio padrão
desvio_padrao_manual_valor = sqrt(variancia_manual_valor);

% Exibir os resultados calculados manualmente
fprintf('\nResultados calculados manualmente do diametro:\n');
fprintf('Média: %.2f\n', media_manual_valor);
fprintf('Variância: %.6f\n', variancia_manual_valor);
fprintf('Desvio Padrão: %.6f\n', desvio_padrao_manual_valor);

% Cálculo da incerteza Tipo A (incerteza estatística)
% Baseada no desvio padrão da média
n = length(vetor);
incerteza_A = desvio_padrao_valor / sqrt(n);
fprintf('\nCálculo das Incertezas:\n');
fprintf('Incerteza Tipo A: %.6f mm\n', incerteza_A);

% Cálculo da incerteza Tipo B (incerteza instrumental)
% Para uma distribuição retangular (uniforme), a incerteza é a precisão do instrumento dividida por raiz de 3
precisao_instrumento = 0.05; % mm - menor divisão do instrumento
incerteza_B = precisao_instrumento / sqrt(3);
fprintf('Incerteza Tipo B (instrumental): %.6f mm\n', incerteza_B);

% Cálculo da incerteza combinada
% Usando a raiz quadrada da soma dos quadrados das incertezas
incerteza_combinada = sqrt(incerteza_A^2 + incerteza_B^2);
fprintf('Incerteza Combinada: %.6f mm\n', incerteza_combinada);


% Apresentação do resultado final com incerteza
fprintf('\nResultado Final: %.5f ± %.5f mm\n', media_valor, incerteza_combinada);