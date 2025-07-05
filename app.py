import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Leer el CSV en un DataFrame
df = pd.read_csv("vehicles_us.csv")

# 2. Header principal
st.header("📈 Exploración Interactiva del Dataset de Vehículos")

# 3. Botón para construir un histograma de Kilometraje
if st.button("🔢 Construir histograma de Kilometraje"):
    st.write("Creando histograma de Kilometraje (odómetro)")
    fig_hist = px.histogram(
        df,
        x="odometer",
        nbins=30,
        title="Histograma de Kilometraje (millas)",
        labels={"odometer": "Kilometraje (millas)"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# 4. Botón para construir un scatter Precio vs Kilometraje (con regresión manual)
if st.button("🔍 Construir scatter Precio vs Kilometraje"):
    st.write("Creando gráfico de dispersión Precio vs Kilometraje")
    # Scatter base
    fig_scatter = px.scatter(
        df,
        x="odometer",
        y="price",
        labels={"odometer":"Kilometraje (millas)", "price":"Precio (USD)"},
        title="Precio vs Kilometraje"
    )
    # Regresión lineal manual
    df_nm = df[["odometer","price"]].dropna()
    x = df_nm["odometer"].to_numpy()
    y = df_nm["price"].to_numpy()
    m, b = np.polyfit(x, y, 1)
    fig_scatter.add_scatter(
        x=x,
        y=m*x + b,
        mode="lines",
        name="Tendencia",
        line=dict(dash="dash")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# 5. Sidebar: filtros interactivos
st.sidebar.header("🔎 Filtros")

min_year, max_year = int(df.model_year.min()), int(df.model_year.max())
year_range = st.sidebar.slider(
    "Selecciona rango de año",
    min_year, max_year,
    (min_year, max_year)
)

all_types = df["type"].dropna().unique().tolist()
selected_types = st.sidebar.multiselect(
    "Selecciona tipos de anuncio",
    options=all_types,
    default=all_types
)

# 6. DataFrame filtrado según los filtros
df_filtered = df[
    (df.model_year.between(year_range[0], year_range[1])) &
    (df.type.isin(selected_types))
]

# 7. Título del Dashboard
st.title("📊 Dashboard de Anuncios de Coches")

# 8. Gráfico 1: Scatter Precio vs Año de Lanzamiento (filtrado + regresión manual)
st.subheader("Precio vs Año de Lanzamiento")
fig2 = px.scatter(
    df_filtered,
    x="model_year",
    y="price",
    labels={"price":"Precio (USD)", "model_year":"Año"},
    title="Precio vs Año de Lanzamiento"
)
# Regresión manual
df_nm2 = df_filtered[["model_year","price"]].dropna()
x2 = df_nm2["model_year"].to_numpy()
y2 = df_nm2["price"].to_numpy()
m2, b2 = np.polyfit(x2, y2, 1)
fig2.add_scatter(
    x=x2,
    y=m2*x2 + b2,
    mode="lines",
    name="Tendencia",
    line=dict(dash="dash")
)
st.plotly_chart(fig2, use_container_width=True)

# 9. Gráfico 2: Top 10 Tipos por Ventas Globales (filtrado)
st.subheader("Top 10 Tipos por Ventas Globales")
top_types = (
    df_filtered.groupby("type")["price"]
               .sum()
               .sort_values(ascending=False)
               .head(10)
               .reset_index()
)
fig3 = px.bar(
    top_types,
    x="price",
    y="type",
    orientation="h",
    labels={"price":"Ventas (USD)", "type":"Tipo"},
    title="Top 10 Tipos por Ventas Globales"
)
fig3.update_layout(yaxis={"categoryorder":"total ascending"})
st.plotly_chart(fig3, use_container_width=True)
