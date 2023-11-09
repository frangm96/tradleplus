
import plotly.express as px
import random
import streamlit as st
import hmac

DIRECTIONS_EMOJI = {
    "North": "⬆️",
    "South": "⬇️",
    "East": "➡️",
    "West": "⬅️",
    "Northeast": "↗️",
    "Northwest": "↖️",
    "Southeast": "↘️",
    "Southwest": "↙️",
}

color_dic= {'Animal Products':'#ed40f2',
            'Vegetable Products':'#f4ce0f',
            'Animal and Vegetable Bi-Products':'#edbd53',
            'Foodstuffs':'#a0d447',
            'Mineral Products':'#a53200',
            'Chemical Products':'#ed40f2',
            'Plastics and Rubbers':'#ff73ff',
            'Animal Hides':'#75f1b4',
            'Wood Products':'#dd0e31',
            'Paper Goods':'#efdc81',
            'Textiles':'#02a347',
            'Footwear and Headwear':'#2cba0f',
            'Stone And Glass':'#f57d41',
            'Precious Metals':'#892eff',
            'Metals':'#aa7329',
            'Machines':'#2e97ff',
            'Transportation':'#69c8ed',
            'Instruments':'#9e0071',
            'Miscellaneous':'#9c9fb2',
            'Arts and Antiques':'#847290',
            'Weapons':'#9cf2cf'}

def show_country(df_country):
  
    fig = px.treemap(df_country, 
                    path=['Section','HS4'],  # Columna que define la jerarquía
                    values='Trade Value',  # Columna que define el tamaño en porcentajes
                    color='Section',  # Colores basados en la categoría 'Section'
                    color_discrete_map=color_dic,  # Mapeo de colores
                    title=str(round(df_country['Trade Value'].sum()/1e9,2)) +'B'+ ' EXPORTS OEC' if df_country['Trade Value'].sum()>1e9 else str(round(df_country['Trade Value'].sum()/1e6,2)) +'M' + ' EXPORTS OEC',
                    labels={'Section': 'Categoría', 'HS4': 'Nombre de la Caja', 'Trade Value Percentage': 'Porcentaje del Valor Comercial'})


    fig.update_layout(
        width=600,  # Ancho de la figura en píxeles
        height=500  # Alto de la figura en píxeles
    )
    return fig


def show_country_palo(df_country,name_df,random_colors):

    fig = px.treemap(df_country, 
                    path=['variable'],  # Columna que define la jerarquía
                    values='value',  # Columna que define el tamaño en porcentajes
                    color='variable',  # Colores basados en la categoría 'Section'
                    color_discrete_sequence =random_colors,  # Mapeo de colores
                     title=  str(round(df_country['value'].sum()/1e9,2)) +f'B {name_df}' if df_country['value'].sum()>1e9 else str(round(df_country['value'].sum()/1e6,2)) +f'M {name_df}'if df_country['value'].sum()>1e6 else str(round(df_country['value'].sum()/1e3,2)) +f'mil {name_df}'if df_country['value'].sum()>1e3 else str(round(df_country['value'].sum(),2)) +f' {name_df}' ,
                    # labels={'variable': 'Categoría', 'value': 'Valor'}
    )

    fig.update_layout(
        width=600,  # Ancho de la figura en píxeles
        height=500  # Alto de la figura en píxeles
    )
    return fig


def random_color():
    
    return f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False
