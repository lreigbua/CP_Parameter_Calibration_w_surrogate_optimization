# Damask_CP_parameters_calibration_w_surrogate_optimization

## Introduction

This code automatically calibrates Crystal Plasticity parameters by fitting an experimental stress-strain curve of the material to model. To do so, Damask simulations are combined with a matlab code that uses surrogate optimization (https://es.mathworks.com/discovery/surrogate-optimization.html).

Matlab's surrogate optimization will try different combination of CP parameters to develop a surrogate function that mimics the behavior of the stress-strain curve and can be derived mathematically. This surrogate function is much faster to minimize since it can be derived mathematically. By finding the minima of the surrogate function, it can make a guess of the CP parameters that minimize the difference between the simulated stress-strain and the experimental one. With further guesses, the surrogate function will become more accurate and will eventually find a combination of CP parameters that matches well the experimental stress-strain curve.

The first figure shows how the surrogate optimization is finding a combination of CP parameters that minimizes the error function, and with a higher number of simulations it gets closer to zero error. The second figure shows how the stress-strain with the calibrated parameters matches the experimental curve.

<img src="https://github.com/Strathclyde-AFRC-Computational-Sciences/Damask_CP_parameters_calibration_w_surrogate_optimization/assets/93150422/4f6a57ac-8fe5-461d-9061-58697c72cc36" height="300" width="400">

<img src="https://github.com/Strathclyde-AFRC-Computational-Sciences/Damask_CP_parameters_calibration_w_surrogate_optimization/assets/93150422/e7e857fd-6935-4ce7-8d0c-7846315b724a" height="300" width="400">

## Description
The current code calibrates only the plasticity parameters xi_0_sl, xi_inf_sl and h_0_sl-sl from the phenomenological crystal plasticity model in Damask. The ratios between the different slip systems and phases for each parameter are kept constant. Therefore, only 3 parameters are calibrated by the surrogate optimization model which scale the 3 plasticity constants separately:

h_0_sl-sl*param(1)
xi_0_sl*param(2)
xi_inf_sl*param(3)

## How to Run
Specify inputs in config.json. You need to specify the names of the phases in your RVE and the upper and lower bounds for you param(1-3)

Run main.m with matlab in src folder

the results are saved in optimized_CP.txt
