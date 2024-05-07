import streamlit as st
import pandas as pd
import plotly.express as px

data_path = '/workspaces/streamlit-dashboard/integrated_water_related_data.csv'
data = pd.read_csv(data_path)

st.set_page_config(page_title="Health and Environmental Dashboard", layout="wide")

# header for the entire dashboard
st.title("Wastewater Health Impact Dashboard")

# Adding information about the cause explaining the importance of wastewater management
st.markdown("""
- **Health:** Proper wastewater management is essential for preventing the spread of diseases and contaminants, safeguarding public health and well-being.
- **Environment:** Effective treatment and disposal of wastewater mitigate environmental pollution, preserving ecosystems, and maintaining biodiversity.
- **Carbon Density:** Managing wastewater reduces carbon emissions, contributing to efforts to mitigate climate change and promote environmental sustainability.
- **Society:** By conserving resources and protecting water sources, wastewater management contributes to a more sustainable society, ensuring access to clean water for future generations.
""")

# Sidebar for country selection
country = st.sidebar.selectbox('Select a Country', data['Entity'].unique())

# Filter data based on selected country
country_data = data[data['Entity'] == country]

# Sidebar options for selecting data series for the time series chart
agricultural_waste = st.sidebar.checkbox('Show Agricultural Wastewater', True)
industrial_waste = st.sidebar.checkbox('Show Industrial Wastewater', True)

# Add a slider for selecting the year range in the sidebar or main page
year_range = st.sidebar.slider(
    "Select the Year Range",
    min_value=int(country_data['Year'].min()),
    max_value=int(country_data['Year'].max()),
    value=(int(country_data['Year'].min()), int(country_data['Year'].max())),
    key='year_range_slider'  # Unique key for this slider
)

# Filter the data based on the selected year range
filtered_country_data = country_data[(country_data['Year'] >= year_range[0]) & (country_data['Year'] <= year_range[1])]

# Section header
st.header(f'Data for {country}')


# Creating a dual-axis plot using Plotly Express with customized colors
fig = px.bar(filtered_country_data, x='Year', y='Premature_Death_Count', 
             labels={'Premature_Death_Count': 'Premature Death Count'},
             title='Premature Death Count and Urban Wastewater Discharged',
             color_discrete_sequence=['#004c6d'])  # Dark blue color for the bars

# Adding a line graph for urban wastewater on a secondary y-axis
fig.add_scatter(x=filtered_country_data['Year'], y=filtered_country_data['Urban wastewater, all sources, discharged without treatment(million m3)'],
                mode='lines+markers', name='Urban Wastewater (million m3)', yaxis='y2',
                marker=dict(color='#ff7f0e'))  # Orange color for the line

# Update layout to include a second y-axis and adjust legend positioning
fig.update_layout(
    yaxis2=dict(title='Urban Wastewater (million m3)', overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
The graph above visualizes the relationship between urban wastewater discharge and premature death counts. 
This highlights the direct health impacts of inadequate water treatment and urban planning.
""")

# Creating the time series analysis chart using Plotly
if agricultural_waste or industrial_waste:
    plot_data = filtered_country_data[['Year']]
    if agricultural_waste:
        plot_data['Agricultural Wastewater'] = filtered_country_data['Agricultural (incl. forestry + fisheries) wastewater, all sources, direct discharges(million m3)']
    if industrial_waste:
        plot_data['Industrial Wastewater'] = filtered_country_data['Industrial wastewater, all sources, discharged without treatment(million m3)']

    fig = px.line(plot_data, x='Year', y=[col for col in plot_data.columns if col != 'Year'],
                  labels={'value': 'Volume (million m3)', 'variable': 'Type of Wastewater'},
                  title='Wastewater Discharge Trends')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
The line chart demonstrates the annual trends in agricultural and industrial wastewater discharges. 
This data helps in understanding how different sectors contribute to overall water pollution over time.
""")

# Adding the other 2 visualisations
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Agricultural Discharges to Inland Waters Over Time")
    # Aggregate the data for agricultural discharges by year
    agri_data = filtered_country_data.groupby('Year')['Agricultural (incl. forestry + fisheries) wastewater, all sources, direct discharges(million m3)'].sum().reset_index()
    fig_agri = px.line(
        agri_data, 
        x='Year', 
        y='Agricultural (incl. forestry + fisheries) wastewater, all sources, direct discharges(million m3)', 
        title='Agricultural Wastewater Discharges Over Time',
        markers=True,
        labels={'Agricultural (incl. forestry + fisheries) wastewater, all sources, direct discharges(million m3)': 'Volume (million m³)'}
    )
    fig_agri.update_layout(
        plot_bgcolor="white",
        xaxis_title="Year",
        yaxis_title="Total Volume (million m³)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True)
    )
    st.plotly_chart(fig_agri, use_container_width=True)

    st.markdown("""
This plot traces the volume of agricultural wastewater discharged into inland waters annually. 
The fluctuations indicate changes in agricultural practices and environmental policy impacts over the years.
""")

with col4:
    st.markdown("### Total Discharges to Inland Waters Over Time")
    # Aggregate the data for total discharges to inland waters by year
    total_discharge_data = filtered_country_data.groupby('Year')['Total discharges to Inland waters(million m3)'].sum().reset_index()
    fig_total = px.line(
        total_discharge_data, 
        x='Year', 
        y='Total discharges to Inland waters(million m3)', 
        title='Total Discharges to Inland Waters Over Time',
        markers=True,
        labels={'Total discharges to Inland waters(million m3)': 'Volume (million m³)'}
    )
    fig_total.update_layout(
        plot_bgcolor="white",
        xaxis_title="Year",
        yaxis_title="Total Volume (million m³)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True)
    )
    st.plotly_chart(fig_total, use_container_width=True)

    st.markdown("""
This line chart provides insights into the total volume of discharges to inland waters over time, reflecting the cumulative impact of all water-related activities on inland water bodies.
""")