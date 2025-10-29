clc;
clear;
close all;


R5 = 10;       
adc_res = 10;  
adc_max = 2^adc_res - 1;


data1 = csvread('ntc.csv');
T = data1(:, 1);               
R = data1(:, 2);    


ad = adc_max* (R ./ (R5 + R));


figure;
plot(ad, T, 'bo-');
grid on;

hold on;
p = polyfit(ad, T, 10); 


ad2 = 0:adc_max;             
T2 = round(polyval(p, ad2), 1);

plot(ad2, T2, 'r');
grid on;

dlmwrite('data.dlm', T2 * 10, ',');

