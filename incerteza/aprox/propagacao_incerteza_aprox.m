% Algoritmo para calcular a propagação de incertezas para uma esfera
% Valores do diâmetro da esfera
diametro = 27.53; % mm
incerteza_diametro = 0.18; % mm
% Valores da massa da esfera
massa = 30.347; % g
incerteza_massa = 0.007; % g
fprintf('Dados de entrada:\n');
fprintf('Diâmetro: %.2f ± %.2f mm\n', diametro, incerteza_diametro);
fprintf('Massa: %.3f ± %.3f g\n', massa, incerteza_massa);

% Cálculo do raio e sua incerteza
raio = diametro / 2;
incerteza_raio = incerteza_diametro / 2;

% Aplicando regras de algarismos significativos ao raio
% A incerteza do raio determina as casas decimais do valor do raio
% Como a incerteza do diâmetro é 0.18, a do raio é 0.09, mantendo 2 casas decimais
raio_final = round(raio * 100) / 100;
incerteza_raio_final = round(incerteza_raio * 100) / 100;
fprintf('\nRaio: %.2f ± %.2f mm\n', raio_final, incerteza_raio_final);

% Cálculo do volume da esfera
% V = (4/3) * pi * r³
volume = (4/3) * pi * raio^3;

% Propagação de incerteza para o volume
% V = (4/3) * pi * r³
% dV/dr = 4 * pi * r²
derivada_volume_raio = 4 * pi * raio^2;
incerteza_volume = abs(derivada_volume_raio) * incerteza_raio;

% Aplicando regras de algarismos significativos ao volume
% Determinando o número de algarismos significativos baseado na incerteza
incerteza_volume_str = sprintf('%.10f', incerteza_volume);
primeiro_digito_volume = regexp(incerteza_volume_str, '[1-9]', 'once');
primeiro_valor_volume = str2double(incerteza_volume_str(primeiro_digito_volume));

% Determinando casas decimais para o volume
if primeiro_valor_volume == 1 || primeiro_valor_volume == 2
    % Para incertezas que começam com 1 ou 2, mantém 2 algarismos significativos
    casas_volume = ceil(log10(volume/incerteza_volume)) + 1;
else
    % Para incertezas que começam com 3-9, mantém 1 algarismo significativo
    casas_volume = ceil(log10(volume/incerteza_volume));
end
fator_volume = 10^(floor(log10(incerteza_volume)));
volume_final = round(volume / fator_volume) * fator_volume;
incerteza_volume_final = round(incerteza_volume / fator_volume) * fator_volume;

% Exibir resultado do volume com incerteza
fprintf('\nVolume:\n');
fprintf('V = (4/3) * π * r³\n');
fprintf('dV/dr = 4 * π * r²\n');
fprintf('Volume = %.1f ± %.1f mm³\n', volume_final, incerteza_volume_final);

% Conversão para cm³
volume_cm3 = volume / 1000; % 1000 mm³ = 1 cm³
incerteza_volume_cm3 = incerteza_volume / 1000;

% Aplicando regras para volume em cm³
fator_volume_cm3 = 10^(floor(log10(incerteza_volume_cm3)));
volume_cm3_final = round(volume_cm3 / fator_volume_cm3) * fator_volume_cm3;
incerteza_volume_cm3_final = round(incerteza_volume_cm3 / fator_volume_cm3) * fator_volume_cm3;

% Determinando o número de casas decimais
casas_decimais_volume_cm3 = max(0, -floor(log10(fator_volume_cm3)));
formato_volume_cm3 = sprintf('%%.%df ± %%.%df cm³\n', casas_decimais_volume_cm3, casas_decimais_volume_cm3);
fprintf('Volume = ');
fprintf(formato_volume_cm3, volume_cm3_final, incerteza_volume_cm3_final);

% Cálculo da densidade
% ρ = m/V
densidade = massa / volume_cm3; % g/cm³

% Propagação de incerteza para a densidade
% ρ = m/V
% dρ/dm = 1/V
% dρ/dV = -m/V²
derivada_densidade_massa = 1 / volume_cm3;
derivada_densidade_volume = -massa / (volume_cm3^2);

% Aplicação da fórmula de propagação de incertezas
% σρ = √[(dρ/dm)² * σm² + (dρ/dV)² * σV²]
incerteza_densidade = sqrt((derivada_densidade_massa * incerteza_massa)^2 + ...
 (derivada_densidade_volume * incerteza_volume_cm3)^2);

% Aplicando regras para densidade
incerteza_densidade_str = sprintf('%.10f', incerteza_densidade);
primeiro_digito_densidade = regexp(incerteza_densidade_str, '[1-9]', 'once');
primeiro_valor_densidade = str2double(incerteza_densidade_str(primeiro_digito_densidade));

% Determinando fator de arredondamento para densidade
if primeiro_valor_densidade == 1 || primeiro_valor_densidade == 2
    casas_densidade = 2; % 2 algarismos significativos na incerteza
else
    casas_densidade = 1; % 1 algarismo significativo na incerteza
end

% Encontrando a casa decimal apropriada
posicao_decimal = strfind(incerteza_densidade_str, '.');
casas_decimais_densidade = casas_densidade + primeiro_digito_densidade - posicao_decimal - 1;
fator_densidade = 10^(-casas_decimais_densidade);

densidade_final = round(densidade / fator_densidade) * fator_densidade;
incerteza_densidade_final = round(incerteza_densidade / fator_densidade) * fator_densidade;

% Exibir resultado da densidade com incerteza
fprintf('\nDensidade:\n');
fprintf('ρ = m/V\n');
fprintf('dρ/dm = 1/V\n');
fprintf('dρ/dV = -m/V²\n');
formato_densidade = sprintf('%%.%df ± %%.%df g/cm³\n', casas_decimais_densidade, casas_decimais_densidade);
fprintf('Densidade = ');
fprintf(formato_densidade, densidade_final, incerteza_densidade_final);

% Cálculo da área superficial
% A = 4 * π * r²
area = 4 * pi * raio^2;

% Propagação de incerteza para a área
% A = 4 * π * r²
% dA/dr = 8 * π * r
derivada_area_raio = 8 * pi * raio;
incerteza_area = abs(derivada_area_raio) * incerteza_raio;

% Aplicando regras para área
incerteza_area_str = sprintf('%.10f', incerteza_area);
primeiro_digito_area = regexp(incerteza_area_str, '[1-9]', 'once');
primeiro_valor_area = str2double(incerteza_area_str(primeiro_digito_area));

% Determinando fator de arredondamento para área
if primeiro_valor_area == 1 || primeiro_valor_area == 2
    casas_area = 2; % 2 algarismos significativos na incerteza
else
    casas_area = 1; % 1 algarismo significativo na incerteza
end

% Encontrando o fator de arredondamento para área
fator_area = 10^(floor(log10(incerteza_area)));
area_final = round(area / fator_area) * fator_area;
incerteza_area_final = round(incerteza_area / fator_area) * fator_area;

% Exibir resultado da área com incerteza
fprintf('\nÁrea Superficial:\n');
fprintf('A = 4 * π * r²\n');
fprintf('dA/dr = 8 * π * r\n');
fprintf('Área = %.0f ± %.0f mm²\n', area_final, incerteza_area_final);

% Resumo dos resultados
fprintf('\nResumo dos Resultados (com algarismos significativos corretos):\n');
fprintf('Raio: %.2f ± %.2f mm\n', raio_final, incerteza_raio_final);
fprintf('Volume: ');
fprintf(formato_volume_cm3, volume_cm3_final, incerteza_volume_cm3_final);
fprintf('Densidade: ');
fprintf(formato_densidade, densidade_final, incerteza_densidade_final);
fprintf('Área Superficial: %.0f ± %.0f mm²\n', area_final, incerteza_area_final);

% Cálculo das incertezas relativas
incerteza_relativa_raio = (incerteza_raio_final / raio_final) * 100;
incerteza_relativa_volume = (incerteza_volume_cm3_final / volume_cm3_final) * 100;
incerteza_relativa_densidade = (incerteza_densidade_final / densidade_final) * 100;
incerteza_relativa_area = (incerteza_area_final / area_final) * 100;

fprintf('\nIncertezas Relativas:\n');
fprintf('Raio: %.2f%%\n', incerteza_relativa_raio);
fprintf('Volume: %.2f%%\n', incerteza_relativa_volume);
fprintf('Densidade: %.2f%%\n', incerteza_relativa_densidade);
fprintf('Área Superficial: %.2f%%\n', incerteza_relativa_area);