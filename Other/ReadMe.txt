11/01/2023 "testPinch2.inp" is the working version.--> Worked

11/01/2023 "testPinch3.inp" is the new version I am building to test multiple nodes from different load cases.
This .inp file has the 3 steps with the first being the initial step. I have changed the other steps to 
Load1 and Load2 to test the idea for the actual experiment.

06/02/2023 "TestJob-2.inp" is the fastest model in the arsenal but it might be flawed. I have run it on two occasions.
In the first instance it failed because I essentially restricted my Poisson's ratios, refer to today's Supervisor presentation.
This worked but larger function evals. In the first two cases I used "trans" keyword to select the material using my Pseudo-latin Hypercube 
method of sampling. I plan on using the "ortho" keyword to test the next lot of optimisation to determine if that makes a difference.

