import numpy as np
from math import factorial, sqrt

def probabilidadHiper(N,T,n,x1,x2):
    rango = range(x1,x2+1,1)
    resultados= []
    tProb =0 
    #Empiezo la grafica
    grafica = '{"cols": [{"id":"","label":"X","pattern":"","type":"number"},{"id":"","label":"P","pattern":"","type":"number"}],"rows": ['
    for x in rango:
        p = (factorial(N-T) * factorial(T) * factorial(n) * factorial(N-n))/ (factorial(n-x) * factorial(N-T-n+x) * factorial(T-x) * factorial(N) * factorial(x))
        tProb= tProb+p
        resultados.append([x, p])
        grafica = grafica + '{"c":[{"v":'+str(x)+',"f":null},{"v":'+str(p)+',"f":null}]},'
    grafica = grafica + ']}'
    print(resultados)
    return resultados,grafica,tProb

def mediaHiper(n,N,T): 
    m = (n*T)/N
    return m

def desvHiper(n,T,N):
    d = sqrt(((n*T)/N) * (1-(T/N))) * sqrt((N-n)/(N-1))
    return d



