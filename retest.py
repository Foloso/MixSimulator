import nevergrad as ng

def square(x, y=12):
    return sum((x - .5)**2) + abs(y)

def constraint_check(x):
    constraint = True
    for i in range(0, len(x)):
        if x[i] < 1:
            constraint = False
            break
    return constraint

# optimization on x as an array of shape (2,)
optimizer = ng.optimizers.OnePlusOne(parametrization=2, budget=100)

optimizer.parametrization.register_cheap_constraint(lambda x: constraint_check(x))

recommendation = optimizer.minimize(square)
print(recommendation.value)