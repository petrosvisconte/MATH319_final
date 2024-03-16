#!/usr/bin/python3

import math


class Var:
    def __init__(self, val, der, seed):
        self.val = val
        self.der = der
        self.seed = seed

def neg(var):
    return Var(var.val, -var.der, var.seed)

def c(k, var):
    return Var(var.val, k*var.der, var.seed)

def sum(vars):
    deriv = 0
    for i in vars:
        deriv += i.der
    return Var(0, deriv)

def product(vars):
    deriv = 0
    for i in range(len(vars)):
        deriv_part = vars[i].der
        for j in range(len(vars)):
            if i != j:
                deriv_part *= vars[j].val
        deriv += deriv_part
    return Var(0, deriv)

def sin(vars):
    try:
        iter(vars)
        if isinstance(vars, tuple):
            deriv = 0
            for i in range(len(vars)):
                deriv_part = vars[i].der
                inner_value = vars[i].val
                for j in range(len(vars)):
                    if i != j:
                        deriv_part *= vars[j].val
                        inner_value *= vars[j].val
                deriv += deriv_part*math.cos(inner_value)
            return Var(0, deriv)
    except TypeError:
        return Var(0, vars.der*math.cos(vars.val))
    
def cos(vars):
    try:
        iter(vars)
        if isinstance(vars, tuple):
            deriv = 0
            for i in range(len(vars)):
                deriv_part = vars[i].der
                inner_value = vars[i].val
                for j in range(len(vars)):
                    if i != j:
                        deriv_part *= vars[j].val
                        inner_value *= vars[j].val
                deriv += deriv_part*math.sin(inner_value)
            return Var(0, -deriv)
    except TypeError:
        return Var(0, -vars.der*math.sin(vars.val))

def pow(n, vars):
    try:
        iter(vars)
        if isinstance(vars, tuple):
            deriv = 0
            for i in range(len(vars)):
                inner_value = vars[i].val
                for j in range(len(vars)):
                    if i != j:
                        inner_value *= vars[j].val
                deriv += vars[i].der*n*math.pow(inner_value, n-1)
            return Var(0, deriv)
    except TypeError:
        return Var(0, vars.der*n*math.pow(vars.val, n-1))

def funct(x,y):
    w1 = product((sum((y, neg(product((x,x))))), sum((y, neg(product((x,x)))))))
    w2 = sum((w1, neg(c(2,x)), product((x,x))))
    return w2

def compute_grad(vars):
    grad = [0] * len(vars) 
    for i in range(len(vars)):
        vars[i].der = 1
        grad[i] = funct(*vars).der
        vars[i].der = 0
    return grad

def main():
    x = Var(3, 1)
    y = Var(5, 0)
    z = Var(2, 0)
    f = funct(x,y)
    print(f.der)
    
    x.der = 0
    y.der = 1
    f = funct(x,y)
    print(f.der)
    
    vars = (x, y)
    grad = compute_grad(vars)
    print(grad)

    x.der = 1
    print(sin(((x,y,z))).der)

main()