#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pydeck as pdk
import numpy as np
import streamlit as st
import datetime

data = pd.read_csv("https://raw.githubusercontent.com/Xyzic/IS545/main/datasets/Crimes_2020.csv?token=AA6RB2VV5Q7Q6DIWP4VSFV3ASFU4O")

data.head()


# In[2]:


'''
# IS 545 Final Project - Het Patel

_Disclaimer:_ I am using the data as it is given on the Chicago City data webpage
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/data

This does not mean I agree with the data or that I claim that it is 100% valid and unbiased. 
It is just a dataset I have used for this project.

Also, there are some very sensitive topics shown. Proceed at your own discretion.
'''


# In[12]:


st.sidebar.title("Filter Data by Type(s) of Crimes")
filters = st.sidebar.multiselect(
    "What types of crimes would you like to see?",
    data["Primary Type"].unique().tolist()
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
curr_day = st.sidebar.date_input("What day of all crimes do you want to see?", datetime.date(2020, 1, 1), min_value = datetime.date(2020, 1, 1), max_value = datetime.date(2020, 12, 31))


# In[15]:


filtered_dayta = data.loc[(data['Date'].dt.date == curr_day)]
latlonchicday = filtered_dayta.filter(['Latitude', 'Longitude']).rename(columns = {"Latitude": "lat", "Longitude": "lon"}).dropna()


# In[ ]:


daylayer = pdk.Layer(
    "ScatterplotLayer",
    data = latlonchicday,
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
r2 = pdk.Deck(
    layers=[daylayer],
    initial_view_state=view_state
)
st.pydeck_chart(r2)


# In[13]:


# st.header("Crime Totals throughout the Day")

# st.cache(suppress_st_warning=True)
# data_load_state = st.text('Converting data... (This will take awhile)')
# data['Date'] = pd.to_datetime(data['Date'])
# data_load_state.text("Done!")


# In[8]:


# hist_values = np.histogram(data['Date'].dt.hour, bins = 24, range = (0, 24))[0]
# st.bar_chart(hist_values)


# In[ ]:




