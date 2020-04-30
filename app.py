# Importamos la libreria

from flask import Flask, render_template, redirect, url_for, request, flash, make_response
from math import factorial, sqrt
import numpy as np
import funciones as fn
# Se crea un objeto app de flask, es el objeto inicial con el cual se va a lanzar el framework
app = Flask(__name__)
# Siempre es necesario inicializar la sesion para que no existan erroes
app.secret_key = 'mysecretkey'
# Decorador para definir la ruta para la pagina principal
@app.route("/")
# Se define una funcion para la ruta de la pagina principal
def indexPage():
    # Lo necesario para enlazar las templates es utilizar el recurso render template
    return render_template("index.html")


@app.route("/binomial")
def fnBinomial():
    return render_template("binomial.html")


@app.route("/hiper")
def fnHiper():
    return render_template("hipergeometrica.html")


@app.route("/calcularBinomial", methods=['POST'])
def calcularBinomial():
    media = 0
    desv = 0
    fc = 0
    sesgo = 0
    curtosis = 0
    mediana = 0
    if request.method == 'POST':
        # Extraigo los parametros del formulario
        n = int(request.form['muestra'])
        x1 = int(request.form['x1'])
        x2 = int(request.form['x2'])
        p = float(request.form['p'])
        q = 100-p
        try:
            # trata de extraer el valor de N
            N = 0
            N = int(request.form['N'])
        except:
            # No hay valor de N hacer con poblacion infinita
            media = n*p/100
            desv = sqrt(n*p*q)/100

        if N != 0 and (n/N)*100 > 5:
            # EsPoblacion Infinita
            media = n*p/100
            desv = sqrt(n*p*q)/100

        elif N != 0 and (n/N)*100 <= 5:
            # Es poblacion Finita
            media = n*p/100
            fc = sqrt((N-n)/(N-1))
            desv = fc * sqrt(n*p*q)/100

        # Empiezo la grafica
        grafica = '{"cols": [{"id":"","label":"X","pattern":"","type":"number"},{"id":"","label":"P","pattern":"","type":"number"}],"rows": ['

        # Verifico que la muestra sea mayor que los numeros de exitos deseados
        if n >= x1 and x2:
            # Verifico que la suma de las probabilidades de exito y fracaso sean iguales a 100

            rango = []
            resultados = []
            suma = 0
            p = p/100
            q = q/100
            rango = range(x1, x2+1, 1)

            # Calculo de la mediana
            mediana = np.median(rango)

            # Recorro el rango y calculo la probabilidad
            for x in rango:
                n_x = n-x
                resultado = (factorial(n) / (factorial(x) *
                                             factorial(n-x))) * (p**x) * (q**n_x)
                # Sumo cada uno de los resultados
                suma = suma + resultado
                # agrego cada resultado al array
                resultados.append([x, resultado])
                # le agrego la parte de los datos al array de la grafica
                grafica = grafica + \
                    '{"c":[{"v":'+str(x)+',"f":null},{"v":' + \
                    str(resultado)+',"f":null}]},'
            grafica = grafica + ']}'

            # Calculo el sesgo y curtosis
            sesgo, curtosis = fn.sesgoCurtosis(p, n)

            return render_template('resultadoBinomial.html', data=resultados, g=grafica, suma=suma, media=media, desv=desv, fc=fc, sesgo=sesgo, curtosis=curtosis, mediana=mediana)

        else:
            flash('La suma del porcentaje de probabilidades no es igual a 100')
        return redirect(url_for('fnBinomial'))
    else:
        flash('El valor menor o mayor de exitos deseados debe de ser menor al tamaño de la muestra ')
        return redirect(url_for('fnBinomial'))


@app.route('/calculoHiper', methods=['POST'])
def calcularHiper():
    if request.method == 'POST':
        n = int(request.form['muestra'])
        N = int(request.form['N'])
        T = int(request.form['T'])
        x1 = int(request.form['x1'])
        x2 = int(request.form['x2'])
        mediana =0
        rango = []

        resultados, grafica, total = fn.probabilidadHiper(N, T, n, x1, x2)
        media = fn.mediaHiper(n, N, T)
        desv = fn.desvHiper(n, T, N)
        p = media/n
        sesgo, curtosis = fn.sesgoCurtosis(p, n)
        rango = range(x1, x2+1, 1)
        mediana = np.median(rango)
        print(media , mediana)
        return render_template('resultadoHiper.html', data=resultados, grafica=grafica, media=media, desv=desv, total=total, sesgo=sesgo, curtosis=curtosis, mediana=mediana)


@app.route('/poisson')
def poissonPage():
    return render_template('poisson.html')


@app.route('/calcularPoisson', methods=['POST'])
def calcularPoisson():
    if request.method == 'POST':
        media = float(request.form['media'])
        x1 = int(request.form['x1'])
        x2 = int(request.form['x2'])
        data, grafica, tProb = fn.probPoisson(x1, x2, media)
        desv= sqrt(media)
        return render_template('resultPoisson.html', data=data, grafica=grafica, total=tProb,desv=desv)


# Colas de espera
@app.route('/mm1')
def colasMm1():
    return render_template('colasmm1.html')


@app.route('/calcularmm1', methods=['POST'])
def calcularColasMm1():
    if request.method == 'POST':
        rservicio = int(request.form['rservicio'])
        tllegada = int(request.form['tllegada'])
        n1 = int(request.form['n1'])
        n2 = int(request.form['n2'])
        try:
            tiempo = float(request.form['tiempo'])
        except:
            tiempo = 0

        lq, wq, probUtilizacion = fn.mm1Lq(rservicio, tllegada)
        ls, ws = fn.mm1Ls(rservicio, tllegada)
        data = fn.nUnidadesSistema(tllegada, rservicio, n1, n2)
        probOcio = round((1-probUtilizacion),4)
        if tiempo != 0:
            probTiempoCola = fn.wqMayorTiempoCola(probUtilizacion, tiempo, rservicio)
            probTiempoSistema = fn.wsMayorTiempoSistema(rservicio, probUtilizacion, tiempo)
        else:
            probTiempoCola = 0
            probTiempoSistema = 0
        return render_template('resultadocolasmm1.html', data=data, lq=lq, wq=wq, ls=ls, ws=ws, probUtilizacion=probUtilizacion, probOcio = probOcio, probTiempoCola = probTiempoCola,tiempo = tiempo, probTiempoSistema=probTiempoSistema)


@app.route('/cookie')
def cookie(grafica):
    res = make_response('Cookie Establecida')
    print(grafica)
    res.set_cookie('nombre', 'Línea de Código')
    return res


# Ejemplos de lo antes trabajado
"""
@app.route('/otherPage')
def otherPage():
    return render_template('other.html')
#Funciones que reciben parametros desde las urls pueden ser int, str o float
@app.route('/prueba/<cadena>')
def pruebaCadena(cadena):
    return 'Hola %s' %cadena

@app.route('/pruebas/<int:numero>')
def pruebaNumeros(numero):
    return 'Hola %s' %numero

@app.route('/usuario/<nombreUser>')
def user(nombreUser):
    #Hay 3 formas de redireccion a paginas, ya sea a funciones o a rutas
    #return suma()
    #return redirect('/suma')
    return redirect(url_for('suma'))

@app.route('/suma')
def suma():
    return 'La suma es> 44' 
"""


# Funcion principal
if __name__ == "__main__":
    # Ejecuta el objeto app
    # app.run()
    # Para evitar recargar el levantado del servidor se usa
    app.run(debug=True)
