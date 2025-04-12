% Dados fornecidos
numerosUnicos = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
frequencias = [6, 7, 14, 22, 21, 18, 24, 15, 13, 7, 5];
total = sum(frequencias); % Total = 152

% Criar vetor com todos os dados (para cálculos estatísticos)
dados = [];
for i = 1:length(numerosUnicos)
    dados = [dados, repmat(numerosUnicos(i), 1, frequencias(i))];
end

% Calcular média e desvio padrão
media = mean(dados);
desvioPadrao = std(dados);

% Configurar figura
figure('Position', [100, 100, 1000, 600]);

% Plotar histograma
h = histogram(dados, 'BinEdges', [1.5:1:12.5], 'Normalization', 'count');
hold on;

% Configurar eixos e títulos
xlabel('Valor');
ylabel('Frequência');
title('Histograma com Ajuste Gaussiano', 'FontSize', 14);
grid on;

% Definir os centros dos bins do histograma
centrosBins = numerosUnicos;
binWidth = 1;  % Largura do bin do histograma

% Calcular a curva gaussiana nos centros dos bins
yGaussBins = total * binWidth * (1/(desvioPadrao*sqrt(2*pi))) * exp(-(centrosBins-media).^2 / (2*desvioPadrao^2));

% Plotar pontos da gaussiana nos centros dos bins
plot(centrosBins, yGaussBins, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');

% Para visualização da curva contínua, criar também uma versão suavizada
x = linspace(min(numerosUnicos)-1, max(numerosUnicos)+1, 1000);
yGauss = total * binWidth * (1/(desvioPadrao*sqrt(2*pi))) * exp(-(x-media).^2 / (2*desvioPadrao^2));

% Plotar curva gaussiana contínua
plot(x, yGauss, 'r-', 'LineWidth', 2);

% Calcular o R² (coeficiente de determinação)
% Primeiramente, obter os valores observados e preditos nos pontos centrais do histograma
pontosX = numerosUnicos;
pontosYObs = frequencias;

% Calcular valores previstos pela gaussiana nos pontos centrais
pontosYPred = total * binWidth * (1/(desvioPadrao*sqrt(2*pi))) * exp(-(pontosX-media).^2 / (2*desvioPadrao^2));

% Calcular R²
SSres = sum((pontosYObs - pontosYPred).^2);
SStot = sum((pontosYObs - mean(pontosYObs)).^2);
R2 = 1 - (SSres / SStot);

% Adicionar texto com informações estatísticas
infoText = sprintf('Média = %.2f\nDesvio Padrão = %.2f\nR² = %.4f', media, desvioPadrao, R2);
text(max(numerosUnicos)-2, max(frequencias)*0.9, infoText, 'BackgroundColor', [0.9 0.9 0.9], 'EdgeColor', 'k', 'FontSize', 12);

% Adicionar legenda
legend('Histograma', 'Valores Gaussianos nos Bins', 'Distribuição Gaussiana Contínua');

% Exibir resultados no console também
fprintf('Estatísticas:\n');
fprintf('Média = %.2f\n', media);
fprintf('Desvio Padrão = %.2f\n', desvioPadrao);
fprintf('R² = %.4f\n', R2);

% Salvar figura como imagem
saveas(gcf, 'histograma_gaussiano.png');