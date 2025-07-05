import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Lee el CSV en un DataFrame
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
        title="Histograma de Kilometraje (millas)"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# 4. Botón para construir un scatter Precio vs Kilometraje
if st.button("🔍 Construir scatter Precio vs Kilometraje"):
    st.write("Creando gráfico de dispersión Precio vs Kilometraje")
    fig_scatter = px.scatter(
        df,
        x="odometer",
        y="price",
        labels={"odometer":"Kilometraje (millas)", "price":"Precio (USD)"},
        trendline="ols",
        title="Precio vs Kilometraje"
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

all_types = df["type"].unique().tolist()
selected_types = st.sidebar.multiselect(
    "Selecciona tipos de anuncio",
    options=all_types,
    default=all_types
)

# 6. DataFrame filtrado según los filtros de la barra lateral
df_filtered = df[
    (df.model_year.between(year_range[0], year_range[1])) &
    (df.type.isin(selected_types))
]

# 7. Título del Dashboard
st.title("📊 Dashboard de Anuncios de Coches")

# 8. Gráfico 1: Scatter Precio vs Año de Lanzamiento (filtrado)
st.subheader("Precio vs Año de Lanzamiento")
fig2 = px.scatter(
    df_filtered,
    x="model_year",
    y="price",
    labels={"price":"Precio (USD)", "model_year":"Año"},
    trendline="ols",
    title="Precio vs Año de Lanzamiento"
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
