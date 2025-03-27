import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa de Aeropuertos en Florida", layout="wide")

st.title("🛫 Capacidad de Aeropuertos en Florida (Enplanements 2023)")
st.markdown("""
Este mapa muestra los principales aeropuertos de Florida, representando su volumen de pasajeros mediante el tamaño y color de cada punto.
""")

# Cargar el archivo CSV
df = pd.read_csv('aeropuertos_con_enplanements.csv')

# Asegurar que los datos estén correctos
df['CY 23 Enplanements'] = pd.to_numeric(df['CY 23 Enplanements'], errors='coerce')

# Definir colores por rango de pasajeros
def get_color(pax):
    if pax > 30_000_000:
        return 'darkblue'
    elif pax > 15_000_000:
        return 'blue'
    elif pax > 5_000_000:
        return 'lightblue'
    elif pax > 1_000_000:
        return 'orange'
    else:
        return 'lightgray'

# Crear mapa
m = folium.Map(location=[27.5, -81], zoom_start=6)

# Agregar puntos
for _, row in df.iterrows():
    pax = row['CY 23 Enplanements']
    if pd.isna(pax): continue  # omitir vacíos

    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=max(pax / 1_000_000, 2),  # Escala de tamaño
        color=get_color(pax),
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['IATA']}: {int(pax):,} pasajeros"
    ).add_to(m)

# Agregar leyenda HTML
legend_html = """
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 230px;
    background-color: white;
    border:2px solid gray;
    z-index:9999;
    font-size:14px;
    padding: 10px;
    border-radius: 5px;
">
<b>Capacidad por aeropuerto</b><br>
<i style="background:darkblue; width:12px; height:12px; display:inline-block;"></i> Más de 30M<br>
<i style="background:blue; width:12px; height:12px; display:inline-block;"></i> 15M–30M<br>
<i style="background:lightblue; width:12px; height:12px; display:inline-block;"></i> 5M–15M<br>
<i style="background:orange; width:12px; height:12px; display:inline-block;"></i> 1M–5M<br>
<i style="background:lightgray; width:12px; height:12px; display:inline-block;"></i> Menos de 1M
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Mostrar mapa en Streamlit
st_data = st_folium(m, width=1000, height=600)
