clear all;
load('project1_data.mat')
N=1e5; % number of coins
p=0.001; % prevalence
x=(rand(N,1)<p); % see explanation in text below
% printouts about properties of x
fprintf('Min(x) = %1d\n',min(x)); % prints 0
fprintf('Max(x) = %1d\n',max(x)); % prints 1
fprintf('Sum(x) = %6d\n',sum(x)); % prints number close to 1000
fprintf('Number ones = %6d\n',sum(x==1));
fprintf('Number zeros= %6d\n',sum(x==0));
%divide into B patches
B = [5,10,20,40];
number_of_patches(length(B)) = 0;
for b = 1:length(B)
number_of_patches(b) = N/B(b);
end
first(:, : ) = reshape(x, B(1), number_of_patches(1));
second(:, : ) = reshape(x, B(2), number_of_patches(2));
third(:, : ) = reshape(x, B(3), number_of_patches(3));
forth(:, : ) = reshape(x, B(4), number_of_patches(4));
problems_in_first = any(first);
problems_in_second = any(second);
problems_in_third = any(third);
problems_in_forth = any(forth);
faulty_batches_1 = sum(problems_in_first);
faulty_batches_2 = sum(problems_in_second);
faulty_batches_3 = sum(problems_in_third);
faulty_batches_4 = sum(problems_in_forth);
M2(b) = 0;
M2(1) = faulty_batches_1 * B(1);
M2(2) = faulty_batches_2 * B(2);
M2(3) = faulty_batches_3 * B(3);
M2(4) = faulty_batches_4 * B(4);
M1(b) = 0;
for n = 1:b
M1(n)=number_of_patches(n);
end
M3 = M1 +M2;
plot(B,M1,'*-',B,M2,'o-',B,M3,'+-');
xlabel('Batch size B');
ylabel('Number of measurements');
legend('M1','M2','Total');
%part 2
id=20; %my student id number is 2
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
fprintf('Special Indexs: ');
for i = 1:30
if pool(i) == 1
fprintf('%d ',i);
end
end
fprintf('\n');