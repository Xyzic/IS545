#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pydeck as pdk
import numpy as np
import streamlit as st
from datetime import timedelta
import datetime
import time
import matplotlib.pyplot as plt
import altair as alt

data = pd.read_csv("https://raw.githubusercontent.com/Xyzic/IS545/main/final/datetime_Crimes.csv?token=AA6RB2VNCRKJCJNQURR467TASYBCM")
data['Date'] = pd.to_datetime(data['Date'])


# In[2]:


'''
# IS 545 Final Project - Het Patel

_Disclaimer:_ I am using the data as it is given on the Chicago City data webpage
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/data

This does not mean I agree with the data or that I claim that it is 100% valid and unbiased. 
It is just a dataset I have used for this project.

Also, there are some very sensitive topics shown. Proceed at your own discretion.
'''


# In[3]:


st.header("Crime Locations")
st.sidebar.title("Filter Data by Type(s) of Crimes")
filters = st.sidebar.multiselect(
    "What types of crimes would you like to see?",
    data["Primary Type"].unique().tolist(),
    help = "Used for the 'Crime Locations' Map"
)

st.write('Filter(s): ')
for i in filters:
    st.write(i)


# In[4]:


filtered_data = data.loc[(data['Primary Type'].isin(filters))]
latlonchic = filtered_data.filter(['Latitude', 'Longitude']).rename(columns = {"Latitude": "lat", "Longitude": "lon"}).dropna()


# In[5]:


layer = pdk.Layer(
    "ScatterplotLayer",
    data = latlonchic,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=30,          # Radius is given in meters
    get_fill_color=[255, 1, 1, 140],  # Set an RGBA value for fill
    pickable=False)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-87.6298, latitude= 41.8781, zoom=9, min_zoom=9, max_zoom=13, pitch=0, bearing=0
)

# Combined all of it and render a viewport
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state
)
st.pydeck_chart(r)


# In[6]:


st.header("Crimes Filtered by the Day")
st.sidebar.title("Filter Data by the Day")
curr_day = st.sidebar.date_input("What day of all crimes do you want to see?", datetime.date(2020, 1, 1), min_value = datetime.date(2020, 1, 1), max_value = datetime.date(2020, 12, 31), help = "Used for the 'Crimes Filtered by the Day' Map")

typeList = data["Primary Type"].unique().tolist()
currDayDF = data.loc[(data['Date'].dt.date == curr_day)]
runningtotal = {}
for key in typeList:
    temp = (currDayDF[currDayDF['Primary Type'] == str(key)])
    runningtotal[key] = len(temp.index)

st.write("Displayed Day: ", curr_day)
st.write("*Totals by Type*")
st.write(runningtotal)


# In[7]:


filtered_dayta = data.loc[(data['Date'].dt.date == curr_day)]
latlonchicday = filtered_dayta.filter(['Latitude', 'Longitude']).rename(columns = {"Latitude": "lat", "Longitude": "lon"}).dropna()


# In[8]:


daylayer = pdk.Layer(
    "ScatterplotLayer",
    data = latlonchicday,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=100,          # Radius is given in meters
    get_fill_color=[255, 1, 1, 140],  # Set an RGBA value for fill
    pickable=False)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-87.6298, latitude= 41.8781, zoom=9, min_zoom=9, max_zoom=15, pitch=0, bearing=0
)

# Combined all of it and render a viewport
r2 = pdk.Deck(
    layers=[daylayer],
    initial_view_state=view_state
)
st.pydeck_chart(r2)


# In[9]:


st.header("Totals of Crimes for a Date Range")


# In[10]:


st.sidebar.header("Totals of Types of Crimes in a Selected Date Range")
days_passed = st.sidebar.date_input("Show Crime Type Totals within this Range", min_value = datetime.date(2020, 1, 1), 
                                    max_value = datetime.date(2020, 12, 31), 
                                    value = (datetime.date(2020, 1, 1), datetime.date(2020, 1, 2)), 
                                    help = "Used for the Animated Line Chart")
req_date_init = days_passed[0].strftime("%B %d")
req_date_final = days_passed[1].strftime("%B %d")


# In[21]:


line_filters = st.sidebar.multiselect(
    "What types of crimes?",
    data["Primary Type"].unique().tolist(),
)
line_filtered_data = data.loc[(data['Primary Type'].isin(line_filters))]
st.write("Showing crimes of type(s): ", line_filters, " from ", req_date_init, " to ", req_date_final)


# In[19]:


total_data = line_filtered_data[['Date', 'Primary Type']].copy()

date_clumps = total_data.copy()
date_clumps['Date'] = total_data['Date'].dt.date

data_date_counts = date_clumps.groupby(['Date', 'Primary Type']).size().to_frame(name = "Count").reset_index()
range_data = data_date_counts.loc[(data_date_counts['Date'] >= days_passed[0]) & (data_date_counts['Date'] <= days_passed[1])]

final_data = range_data.copy()#.set_index('Date')
# final_data['Date'] = pd.to_datetime(final_data['Date'])
# final_data = final_data.set_index([final_data.index, 'Primary Type'])['Count'].unstack().fillna(0)

plot_range = alt.Chart(final_data).mark_line().encode(
    x = 'Date',
    y = 'Count',
    color = 'Primary Type'
).properties(
    width = 1400,
    height= 750
)

st.altair_chart(plot_range)


# In[12]:


st.header("Crime Traffic by Location")
st.subheader("This hex plot shows the crime density by area in the city, filtered by the sidebar")


# In[26]:


st.sidebar.title("Filter Hex Plot by Type(s) of Crimes")
hex_filters = st.sidebar.multiselect(
    "What types of crime areas would you like to see?",
    data["Primary Type"].unique().tolist(),
    help = "Used for the Hexagon Map"
)

hex_filtered_data = data.loc[(data['Primary Type'].isin(hex_filters))]
latlonchichex = hex_filtered_data.filter(['Latitude', 'Longitude']).rename(columns = {"Latitude": "lat", "Longitude": "lon"}).dropna()


layer2 = pdk.Layer(
    'HexagonLayer',
    latlonchichex,
    get_position='[lon, lat]',
    auto_highlight=True,
    elevation_scale=20,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1)

# Set the viewport location
view_state_hex = pdk.ViewState(
    longitude=-87.6298, latitude= 41.8781, zoom=9, min_zoom=8, max_zoom=13, pitch=40, bearing=50
)

# Combined all of it and render a viewport
r3 = pdk.Deck(
    layers=[layer2],
    initial_view_state=view_state_hex,
    tooltip={
        'html': '<b>Crime Count:</b> {elevationValue}',
        'style': {
            'color': 'white'
        }
    }
)
st.pydeck_chart(r3)


# In[13]:


st.header("Crime Totals throughout the Day")
st.subheader("*A histogram, binned by the hour, of total crimes taken at that hour in 2020*")


# In[14]:


hist_values = np.histogram(data['Date'].dt.hour, bins = 24, range = (0, 24))[0]
st.bar_chart(hist_values)
st.write("*Seems like midnight and noon are the most crime-heavy times.*")
st.write("*With 5 and 6 AM being the 'safest' times.*")


# In[ ]:




