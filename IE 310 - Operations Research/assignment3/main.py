from pulp import *
Foods = ['OATS', 'CHICKEN', 'EGGS', 'MILK', 'KUCHEN', 'BEANS']

portionSize = {'OATS': 28, 
         'CHICKEN': 100, 
         'EGGS': 2, 
         'MILK': 237, 
         'KUCHEN': 170, 
         'BEANS': 260}

energy = {'OATS': 110, 
          'CHICKEN': 205, 
          'EGGS': 160, 
          'MILK': 160, 
          'KUCHEN': 420, 
          'BEANS': 260}

protein = {'OATS': 4, 
              'CHICKEN': 32, 
              'EGGS': 13, 
              'MILK': 8, 
              'KUCHEN': 4, 
              'BEANS': 14}

calcium = {'OATS': 2, 
              'CHICKEN': 12, 
              'EGGS': 54, 
              'MILK': 285, 
              'KUCHEN': 22, 
              'BEANS': 80}

price = {'OATS': 30, 
         'CHICKEN': 240, 
         'EGGS': 130, 
         'MILK': 90, 
         'KUCHEN': 200, 
         'BEANS': 60}

limit = {'OATS': 4, 
         'CHICKEN': 3, 
         'EGGS': 2, 
         'MILK': 8,  
         'KUCHEN': 2, 
         'BEANS': 2}

prob = LpProblem("The_Diet_Problem", LpMinimize)
food_vars = LpVariable.dicts("Foods",Foods,0)

# x[f] = x of f for one portion
# x[f] / portionSize[f] = x of f for one unit (g, cc or number (egg))
prob += lpSum([price[f] * food_vars[f] for f in Foods]) # objective function
prob += lpSum([energy[f] * food_vars[f] for f in Foods]) >= 2000, "CaloryRequirement"
prob += lpSum([protein[f] * food_vars[f] for f in Foods]) >= 55, "FoodRequirement"
prob += lpSum([calcium[f] * food_vars[f] for f in Foods]) >= 800, "CalciumRequirement"
for f in Foods:
    prob += food_vars[f] <= limit[f]

# Solve the problem
prob.solve()
print(prob)

print(LpStatus[prob.status])
print("Optimal objective function value = ", value(prob.objective))


for f in Foods:
    print(f, "=", food_vars[f].varValue)