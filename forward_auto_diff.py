#!/usr/bin/python3

import math


class Var:
    def __init__(self, val, der):
        self.val = val
        self.der = der

def neg(var):
    return Var(var.val, -var.der)

def c(k, var):
    return Var(var.val, k*var.der)

def sum(vars):
    deriv = 0
    value = 0
    for i in vars:
        deriv += i.der
        value += i.val
    return Var(value, deriv)

def product(vars):
    deriv = 0
    if len(vars) == 0:
        return Var(1, 0)
    value = math.prod(var.val for var in vars)
    for i in range(len(vars)):
        deriv_part = vars[i].der
        for j in range(len(vars)):
            if i != j:
                deriv_part *= vars[j].val
        deriv += deriv_part
    return Var(value, deriv)

def sin(var):
    if isinstance(var, tuple):
        deriv = 0
        val = 1
        for i in range(len(var)):
            deriv_part = var[i].der
            inner_value = var[i].val
            for j in range(len(var)):
                if i != j:
                    deriv_part *= var[j].val
                    inner_value *= var[j].val
            deriv += deriv_part * math.cos(inner_value)
            val *= math.sin(var[j].val)
        return Var(val, deriv)
    else:
        return Var(math.sin(var.val), var.der * math.cos(var.val))

def cos(var):
    if isinstance(var, tuple):
        deriv = 0
        val = 1
        for i in range(len(var)):
            deriv_part = var[i].der
            inner_value = var[i].val
            for j in range(len(var)):
                if i != j:
                    deriv_part *= var[j].val
                    inner_value *= var[j].val
            deriv -= deriv_part * math.sin(inner_value)
            val *= math.cos(var[j].val)
        return Var(val, -deriv)
    else:
        return Var(math.cos(var.val), -var.der * math.sin(var.val))

def pow(n, var):
    if isinstance(var, tuple):
        deriv = 0
        val = 1
        for i in range(len(var)):
            inner_value = var[i].val
            for j in range(len(var)):
                if i != j:
                    inner_value *= var[j].val
            deriv += var[i].der * n * math.pow(inner_value, n - 1)
            val *= math.pow(var[j].val, n)
        return Var(val, deriv)
    else:
        return Var(math.pow(var.val, n), var.der * n * math.pow(var.val, n - 1))


def funct(x,y):
    f1 = sum((pow(2,y), c(2,neg(product((y, pow(2,x))))), pow(4,x), neg(c(2,x)), pow(2,x)))
    return f1 

def compute_grad(vars):
    grad = [0] * len(vars) 
    for i in range(len(vars)):
        vars[i].der = 1
        grad[i] = funct(*vars).der
        vars[i].der = 0
    return grad

# def main():
#     x = Var(3, 1)
#     y = Var(5, 0)
#     z = Var(2, 0)
#     f = funct(x,y)
#     print(f.der)
    
#     x.der = 0
#     y.der = 1
#     f = funct(x,y)
#     print(f.der)
    
#     x = Var(3, 1)
#     y = Var(5, 0)
#     z = Var(2, 0)
#     vars = (x, y)
#     grad = compute_grad(vars)
#     print(grad)


# main()
