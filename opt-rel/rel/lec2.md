# L2 Exercise

---

## An electronic component has a thermal-mechanical fatigue failure mechanism. The one life requirement is 7300 thermal cycles at the temperature variation ΔT = 43degC. It is known that the component can operate between -40degC and +85degC without causing catastrophic (instant) failure. The acceleration factor follows the Coffin Manson model, with the co-efficient m = 2.5 (based on guess estimate). The reliability of the electronic component related to the thermal-mechanical fatigue follows Weibull distribution with β = 1.8 (based on guess estimate)

1. What is the minimum thermal cycles we can apply to demonstrate one lifetime of the electronic component at accelerated testing?

$A_f = \left(\frac{\Delta T_t}{\Delta T_u}\right)^{m} =  \left(\frac{85-(-40)}{43}\right)^{2.5} = 14.4$
$n_t = \frac{n_u}{A_f} = \frac{7300}{14.4} = 507$

2. It requires to demonstrate reliability R=0.99 at 50% confidence level at the end of one life. If the Success-run test strategy is to be implemented, how many testing samples are required to test at the minimum thermal cycles calculated in Step 1?

$N = \frac{\ln{(1-C)}}{\ln{(R)}} = \frac{\ln{(1-0.5)}}{\ln{(0.99)}} = 69$

3. If the requirement is changed to reliability R=0.999 at 99% confidence level because the electronic component is to be used for a life-critical application, how many testing samples would be required to test at the minimum thermal cycles calculated in Step 1?

$N = \frac{\ln{(1-C)}}{\ln{(R)}} = \frac{\ln{(1-0.999)}}{\ln{(0.99)}} = 688$

4. If you only have 12 testing samples, how would you re-design the Success-run test to demonstrate reliability R=0.99 at 50% confidence level at the end of one life?
_We can revise the testing sample size using the following expression:_
$X_{new} = X_{old}\cdot\sqrt[\beta]{\frac{N_{old}}{N_{new}}} = 7300\cdot\sqrt[1.8]{\frac{688}{12}} = 69218$

5. If it is a newly developed electronic component, the coefficient m in the Coffin Manson model is not known, how would you design a Calibrated Accelerated Life Test (CALT) to find out the m value? Please illustrate by providing a testing example.



