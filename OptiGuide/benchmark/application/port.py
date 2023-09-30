import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import time

berthCapacities = dict({"Berth1" : 10000,
               "Berth2" : 20000,
               "Berth3" : 1000,
               "Berth4" : 40000})

berths = berthCapacities.keys()

warehouseCapacities = dict({"Warehouse1" : 10000,
                    "Warehouse2" : 20000,
                    "Warehouse3" : 10000,
                    "Warehouse4" : 40000})

warehouses = warehouseCapacities.keys()

shipping_costs= dict({("Berth1", "Warehouse1") : 10*1000/100,
                    ("Berth1", "Warehouse2") : 20*1000/100,
                    ("Berth1", "Warehouse3") : 30*1000/100,
                    ("Berth1", "Warehouse4") : 100*1000/100,
                    ("Berth2", "Warehouse1") : 10*1000/100,
                    ("Berth2", "Warehouse2") : 60*1000/100,
                    ("Berth2", "Warehouse3") : 40*1000/100,
                    ("Berth2", "Warehouse4") : 70*1000/100,
                    ("Berth3", "Warehouse1") : 20*1000/100,
                    ("Berth3", "Warehouse2") : 40*1000/100,
                    ("Berth3", "Warehouse3") : 110*1000/100,
                    ("Berth3", "Warehouse4") : 10*1000/100,
                    ("Berth4", "Warehouse1") : 10*1000/100,
                    ("Berth4", "Warehouse2") : 120*1000/100,
                    ("Berth4", "Warehouse3") : 50*1000/100,
                    ("Berth4", "Warehouse4") : 10*1000/100})

routes = shipping_costs.keys()
cost = shipping_costs.values()

## Model deployment
model = gp.Model("Port Logistics")

# OPTIGUIDE DATA CODE GOES HERE


trucks = model.addVars(routes, name="trucks", vtype=GRB.INTEGER)

## Objective function
total_cost = gp.quicksum(trucks[i,j] * cost[i,j] for i,j in routes)
containers_left = gp.quicksum(berthCapacities[b] - gp.quicksum(trucks[i,b] for i in berthCapacities.keys() if (i,b) in routes) for b in berthCapacities.keys())
alpha = 0.5 # weight for the cost objective
model.setObjective(alpha * total_cost + (1 - alpha) * containers_left, GRB.MINIMIZE)

# berth capacity constraints
ware_constrs = model.addConstrs(gp.quicksum(trucks.select(warehouse, '*')) <= warehouseCapacities[warehouse] for warehouse in warehouseCapacities.keys())
berth_constrs = model.addConstrs(gp.quicksum(trucks.select('*', berth)) <= berthCapacities[berth] for berth in berthCapacities.keys())
model.optimize()

m = model

# OPTIGUIDE CONSTRAINT CODE GOES HERE


# Solve
m.update()
model.optimize()

print(time.ctime())
if m.status == GRB.OPTIMAL:
    print(f'Optimal cost: {m.objVal}')
else:
    print("Not solved to optimality. Optimization status:", m.status)