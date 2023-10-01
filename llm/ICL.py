# In-context learning examples.
example_qa = """
----------
Question: Why is it not recommended to only use one warehouse for berth 1?
Answer Code:
```python
z = m.addVars(warehouses, vtype=GRB.BINARY, name="z")
m.addConstr(sum(z[w] for w in warehouses) <= 1, "_")
for w in warehouses:
    m.addConstr(shipping_costs['Berth1', w] <= warehouseCapacities[w] * z[w], "_")
```

----------
Question: What if there's a 50% jump in the capacity of warehouse 1?
Answer Code:
```python
warehouses["Warehouse1"] = warehouses["Warehouse1"] * (1 + 50/100)
```

"""