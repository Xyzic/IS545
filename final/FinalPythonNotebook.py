#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd
import pydeck as pdk
import numpy as np
import streamlit as st

data = pd.read_csv("https://raw.githubusercontent.com/Xyzic/IS545/main/datasets/Crimes_2020.csv?token=AA6RB2VV5Q7Q6DIWP4VSFV3ASFU4O")

data.head()


# In[27]:


'''
# IS 545 Final Project - Het Patel

_Disclaimer:_ I am using the data as it is given on the Chicago City data webpage
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/data

This does not mean I agree with the data or that I claim that it is 100% valid and unbiased. 
It is just a dataset I have used for this project.

Also, there are some very sensitive topics shown. Proceed at your own discretion.
'''


# In[51]:


st.sidebar.title("Filter Data by Type(s) of Crimes")
filters = st.sidebar.multiselect(
    "What types of crimes would you like to see?",
    data["Primary Type"].unique().tolist()
)

st.sidebar.title("Filter Plot by Time")
times = st.sidebar.slider('Days Passed', 1, 365, 1, 1, help = 'Adjust the number of days passed in 2020')

st.write('Filter(s): ')
for i in filters:
    st.write(i)


# In[54]:


filtered_data = data.loc[(data['Primary Type'].isin(filters))]
latlonchic = filtered_data.filter(['Latitude', 'Longitude']).rename(columns = {"Latitude": "lat", "Longitude": "lon"}).dropna()


# In[58]:


layer = pdk.Layer(
    "ScatterplotLayer",
    data = latlonchic,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=150,          # Radius is given in meters
    get_fill_color=[255, 1, 1, 140],  # Set an RGBA value for fill
    pickable=True)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-87.6298, latitude= 41.8781, zoom=9, min_zoom=9, max_zoom=13, pitch=0, bearing=0
)

# Combined all of it and render a viewport
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": str(filtered_data['Date']), "style": {"color": "white"}},
)
st.pydeck_chart(r)


# In[ ]:




