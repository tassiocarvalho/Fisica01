% Algoritmo para calcular a propagação de incertezas para uma esfera

% Valores do diâmetro da esfera
diametro = 27.53;             % mm
incerteza_diametro = 0.18;    % mm

% Valores da massa da esfera
massa = 30.347;               % g
incerteza_massa = 0.007;      % g

fprintf('Dados de entrada:\n');
fprintf('Diâmetro: %.2f ± %.2f mm\n', diametro, incerteza_diametro);
fprintf('Massa: %.3f ± %.3f g\n', massa, incerteza_massa);

% Cálculo do raio e sua incerteza
raio = diametro / 2;
incerteza_raio = incerteza_diametro / 2;
fprintf('\nRaio: %.2f ± %.2f mm\n', raio, incerteza_raio);

% Cálculo do volume da esfera
% V = (4/3) * pi * r³
volume = (4/3) * pi * raio^3;

% Propagação de incerteza para o volume
% V = (4/3) * pi * r³
% dV/dr = 4 * pi * r²
derivada_volume_raio = 4 * pi * raio^2;
incerteza_volume = abs(derivada_volume_raio) * incerteza_raio;

% Exibir resultado do volume com incerteza
fprintf('\nVolume:\n');
fprintf('V = (4/3) * π * r³\n');
fprintf('dV/dr = 4 * π * r²\n');
fprintf('Volume = %.2f ± %.2f mm³\n', volume, incerteza_volume);

% Conversão para cm³
volume_cm3 = volume / 1000;  % 1000 mm³ = 1 cm³
incerteza_volume_cm3 = incerteza_volume / 1000;
fprintf('Volume = %.4f ± %.4f cm³\n', volume_cm3, incerteza_volume_cm3);

% Cálculo da densidade
% ρ = m/V
densidade = massa / volume_cm3;  % g/cm³

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

% Exibir resultado da densidade com incerteza
fprintf('\nDensidade:\n');
fprintf('ρ = m/V\n');
fprintf('dρ/dm = 1/V\n');
fprintf('dρ/dV = -m/V²\n');
fprintf('Densidade = %.4f ± %.4f g/cm³\n', densidade, incerteza_densidade);

% Cálculo da área superficial
% A = 4 * π * r²
area = 4 * pi * raio^2;

% Propagação de incerteza para a área
% A = 4 * π * r²
% dA/dr = 8 * π * r
derivada_area_raio = 8 * pi * raio;
incerteza_area = abs(derivada_area_raio) * incerteza_raio;

% Exibir resultado da área com incerteza
fprintf('\nÁrea Superficial:\n');
fprintf('A = 4 * π * r²\n');
fprintf('dA/dr = 8 * π * r\n');
fprintf('Área = %.2f ± %.2f mm²\n', area, incerteza_area);

% Resumo dos resultados
fprintf('\nResumo dos Resultados:\n');
fprintf('Raio: %.2f ± %.2f mm\n', raio, incerteza_raio);
fprintf('Volume: %.4f ± %.4f cm³\n', volume_cm3, incerteza_volume_cm3);
fprintf('Densidade: %.4f ± %.4f g/cm³\n', densidade, incerteza_densidade);
fprintf('Área Superficial: %.2f ± %.2f mm²\n', area, incerteza_area);

% Cálculo das incertezas relativas
incerteza_relativa_raio = (incerteza_raio / raio) * 100;
incerteza_relativa_volume = (incerteza_volume_cm3 / volume_cm3) * 100;
incerteza_relativa_densidade = (incerteza_densidade / densidade) * 100;
incerteza_relativa_area = (incerteza_area / area) * 100;

fprintf('\nIncertezas Relativas:\n');
fprintf('Raio: %.2f%%\n', incerteza_relativa_raio);
fprintf('Volume: %.2f%%\n', incerteza_relativa_volume);
fprintf('Densidade: %.2f%%\n', incerteza_relativa_densidade);
fprintf('Área Superficial: %.2f%%\n', incerteza_relativa_area);