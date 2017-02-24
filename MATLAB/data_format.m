clear
load('data2.mat')

%get training data
train_vecs = [train_vecsMAGA; train_vecsNMP];
train_labels = ones(4000, 1);
train_labels(1:2000, 1) = -1;

%randomize training data
rand('seed', 1);
inds = randperm(size(train_vecs, 1));
train_vecs = train_vecs(inds, :);
train_labels = train_labels(inds, :);

%get test data
test_vecsMAGA = test_vecsMAGA(1:3000,:);
test_vecsNMP = test_vecsNMP(1:3000,:);
test_vecs = [test_vecsMAGA; test_vecsNMP];
test_labels = ones(6000, 1);
test_labels(1:3000, 1) = -1;