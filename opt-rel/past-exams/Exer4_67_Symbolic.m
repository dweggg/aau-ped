% Optimization course, Aalborg University, by Erik Lund & Henrik Clemmensen
% Pedersen %ερωτηση 1,16,17
% Solution for Arora Exercise 4.67 ,%ex.1,16,17exam2022
%SOSOSOSOSSOS ΣΕ ΑΥΤΗ ΤΗΝ ΑΣΚΗΣΗ ΑΛΛΑΖΩ ΤΟ F ΚΑΙ ΤΟ L
% Symbolic expressions are used for setting up the KKT conditions.

% Clear variables, screen and figures
% 'clear all' clears everything but may decrease performance, so only 'clear' is used
clear; clc; close all;

% Initial guess for {x1, x2, u1, u2, s1, s2}^T:
x0 = [1 1 1 1 1 1]';
% Increase maximum number of function evaluations in fsolve
MyOptions=optimset('MaxFunEvals',1000);
% Solve the KKT conditions defined in function KKTSystem_Symbolic:
x = fsolve(@KKTSystem_Symbolic, x0, MyOptions)
% Write the value of the objective function
f = (2*x(1))^3 + x(2)^2 - 3*(x(1)-6) - 2*(x(2) + 3) + 4*x(1)*x(2) %οταν θα αλλαξω την εξισωση για f να εχω παρενθεσεις

% The function KKTSystem_Symbolic returns current values of the KKT system
function c = KKTSystem_Symbolic(x)
  % Input: x(1)=x1, x(2)=x2, x(3)=u1, x(4)=u2, x(5)=s1, and x(6)=s2
  % Output: the KKT system (gradients of Lagrangian L)

  % First define the symbolic variables used
  syms x1 x2 u1 u2 s1 s2 L KKT   %αν εχω παραπανω g εξισωσεις τοτε να ερθω εδω και να προσθεσω χ,υ και s
  % The symbolic expression for the Lagrangian L:
  L = ((2*x(1))^3 + x(2)^2 - 3*(x(1)-6) - 2*(x(2) + 3) + 4*x(1)*x(2)) + u1*(x(1) + x(2) -10 + s1^2) + u2*(x(1) -8 + s2^2); %after u we put our values for g
  dx1=diff(L,x1)
  dx2=diff(L,x2)  %αν εχω παραπανω g παλι να ερθω εδω για να προσθεσω τη διαφορα
  % Symbolic differentiation yields the 6 KKT conditions:
  KKT = [diff(L,x1);     %παλι αν εχω παραπανω  να ερθω να προσθεσω εδω
         diff(L,x2);
         diff(L,u1); 
         diff(L,u2); 
         diff(L,s1); 
         diff(L,s2)]; 
  % Compute the current numerical values of the gradient conditions
  % by substituting {x1,x2,u1,u2,s1,s2} in KKT with the vector x:
  c = double(subs(KKT, {x1,x2,u1,u2,s1,s2}, {x(1),x(2),x(3),x(4),x(5),x(6)}));
end

%ερωτηση 16:
%1)παιρνω dx1 και dx2 τα τελευταια 2 ( εξισωσεις μεγαλες)
%2)παιρνω οπως ειναι τις εξισωσεις g1,g2 με τις ανισοτητες τους και παλι
%τικαρω ακομα 2 απαντησεις
%3)u1*g1, u2*g2 αλλα αυτα να ισουνται με 0
%4) υ >= του 0 ΠΑΝΤΑ!!!!!

%ερωτηση 17:
%1)παιρνω χ1 και χ2 απο το script στο command window και αν κανω τα
%κλασματα που ηδη εχω διαιρεση θα μου βγαλουν αυτα τα νουμερα
%2)τα επομενα δυο νουμερα (δηλαδη 3ο και 4ο ) απο το χ στο command window
%ειναι για το u1 και u2 
%3) βαζω τα χ1 και χ2 που βρηκα απο το command window στις αρχικες μου g
%εξισωσεις κανω πραξεις και ετσι βγανουν οι τιμες για το g1 και g2.

%ερωτηση 1
% ιδια ιαδικασια εξαρταται απο το τι σε ρωταει η ασκηση 
