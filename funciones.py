import numpy as np
from math import factorial, sqrt, e


def probabilidadHiper(N, T, n, x1, x2):
    rango = range(x1, x2+1, 1)
    resultados = []
    tProb = 0
    # Empiezo la grafica
    grafica = '{"cols": [{"id":"","label":"X","pattern":"","type":"number"},{"id":"","label":"P","pattern":"","type":"number"}],"rows": ['
    for x in rango:
        p = (factorial(N-T) * factorial(T) * factorial(n) * factorial(N-n)) / \
            (factorial(n-x) * factorial(N-T-n+x) *
             factorial(T-x) * factorial(N) * factorial(x))
        tProb = tProb+p
        resultados.append([x, p])
        grafica = grafica + \
            '{"c":[{"v":'+str(x)+',"f":null},{"v":'+str(p)+',"f":null}]},'
    grafica = grafica + ']}'
    print(resultados)
    return resultados, grafica, tProb


def mediaHiper(n, N, T):
    m = (n*T)/N
    return m


def desvHiper(n, T, N):
    d = sqrt(((n*T)/N) * (1-(T/N))) * sqrt((N-n)/(N-1))
    return d


def sesgoCurtosis(p, n):
    q = 1-p
    # Calculo el sesgo
    sesgo = (q-p)/sqrt(n*p*q)

    # Calculo de la curtosis
    curtosis = 3+((1-(6*p*q))/sqrt(n*p*q))

    return sesgo, curtosis


def probPoisson(x1, x2, media):
    result = []
    rango = range(x1, x2+1, 1)
    tProb = 0
    # Empiezo la grafica
    grafica = '{"cols": [{"id":"","label":"X","pattern":"","type":"number"},{"id":"","label":"P","pattern":"","type":"number"}],"rows": ['
    for x in rango:
        p = (media ** x)/(factorial(x) * e**(media))
        result.append([x, p])
        grafica = grafica + \
            '{"c":[{"v":'+str(x)+',"f":null},{"v":'+str(p)+',"f":null}]},'
        tProb = tProb+p
    grafica = grafica + ']}'
    return result, grafica, tProb


def mm1Lq(rservicio, tllegada):
    lq = ((tllegada**2)/(rservicio * (rservicio-tllegada)))
    wq = lq/tllegada
    probUtilizacion = tllegada/rservicio
    return lq, wq, probUtilizacion


def mm1Ls(rservicio, tllegada):
    ls = ((tllegada)/(rservicio-tllegada))
    ws = ls/tllegada
    return ls, ws


def nUnidadesSistema(tllegada, rservicio, n1, n2):
    rango = range(n1, n2+1, 1)
    result = []

    for x in rango:
        pn = (1-(tllegada/rservicio)) * (tllegada/rservicio) ** x
        result.append([x, pn])

    return result
