data

f = fit(pix_train, dis_train, 'poly5');

plot(f, pix_train, dis_train);
title('distance/m against size in pixel values');
xlabel('Car size in pixel velues/number of pixels');
ylabel('Real world distance/m');
grid on;

pre = f.a.* exp(f.b.*pix_train);
error = abs(dis_train - pre);

mean(error)

pre = f.a.* exp(f.b.*pix_test);
error_t = abs(dis_test - pre);

mean(error_t)


