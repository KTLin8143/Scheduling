#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# This example formulates and solves the following simple MIP model:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#  x, y, z binary

from gurobipy import *

try:
    n = 6
    # Create a new model
    m = Model("mip1")

    # Create variables
    x = [[[0 for t in range(0, n - 1)] for j in range(0, n)] for i in range(0, n)]
    z = [[0 for t in range(0, n - 1)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            for t in range(0, n - 1):
                x[i][j][t] = m.addVar(vtype=GRB.BINARY, name="x")

    for i in range(0, n):
        for t in range(0, n - 1):
            z[i][t] = m.addVar(vtype=GRB.BINARY, name="z")

    m.update()

    # Set objective
    expr = LinExpr()
    for i in range(0, n):
            expr += z[i][t]
    m.setObjective(expr, GRB.MINIMIZE)

    # Add constraint 1
    for j in range(0, n):
        for t in range(0, n - 1):
            expr = LinExpr()
            for i in range(0, n):
                expr += (x[i][j][t] + x[j][i][t])
            m.addConstr(expr, GRB.EQUAL, 1)

    # Add constraint 2
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                expr = LinExpr()
                for t in range(0, n - 1):
                    expr += (x[i][j][t] + x[j][i][t])
                m.addConstr(expr, GRB.EQUAL, 1)

    # Add constraint 3
    for i in range(0, n):
        for t in range(1, n - 1):
            expr = LinExpr()
            for j in range(0, n):
                expr += x[i][j][t - 1]
            for j in range(0, n):
                expr += x[i][j][t]
            expr += -z[i][t]
            m.addConstr(expr, GRB.LESS_EQUAL, 1)

    # Add constraint 4
    for i in range(0, n):
        for t in range(1, n - 1):
            expr = LinExpr()
            for j in range(0, n):
                expr += x[j][i][t - 1]
            for j in range(0, n):
                expr += x[j][i][t]
            expr += -z[i][t]
            m.addConstr(expr, GRB.LESS_EQUAL, 1)

    m.optimize()

    print('Obj: %g' % m.objVal)


except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
