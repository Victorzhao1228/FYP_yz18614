clear all

train = load('train.txt');
dis_train = train(:,1);
pix_train = train(:,2);

test = load('test.txt');
dis_test = test(:,1);
pix_test = test(:,2);

dis_train_1 = (dis_train - min(dis_train))./(max(dis_train) - min(dis_train));
dis_train_2 = (dis_train - mean(dis_train))./sqrt(var(dis_train));

s= load('size.txt');
size_car = s(:,2:end);
