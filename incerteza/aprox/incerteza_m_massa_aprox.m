% Algoritmo para calcular estatísticas e incertezas da massa da esfera em gramas
% Vetor com os valores da massa da esfera em gramas
vetor = [30.35 30.36 30.35 30.34 30.33 30.35 30.33 30.36 30.36 30.34];
% Cálculo da média do vetor
media_valor = mean(vetor);
% Cálculo da variância do vetor
variancia_valor = var(vetor);
% Cálculo do desvio padrão do vetor
desvio_padrao_valor = std(vetor);
% Exibir os resultados
fprintf('Análise da Massa da Esfera:\n');
fprintf('Vetor de massas (g): ');
fprintf('%.2f ', vetor);
fprintf('\n');
fprintf('Média: %.6f g\n', media_valor);
fprintf('Variância: %.6f g²\n', variancia_valor);
fprintf('Desvio Padrão: %.6f g\n', desvio_padrao_valor);
% Implementando manualmente os cálculos
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
fprintf('\nResultados calculados manualmente da massa da esfera:\n');
fprintf('Média: %.6f g\n', media_manual_valor);
fprintf('Variância: %.6f g²\n', variancia_manual_valor);
fprintf('Desvio Padrão: %.6f g\n', desvio_padrao_manual_valor);
% Cálculo da incerteza Tipo A (incerteza estatística)
% Baseada no desvio padrão da média
n = length(vetor);
incerteza_A = desvio_padrao_valor / sqrt(n);
fprintf('\nCálculo das Incertezas:\n');
fprintf('Incerteza Tipo A: %.6f g\n', incerteza_A);
% Cálculo da incerteza Tipo B (incerteza instrumental)
% Para uma distribuição retangular (uniforme), a incerteza é a precisão do instrumento dividida por raiz de 3
precisao_instrumento = 0.01; % g - considerando precisão de 0.01g para balança típica
incerteza_B = precisao_instrumento / sqrt(3);
fprintf('Incerteza Tipo B (instrumental): %.6f g\n', incerteza_B);
% Cálculo da incerteza combinada
% Usando a raiz quadrada da soma dos quadrados das incertezas
incerteza_combinada = sqrt(incerteza_A^2 + incerteza_B^2);
fprintf('Incerteza Combinada: %.6f g\n', incerteza_combinada);

% PARTE AJUSTADA - Aplicando regras de algarismos significativos
% -----------------------------------------------------------------

% Análise da incerteza para determinar o número de algarismos significativos
incerteza_str = sprintf('%.10f', incerteza_combinada);
incerteza_str = regexprep(incerteza_str, '^0\.|^\.', '');
incerteza_str = regexprep(incerteza_str, '^0+', '');
primeiro_digito = str2double(incerteza_str(1));

% Determina número de algarismos significativos baseado no primeiro dígito
if primeiro_digito == 1 || primeiro_digito == 2
    % Para 1 ou 2, manter 2 algarismos significativos
    num_sig_digitos = 2;
else
    % Para 3 ou maior, podemos usar 1 algarismo (mais conservador)
    num_sig_digitos = 1;
end

% Encontra a casa decimal para o último dígito significativo da incerteza
incerteza_full_str = sprintf('%.10f', incerteza_combinada);
idx_primeiro_nao_zero = find(incerteza_full_str ~= '0' & incerteza_full_str ~= '.', 1);
posicao_decimal = 0;
for i = idx_primeiro_nao_zero:length(incerteza_full_str)
    if incerteza_full_str(i) == '.'
        continue;
    end
    posicao_decimal = posicao_decimal + 1;
    if posicao_decimal == num_sig_digitos
        break;
    end
end

% Calcula número de casas decimais baseado na posição do ponto
casas_decimais = find(incerteza_full_str == '.', 1);
casas_decimais = i - casas_decimais;

% Arredonda a incerteza para o número correto de algarismos significativos
% Aplicando regras de arredondamento diretamente
valor_ajustado = incerteza_combinada * 10^casas_decimais;
parte_fracionaria = abs(valor_ajustado - floor(abs(valor_ajustado)));

% Aplicando as regras de arredondamento
if parte_fracionaria < 0.5
    % X000 a X499: arredonda para baixo
    incerteza_final = floor(valor_ajustado) / 10^casas_decimais;
elseif parte_fracionaria > 0.5
    % X501 a X999: arredonda para cima
    incerteza_final = ceil(valor_ajustado) / 10^casas_decimais;
else
    % Caso X500: arredonda para o valor par mais próximo
    inteiro = floor(valor_ajustado);
    if mod(inteiro, 2) == 0
        % Se o inteiro é par, mantém (arredonda para baixo)
        incerteza_final = inteiro / 10^casas_decimais;
    else
        % Se o inteiro é ímpar, soma 1 (arredonda para cima)
        incerteza_final = (inteiro + 1) / 10^casas_decimais;
    end
end

% Arredonda a média para ter o mesmo número de casas decimais que a incerteza
% Usando a mesma lógica de arredondamento
valor_ajustado = media_valor * 10^casas_decimais;
parte_fracionaria = abs(valor_ajustado - floor(abs(valor_ajustado)));

if parte_fracionaria < 0.5
    media_final = floor(valor_ajustado) / 10^casas_decimais;
elseif parte_fracionaria > 0.5
    media_final = ceil(valor_ajustado) / 10^casas_decimais;
else
    inteiro = floor(valor_ajustado);
    if mod(inteiro, 2) == 0
        media_final = inteiro / 10^casas_decimais;
    else
        media_final = (inteiro + 1) / 10^casas_decimais;
    end
end

% Apresentação do resultado final com incerteza formatada corretamente
fprintf('\nResultado Final Ajustado (conforme regras de algarismos significativos):\n');
formato = sprintf('%%.%df ± %%.%df g\n', casas_decimais, casas_decimais);
fprintf(formato, media_final, incerteza_final);