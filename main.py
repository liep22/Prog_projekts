import flask 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from flask import  send_file


app = flask.Flask(__name__)

@app.route('/')
def home():
 return flask.render_template('home.html')


@app.route('/download')
def download_file():
    path = "projekts.2_prog.csv"
    return send_file(path, as_attachment=True)
    

@app.route('/stabini',methods=['GET'] )
def stabini():
        
        df = pd.read_csv('projekts.2_prog.csv', delimiter=';')# Nolasiet CSV failu, norādot atdalītāju
        df.columns = df.columns.str.strip()# Noņemiet atstarpes no kolonnu nosaukumiem
        df = df.dropna()
        filtered_df = df[df['Dienas veids'].str.contains('Saulains|Apmācies ar sauli', na=False)]

        plt.figure(figsize=(15, 10))  # Piemērs: platums = 20 collas, augstums = 10 collas
        ax = plt.gca()  # Iegūstiet pašreizējo asu objektu
        filtered_df.plot(kind='bar', x='Diena', y='Dienas temperatūra', ax=ax, color = '#faa803')

        plt.xticks(rotation=90)  # Rotācija par 90 grādiem, lai vērtības būtu vertikāli
        plt.xlabel('Dienas')
        plt.ylabel('Temperatūra')
        plt.title('Temperatūra')
        plt.subplots_adjust(bottom=0.3)  # Pielāgo figūras marginus
        plt.savefig('static/diagramma.png')  # Saglabā attēlu failā
        plt.close()
        return flask.render_template('stabini.html')

@app.route('/linijas')
def linijas():
    df = pd.read_csv('projekts.2_prog.csv', delimiter=';')
    df.columns = df.columns.str.strip()  # Noņemiet atstarpes no kolonnu nosaukumiem
    df = df.dropna()
    df = df.sort_values(by='Diena')

    plt.figure()
    plt.plot(df['Diena'], df['Dienas temperatūra'], marker='o', color='#f9e605', label='Temperatūra (°C)')
    plt.plot(df['Diena'], df['Vēja brāzmu ātrums(vidējais)'], marker='s', color='#05c2f9', label='Vēja brāzmas (m/s)')
    plt.title('Temperatūra un vēja brāzmas salīdzinājums')
    plt.xlabel('Dienas')
    plt.ylabel('Vērtības')
    plt.legend() 
    plt.grid(True)
    plt.savefig('static/line.png')
    plt.close()
    
    return flask.render_template('line.html')

@app.route('/histogramma')
def histogramma():
    df = pd.read_csv('projekts.2_prog.csv', delimiter=';')
    df.columns = df.columns.str.strip()  # Noņemiet atstarpes no kolonnu nosaukumiem
    df = df.dropna()
    
    plt.figure()
    df.hist(column='Gaisa spiediens mmHg', bins = 10, color = '#fa3b03')
    ax = df.hist(column='Gaisa spiediens mmHg', bins=40, color = '#fa3b03')
    plt.savefig('static/histogramma.png')
    plt.clf()
    plt.close()
    

    df_filtrs = df[df['Vēja virziens'].str.contains('Ziemeļi|Dienvidi', na=False)]
    df_filtrs.plot(kind='scatter', x='Diena', y='Gaisa spiediens mmHg', color = '#328929')
    plt.savefig('static/scatter.png')
    plt.close()
    return flask.render_template('hist_scatter.html')
    




@app.route('/heatmap')
def heatmap():
    df = pd.read_csv('projekts.2_prog.csv', delimiter=';')

    df['Mitrums g/m3'] = pd.to_numeric(df['Mitrums g/m3'].str.replace(',', '.'), errors='coerce')

    heatmap_data = df.pivot_table(index='Diena', columns='Nakts temperatūra', values='Mitrums g/m3')

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt='.2f', cbar_kws={'label': 'Korelācijas koeficients'})
    plt.title("Siltuma karte ")
    plt.savefig('static/heatmap.png')
    plt.close()



    df = pd.read_csv('projekts.2_prog.csv', delimiter=';')
    df['Nakts temperatūra'] = pd.to_numeric(df['Nakts temperatūra'], errors='coerce')
    df['Mitrums g/m3'] = pd.to_numeric(df['Mitrums g/m3'].str.replace(',', '.'), errors='coerce')


    correlation_matrix = df[['Nakts temperatūra', 'Mitrums g/m3']].corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar_kws={'label': 'Korelācijas koeficients'})
    plt.title("Korelācija starp nakts temperatūru un gaisa mitrumu")
    plt.savefig('static/korelacija.png')
    plt.close()

    return flask.render_template('korelacija_heatmap.html')

    
if __name__ == "__main__":
 app.run(debug=True)
