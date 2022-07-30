import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

class Estadistica:

    def __init__(self):

        self.df = pd.read_csv('info/accidentes.csv')
    
    def datosExcel(self):
        return self.df

    def graficoHoraVictimas(self):

        img = io.BytesIO()

        fecha = self.df['HORA'].unique()
        precio = []
        for i in fecha:
            suma = self.df.loc[self.df['HORA'] == i, ['TOTAL_VICTIMAS']].sum()[0]
            precio.append(suma)

        plt.figure(figsize=(10,5))
        plt.bar(fecha, precio, color="silver")
        plt.title('Numero de victimas en accidentes con respecto a la hora diaria.')
        plt.xticks(rotation=10)
        plt.ylabel('Numero de victimas.')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficoFrecuenciaPrecio(self):

        img = io.BytesIO()

        x = self.df['CLASE']
        plt.figure(figsize=(10,5))
        plt.hist(x, bins=None, color="green")
        plt.title('Frecuencia con que se produce un accidente clase...')
        plt.xticks(rotation=10)
        plt.ylabel('Frecuencia')

        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url
        
    def graficocriptomonedas(self):
    
        img = io.BytesIO()

        fecha = self.df['DIA'].unique()
        pagos = []
        for i in fecha:
            suma = self.df.loc[self.df['DIA'] == i, ['NUM_FALLECIDO']].sum()[0]
            pagos.append(suma)

        plt.figure(figsize=(10,5))
        plt.bar(fecha, pagos, color="blue")
        plt.title('Dia de las semana.')
        plt.xticks(rotation=10)
        plt.ylabel('Numeros de fallecidos.')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url