x = [15, 35, 51, 60, 73, 86, 86, 90, 110, 127, 132, 142, 103];
y = [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20];

figure; hold on

plot(x, y, '*');
xlabel('Pixel Values/number of pixels', 'fontsize', 16);
ylabel('Real world distance/m' ,'fontsize', 16);
title('Distance against pixel value in IPM images', 'fontsize', 16);

f = fit(x',y', 'poly1')
pre = x.*f.p1 + f.p2;

error = abs(y - pre);

mean (error)
plot(x, pre);

var(error);
