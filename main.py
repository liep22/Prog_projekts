import flask
import pandas as pd
import matplotlib.pyplot as plt



app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/stabini',methods=['GET'] )
def stabini():
        
        df = pd.read_csv('projekts.2_prog.csv', delimiter=';')# Nolasiet CSV failu, norādot atdalītāju
        df.columns = df.columns.str.strip()# Noņemiet atstarpes no kolonnu nosaukumiem
        df = df.dropna()
        filtered_df = df[df['Dienas veids'].str.contains('Saulains|Apmācies ar sauli', na=False)]

        plt.figure(figsize=(15, 10))  # Piemērs: platums = 20 collas, augstums = 10 collas
        ax = plt.gca()  # Iegūstiet pašreizējo asu objektu
        filtered_df.plot(kind='bar', x='Diena', y='Dienas temperatūra', ax=ax)

        plt.xticks(rotation=90)  # Rotācija par 90 grādiem, lai vērtības būtu vertikāli
        plt.xlabel('Dienas')
        plt.ylabel('Temperatūra')
        plt.title('Temperatūra')
        plt.subplots_adjust(bottom=0.3)  # Pielāgo figūras marginus
        plt.savefig('static/diagramma.png')  # Saglabā attēlu failā
        return flask.render_template('stabini.html')



@app.route('/histogramma')
def histogramma():
    df = pd.read_csv('projekts.2_prog.csv', delimiter=';')
    df.columns = df.columns.str.strip()  # Noņemiet atstarpes no kolonnu nosaukumiem
    df = df.dropna()
    
    df.hist(column='Gaisa spiediens mmHg', bins = 10)
    ax = df.hist(column='Gaisa spiediens mmHg', bins=40)
    plt.savefig('static/histogramma.png')

    df_filtrs = df[df['Vēja virziens'].str.contains('Ziemeļi|Dienvidi', na=False)]
    df_filtrs.plot(kind='scatter', x='Diena', y='Gaisa spiediens mmHg')
    plt.savefig('static/scatter.png')

    return flask.render_template('hist_scatter.html')
    
if __name__ == "__main__":
 app.run(debug=True)
