%OPTIMIZATION 
%%CA - LECTURE 1 - DETERMINE THE OPTIMUM SOLUTION TO THE PROBLEM USING GRAPHICAL
%METHOD FOR ANY EQUATION
    clear; clc; close all;

%GRID %***CHANGE THIS ACCORDINGLY
    [x1,x2] = meshgrid(-5:0.5:5.0, -5:0.5:5.0);     

% PROBLEM DESCRIPTION %***CHANGE THIS BASED ON PROBLEM

%REMEMBER USE THESE OPERATORS ".*", "./", ".^"  
%CHANGE THIS SECTION
    P = (x1+3).^2+(-x2+2).^2;  %function
    g1 = -x1+x2-3;
    g2 = x1+1;  
    %g3 = ....; 
    %g4 = ....;
    %g5 =...;
    
%DIPLAY X - AXIS
    x_axis=x1;
    y_axis=x2;
    

%GRAPH SET UP
    cla reset  % Initialization statements; these do not need to end by a semicolon
    axis auto  % Minimum and maximum values for axes are determined automatically
               % Limits for x- and y-axes may also be specified with the command
                %axis ([xmin xmax ymin ymax])
    
    
    % Specifies labels for x- and y-axes
    xlabel('x_1 - Number of A machines'), ylabel('x_2 - Number of B machines')          
    title ('Profit maximization problem') % Display a title for the problem
    hold on    % Retains the current plot and axes properties for all subsequent plots

%PLOT CONSTRAIN FUNCTION %***CHANGE THIS (ELIMINATE OR ADD BASED ON
    %CONSTRAIN AND CHANGE POSITION OF THE TEXT
    % Use the "contour" command to plot cost and constraint functions
    cv1 = [0 0];                                       
    const1 = contour(x1,x2,g1,cv1,'r', 'linewidth',2);
    const2 = contour(x1,x2,g2,cv1,'g', 'linewidth',2);  
    %const3 = contour(x1,x2,g3,cv1,'y', 'linewidth',2);
    %const4 = contour(x1,x2,g4,cv1,'b', 'linewidth',2);  
    %const5 = contour(x1,x2,g5,cv1,'v', 'linewidth',2);   
    
%PLOT X AND Y AXIS
    constX1 = contour(x1,x2,x_axis,cv1,'k', 'linewidth',1);
    constX2 = contour(x1,x2,y_axis,cv1,'k', 'linewidth',1);  
    
%COUNTOURS GRAPH FOR FUNCTION
    fv = [0.01,0.5,1, 2,3, 4, 5, 6,7, 8];                %***CHANGE THIS % % Contour levels
    [fs, fh] = contour(x1,x2,P,fv,'r');                 % 'r' specifies red lines for profit function contours
    clabel(fs, fh)                                      % Automatically puts the contour value on the graph

%MANUALLY IMPUT POSITION OF THE OPTIMUL 
    % %***CHANGE THIS - AFTER YOU WORK OUT THE OPTIMUM
    a=-2; %x1
    b=1;  %x2
    
    Optimal_Values=[a b]

%PLOT OPTIMUM    
    plot(a,b,'bo','linewidth',2) ;

% Finally, we plot the constraint functions minus a small number in order
% to indicate the feasible domain clearly on the plot - add shadings
    contour(x1,x2,g1-0.2,cv1,'Color',[.8 .8 .8], 'linewidth',3);  % Plots g1-0.25 in order to indicate feasible space
    contour(x1,x2,g2-0.2,cv1,'Color',[.8 .8 .8], 'linewidth',3);  % Plots g2-0.015 in order to indicate feasible space
    %contour(x1,x2,g3-0.2,cv1,'Color',[.8 .8 .8], 'linewidth',3);  % Plots g3-0.015 in order to indicate feasible space
    %contour(x1,x2,g4-0.2,cv1,'Color',[.8 .8 .8], 'linewidth',3);  % Plots g4-0.2 in order to indicate feasible space
    %contour(x1,x2,g5-0.2,cv1,'Color',[.8 .8 .8], 'linewidth',3);  % Plots g5-0.2 in order to indicate feasible space

%RE-PLOT OPTIMUM
    plot(a,b,'bo','linewidth',2); 

% Add legends to the plot
legend('g_1(x)','g_2(x)','x_1- axis', 'x_2- axis', 'f(x)', 'Optimum','AutoUpdate','off'); 

hold off                             % Indicates end of this plotting sequence
                                     % Subsequent plots will appear in separate windows
%% CA - LECTURE 5 EXAMPLE1 CONVERT TO LINEAR OPTIMISATION LP FORM - FIND x,b,C,A
%Also called STANDARD LINEAR PROBLEM DEFINITION
clc,clear all 

syms x1 x2

%PROBLEM FORMULATION ***Change this 
    %Function
    f=-5*x1+2*x2;   

    %s.t. Subject to the following constrains ***Change this 
    g1=-x1+x2; %g1 <=6
    b1=6;

    g2=x1/2+x2; %g2<=10
    b2=10;

    g3=-(-2*x1+x2); %g3<=20 --> this was changed from -2*x1+x2>=-20 you change sign both ways
    b3=20;

%STEP 1 - ELIMINATE UNRESTRICTED VARIABLE - NOT REQUIRED HERE
    %x3 is free sign == unrestricted variable, introduce 2 more variables x4 x5:
    %x3=x4-x5; %where x4>=0 and x5>=0
    % syms x4 x5
    % f=subs(f,x3,x4-x5); %sub in function f, x3, with x4-x5
    % g1=subs(g1,x3,x4-x5);
    % g2=subs(g2,x3,x4-x5);
    %now all xk>=0;

%STEP 2 introducing surplus variables x6 x7 x8
    syms x6 x7 x8
    %the surplus variable are used to convert inequality to equality constrain
    %***Change this maybe - based on how many g you have
    g1=g1+x6; 
    g2=g2+x7;
    g3=g3+x8;

%STEP 3 convert to matrix form f(x)=c'*x s.t. A*x=b all x>=0
     x=[x1 x2 x6 x7 x8] %***Change this maybe
     b=[b1;b2;b3]       %***Change this maybe
     c=equationsToMatrix(f,x)'
     A1=equationsToMatrix(g1,x);
     A2=equationsToMatrix(g2,x);
     A3=equationsToMatrix(g3,x);

     A=[A1;A2;A3]       %***Change this maybe
     
 %continue with the exel
                                     
%% C(x) MATRIX SOLVER - Find Hessian H(x) and C(x)- non linear
clc, clear all, close all
%Set unknown
syms x1 x2

%Function
    %f=3*(x1)^2+2*(x1)*(x2)+2*(x2)^2+7
    f=(x1-x2)^2 + (x1-2)^2 +7
    
%Differentiations
a=diff(f,x1);  %df_dx1
b=diff(f,x2);  %df_dx2

c=diff(a,x1);   %2f_d2x1
d=diff(b,x2);   %d2f_d2x2

e=diff(a,x2);   %d2f_d2x1x2
f=diff(b,x1);   %d2f_d2x2x1


% Find c(x)
c_x=[a;b];

% Find H(x)
H_x=[c e;f d];

%Display
c_x

H_x

%Eigen Values
lambda=eig(H_x);
Lamb1=lambda(1,1)
Lamb2=lambda(2,1)                                     
                                     %% Gradient and hessian vector
clc, clear all
syms x1 x2 x3 x4

    % cost function
f=2*x1^2+2*x2^2-5*x1*x2;
    % initial values
x1_initial=1;
x2_initial=1;
% x3_initial=
% x4_initial=
initial_point=[x1_initial; x2_initial];
    % vector direction
%d=[0.1; -0.1]
   % target point 
x1_new=1.2;
x2_new=0.8;
new_point=[x1_new; x2_new]
d=new_point-initial_point
dT=transpose(d)
   
cT=gradient(f) % defined as array (1xn) = already transposed
cT_initial=vpa(subs(cT,[x1,x2],[x1_initial x2_initial]))%substitute from symbolic to numeric
H=hessian(f)
H_initial=subs(H,[x1,x2],[x1_initial x2_initial]) %substitute from symbolic to numeric
%eigen_values=eig(H_initial)
%if the eigen values have different signs A is indefinite, the gradient of the quadratic
%function gradF=A*x or H = A;
%if both are positive -> H(xp)=0 ; xp=local minimum
%if both are negative -> xp= local maximum
%if H(x) does not depend on variables -> constant -> global minimum/maximum
f_initial=subs(f,[x1,x2],[x1_initial, x2_initial]);
taylor_approx=f_initial+dot(cT_initial,d)+0.5*(dT*H_initial)*d;
f_approx=vpa(taylor_approx) %convert a fraction into number
f_exact=vpa(subs(f,[x1,x2],[x1_new, x2_new]))
error=(abs(subs(f,[x1,x2],[x1_new,x2_new])-taylor_approx)/subs(f,[x1,x2],[x1_new,x2_new]))
%% Lagrangian with inequality constrains exercise 6.67
clear, clc, close all
syms u1 u2 v s1 s2 x1 x2 x3 x4 x5 x6

    %objective function
    f=(x1+1)^2+(-x2+1)^2;
%     %inequality constrain function
    g1=x1+0.5*x2-2;
    g2=1-x1;

% definition of lagragian ec. L=f+v*h+u*(g+s^2)
 L=f+u1*(g1+s1^2)+u2*(g2+s2^2);
 %this expression prints out what to put in the Lagragian iteration solver
 %function. 
 % REMEMBER TO CHANGE x1...xN to x(1)...x(n)
subs(gradient(L, [x1, x2, u1, u2, s1, s2]),[x1, x2, u1, u2, s1, s2],[x1 x2 x3 x4 x5 x6])
%% example 10.2
clc, clear, close all 
syms x1 x2 alpha
f=3*x1^2+2*x1*x2+2*x2^2+7;
c=gradient(f,[x1 x2]);
c_initial=subs(c,[x1 x2],[1 2]);
d=[-1,-1];
necessary_condition=dot(c_initial,d);
%its negative, meaning its a decreasing direction
f_x=subs(f,[x1 x2],[1 2]);
x_initial=[1 2];
x_k1=x_initial+alpha*d;
f_k1=expand(subs(f,[x1 x2],[x_k1(1) x_k1(2)])); %line search f(alpha)
step_size=solve(diff(f_k1,alpha),alpha);
x_k1=subs(x_k1,alpha,step_size)

%% example 10.4
clc, clear all
syms x1 x2 alpha
f=x1^2+x2^2-2*x1*x2;
x_initial=[1 0];
k=0;
epsilon=0.0001;
c=gradient(f,[x1 x2]);
c_k=subs(c,[x1 x2],[x_initial(1:2)]);
%lenght of the gradient = norm 
%chec
if norm(c_k)>epsilon
disp('continue');
d=-c_k;
x_k1=x_initial+alpha*d';
%update f(alpha)
f_k1=expand(subs(f,[x1 x2],x_k1(1:2)));
step_size=solve(diff(f_k1,alpha),alpha);
diff(diff(f_k1)); %curvature check >0
else    disp('stop');
end
x_k1=subs(x_k1,alpha,step_size);
c_k1=subs(c,[x1 x2],x_k1(1:2));
d_k1=-c_k1

%% 10.4
clc, clear all, close all
syms x1 x2 x3
f=x1^2+2*x2^2+2*x3^2+2*x1*x2+2*x2*x3;
c=gradient(f,[x1 x2 x3]);
c_x0=subs(c,[x1 x2 x3],[1 2 3]);
d=[-3 10 -12];
nec_condition=dot(c_x0,d);
%% 10.22
clc, clear all, close all
syms x1 x2 x3 alpha
f=(x1-2)^2+(x2-1)^2;
x0=[4 4];
d=[-4 -6];
x_k1=x0+alpha*d;
f_alpha=expand(subs(f,[x1 x2],[x_k1]));
f_grad_alpha=gradient(f_alpha);
alpha_opt=solve(f_grad_alpha,alpha);
x_k1=subs(x_k1,alpha,alpha_opt)
f_x0=subs(f,[x1 x2],x0)
f_xk1=subs(f,[x1 x2],x_k1)


%% 10.32
%Using equal interval search increase alpha by d=0.05 until the function
%doesnt increase any more
clc, clear all, close all
syms x1 x2 x3 alpha
f_alpha=52*alpha^2 - 52*alpha + 13; %saved in function exercise10_32
d=0.05;
alpha0=0;
f_alpha_k0=subs(f_alpha,alpha,alpha0);
alpha_k1=alpha0+d;
i=1;
%f_alpha_k1=exercise10_32(alpha)
f_alpha_k1=subs(f_alpha,alpha,alpha_k1);
while f_alpha_k0>f_alpha_k1
f_alpha_k0=f_alpha_k1;
alpha_k1=alpha_k1+d;
f_alpha_k1=subs(f_alpha,alpha,alpha_k1);
i=i+1;
end
lower_bound=f_alpha_k0;
upper_bound=f_alpha_k1;
lower_alpha=alpha_k1-2*d
upper_alpha=alpha_k1
i
%% 10.42 golden section method
clc, clear all, close all
syms x1 x2 x3 alpha
%f_alpha_ex=52*alpha^2 - 52*alpha + 13; %saved in function exercise10_32
d=0.05;
alpha0=0;
epsilonGS = 0.001; % Convergence criteria in golden section (GS) search
nMaxGSIter = 100;  % Maximum number of iterations to use in golden section search
% with an arrow in next line we can run everythin untill then
% that allows us to step in and check how the loops updates in the Golden
% section function
% in the lin 77 defines the interval with a__u and u_l, placing the mouse
% over those we can check the values
[alpha, f_alpha] = GoldenSection(@exercise10_32, d, epsilonGS, nMaxGSIter)

%% 10.52 steepest method    di=-ci
clc, clear all, close all 
format short g
syms x1 x2 alpha
f_x=(x1-x2)^2+(x1-2)^2+7;
x0=[-1 1];
c=gradient(f_x,[x1 x2]);
c0=subs(c,[x1 x2],[x0]);
check0=norm(c0); % STOP SEARCHING CRITERIA: since its not zero (>epsilon), the vectors length >0; then x0 its not minimum point
%steepest means going perpendicular to the slope
%remember that two vectors with oposite signs are perpendicular¿?¿?¿?¿?
d0=-c0;
xk1=x0+alpha*d0';
f_alpha=expand(subs(f_x,[x1 x2],xk1));
%optimal alpha
alpha_opt=solve(diff(f_alpha,alpha));
epsilon=0.001;
d=0.05;
[alpha_0,f_alpha_0]=GoldenSection(@exercise10_52,d,epsilon,1000);
alpha_0=round(alpha_0*10^2)/10^2;
xk1=subs(xk1,alpha,alpha_0);
c1=subs(c,[x1 x2],[xk1]);
check1=norm(c1); % continue until norm(c)=0 or <epsilon

d1=-c1;
xk2=xk1+alpha*d1';
f_alpha2=expand(subs(f_x,[x1 x2],xk2))
alpha_opt1=solve(diff(f_alpha2,alpha));
xk2=subs(xk2,alpha,alpha_opt1);
f_xk2=subs(f_x,[x1 x2],xk2);

%% example 10.6 of conjugate method lecture 4
clc
syms x1 x2 x3 alpha
f=x1^2+2*x2^2+2*x3^2+2*x1*x2+2*x2*x3;
x0=[2 4 10];
    % first step C(x0) same as steepest
c=gradient(f,[x1 x2 x3]);
c0=subs(c,[x1 x2 x3],[x0]);
% check lenght of c is greater than epsilon for notstopping criteria
l_c0=norm(c0); % 63.6>epsilon, dont stop the music
d0=-c0'; %remember to convert from vector to array
xk1=x0+alpha*d0;
f_alpha=subs(f,[x1 x2 x3],xk1);
alpha0=solve(diff(f_alpha),alpha);
xk1=double(subs(xk1,alpha,alpha0));
    % second step gradient and cost at xk1
c1=double(subs(c,[x1 x2 x3],xk1));
f1=double(subs(f,[x1 x2 x3], xk1));
l_c1=norm(c1); %check its greater than epsilon, otherwise stop
beta1=double((norm(c1)/norm(c0))^2);
d1=double(-c1'+beta1*d0);%remember to transpose c from vector to array
xk2=xk1+alpha*d1;
alpha1=double(solve(diff(subs(f,[x1 x2 x3],xk2))));
xk2=double(subs(xk2,alpha,alpha1));
f2=double(subs(f,[x1 x2 x3],xk2));
    %third step, next iteration
c2=double(subs(c,[x1 x2 x3],xk2));
l_c2=norm(c2);% 


%% 10.68 conjugate method exercise lecture 4   
% d(k)=-c(k)+b(k)*d(k-1) where b=beta= ( norm(c(k)) / norm(c(k-1)) )^2
clc
syms x1 x2 
f=x1^2+2*x2^2-4*x1-2*x1*x2;
x0=[1 1];
% complete two iterations

    % first step C(x0) same as steepest
c=gradient(f,[x1 x2]);
c0=subs(c,[x1 x2],[x0]);
% check lenght of c is greater than epsilon for notstopping criteria
l_c0=norm(c0); % 63.6>epsilon, dont stop the music
d0=-c0'; %remember to convert from vector to array
xk1=x0+alpha*d0;
f_alpha=subs(f,[x1 x2],xk1);
alpha0=solve(diff(f_alpha),alpha);
xk1=double(subs(xk1,alpha,alpha0));
 % second step gradient and cost at xk1
c1=double(subs(c,[x1 x2],xk1));
f1=double(subs(f,[x1 x2], xk1));
l_c1=norm(c1); %check its greater than epsilon, otherwise stop
beta1=double((norm(c1)/norm(c0))^2);
d1=double(-c1'+beta1*d0);%remember to transpose c from vector to array
xk2=xk1+alpha*d1;
alpha1=double(solve(diff(subs(f,[x1 x2],xk2))));
xk2=double(subs(xk2,alpha,alpha1));
f2=double(subs(f,[x1 x2],xk2));
    %third step, next iteration
c2=double(subs(c,[x1 x2],xk2));
l_c2=norm(c2);
%% example 11.6 modified newtons method
clc, syms x1 x2 alpha
f=3*x1^2+2*x1*x2+2*x2^2+7; x0=[5 10]; epsilon=0.0001;
 %step 1 just defining x0
    x0;
 %step 2 c0
 c=gradient(f,[x1 x2]);
 c0=double(subs(c,[x1 x2],x0));
 l_c0=norm(c0)>epsilon;
 %step 3 H
 H=hessian(f,[x1 x2]);
 eigen=(eig(H)>=0);
 %step 4 d
 d0=-H^(-1)*c0;
%step 5 alpha
 xk1=x0+alpha*d0'; %remember to transpose d'
 f_alpha=subs(f,[x1 x2],xk1);
 alpha0=solve(diff(f_alpha));
 xk1=subs(xk1,alpha,alpha0);
 c1=subs(c,[x1 x2],xk1);
 l_c1=(norm(c1)>epsilon);

 %% 11.10 MODIFIED NEWTONS
 % complete one iteration
 clc, syms x1 x2 alpha
 f=(x1-x2)^2+(x1-2)^2 + 7; 
 %step one its just setting:
 x0=[-1 1]; k=0; epsilon=0.001;
 %step two c0
 c=gradient(f,[x1 x2]);
 c0=double(subs(c,[x1 x2],x0));
 l_c0=norm(c0)>epsilon;
 %step three H
 H=hessian(f,[x1 x2]);
 eigen=eig(H)>=0;
 %step four H^-1, d0 and descent condition
 H_inv=H^-1;
 d0=-H^-1*c0;
 descent_check=0>dot(c0,d0);
%step five xk1
xk1=x0+alpha*d0'; %remember to transpose d
f_alpha=subs(f,[x1 x2],xk1);
alpha0=solve(diff(f_alpha));
xk1=subs(xk1,alpha,alpha0);
%step six = step two k=k+1
c1=double(subs(c,[x1 x2],xk1));
l_c1=norm(c1)>0; %norm is 0 means we converged
xk1
%% 11.22 two iterations of DFP METHOD
clc, syms x1 x2 alpha
f=x1^2+2*x2^2-4*x1-2*x1*x2; 
%step 1 k=0
x0=[1 1]; epsilon=0.001;
A0=eye(2,2);
c=gradient(f,[x1 x2]);
c0=double(subs(c,[x1 x2],x0));
%step 2 convergency check
l_c=norm(c0)>epsilon;
%step 3 d0
d0=-A0*c0;
%step 4 alpha0
xk1=x0+alpha*d0';%remember to transpose d
f_alpha=subs(f,[x1 x2],xk1);
alpha0=solve(diff(f_alpha));
%step 5 xk1
xk1=subs(xk1,alpha,alpha0);
%step 6 c1 s0 y0 z0 correctional matrices (B0 C0) --- A1
c1=subs(c,[x1 x2],xk1);
s0=alpha0*d0; %change in design
y0=c1-c0;  %change in gradient
z0=A0*y0; %the gradient of the next point
B0=(s0*s0')/(dot(s0,y0)); %Correctional matrix
C0=double((-z0*z0')/dot(y0,z0)); %Correctional matrix
A1=double(A0+B0+C0);
    %step 7 == 1.1 k=k+1
c1=subs(c,[x1 x2],xk1);
    %step 8 == 2.1
l_c1=double(norm(c1))>epsilon;
    %step 9 == 3.1
d1=-A1*c1;
    %step 10 ==  4.1
xk2=xk1+alpha*d1';
f_alpha=subs(f,[x1 x2],xk2);
alpha1=solve(diff(f_alpha));
    %step 11 == 5.1
xk2=subs(xk2,alpha,alpha1);
    %step 12 == 6.1
c2=subs(c,[x1 x2],xk2);
s1=alpha1*d1;
y1=c2-c1;
z1=A1*y1;

B1=(s1*s1')/dot(s1,y1);
C1=(-z1*z1')/dot(y1,z1);

A2=A1+B1+C1;

%% OPTIMIZATION SECOND PART HENRIK
%% LECTURE 5 EXAMPLE1 CONVERT TO LINEAR OPTIMISATION LP FORM
clc, syms x1 x2 x3
f=5*x1+4*x2-x3;
%s.t.
g1=x1+2*x2-x3; %g1 >=1
b1=1;

g2=2*x1+x2+x3; %g2>=4
b2=4;

%x1>=0 ; x2>=0; 

    %STEP 1 eliminating unrestricted variables
%x3 is free sign == unrestricted variable, introduce 2 more variables x4 x5:
%x3=x4-x5; %where x4>=0 and x5>=0
syms x4 x5
f=subs(f,x3,x4-x5); %sub in function f, x3, with x4-x5
g1=subs(g1,x3,x4-x5);
g2=subs(g2,x3,x4-x5);
%now all xk>=0;

    %STEP 2 introducing surplus variables x6 x7
syms x6 x7
%the surplus variable are used to convert inequality to equality constrain
%positive if g1<=1 ; but negative since >=1
g1=g1-x6;
%positive if g2<=4 ; but negative since >=4
g2=g2-x7;
% all xk>=0;

    %STEP 3 convert to matrix form f(x)=c'*x s.t. A*x=b all x>=0
 x=[x1 x2 x4 x5 x6 x7]
 b=[b1;b2]
 c=equationsToMatrix(f,x)'
 A1=equationsToMatrix(g1,x);
 A2=equationsToMatrix(g2,x);
 
 A=[A1;A2]
 
 %% LECTURE 5 EXAMPLE 2: Simplex method
 clc, clear all
 
 syms x1 x2
 
 f_x=2*x1-x2; %CHANGE THIS
 
 g1=-x1+2*x2; %<=10 %CHANGE THIS
 g2=3*x1+2*x2; %<=18 %CHANGE THIS
 
 b1=10; %CHANGE THIS
 b2=18; %CHANGE THIS
 
 %STEP 1 eliminating unrestricted variables
 %We don't have it
 % x1 and x2 >=0
    %STEP 2 SURPLUS VARIABLES X3 X4 for inequality constrain
syms x3 x4 
g1=g1+x3; %CHANGE THE SIGN OF THIS IF G1<= IS + , IF G1>= THEN -
g2=g2+x4; %CHANGE THE SIGN OF THIS IF G2<= IS + , IF G2>= THEN -
%all x >=0
x=[x1 x2 x3 x4]; %CHANGE IF YOU HAVE OTHER VARIABLES
c=equationsToMatrix(f_x,x)
A1=equationsToMatrix(g1,x); % A*x=b
A2=equationsToMatrix(g2,x);


    %tableau
    syms cf BV1 BV2 b
tab0=[x1 x2 x3 x4 b];
tab1=[A1,b1];
tab2=[A2,b2];
tab3=[c,cf];
tab=[tab0;tab1;tab2;tab3] 

%NOW COPY AND PASTE TO EXCEL

%Paste , paste option, text import wizard, fixed width
%clean up table with find and replace , [ ] for nothing
%% LECTURE 5 EXERCISE 8.4 LINEAR OPTIMISATION FORM
clc, syms x1 x2
f=2*x1-3*x2;
g1=x1+x2; %inequality <=1
b1=1;
g2=-2*x1+x2; %inequality >=2
b2=2;
 %step 1 unrestricted variables - none
 %step 2 inequality to equality
 syms x3 x4 b
g1=g1+x3;
g2=g2-x4;
%all x>=0

    %step 3 equation to matrix
x=[x1 x2 x3 x4];
c=equationsToMatrix(f,x);
A1=equationsToMatrix(g1,x); % A*x=b
A2=equationsToMatrix(g2,x);
    %tableau
    syms cf
tab0=[x1 x2 x3 x4 b];
tab1=[A1,b1];
tab2=[A2,b2];
tab3=[c,cf];
tab=[tab0;tab1;tab2;tab3];
%% LECTURE 5 EXERCISE 8.38 LINEAR OPTIMISATION PROBLEM FORM + MINIMUM POINT
clc, syms x1 x2
f=-x1+x2;
g1=2*x1+x2;% ≤ 4
b1=4;
g2=-x1-2*x2;% ≥ −4
b2=-4;
% x1 x2>=0;
    %STEP 1 check minimizing sign & unrestricted values: none
    %STEP 2 inequality to equality
        % IMPORTANT if >= then -x
        % if =-b change sign of g after adding surplus value
                    %and change sign of b
syms x3 x4
if b1>0 g1=g1+x3;
else, g1=-(g1+x3); b1=-b1;
end

if b2>0 g2=g2-x4; %SINCE g2>=b2 -X4
else, g2=-(g2-x4); b2=-b2;
end
g1;
g2;
    %STEP 3 equation2matrix
x=[x1 x2 x3 x4];
c=equationsToMatrix(f,x);
A1=equationsToMatrix(g1,x); % A*x=b
A2=equationsToMatrix(g2,x);
    %tableau
syms cf
tab0=[x1 x2 x3 x4 b];
tab1=[A1,b1];
tab2=[A2,b2];
tab3=[c,cf];
tab=[tab0;tab1;tab2;tab3];

%% LECTURE 5 LINEAR OPTIMISATION PROBLEM (LP) FORM AND MINIMIZE
clc, syms x1 x2
%maximize
f = x1 + x2;
g1=4*x1 + 3*x2; %≤ 
b1=9;
g2=x1 + 2*x2;% ≤ 
b2=6;
g3=2*x1 + x2;% ≤ 
b3=6;
%x1 ≥ 0
%x2 ≥ 0
%STEP 1 check minimize sign & unrestricted values: none 
f=-f;
%STEP 2 inequality to equality
        % IMPORTANT if >= then -x
        % if =-b change sign of g after adding surplus value
                    %and change sign of b
syms x3 x4 x5
if b1>0 g1=g1+x3;
else, g1=-(g1+x3); b1=-b1;
end

if b2>0 g2=g2+x4;
else, g2=-(g2+x4); b2=-b2;
end

if b3>0 g3=g3+x5;
else, g3=-(g3+x5); b3=-b3;
end
g1;
g2;
g3;
    %STEP 3 equation2matrix
x=[x1 x2 x3 x4 x5];
c=equationsToMatrix(f,x);
A1=equationsToMatrix(g1,x); % A*x=b
A2=equationsToMatrix(g2,x);
A3=equationsToMatrix(g3,x);

    %tableau
syms cf

tab0=[x1 x2 x3 x4 x5 b];
tab1=[A1,b1];
tab2=[A2,b2];
tab3=[A3,b3];
tab4=[c,cf];
tab=[tab0;tab1;tab2;tab3;tab4]

%% LECTURE6 EXAMPLE 1
clc, syms x1 x2 
f=(x1-1)^2+(x2-1)^2;
g1=x1+x2-4; %<=
g2=2-x1; %<=0;
 % STEP 1 lagrangian L=f+v*h+u*g
 syms u1 u2
 L=f+u1*g1+u2*g2;

 % STEP 2 GRADIENT CONDITION
 grad_L=gradient(L,[x1 x2]);

 % STEP 3 feasibility check
 H_f=hessian(L,[x1 x2]); % without L.M.
 %since ¿?¿? positive - isolated minimum point
 
%% Langrangian iteration solver 
clc, clear, close all
x0=[1 1 1 1 1 1];
MyOptions=optimset('MaxFunEvals', 1000)
x=fsolve(@KKKSystem,x0,MyOptions)
function c=KKKSystem(x)
c(1)=2*(x(1)-1)+x(3)-x(4);
c(2)=2*(x(2)-1)+x(3);
c(3)=x(1)+x(2)-4+x(5)^2;
c(4)=2-x(1)+x(6)^2;
c(5)=2*x(3)*x(5);
c(6)=2*x(4)*x(6);
end
%%
function f=exercise10_32(alpha)
f=52*alpha^2 - 52*alpha + 13;
end
%%
function f=exercise10_52(alpha)
f=40*alpha^2 - 20*alpha - 3;
end