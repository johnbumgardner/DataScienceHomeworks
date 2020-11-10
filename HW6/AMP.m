%---------
% AMP.m
% Script for simulating AMP algorithm.
% Modified code by Yanting Ma.
% Dror Baron, 11.2.2016
%---------

%---------
% initialization
%---------
clear

% y = sqrt(gamma)*A*x + z
% solve for x given y,A
N = 2000; % length of signal
M = 500; % number of measurements
delta = M/N; % measurement rate
gamma=10; % SNR

% signal parameters
var_x=1;
epsilon = 0.1; % probability of nonzero signal

% AMP parameters
max_iter = 20; % number of AMP iterations
lambda=0.3; % damping parameter

%---------
% generate signal
%---------
x = zeros(0,N);
for i = 1:N
    val = rand();
    if val < (epsilon / 2)
        x(i) = -1;
    elseif (val > (epsilon / 2)) & (val < epsilon)
        x(i) = 1;
    
    else 
        x(i) = 0;
    end     
end

stem(1:200, x(1:200))

%---------
% matrix
%---------
A = 1/sqrt(M)*randn(M,N); % unit norm columns
AT = A';% transpose of A

mean(var(A))
mean(mean(A))
%---------
% measurements
%---------
% y = sqrt(gamma)*A*x + z
y = sqrt(gamma)*A.*x + randn(M,1);% measurements

% normalize differently with gamma
y=y/sqrt(gamma);


%---------
% AMP algorithm
%---------
% initialization
mse = zeros(max_iter,1); % store mean square error
xt = zeros(N,1);% estimate of signal
dt = zeros(N,1);% derivative of denoiser
rt = zeros(M,1);% residual

for iter = 1:max_iter
    % update residual
    rt = y - A*xt + 1/delta*mean(dt)*rt;
    % compute pseudo-data
    vt = xt + AT*rt;
    % estimate scalar channel noise variance; estimator is due to Montanari
    var_t = mean(rt.^2);
    % denoising
    [xt1,dt] = denoise(vt,var_x,var_t,epsilon);
    % damping step
    xt=lambda*xt1+(1-lambda)*xt;
    mse(iter) = (mean(xt-x).^2);
end

%% plot result
%figure;
plot(mse,'o-');
xlabel('Iteration')
ylabel('MSE')
fprintf('AMP error = %10.6f\n',min(mse));

return

%---------
% linear programming
%---------
% xhat = argmin ||x||_1 s.t. y=A*x
% take x=xpos-xneg
% xpos>=0, xneg>=0
% xhat=argmin xpos+xneg s.t. y=A*(xpos-xneg)
fprintf('solving ell1\n')
f=ones(2*N,1);
Aeq=[A -A];
beq=y;
lb=zeros(2*N,1); % lower bound zero
ub=ones(2*N,1)*inf; % upper bound is infinity
xsolve=linprog(f,[],[],Aeq,beq,lb,ub);
xp=xsolve(1:N);
xn=xsolve(N+1:2*N);
xell1=xp-xn;
fprintf('ell1 error = %10.6f\n',mean((xell1-x).^2))

% graphics
Nplot=100;
plot(1:Nplot,x(1:Nplot),'o',1:Nplot,xt(1:Nplot),'*',1:Nplot,xell1(1:Nplot),'+')
legend('x','AMP','ell1')


function [xhat,d]=denoise(v,var_x,var_z,epsilon);

term1 = (1-epsilon)*normpdf(v,0,sqrt(var_z));
term2 = epsilon*normpdf(v,0,sqrt(var_x+var_z));
xW=var_x/(var_x+var_z)*v; % Wiener filter
xhat=term2./(term1+term2).*xW; % denoised version, x(t+1)

% empirical derivative
Delta=1e-10; % perturbation
term1_d = (1-epsilon)*normpdf(v+Delta,0,sqrt(var_z));
term2_d = epsilon*normpdf(v+Delta,0,sqrt(var_x+var_z));
xW2=var_x/(var_x+var_z)*(v+Delta);% Wiener filter
xhat2=xW2.*term2_d./(term1_d+term2_d);
d=(xhat2-xhat)/Delta;
end