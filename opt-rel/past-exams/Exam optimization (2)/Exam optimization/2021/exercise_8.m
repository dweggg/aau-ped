
% Cl e a r memory and f i g u r e s
close all
clear 
clc
% Se t up c o s t c o e f f i c i e n t v e c t o r c
c =[-5;2;0;0;0];
% Se t up e q u a l i t y c o e f f i c i e n t matrix and v e c t o r
Ah=[0 0 0 0 0];
bh=[0] ;
% Se t up i n e q u a l i t y c o e f f i c i e n t matrix and v e c t o r
Ag=[-1 1 1 0 0; 0.5 1 0 1 0; -2 1 0 0 -1] ;
bg = [6; 10; 20];
% S e t ti n g upper and l ow e r bounds
lb = [0 0] ;
ub = [ inf inf ] ;
x0 = [0 0] ;
% S ol v e l i n e a r mi nimi z a ti o n problem
[x_opt fval]= linprog(c,Ag,bg,Ah,bh,lb,ub,x0)
