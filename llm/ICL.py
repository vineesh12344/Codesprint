# In-context learning examples.
example_qa = """
----------
Question: Why is it not recommended to use just one supplier for roastery 2?
Answer Code:
```python
z = m.addVars(suppliers, vtype=GRB.BINARY, name="z")
m.addConstr(sum(z[s] for s in suppliers) <= 1, "_")
for s in suppliers:
    m.addConstr(x[s,'roastery2'] <= capacity_in_supplier[s] * z[s], "_")
```

----------
Question: What if there's a 13% jump in the demand for light coffee at cafe1?
Answer Code:
```python
light_coffee_needed_for_cafe["cafe1"] = light_coffee_needed_for_cafe["cafe1"] * (1 + 13/100)
```

"""