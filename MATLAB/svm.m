load('data2_ready.mat')

num_features = [20, 50, 100, 200, 300, 500, 1000, 1500, 2000, 2500, 3000, 3382];
accuracy = zeros(1,12);

for n = 1:12
    %size down data
    num = num_features(n);
    
    %reduce with svd
    %train_vec1 = reduce(train_vecs, num);
    %test_vec1 = reduce(test_vecs, num);
    
    %simple reduce:
    train_vec1 = train_vecs(:, 1:num);
    test_vec1 = test_vecs(:, 1:num);
    
    %train svm
    svm_model = fitclinear(train_vec1, train_labels);

    %cvsvm_model = crossval(svm_model);
    %classloss = kfoldLoss(cvsvm_model);
    %[labels_predict, scores] = kfoldPredict(cvsvm_model);

    [labels_predict, scores] = predict(svm_model, test_vec1);

    %get accuracy
    num_correct = 0;
    total = size(labels_predict, 1);
    
    for i=1:total
        if(labels_predict(i) == test_labels(i))
            num_correct = num_correct + 1;
        end
    end
    accuracy(1,n) = num_correct/total;
    
end

plot(num_features, accuracy)
title('Features vs Accuracy')
xlabel('Number of Features')
ylabel('Accuracy')

%get most positive and most negative scores and indices
% [sorted1, indices1] = sort(scores(:,1), 'descend');
% top_maga_i = indices1(1:5);
% 
% [sorted2, indices2] = sort(scores(:,2), 'descend');
% top_nmp_i = indices2(1:5);