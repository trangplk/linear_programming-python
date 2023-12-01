# Warehouse Optimization using Linear Programming
## Overview

This repository contains a Python script for optimizing warehouse operations using Linear Programming (LP). The LP model is designed to optimize warehouse storage assignments to reduce traveling costs, with a specific focus on minimizing forklift travel distances and maximizing space utilization. Static Turnover Rate Policy was used to prioritize SKU.

## Prerequisites

Ensure you have the following libraries installed before running the script:

- `pulp`
- `pandas`
- `matplotlib`
- `numpy`

Install the required libraries using:

```bash
pip install pulp pandas matplotlib numpy
```

## How to Use

**Run the Python script:**

   ```bash
   python lp_6class_Ilayout_tos.py
   ```

## Input Data

The script reads input data from an Excel file (`6class_1stlayout_tos.xlsx`). Ensure that this file is present in the specified location. The input file contains data related to weekly inbound & outbound predictions and the Static Turnover Rate (TOS) prioritization order for each SKU in each week.

## LP Model Setup

### Computation of `a`, `d`

I adopted a 16-week moving average for the forecasting model to predict incoming (`a`) and outgoing pallets (`d`) from week 17 to week 52. TOS is incorporated into the model (refer to [Appendix 1](#appendix-1)).

### Linear Programming (LP) Model: Objective Function, Decision Variables, and Constraints

#### Objective Function

The objective is to minimize the average storage and retrieval costs in each class across all products and periods. The costs are computed based on the distance traveled.

#### Costs Assumptions

- Traveling costs in each class = Average distance traveled (m) for each pallet postion.

#### Modified Objective Function to Incorporate TOS and TOD (only when running Python)

The objective function is modified to include TOS prioritization rule. The costs are adjusted for each SKU = Original Distance + TOS. The final actual result can be obtained by multiplying the decision variables result with the unmodified costs.

#### Decision Variables

- `v[i][j][t]`: Pallet quantity of SKU i to be stored in Class j at Day t.
- `w[i][j][t]`: Pallet quantity of SKU i to be retrieved in Class j at Day t.
- `x[i][j][t]`: Inventory level of SKU i, in Class j, at Day t.

#### Constraints

- Incoming shipments should match the sum of all products stored across all storage classes during the specified time period.
- Outgoing shipments should align with the total of all products retrieved from all storage classes within the given time frame.
- The inventory level in the next period (t+1) is the current inventory at time t plus the items stored minus the items retrieved.
- The inventory level at time t plus the items stored during period t must not exceed the warehouse capacity.
- Inventory levels must not fall below zero.
- Quantities for storage and retrieval processes must not be negative.
- The initial inventory for the first day (t=1) of the current week (t) is carried over from the ending inventory of the sixth day (t=6) of the previous week.
- For the mathematical expressions of the LP Model, refer to [Appendix 2](#appendix-2).

## Results

After solving the LP problem for each week, the script prints the optimization status, decision variable values, and the total cost. Additionally, the results are saved in individual sheets within the output Excel file for further analysis.

## Notes
- Make sure to update the file paths and names according to your system and preferences.
- The LP model is designed for a specific set of constants and assumptions. Modify them based on your warehouse specifications.
- To run for different scenarios (different number of classes, distance, SKU, etc), please modify the code accordingly


## Appendices

### Appendix 1: TOS Policies
<img width="217" alt="image" src="https://github.com/trangplk/lp-programming-python/assets/152631495/aa71531b-5fc7-4cee-a291-5cc3204ddd6c">


### Appendix 2: Mathematical Expressions of the LP Model

<img width="343" alt="image" src="https://github.com/trangplk/lp-programming-python/assets/152631495/e44d2a05-6104-46b7-8b5d-b7430c7698ff">
<img width="237" alt="image" src="https://github.com/trangplk/lp-programming-python/assets/152631495/1c3f3d90-3757-49af-8b83-836469ff9c25">

