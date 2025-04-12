% Código para plotar o gráfico de incertezas relativas
% Dados das incertezas relativas (em %)
grandezas = {'Raio', 'Volume', 'Densidade', 'Área Superficial'};
incertezas_relativas = [0.65, 1.83, 1.80, 1.26];

% Criação do gráfico de barras
figure('Position', [100, 100, 800, 500]); % Define o tamanho da figura
bar(incertezas_relativas, 'FaceColor', [0.3, 0.6, 0.9]);

% Adiciona rótulos e título
set(gca, 'XTick', 1:length(grandezas), 'XTickLabel', grandezas);
set(gca, 'FontSize', 12);
ylabel('Incerteza Relativa (%)', 'FontSize', 14);
title('Incertezas Relativas das Grandezas Medidas e Calculadas', 'FontSize', 16);
grid on;
box on;

% Adiciona os valores específicos acima de cada barra
text_offset = 0.05; % Ajusta a posição vertical do texto
for i = 1:length(incertezas_relativas)
    text(i, incertezas_relativas(i) + text_offset, [num2str(incertezas_relativas(i), '%.2f') '%'], ...
        'HorizontalAlignment', 'center', 'FontSize', 12);
end

% Ajusta os limites do eixo Y para melhor visualização
current_ylim = ylim;
ylim([0, current_ylim(2) * 1.2]); % Adiciona 20% de espaço acima da barra mais alta

% Salva a figura como imagem
print('-dpng', 'incertezas_relativas.png', '-r300');

% Exibe mensagem de confirmação
disp('Gráfico de incertezas relativas gerado e salvo como "incertezas_relativas.png"');