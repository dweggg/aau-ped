# PI tuning

We tried with 300Hz actual, we got 180Hz for tuning, then we got ~70% magnitude at 300Hz sinewave, which means parameters are close. At 280Hz sinewave we got 70% for real.

Then 400Hz, tuned to 213Hz and exactly 70%

Then 500Hz, tuned to 240Hz and spot on 70%

Empirical tuning to aim for 5% overshoot, Kp 1 Ki 315, bw 110Hz

# Resistance

id [Apk]	vd [Vpk]
0.5			3.4
1			5.4
1.5			6.7
2			7.3
2.5			7.8
3 			8.1
3.5 		8.4
4 			8.7
4.5 		8.9
5 			9.2
5.5 		9.4
6 			9.5

# Speed PI

We tuned to 30Hz and we got 36Hz BW

A lot of overshoot and then we remove Kp 
Friction so low that we have no SSE with step response 0 - 200 [RPM]

Then with some low load torque we get SSE

Tl[Nm]	SSE [RPM]
2 		6
4 		12
8  		22
10  	30

# CLFO

## PLL 
Kp 50 Ki 250 -23deg 10Nm 1000RPM
Kp 100 Ki 500 -18deg 10Nm 1000RPM
500RPM -2deg 0Nm SS
500RPM -6deg 10Nm SS
200RPM oscillating 0Nm SS
200RPM -7deg 10Nm SS

## V/f control
4Hz 4V/Hz

id = 20A, iq = 0A

Positive theta

## I/f contol
40Hz 10A
0Nm id 10A iq 0A
2Nm id 9.7A iq 2.5A
5Nm id 8A iq 6A
