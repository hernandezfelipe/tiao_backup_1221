import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import sleep
import base64
import os

plt.set_loglevel('WARNING') 
#
df = pd.read_csv('/home/pi/tiao/temperature.txt', sep=';', header=None)
df.rename(columns={0:'date', 1:'temp', 2:'hum'}, inplace=True)
##df['data'] = pd.to_datetime(df['date'])
df['data'] = pd.to_datetime(df['date'].iloc[1:]).dt.strftime("%d-%m-%Y %H:%M:%S")
#df['ano'] = pd.to_datetime(df['data']).dt.year
#df['mes'] = pd.to_datetime(df['data']).dt.month
#df['dia'] = pd.to_datetime(df['data']).dt.day
#df['hora'] = pd.to_datetime(df['data']).dt.hour
#
#g = df.groupby(['dia','mes','ano', 'hora'])[['temp', 'hum']].mean().reset_index().sort_values(by=['ano','mes','dia','hora'], ascending=True)
#g['data'] = g['dia'].astype('int').astype(str) + '-' + g['mes'].astype('int').astype(str) + '-' +  g['ano'].astype('int').astype(str) + ' ' + g['hora'].astype('int').astype(str)
#
#g.to_csv('data.csv', index=False)

g = pd.read_csv('data.csv')

fig, ax = plt.subplots()
    
sns.lineplot(data=g, x='data', y='temp', ax=ax)

sns.lineplot(data=g, x='data', y='hum', ax=ax)
    
plt.legend(labels=['Temperature', 'Humidity %'])
    
plt.xlabel('Date/Hour')
plt.ylabel('Measurement')
ax.set_xticks([g['data'].iloc[0], g['data'].iloc[len(g)//2], g['data'].iloc[-1]])

ax.tick_params(axis='x', labelsize=5)

ax.grid()



def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href
    


st.text('{} - Temp: {}\N{DEGREE SIGN}C - Hum: {}%'.format(df['data'].iloc[-1], df['temp'].iloc[-1], df['hum'].iloc[-1]))
st.pyplot(fig)
st.markdown(get_table_download_link(g), unsafe_allow_html=True)
    

  
