import pandas
import plotly.express as px
import random
import streamlit as st

from datetime import datetime

from src.utils import show_country, show_country_palo, random_color

#################################################
##LOAD DATA
#################################################

countries_direction_df = pandas.read_csv('data/countries_direction.csv',index_col=0)
countries_distances_df = pandas.read_csv('data/countries_distances.csv',index_col=0)
# Get the current date as an integer (e.g., 20231104 for November 4, 2023)
current_date = int(datetime.now().strftime("%Y%m%d"))
random.seed(current_date)
# Create a dictionary to map the graph type to its data and function
graph_data_mapping = {
    'Tradle': {
        'data_file': 'data/all_countries.csv',
        'graph_function': show_country
    },
    'Palo extras 0 ': {
        'data_file': ('data/Country_data_palo.xlsx',0),
        'graph_function': show_country_palo
    },
    'Palo extras 1': {
    'data_file': ('data/Country_data_palo.xlsx',1),
    'graph_function': show_country_palo
    },
    'Palo extras 2': {
        'data_file': ('data/Country_data_palo.xlsx',2),
        'graph_function': show_country_palo
    },    
    'Palo extras 3': {
        'data_file': ('data/Country_data_palo.xlsx',3),
        'graph_function': show_country_palo
    },    
    'Palo extras 4': {
        'data_file': ('data/Country_data_palo.xlsx',4),
        'graph_function': show_country_palo
    },

}

#################################################
#INIT
#################################################
if 'intentos' not in st.session_state:
    st.session_state.intentos = 0
if 'graficos' not in st.session_state:
    st.session_state.graficos = 0
puntos_graficos={1:1,2:1,3:2,4:2,5:4}

#################################################
#Gráficos
#################################################
if 'selected_graph_type' not in st.session_state:
    st.session_state.selected_graph_type =  random.choice(list(graph_data_mapping.keys()))

# Display the selected graph type on the screen
selected_graph_type = st.session_state.selected_graph_type
st.title(selected_graph_type)

# Load data and display the graph
data_file = graph_data_mapping[selected_graph_type]['data_file']
graph_function = graph_data_mapping[selected_graph_type]['graph_function']



if selected_graph_type =='Tradle':
    data = pandas.read_csv(data_file) 

else: 
    data_file_path, sheet_number= data_file
    data = pandas.read_excel(data_file_path, sheet_number)
    xls = pandas.ExcelFile(data_file_path)
    sheet_name = xls.sheet_names[sheet_number]
    if sheet_name=='SURFACE 2019':
        data['SURFACE 2019']=data['SURFACE 2019'].drop(columns=['Total km^2'])
    data=data.melt(id_vars='Country')

st.title(f'Tienes <font color="red"> {20 - (st.session_state.intentos*2)-st.session_state.intentos } </font>- puntos')

random.seed(current_date)
Country_name = random.choice(data.Country.unique())

df_Country = data[data.Country == Country_name]
random_colors = [random_color() for _ in range(len(df_Country))]

fig = graph_function(df_Country) if selected_graph_type =='Tradle' else graph_function(df_Country,sheet_name, random_colors) 

st.plotly_chart(fig)



Country_namelist=data.Country.unique()
Country_namelist.sort()
selected_Country = st.selectbox('Selecciona un pais:',Country_namelist )

# Agregar un botón

if 'text' not in st.session_state:
    st.session_state.text = ""

# Lógica para incrementar intentos cuando se presiona el botón
if st.button("Enviar"):
    st.session_state.intentos += 1

    if selected_Country == Country_name:
        st.session_state.text = st.session_state.text+ f'{str(st.session_state.intentos)} - <font color="green"> {selected_Country} </font><br>'
    else:
        st.session_state.text = st.session_state.text+ f'{str(st.session_state.intentos)} - <font color="red"> {selected_Country} </font>- {countries_distances_df[Country_name][selected_Country]} km {countries_direction_df[Country_name][selected_Country]} <br>'

    # Display the styled text
st.write(st.session_state.text , unsafe_allow_html=True)