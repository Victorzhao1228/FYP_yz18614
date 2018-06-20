data

modelfun = @(b,pix_train)(b(1).*exp(-b(2).*pix_train)+ b(3).*exp(-b(4).*pix_train));
beta0 = [100;0.01;20;0.001];
beta = nlinfit(pix_train,dis_train,modelfun,beta0);
f = (beta(1).*exp(-beta(2).*pix_train)+ beta(3).*exp(-beta(4).*pix_train));

train_e = zeros(1000,1);
test_e = zeros(1000,1);
b = zeros(1,1000);



for j = 1:1:1000
    b(j) = 0 + j*0.0001;

    fx = beta(1).*exp(-b(j).*pix_train) + beta(3).*exp(-beta(4).*pix_train);
    error = abs(dis_train - fx);
    train_e(j) = mean(error);

    fx_t = beta(1).*exp(-b(j).*pix_test) + beta(3).*exp(-beta(4).*pix_test);
    error_t = abs(dis_test - fx_t);
    test_e(j) = mean(error_t);  
end

which_b2 = find(test_e == min(test_e));
final_b2 = b(:,which_b2);

beta(2) = final_b2;

%%
train_e1 = zeros(200,1);
test_e1 = zeros(200,1);
b = zeros(1,200);
b(1) = beta(1) - 5;

for j = 1:1:200

    fx = b(j).*exp(-beta(2).*pix_train) + beta(3).*exp(-beta(4).*pix_train);
    error = abs(dis_train - fx);
    train_e1(j) = mean(error);

    fx_t = b(j).*exp(-beta(2).*pix_test) + beta(3).*exp(-beta(4).*pix_test);
    error_t = abs(dis_test - fx_t);
    test_e1(j) = mean(error_t);  
    
    b(j+1) = b(1) + j*0.05;
end

which_b1 = find(test_e1 == min(test_e1));
final_b1 = b(:,which_b1);

beta(1) = final_b1;

%%

figure; hold on 
count = 1:1000;
plot(count, train_e, 'linewidth', 1.5);
plot(count, test_e, 'linewidth', 1.5);
grid on
xlabel('Number of Literation');
ylabel('Absolute distance error');
legend('Training error', 'Test error');
title('Training process with changing parameter');

figure; hold on
count = 1:200;
plot(count, train_e1, 'linewidth', 1.5);
plot(count, test_e1, 'linewidth', 1.5);
grid on
xlabel('Number of Literation');
ylabel('Absolute distance error');
legend('Training error', 'Test error');
title('Training process with changing parameter');

%%
for i = 1:size(size_car,1)
    variance(i) = var(size_car(i,:));
    std(i) = sqrt(variance(i));
    mean_car(i) = mean(size_car(i,:));
end

%% max, min of size of car at certain distance

mean_pre =  (beta(1).*exp(-beta(2).*mean_car)+ beta(3).*exp(-beta(4).*mean_car));
max_car = mean_car + 3.*std;
min_car = mean_car - 3.*std;

min_pre = (beta(1).*exp(-beta(2).*max_car)+ beta(3).*exp(-beta(4).*max_car));
max_pre = (beta(1).*exp(-beta(2).*min_car)+ beta(3).*exp(-beta(4).*min_car));

pre_range = [min_pre', mean_pre', max_pre'];

figure; hold on
plot(mean_car, max_pre, 'linewidth', 1.5);
plot(mean_car, mean_pre, 'linewidth', 1.5);
plot(mean_car, min_pre, 'linewidth', 1.5);
grid on;
legend('Maximum distance', 'Mean distance', 'Minimum distance');
title('Range of distance detection at certain size of car in pixel values');
xlabel('Size of car in pixel values');
ylabel('Distance of car');


%%

f_new = (beta(1).*exp(-beta(2).*pix_train)+ beta(3).*exp(-beta(4).*pix_train));
predict = (beta(1).*exp(-beta(2).*pix_test)+ beta(3).*exp(-beta(4).*pix_test));
error_final =  abs(dis_test - predict);
mean(error_final)
figure; hold on
plot(pix_train, dis_train, '.');
plot(pix_train, f, 'linewidth', 1.5);
e = errorbar(pix_test, predict, error_final);
e.Color = 'b';
e.LineWidth = 1;
grid on
xlabel('Car size in Pixel Value');
ylabel('Car distance/meter');
title('Nonlinear Regression Model for pixel size vs distance');

%%

figure;
plot(s(:,1), std, 'linewidth', 1.5);
grid on;
xlabel('Different distance');
ylabel('Standard deviations of size of car in pixel values');
title('Standard deviations against distance');
figure;
plot(s(:,1), mean_car, 'linewidth', 1.5);
grid on;
xlabel('Different distance');
ylabel('Mean of size of car in pixel values');
title('Mean against distance');


distance_mean = beta(1).* exp(-beta(2).*mean_car + beta(2)^2.*variance/2)+ beta(3).* exp(-beta(4).*mean_car + beta(4)^2.*variance/2);

distance_var = beta(1)^2.*(exp(2*-beta(2).*mean_car+beta(2)^2.*variance)).*(exp(beta(2)^2) - 1);


error_mean = abs(distance_mean' - s(:,1));
error_var = distance_var;

error_allmean = mean(error_mean);
error_allvar = mean(error_var);

dif_var = log((exp(error_allvar) - 1)/3);
dif_mean = log(3*exp(error_allmean)) + 0.5*(error_allvar - dif_var);

