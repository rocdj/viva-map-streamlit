import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa interactivo - Aeropuertos en Florida", layout="wide")

st.title("Capacidad de Aeropuertos en Florida")
st.markdown("""
Este mapa muestra los aeropuertos relevantes de Florida y su capacidad utilizando datos de **enplanements 2023**.  
El tamaño de cada punto representa el volumen de pasajeros del aeropuerto.
""")

# Cargar tus datos aquí
df = pd.read_csv('aeropuertos_con_enplanements.csv')  # Asegúrate de tener columnas: IATA, Lat, Lon, CY 23 Enplanements

# Crear mapa base
m = folium.Map(location=[27.5, -81], zoom_start=6)

# Agregar puntos
for _, row in df.iterrows():
    radius = max(row['CY 23 Enplanements'] / 1_000_000, 2)
    popup = f"{row['IATA']}: {int(row['CY 23 Enplanements']):,} pasajeros"
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=radius,
        popup=popup,
        color='blue',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

# Mostrar mapa en Streamlit
st_data = st_folium(m, width=1000, height=600)
