clear all;
%load('project1_data.mat')
N=1e5; % number of coins
p=0.13; % prevalence
x=(rand(N,1)<p); % see explanation in text below
% printouts about properties of x
fprintf('Min(x) = %1d\n',min(x)); % prints 0
fprintf('Max(x) = %1d\n',max(x)); % prints 1
fprintf('Sum(x) = %6d\n',sum(x)); % prints number close to 1000
fprintf('Number ones = %6d\n',sum(x==1));
fprintf('Number zeros= %6d\n',sum(x==0));
%divide into B patches
B = [5,10,20,40,50,100,200];
number_of_patches(length(B)) = 0;

%Find theoretical probability of a batch needing to be tested
probabilities(length(B)) = 0;
for i = 1:length(probabilities)
   probabilities(i) = 1 - ((1-p)^B(i)); 
end

for b = 1:length(B)
    number_of_patches(b) = N/B(b);
end
first(:, : ) = reshape(x, B(1), number_of_patches(1));
second(:, : ) = reshape(x, B(2), number_of_patches(2));
third(:, : ) = reshape(x, B(3), number_of_patches(3));
forth(:, : ) = reshape(x, B(4), number_of_patches(4));
fifth(:, : ) = reshape(x, B(5), number_of_patches(5));
sixth(:, : ) = reshape(x, B(6), number_of_patches(6));
seventh(:,: ) = reshape(x, B(7), number_of_patches(7));
problems_in_first = any(first);
problems_in_second = any(second);
problems_in_third = any(third);
problems_in_forth = any(forth);
problems_in_fifth = any(fifth);
problems_in_sixth = any(sixth);
problems_in_seventh = any(seventh);
faulty_batches_1 = sum(problems_in_first);
faulty_batches_2 = sum(problems_in_second);
faulty_batches_3 = sum(problems_in_third);
faulty_batches_4 = sum(problems_in_forth);
faulty_batches_5 = sum(problems_in_fifth);
faulty_batches_6 = sum(problems_in_sixth);
faulty_batches_7 = sum(problems_in_seventh);
M2(b) = 0;
M2(1) = faulty_batches_1 * B(1);
M2(2) = faulty_batches_2 * B(2);
M2(3) = faulty_batches_3 * B(3);
M2(4) = faulty_batches_4 * B(4);
M2(5) = faulty_batches_5 * B(5);
M2(6) = faulty_batches_6 * B(6);
M2(7) = faulty_batches_7 * B(7);
M1(b) = 0;

numerical_prob(b) = 0;
numerical_prob(1) = faulty_batches_1 / number_of_patches(1);
numerical_prob(2) = faulty_batches_2 / number_of_patches(2);
numerical_prob(3) = faulty_batches_3 / number_of_patches(3);
numerical_prob(4) = faulty_batches_4 / number_of_patches(4);
numerical_prob(5) = faulty_batches_5 / number_of_patches(5);
numerical_prob(6) = faulty_batches_6 / number_of_patches(6);
numerical_prob(7) = faulty_batches_7 / number_of_patches(7);

for n = 1:b
    M1(n)=number_of_patches(n);
end
M3 = M1 +M2;
figure(1);
plot(B,M1,'*-',B,M2,'o-',B,M3,'+-');
xlabel('Batch size B');
ylabel('Number of measurements');
legend('M1','M2','Total');
title('Measurements Req')

figure(2);
plot(B,probabilities,'*-',B,numerical_prob,'o-');
xlabel('Batch size B');
ylabel('Probability of batch positivity');
legend('Theory','Simulated');
title('Probability of Positive Batches')

%part 2 Nonadaptive test

% go from 25 - 36
for n = 25:36
    fprintf("id = %d: ", n);
    non_adaptive(n) 
end

%nicholas number
non_adaptive(74)
%john number
non_adaptive(20)


function non_adaptive(id)
    load('project1_data.mat')
    y=squeeze(y_all(id,:)); % squeeze returns length-15 vector
    A=squeeze(A_all(id,:,:)); % returns 15x30 matrix
    A_list=squeeze(A_list_all(id,:,:)); % returns 30x3 matrix
    pool = ones(1,30);
    for n = 1:length(y)
        if y(n) == 0
            for m = 1:30
                if A(n,m) == 1
                    pool(m) = 0;
                end
            end
        end
    end
    fprintf('Special Indexes: ');
    for i = 1:30
        if pool(i) == 1
            fprintf('%d ',i);
        end
    end
    fprintf('\n');

end
