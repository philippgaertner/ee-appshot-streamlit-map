import streamlit as st
import streamlit.components.v1 as components
import folium
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(layout = 'wide')    

DATA_SOURCE = "./data/gee_app_point_data.csv"

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

from PIL import Image
zoom_1 = Image.open('img/zoom_1.png')
zoom_3 = Image.open('img/zoom_3.png')
zoom_5 = Image.open('img/zoom_5.png')
zoom_7 = Image.open('img/zoom_7.png')
zoom_9 = Image.open('img/zoom_9.png')
zoom_11 = Image.open('img/zoom_11.png')
zoom_13 = Image.open('img/zoom_13.png')
zoom_15 = Image.open('img/zoom_15.png')
zoom_17 = Image.open('img/zoom_17.png')

images = [
  zoom_1, 
  zoom_3, 
  zoom_5,
  zoom_7, 
  zoom_9,
  zoom_11,
  zoom_13,
  zoom_15,
  zoom_17
  ]


with row1_1:
    st.title("Earth Engine App Finder")
    st.write(
      """
    Creator: Philipp Gärtner | Last Update: 25/01/2022
    """)
    
    
with row1_2:
    st.write(
    """
    ##
    Earth Engine Apps are dynamic, shareable user interfaces for Earth Engine analyses. The <a href="https://github.com/samapriya/ee-appshot">ee-appshot repository</a> creates a weekly snapshot of available Earth Engine Apps and provides their URL’s and script source codes.
    """,unsafe_allow_html=True)
    
    st.markdown("**_Earth Engine App Finder_** analyzes the script source codes, extracts the **Map.setCenter(lon,lat,zoom)** infos and provides the app location. <span style='color:#20A386FF;'>**_Click a point in the map - the Earth Engine App will open in a new browser tab!_**</span>",unsafe_allow_html=True)
    

col1, col2, col3, col4, col5, col6, col7, col8,col9,col10,col11, col12,col13,col14,col15,col16,col17,col18= st.columns([1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7])

with col1:
  st.write("")

with col2:
  st.image(zoom_1, width = 110, caption="zoom 1")

with col3:
  st.write("")
  
with col4:
  st.image(zoom_3, width = 110,caption="zoom 3")

with col5:
  st.write("")  
  
with col6:
  st.image(zoom_5, width = 110,caption="zoom 5")

with col7:
  st.write("")
  
with col8:
  st.image(zoom_7, width = 110,caption="zoom 7")

with col9:
  st.write("")   
  
with col10:
  st.image(zoom_9, width = 110,caption="zoom 9")

with col11:
  st.write("")   
  
with col12:
  st.image(zoom_11, width = 110,caption="zoom 11")

with col13:
  st.write("")  
  
with col14:
  st.image(zoom_13, width = 110,caption="zoom 13")

with col15:
  st.write("")
  
with col16:
  st.image(zoom_15, width = 110,caption="zoom 15")

with col17:
  st.write("")   
  
with col18:
  st.image(zoom_17, width = 110,caption="zoom 17")  

      
st.text("")
st.text("")

row2_1, row2_2 = st.columns((3,2))


with row2_1:
    zoom_filter = st.slider("Select a range of 'zoom' values", 1, 18, (8, 16), step=1)

# Reading the data

@st.cache
def load_data():
    data = pd.read_csv(DATA_SOURCE, sep=';', decimal=',')
    data['zoom'] = data['zoom'].fillna(5)
    data['zoom'] = data['zoom'].astype(int)
    return data


def _plot_dot(point, map_element, color_col, radius=4, weight=1, color='black'):
    color_dict = {
      0: "#440154FF",1: "#481568FF",2: "#482677FF",3: "#453781FF",
      4: "#3F4788FF",5: "#39558CFF",6: "#32648EFF",7: "#2D718EFF",
      8: "#287D8EFF",9: "#238A8DFF",10: "#1F968BFF",11: "#20A386FF",
      12:"#29AF7FFF",13: "#3CBC75FF",14: "#56C667FF",15: "#74D055FF",
      16: "#94D840FF",17:"#B8DE29FF",18: "#DCE318FF",19: "#FDE725FF"
      }

    folium.CircleMarker(location=[point["lat"], point["lon"]], radius=radius, weight=weight,
                        color=color, fill=True,
                        fill_color=color_dict[point[color_col]],
                        fill_opacity=0.9,
                        tooltip="<b>Click me!</b>",
                        popup="<a href='" +  point["url"] + "' target='_blank'>" +  point["url"] + "</a>"
                        ).add_to(map_element)


def generate_map(df):
    map_element = folium.Map(location=[15, 15], zoom_start=2, tiles='cartodbdark_matter')

    df.apply(_plot_dot, axis=1, args=[map_element, "zoom"])

    return map_element


def folium_static(fig, width=800, height=500):
    if isinstance(fig, folium.Map):
        fig = folium.Figure().add_child(fig)

    return components.html(fig.render(), height=(fig.height or height) + 10, width=width)



if __name__ == "__main__":
  
    
    df = load_data()
    
    dict_years = {}

    mask = (df['zoom'] >= zoom_filter[0]) & (df['zoom'] <= zoom_filter[1])

    df_filtered = df.loc[mask]


    for zoom in df_filtered['zoom'].unique():
        dict_years[zoom] = generate_map(df_filtered)


# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row3_1, row3_2= st.columns((2,1))    


domain = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
range_ = ["#481568FF", "#482677FF", "#453781FF", "#3F4788FF", "#39558CFF" ,"#32648EFF" ,"#2D718EFF",
  "#287D8EFF", "#238A8DFF", "#1F968BFF", "#20A386FF" ,"#29AF7FFF" ,"#3CBC75FF", "#56C667FF", "#74D055FF",
 "#94D840FF", "#B8DE29FF" ,"#DCE318FF" 
 ]    


with row3_1:
  folium_static(dict_years[zoom_filter[1]])
  
  
hist = alt.Chart(df_filtered).mark_bar(size = 15).encode(
    y=alt.Y("zoom", axis=alt.Axis(title='Zoom levels', tickMinStep=1)),
    x=alt.X('count()', axis=alt.Axis(title='Number of Apps')),
    color=alt.Color("zoom", scale=alt.Scale(domain=domain, range=range_),
    legend=alt.Legend(title="Used 'zoom' levels by color", orient="bottom")),
    opacity=alt.value(0.7)
).properties(
    width=300,
    height=400
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)  
  

with row3_2:
  st.write("**Distribution of zoom levels**")
  row3_2.altair_chart(hist, use_container_width=True)   
   
