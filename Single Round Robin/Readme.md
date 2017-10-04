# Minimize the Break of Single Round Robin 
循環賽制常用於分組賽或聯賽中，參賽者與其它參賽者逐一進行比賽，每兩名參賽者之間只比賽一場的稱為單循環賽。
一名選手同時在主場或客場連續征戰則有break產生，然而過多的Break會有不公平性產生。
因此我們使用Gurobi來跑數學模型，來最小化break的產生。

## Problem Definition

主場 (H)  客場 (A)
Break定義: 一組隊伍連續兩場在主場(H)或客場(A)，進行比賽。
最小化break: 對單循環淘汰賽來說，假如有n組隊伍(n為偶數)則，其最小的break數為 n-2。

Home (H) or Away (A)
A team has a break in round t if it plays in rounds t and t+1 either two consecutive games at home or two consecutive games away
Minimize the number of breaks
Theorem: For a single round robin tournament with n teams (n being even), the min number of breaks is n ?  2

## Mixed Integer Programming Model
![image](https://github.com/KTLin8143/Scheduling/blob/master/Single%20Round%20Robin/Mini%20Break%20Model.PNG)


## Prerequisites

Gurobi 7.5.1 and Python(or any other laguage)

## Getting started 

### Installing Gurobi

安裝 Gurobi
下載gurobi軟體，並註冊，
```
http://www.gurobi.com/downloads/gurobi-optimizer
```

確認是否有安裝成功:
```
Python 2.7.13 |Anaconda 4.4.0 (64-bit)| (default, May 11 2017, 13:17:26) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
>>> from gurobipy import *
>>>

```
### Python 

Create Gurobi model (m)and variable (x[i][j][t], z[i][t])

``` 
    m = Model("Min_Break")
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

```

Set objective value
m.setObjective 設立model的目標(GRB.MINIMIZE為最小化此目標式)
```
    expr = LinExpr()
    for i in range(0, n):
        for t in range(0, n - 1):
            expr += z[i][t]
    m.setObjective(expr, GRB.MINIMIZE)
```
Add constraint
建立限制式，以求出解

```
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
```

將上述目標式、配合限制式做最佳化 m.optimize()

```
    m.optimize()
```


