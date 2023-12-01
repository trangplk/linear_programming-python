# lp-programming-python
# Warehouse Optimization using Linear Programming
## Overview
This repository contains a Python script for optimizing warehouse operations using Linear Programming (LP). The LP model is designed to make decisions on inventory management, inbound and outbound logistics, and overall cost minimization.

Prerequisites
Ensure you have the following libraries installed before running the script:

pulp
pandas
matplotlib
numpy
Install the required libraries using:

bash
Copy code
pip install pulp pandas matplotlib numpy
How to Use
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repository.git
Navigate to the project directory:

bash
Copy code
cd your-repository
Run the Python script:

bash
Copy code
python warehouse_optimization.py
Input Data
The script reads input data from an Excel file (6class_1stlayout_tos.xlsx). Ensure that this file is present in the specified location. The input file should contain data related to the warehouse layout, classes, and weekly demand predictions.

LP Model Setup
Computation of a, d, x, under the establishment of TOS and TOD Policy
We adopted a 16-week moving average as our forecasting model to predict incoming (a) and outgoing pallets (d) from week 17 to week 52. The script computes daily beginning inventory (x) based on assumptions for the starting pallets on day 1. TOS and TOD policies are incorporated into the model (refer to Appendix 1).

Linear Programming (LP) Model: Objective Function, Decision Variables, and Constraints
Objective Function
The objective is to minimize the average storage and retrieval costs in each class across all products and periods. The costs are computed based on distance traveled, labor costs, and other operating costs.

Costs Assumptions
Traveling costs in each class = Distance traveled (m) x Cost to travel 1m for retrieval/storage ($).
Cost per meter of traveling: 45% labor costs and 55% other operating costs.
Storage/Retrieval cost includes other operating costs and salary pay.
Modified Objective Function to Incorporate TOS and TOD (only when running Python)
The objective function is modified to include TOS and TOD. The costs are adjusted accordingly, and after running the LP model with TOD and TOS incorporated, the final result is obtained by multiplying the decision variables with the unmodified costs.

Decision Variables
v[i][j][t]: Pallet quantity of SKU i to be stored in Class j at Day t.
w[i][j][t]: Pallet quantity of SKU i to be retrieved in Class j at Day t.
x[i][j][t]: Inventory level of SKU i, in Class j, at Day t.
Constraints
All arrivals equal to the total of all products stored in all storage classes in the time period.
All departures equal to the total of all products retrieved from all storage classes in the time period.
Inventory level at t+1 period is the inventory at t plus items stored less items retrieved.
Inventory level at t period plus items stored in period t must be less than the capacity of the warehouse.
Inventory cannot be negative.
Storage and retrieval quantity cannot be negative.
Ending inventory of t=6 of the previous week will be the beginning inventory t=1 of this week.
For the mathematical expressions of the LP Model, refer to Appendix 2.

Results
After solving the LP problem for each week, the script prints the optimization status, decision variable values, and the total cost. Additionally, the results are saved in individual sheets within the output Excel file for further analysis.

Appendices
Appendix 1: TOS and TOD Policies
[Include the details of TOS and TOD policies here]

Appendix 2: Mathematical Expressions of the LP Model
[Include the mathematical expressions of the LP Model here]

Feel free to reach out if you have any questions or need further assistance!
