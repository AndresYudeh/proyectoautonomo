
from flask import Flask, request
from flask.templating import render_template
from calc.Aleatorio import Aleatorio
from calc.Estadistica import Estadistica
from calc.Pronostico import Pronostico
from calc.Simulacion import Simulacion

est = Estadistica()
aleatorio = Aleatorio()
pronostico = Pronostico()
simulacion = Simulacion()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/FrecuenciaFecha')
def grafica1():
    return render_template('grafica1.html',
        imagen1 = est.graficoHoraVictimas())
    
@app.route('/Preciomercado')
def grafica2():
    return render_template('grafica2.html',
        imagen2 = est.graficoFrecuenciaPrecio())
    
@app.route('/Pagomonedas')
def grafica3():
    return render_template('grafica3.html',
        imagen3 = est.graficocriptomonedas())

@app.route('/Datos')
def proyectoDatos():
    return render_template('proyectoDatos.html',
        data=est.datosExcel())

@app.route('/Numerosaleatorios')
def aleatorios():
    return render_template('numerosaleatorios.html')

@app.route('/Pronosticos')
def pronosticos():
    return render_template('pronosticos.html')


@app.route('/inventario', methods=['GET'])
def inventario():
    data = simulacion.modeloInventario()
    return render_template('inventario.html',
        datos=data['datos'],
        df = data['df'],
        imagen = data['img_url'])
    

@app.route('/lineaespera', methods=['GET'])
def banco():
    data = simulacion.banco()
    return render_template('linea.html',
        df = data['df'],
        imagen = data['img_url'])

@app.route('/Analisis')
def proyectoAnalisis():
    return render_template('proyectoAnalisis.html',
        imagen1 = est.graficoHoraVictimas(),
        imagen2 = est.graficoFrecuenciaPrecio(),
        imagen3 = est.graficocriptomonedas())

@app.route('/cuadradosMedios', methods=['POST', 'GET'])
def cuadradosMedio():
    if request.method == 'POST':
        try:
            data = aleatorio.cuadradosMedios(
                int(request.form['n']),
                int(request.form['r']))

            return render_template('cuadradosMedios.html',
                datos = data[0],
                imagen1 = data[1])
        except Exception as error:
            return render_template('cuadradosMedios.html',
                error=error
            )
    elif request.method == 'GET':
        return render_template('cuadradosMedios.html')

@app.route('/congruenciaLineal', methods=['POST', 'GET'])
def congruenciaLineal():
    if request.method == 'POST':
        try:
            data = aleatorio.congruencialLineal(
                int(request.form['n']),
                int(request.form['x']),
                int(request.form['a']),
                int(request.form['c']),
                int(request.form['m']))

            return render_template('congruenciaLineal.html',
                datos = data[0],
                imagen = data[1])
        except Exception as error:
            return render_template('congruenciaLineal.html',
                error = error)

    elif request.method == 'GET':
        return render_template('congruenciaLineal.html')

@app.route('/congruencialMultiplicativo', methods=['POST', 'GET'])
def congruencialMultiplicativo():
    if request.method == 'POST':
        try:
            data = aleatorio.congruencialMultiplicativo(
                int(request.form['n']),
                int(request.form['x']),
                int(request.form['a']),
                int(request.form['m']))

            return render_template('congruencialMultiplicativo.html',
                datos = data[0],
                imagen = data[1])
        except Exception as error:
            return render_template('congruencialMultiplicativo.html',
                error = error)

    elif request.method == 'GET':
        return render_template('congruencialMultiplicativo.html')

@app.route('/distribucionPoisson', methods=['POST', 'GET'])
def distribucionPoisson():
    if request.method == 'POST':
        try:
            data = aleatorio.distribucionPoisson(
                int(request.form['landa']))

            return render_template('distribucionPoisson.html',
                imagen = data)
        except Exception as error:
            return render_template('distribucionPoisson.html',
                error = error)

    elif request.method == 'GET':
        return render_template('distribucionPoisson.html')

@app.route('/promedioMovil', methods=['POST', 'GET'])
def promedioMovil():
    if request.method == 'POST':
        try:
            data = pronostico.promedioMovil(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('promedioMovil.html',
                datos = data[0],
                imagen = data[1],
                mediaMovil3 = data[2],
                mediaMovil4 = data[3])
        except Exception as error:
            return render_template('promedioMovil.html',
                error = error)

    elif request.method == 'GET':
        return render_template('promedioMovil.html')


@app.route('/suavizacionExponencial', methods=['POST', 'GET'])
def suavizacionExponencial():
    if request.method == 'POST':
        try:
            data = pronostico.suavizacionExponencial(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('suavizacionExponencial.html',
                datos = data,
                cargar = True)
        except Exception as error:
            return render_template('suavizacionExponencial.html',
                error = error)

    elif request.method == 'GET':
        return render_template('suavizacionExponencial.html')

@app.route('/regresionLineal', methods=['POST', 'GET'])
def regresionLineal():
    if request.method == 'POST':
        try:
            data = pronostico.regresionLineal(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('regresionLineal.html',
                imagen = data)
        except Exception as error:
            return render_template('regresionLineal.html',
                error = error)

    elif request.method == 'GET':
        return render_template('regresionLineal.html')

@app.route('/regresionCuadratica', methods=['POST', 'GET'])
def regresionCuadratica():
    if request.method == 'POST':
        try:
            data = pronostico.regresionLinealCuadratica(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('regresionCuadratica.html',
                imagen = data)
        except Exception as error:
            return render_template('regresionCuadratica.html',
                error = error)

    elif request.method == 'GET':
        return render_template('regresionCuadratica.html')
    
    
    # jjdjd
        
@app.route('/sistemaMontecarlo')
def sistemaMontecarlo():
    return render_template('sistemaMontecarlo.html')

@app.route('/printSistemaMontecarlo')
def printSistemaMontecarlo():
    return render_template('printSistemaMontecarlo.html')

@app.route('/calcularMontecarlo', methods=['GET', 'POST'])
def calcularMontecarlo():
    tipoArch= request.form.get("tipoarchivo")
    n1 = request.form.get("numeroIteraciones", type=int)
    x01 = request.form.get("semilla", type=int)
    a1 = request.form.get("multiplicador", type=int)
    c1 = request.form.get("incremento", type=int)
    m1 = request.form.get("modulo", type=int)

    pago = request.form.get("x")
    probabilidad = request.form.get("y")

    file = request.files['file'].read()

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from pandas import ExcelWriter
    from matplotlib import pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    import io
    from io import BytesIO
    import base64
    import itertools
    import pandas as pd


    if tipoArch=='1':
        
        file = pd.read_excel(file)
        
        
    elif tipoArch=='2':
        file = pd.read_csv(io.StringIO(file.decode('utf-8')))
        
    elif tipoArch=='3':
        file = pd.read_json(file)

    # file = pd.read_excel(file)
    # tot = pd.DataFrame(file)
    #x = a["X"]
    #tot = a["Y"]

    # datos = {
    # 'Pago' : [0,500,1000,2000,5000,8000,10000],
    # 'Probabilidad': [0.83,0.06,0.05,0.02,0.02,0.01,0.01]
    # }
    df = pd.DataFrame(file)
    # Array para guardar los resultados
    dataArray = []
    # Suma de probabilidad
    sumProbabilidad = np.cumsum(df[probabilidad])
    df['FDP'] = sumProbabilidad
    # Obtenemos los datos mínimos
    datosMin = df['FDP']+0.001
    # Obtenemos los datos máximos
    datosMax = df['FDP']
    # Asignamos al DataFrame
    df['Min'] = datosMin
    df['Max'] = datosMax
    # Se establecen correctamente los datos mínimos
    df['Min'] = df['Min'].shift(periods=1, fill_value=0)
    df
        # n = Cantidad de tenedores de pólizas
    n = n1
    m = m1 # 2**32
    a = a1
    x0 = x01
    c = c1
    # Obtenemos los resultados
    x = [1] * n
    r = [0.1] * n
    for i in range(0, n):
        x[i] = ((a*x0)+c) % m
        x0 = x[i]
        r[i] = x0 / m
    # llenamos el DataFrame
    d = {'ri': r }
    dfMCL = pd.DataFrame(data=d)
    dfMCL

    # Valores máximos
    max = df['Max'].values
    # Valores mínimos
    min = df['Min'].values
    # Definimos el número de pagos
    n = 32
    
    # df = pd.DataFrame(df)

    # data1 = dffx.to_html(classes="table table-hover table-striped", justify="justify-all", border=0)
    
    # Función de búsqueda
    def busqueda(arrmin, arrmax, valor):
        
        for i in range (len(arrmin)):
            if valor >= arrmin[i] and valor <= arrmax[i]:
                return i
    #print(i)
        return -1
    xpos = dfMCL['ri']
    posi = [0] * n
    #print (n)
    for j in range(n):
        val = xpos[j]
        pos = busqueda(min,max,val)
        posi[j] = pos
    # Definiendo un índice para simular datos
    # ind = [1,2,3,4,5,6,7]
    ind = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,238,339,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498]
    df["Indice"] = ind
    # Ordenamos el DataFrame
    df = df[['Indice',pago,probabilidad,'FDP','Min','Max']]
    # Array para guardar los datos
    simula = []
    for j in range(n):
        for i in range(n):
            sim = df.loc[df["Indice"]== posi[i]+1 ]
            simu = sim.filter([pago]).values
            iterator = itertools.chain(*simu)
                    
            for item in iterator:
                a=item
            simula.append(round(a,2))
    # Insertamos en el DataFrame los datos de simulación
    dfMCL["Simulación"] = pd.DataFrame(simula)
    # Sumamos 39 ya que el precio de la acción actual es de 39
    dfMCL["Números de horas"] = dfMCL["Simulación"]
# Suma de Pagos a tenedor
    data = dfMCL['Números de horas'].sum()
    dataArray.append(data)

# Imprimir resultado
    print('Suma de los pagos al tenedor:', data)
    # dat = pd.DataFrame(data)
    # prin_='Suma de los pagos al tenedor: ',data
    # data01=data
    # data01=str(data01)
    # data3=dat.to_html(
    #     classes="col-md-6 mb-3", justify="justify-all")
    dfMCL

    

    buf = io.BytesIO()
    plt.plot(dfMCL['Simulación'], label='Simulación', color='blue')
    plt.plot(dfMCL['Números de horas'], label='Horas', color='red')
    plt.legend()

    fig = plt.gcf()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    plot_url = base64.b64encode(buf.getvalue()).decode('UTF-8')

    data1 = df.to_html(
        classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)

    """ writer = ExcelWriter("static/file/data.xlsx")
    dfMCL.to_excel(writer, index=False)
    writer.save()

    dfMCL.to_csv("static/file/data.csv", index=False)
    """
    data2 = dfMCL.to_html(
        classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)

    """ writer = ExcelWriter("static/file/data.xlsx")
    dfMCL.to_excel(writer, index=False)
    writer.save()

    dfMCL.to_csv("static/file/data.csv", index=False)
    """
    # data3 = data.to_html(
    #     classes="table table-hover table-striped", justify="justify-all", border=0)

    # """ writer = ExcelWriter("static/file/data.xlsx")
    # dfMCL.to_excel(writer, index=False)
    # writer.save()

    # dfMCL.to_csv("static/file/data.csv", index=False)
    # """
    return render_template('printSistemaMontecarlo.html', data=data1, data2=data2,data3=data, image=plot_url)
    # def busqueda(arrmin, arrmax, valor):


if __name__ == '__main__':
    app.run( host="0.0.0.0", port=5000,debug=True)