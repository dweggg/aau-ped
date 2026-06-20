clear all;
clc;

syms x1 x2
F(x1,x2) = -2*x1^3 + 6*x1^2 +3*(x2 -2)^2 
g1(x1,x2) = 2*x1 - 3*x2 + 2;
g2(x1,x2) = x1 + x2 -8;
x0 = [0 0]';
d0 = [-2 10]';
t0 = 1;
x10 = x0 + t0*d0
R0 = 1;
u=[0 2]';
gama = 0.5;
g = [g1;g2];
f0 = F(x0(1),x0(2));
g10 = g1(x0(1),x0(2));
g20 = g2(x0(1),x0(2));

c = gradient(F);
v0 = max(max(0,g(x0(1),x0(2))));
R = sum(u);
phi_0 = f0 + R*v0
f10 = F(x10(1),x10(2));
v10 = max(max(0,g(x10(1),x10(2))));
phi_10 = f10 + R*v10

b0=gama*(d0(1)^2+d0(2)^2);

t1 = 1/2;
x11 = x0 + t1*d0
f11 = F(x11(1),x11(2));
v11 = max(max(0,g(x11(1),x11(2))));
phi_11=f11 + R*v11
Df1=phi_0-t1*b0

%phi_11 < Df1 so we stop here!! no need to do for t2!!

% t2=1/4;
% x12 = x0 + t2*d0
% f12 = F(x12(1),x12(2));
% v12 = max(g(x12(1),x12(2)));
% phi_12=f12 + R*v12
% Df2=phi_0-t2*b0