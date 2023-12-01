from pulp import LpProblem, LpVariable, lpSum, LpMinimize
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


# Constants
M = 10 # Number of products
N = 7 # Number of classes
T = 6 # Number of periods
cj = [656,656,656,656,656,656,500000]# List of capacity of class j
#Read input data from Excel
df=pd.read_excel("/Users/bocchan/Downloads/HPW/6 class _ I layout/6class_1stlayout_tos.xlsx")


## Specify the Excel file name
excel_file_name = "6class_Ilayout_tos_result.xlsx"
# Create an Excel writer object
excel_writer = pd.ExcelWriter(excel_file_name, engine='xlsxwriter')


#Linear Programming Loop
for week in range(17,53):

#LP Setup
    #Filter weekly data
    df_week = df[df["week"]==week]
    #Assign weekly cost
    df_inbound = df_week[['class1_inbound', 'class2_inbound', 'class3_inbound', 'class4_inbound','class5_inbound','class6_inbound','class7_inbound']].drop_duplicates()
    df_outbound = df_week[['class1_outbound', 'class2_outbound', 'class3_outbound', 'class4_outbound','class5_outbound', 'class6_outbound','class7_outbound']].drop_duplicates()
    # List of average store cost of locations in class j
    sj = df_inbound.values.tolist()
    # List of average retrieve cost of locations in class j
    rj = df_outbound.values.tolist()
    #Predicted Inbound list
    ait = [df_week['a'].iloc[i:i+6].tolist() for i in range(0, len(df_week['a'].tolist()), 6)]
    #Predicted Outbound list
    dit = [df_week['d'].iloc[i:i+6].tolist() for i in range(0, len(df_week['d'].tolist()), 6)]


#LP Solving
    # Create LP problem
    model = LpProblem("Warehouse_Optimization", LpMinimize)
    # Decision variables
    v = LpVariable.dicts("v", ((i, j, t) for i in range(1, M+1) for j in range(1, N+1) for t in range(1, T+1)), lowBound=0, cat='Integer')
    w = LpVariable.dicts("w", ((i, j, t) for i in range(1, M+1) for j in range(1, N+1) for t in range(1, T+1)), lowBound=0, cat='Integer')
    x = LpVariable.dicts("x", ((i, j, t) for i in range(1, M+1) for j in range(1, N+1) for t in range(1, T+1)), lowBound=0, cat='Integer')
    # Objective function
    model += lpSum((sj[i-1][j-1] * v[(i, j, t)] + rj[i-1][j-1] * w[(i, j, t)]) for i in range(1, M+1) for j in range(1, N+1) for t in range(1, T+1))
    # Constraints
    for i in range(1, M+1):
        for t in range(1, T+1):
            # Demand constraint
            model += lpSum(v[(i, j, t)] for j in range(1, N+1)) == ait[i-1][t-1]

            # Departure constraint
            model += lpSum(w[(i, j, t)] for j in range(1, N+1)) == dit[i-1][t-1]
            
    for i in range(1, M+1):
        for j in range(1, N+1):
            for t in range(1, T):
                # Inventory balance constraint
                model += x[(i, j, t+1)] == x[(i, j, t)] + v[(i, j, t)] - w[(i, j, t)]

    for j in range(1, N+1):
        for t in range(1, T):
            # Capacity constraint
            model += lpSum(x[(i, j, t)] + v[(i, j, t)] for i in range(1, M+1)) <= cj[j-1]  

    if week == 17:
        for i in range(1, M+1):
            #Initial capacity assumptions
            model += x[(i, 1, 1)] == 25
            model += x[(i, 2, 1)] == 25
            model += x[(i, 3, 1)] == 25
            model += x[(i, 4, 1)] == 25
            model += x[(i, 5, 1)] == 25
            model += x[(i, 6, 1)] == 25
            model += x[(i, 7, 1)] == 5000
    else:
        for i in range(1, M+1):
            for j in range(1, N+1):
                model += x[(i, j, 1)] == ending_inventory[(i, j)] + inbound_decision[(i, j,6)] - outbound_decision[(i, j,6)]

    # Solve the problem
    model.solve()
    
    # After solving the LP problem for each week, save the v and w and x
    inbound_decision = {(i, j,t): v[(i, j, t)].varValue for i in range(1, M+1) for j in range(1, N+1)for t in range(1, T+1)}
    outbound_decision = {(i, j,t): w[(i, j, t)].varValue for i in range(1, M+1) for j in range(1, N+1)for t in range(1, T+1)}
    ending_inventory = {(i, j): x[(i, j, T)].varValue for i in range(1, M+1) for j in range(1, N+1)}

    
# Print results
    print("Status:", model.status)
    print(sum)
    for v in model.variables():
        print(v.name, "=", v.varValue)
    print("Total Cost =", model.objective.value())
    # Calculate the total cost
    total_cost = model.objective.value()
    print("Total Cost =", total_cost)

    
#Write result of each week to excel file
    #Create a list to store LP results
    lp_results = []
    #Iterate through LP variables
    for v in model.variables():
        variable_name = v.name
        variable_value = v.varValue
        lp_results.append((variable_name, variable_value))
    #Convert the lists to dataframes
    results_df = pd.DataFrame(lp_results, columns=['Variable', 'Value'])
    #Write data to the sheet
    sheet_name = "Week_" + str(week)
    results_df.to_excel(excel_writer, sheet_name=sheet_name, index=False)                       
    
        
# Save the Excel file
excel_writer.close()