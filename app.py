import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import Element

st.set_page_config(page_title="Mapa de Aeropuertos en Florida", layout="wide")

st.title("🛫 Capacidad de Aeropuertos en Florida (Enplanements 2023)")
st.markdown("""
Este mapa muestra los principales aeropuertos de Florida.  
El tamaño y color de cada punto representan el volumen anual de pasajeros (enplanements) durante 2023.
""")

# Cargar archivo CSV
df = pd.read_csv('aeropuertos_con_enplanements.csv')

# Asegurar columnas numéricas
df['CY 23 Enplanements'] = pd.to_numeric(df['CY 23 Enplanements'], errors='coerce')

# Función para asignar color según enplanements (naranja = más grande)
def get_color(pax):
    if pax > 20_000_000:
        return 'red'
    elif pax > 10_000_000:
        return 'orange'
    else:
        return 'blue'

# Crear mapa base
m = folium.Map(location=[27.5, -81], zoom_start=6)

# Agregar aeropuertos como puntos
for _, row in df.iterrows():
    pax = row['CY 23 Enplanements']
    if pd.isna(pax): continue

    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=max(pax / 1_000_000, 2),
        color=get_color(pax),
        fill=True,
        fill_opacity=0.75,
        popup=f"{row['IATA']}: {int(pax):,} pasajeros"
    ).add_to(m)

# Leyenda HTML
legend_html = """
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    z-index:9999;
    background-color: white;
    padding: 10px;
    border:2px solid gray;
    border-radius: 5px;
    font-size: 14px;
    ">
<b>Capacidad por aeropuerto</b><br>
<i style="background:orange; width:12px; height:12px; display:inline-block; margin-right:5px;"></i> Más de 30M<br>
<i style="background:gold; width:12px; height:12px; display:inline-block; margin-right:5px;"></i> 15M–30M<br>
<i style="background:lightgreen; width:12px; height:12px; display:inline-block; margin-right:5px;"></i> 5M–15M<br>
<i style="background:lightblue; width:12px; height:12px; display:inline-block; margin-right:5px;"></i> 1M–5M<br>
<i style="background:lightgray; width:12px; height:12px; display:inline-block; margin-right:5px;"></i> Menos de 1M
</div>
"""

m.get_root().html.add_child(Element(legend_html))



# Mostrar mapa en Streamlit
st_data = st_folium(m, width=1000, height=600)



st.markdown("## 📈 Evolución trimestral de la tarifa promedio (MEX–MIA, Top 5 aerolíneas)")

# Procesamiento de la gráfica (usa tus datos ya cargados)
import matplotlib.pyplot as plt

fare_trend_quarterly1 = pd.read_csv('fare_trend_quarterly.csv')
fare_trend_quarterly1 = fare_trend_quarterly1.pivot(index='Quarter', columns='Airline', values='Fare')

airline_colors = {
    'AA': 'grey',   # American Airlines → gris
    'Y4': 'purple',   # Volaris → morado
    'DL': 'red',   # Delta → rojo
    'UA': 'blue',   # United → azul rey
    'AM': '#000080',    # Aeroméxico → azul marino
    '4O': 'black'
}

# Filtrar y ordenar columnas según tu diccionario
ordered_cols = [col for col in airline_colors if col in fare_trend_quarterly1.columns]
fare_trend_quarterly1 = fare_trend_quarterly1[ordered_cols]
color_list = [airline_colors[col] for col in fare_trend_quarterly1.columns]

# Crear la figura con Matplotlib
fig, ax = plt.subplots(figsize=(18, 6))
fare_trend_quarterly11.plot(marker='o', linewidth=2, ax=ax, color=color_list)
ax.set_title('Evolución trimestral de la tarifa promedio - Top 5 aerolíneas (MEX ↔ MIA)')
ax.set_ylabel('Tarifa promedio (USD)')
ax.set_xlabel('Trimestre')
ax.grid(True)
ax.legend(title='Aerolínea', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Mostrar en Streamlit
st.pyplot(fig)
