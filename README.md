# N-Jointed-Arm-Inverse-Kinematics
Python code that demonstrates some math behind N-Jointed Arm Inverse Kinematics 

#### __main__.py<nolink>
- The GUI program that allows the user to interactivly mess around with N-Jointed Arms

#### n_jointed_arm_ik.py<nolink>
- The script that contains the math behind the inverse-kinematics

#### test.py<nolink>
- A series of tests for the ik math to ensure that any new changes keep functionality

## Setup
Run the following in a debian-based terminal:

`git clone https://github.com/PyCee/N-Jointed-Arm-Inverse-Kinematics.git`

`cd N-Jointed-Arm-Inverse-Kinematics/`

`make install`

## Once Installed:
* make test - Runs various math tests to ensure math correctness
* make run - Starts the GUI program to mess around with N-jointed arms

## GUI Components:
* N - The number of joints
* length_(i) - the length of the i'th section
* Point X - The X coordinate of the endpoint
* Point Y - The Y coordinate of the endpoint
* Blue Dot - The beginning of the arm. Should be in the center of the screen
* Red Dot - The point at coordinates (Point X, Point Y). The arm should lead to this point

## Running
* Set N
* Set arm lengths
* Click button to set arm Variables
* Type in point coords and update arm variables, or click in white box to drag endpoint

Lengths determine how far each joint is from the last, and determines the overall reach of the arm. Length 0 is the arm closest to the base