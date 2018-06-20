pixvalue = [1177 950 915 776 655 572 524 484 444 414 368 352 337 293 280 254 225 215 189 179 172];
distance = [2.1 2.5 2.9 3.4 3.9 4.5 5.5 6.1 6.6 7.5 8.4 9.4 10.4 11.2 12.2 13.2 14.2 15.2 15.9 16.9];

figure;
plot(pixvalue, distance, '*');
hold on;
f = fit(pixvalue', distance','exp2');

error = zeros(21,1);
fx = zeros(21,1);
for i = 1:size(pixvalue,2)
    fx(i) = f.a*exp(f.b*pixvalue(i)) + f.c*exp(f.d*pixvalue(i));
    error(i) = abs(distance(i) - fx(i));
end
err = mean(abs(error));
plot(f,pixvalue',distance');
errorbar(pixvalue, distance, error);
ylabel('Distance/m');
xlabel('Car Size');
title('Distance Against Car Size');

%%
far_pix = [48 46 43 43 41 41];
far_distance =  [64.81 68.08 71.35 74.62 77.89 81.15]; 

figure;
plot(far_pix, far_distance, '*');
hold on;
f2 = fit(far_pix', far_distance','exp2');
error_2 = zeros(6,1);
fx_2 = zeros(6,1);
for i = 1:size(far_pix,2)
    fx_2(i) = f2.a*exp(f2.b*far_pix(i)) + f2.c*exp(f2.d*far_pix(i));
    error_2(i) = abs(far_distance(i) - fx_2(i));
end
err_far = mean(abs(error_2));
plot(f2,far_pix',far_distance');
errorbar(far_pix, far_distance, error_2);
ylabel('Distance/m');
xlabel('Car Size');
title('Distance Against Car Size');
