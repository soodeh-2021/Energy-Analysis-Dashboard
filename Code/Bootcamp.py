# Packages  
import pandas as pd 
import numpy as np 
import streamlit as st 
import plotly.express as px 
from PIL import Image
import plotly.graph_objects as go 
import altair as alt 

st.set_page_config(
    page_title= "Energy Analysis Dashboard",
    page_icon="🔋", 
    layout= "wide",
    initial_sidebar_state= "expanded"
)

alt.themes.enable("dark")

# Loading file and converting the date into the right format  
data = pd.read_csv("Data/Panel format.csv")
data["Year"] = pd.to_datetime(data["Year"], format="%Y")
data["Year"] = data["Year"].dt.year

with st.sidebar:
    st.title("🌩️ Energy Dashboard")
    st.markdown("---")

    sidebar_image = Image.open("Image/11.jpg")
    st.sidebar.image(sidebar_image, use_container_width=True)

    # Select a Region
    region = st.sidebar.selectbox("Select a Region:", data["Region"].unique())
    st.markdown("---")

    # Filter the countries based on the selected region
    countries_in_region = data[data["Region"] == region]["Country"].unique()
    country = st.sidebar.selectbox("Select a Country:", countries_in_region)
    st.markdown("---")

    year = st.sidebar.selectbox("Select a Year:", data["Year"].unique())
    st.markdown("---")
    st.write("Use this dashboard to explore energy production trends over time in different countries.")
    st.markdown("---")

# Filter data based on selected country
country_data = data[data["Country"] == country]

st.title(f"Energy Production Time series Analysis for {country}")
st.markdown("""
This dashboard provides a detailed overview of various energy production trends in the selected country. Navigate using the sidebar to choose a different country.
""")

main_image = Image.open("Image/22.jpg")
st.image(main_image, caption="Energy Sources", use_container_width=True)

# Chart creation function
def create_chart(data, y, title, yaxis_title):
    fig = px.line(
        data,
        x="Year",
        y=y,
        title=title,
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    fig.add_annotation(
        x=data["Year"].iloc[-1],
        y=data[y].iloc[-1],
        text="Latest Value",
        showarrow=True,
        arrowhead=2,
        font=dict(color="#E74C3C", size=12)
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=yaxis_title,
        template="plotly_white",
        font=dict(
            family="Arial, sans-serif",
            size=16,
            color="#2C3E50"
        ),
        title=dict(
            text=title,
            font=dict(size=22)
        ),
        margin=dict(l=0, r=0, t=80, b=0),
        legend=dict(
            title="Legend",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified",
        xaxis=dict(
            rangeslider=dict(visible=True),
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            gridcolor="LightGrey"
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            gridcolor="LightGrey"
        )
    )

    fig.update_traces(
        hovertemplate="<b>Year</b>: %{x}<br><b>Value</b>: %{y}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Population Over Time")
create_chart(country_data, "pop", "Population over Time", "Population")

st.subheader("🌊 Hydro Energy Production Over Time")
create_chart(country_data, "hydro_ej", "Hydro Energy Production (Exajoules)", "Exajoules")

st.subheader("⚛️ Nuclear Energy Production Over Time")
create_chart(country_data, "nuclear_ej", "Nuclear Energy Production (Exajoules)", "Exajoules")

st.subheader("♻️ Renewable Energy Production Over Time")
create_chart(country_data, "ren_power_ej", "Renewable Energy Production (Exajoules)", "Exajoules")

st.subheader("☀️ Solar Energy Production Over Time")
create_chart(country_data, "solar_ej", "Solar Energy Production (Exajoules)", "Exajoules")

# Rest of the code remains the same

# ------------------- Adding the Bar Chart -------------------

st.subheader("🔍 Energy Consumption by Source for Selected Year")

# Filter data for the selected year
year_data = data[(data["Country"] == country) & (data["Year"] == year)]

if not year_data.empty:
    # Select relevant energy consumption columns
    energy_consumption = year_data[[
        'coalcons_ej', 
        'gascons_ej', 
        'oilcons_ej', 
        'hydro_ej', 
        'nuclear_ej', 
        'ren_power_ej', 
        'solar_ej', 
        'wind_ej'
    ]].iloc[0]
    
    # Prepare data for bar chart
    energy_sources = energy_consumption.index
    consumption_values = energy_consumption.values
    
    # Create a DataFrame for Plotly
    bar_data = pd.DataFrame({
        'Energy Source': energy_sources,
        'Consumption (Exajoules)': consumption_values
    })
    
    # Remove any NaN or zero values for clarity
    bar_data = bar_data.dropna()
    bar_data = bar_data[bar_data['Consumption (Exajoules)'] > 0]
    
    # Create the bar chart
    fig_bar = px.bar(
        bar_data,
        x='Energy Source',
        y='Consumption (Exajoules)',
        title=f'Energy Consumption by Source in {year}',
        color='Energy Source',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig_bar.update_layout(
        xaxis_title='Energy Source',
        yaxis_title='Consumption (Exajoules)',
        template='plotly_white',
        font=dict(
            family="Arial, sans-serif",
            size=16,
            color="#2C3E50"
        ),
        title=dict(
            text=f'Energy Consumption by Source in {year}',
            font=dict(size=22)
        ),
        margin=dict(l=0, r=0, t=80, b=0),
        hovermode="x unified"
    )
    
    fig_bar.update_traces(
        hovertemplate='<b>Energy Source</b>: %{x}<br><b>Consumption</b>: %{y} Exajoules<extra></extra>'
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning(f"No data available for {country} in {year}.")

# ------------------- Adding the Stacked Area Chart -------------------

st.subheader("📊 Energy Consumption Mix Over Time")

# Select relevant energy consumption columns
energy_columns = [
    'coalcons_ej', 
    'gascons_ej', 
    'oilcons_ej', 
    'hydro_ej', 
    'nuclear_ej', 
    'ren_power_ej', 
    'solar_ej', 
    'wind_ej'
]

# Prepare data for stacked area chart
stacked_data = country_data[['Year'] + energy_columns].copy()

# Melt the DataFrame for Plotly
stacked_data_melted = stacked_data.melt(id_vars='Year', var_name='Energy Source', value_name='Consumption (Exajoules)')

# Remove zero or NaN values
stacked_data_melted = stacked_data_melted.dropna()
stacked_data_melted = stacked_data_melted[stacked_data_melted['Consumption (Exajoules)'] > 0]

# Create the stacked area chart
fig_area = px.area(
    stacked_data_melted,
    x='Year',
    y='Consumption (Exajoules)',
    color='Energy Source',
    title='Energy Consumption Mix Over Time',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

fig_area.update_layout(
    xaxis_title='Year',
    yaxis_title='Consumption (Exajoules)',
    template='plotly_white',
    font=dict(
        family="Arial, sans-serif",
        size=16,
        color="#2C3E50"
    ),
    title=dict(
        text='Energy Consumption Mix Over Time',
        font=dict(size=22)
    ),
    hovermode="x unified"
)

fig_area.update_traces(
    hovertemplate='<b>Year</b>: %{x}<br><b>Energy Source</b>: %{color}<br><b>Consumption</b>: %{y} Exajoules<extra></extra>'
)

st.plotly_chart(fig_area, use_container_width=True)

# ------------------- End of Stacked Area Chart -------------------

# ------------------- Adding the CO₂ Emissions Line Chart -------------------

st.subheader("🌍 CO₂ Emissions per Exajoule Over Time")

# Ensure there are no missing values
co2_data = country_data[['Year', 'co2_combust_per_ej']].dropna()

if not co2_data.empty:
    fig_co2 = px.line(
        co2_data,
        x='Year',
        y='co2_combust_per_ej',
        title='CO₂ Emissions per Exajoule Over Time',
        markers=True,
        line_shape="spline",
        color_discrete_sequence=['#FF5733']
    )

    fig_co2.update_layout(
        xaxis_title='Year',
        yaxis_title='CO₂ Emissions (per Exajoule)',
        template='plotly_white',
        font=dict(
            family="Arial, sans-serif",
            size=16,
            color="#2C3E50"
        ),
        title=dict(
            text='CO₂ Emissions per Exajoule Over Time',
            font=dict(size=22)
        ),
        hovermode="x unified"
    )

    fig_co2.update_traces(
        hovertemplate='<b>Year</b>: %{x}<br><b>CO₂ Emissions</b>: %{y} per Exajoule<extra></extra>'
    )

    st.plotly_chart(fig_co2, use_container_width=True)
else:
    st.warning(f"No CO₂ emissions data available for {country}.")

# ------------------- End of CO₂ Emissions Line Chart -------------------
