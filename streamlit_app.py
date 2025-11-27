# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col #import a function from snowpark to show one column instead of the whole table
import requests # this a Python package library called requests.  The requests library allows us to build and sent REST API calls
#----------------------
st.title(f" :cup_with_straw: Customize your smoothie! :cup_with_straw: ")
st.write(  """Choose the fruits you want in your custom smoothie !  """)
#----------------------
name_on_order = st.text_input("Name of Smoothie: ")
st.write("The name on your Smoothie will be: ", name_on_order)
#------------------------
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))#show only fruit name column.
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
#---------------------
ingredients_list = st.multiselect (
    'choose up to 5 ingredients :'
    ,my_dataframe
    ,max_selections=5)
#---------------------
if ingredients_list: 
    ingredients_string = ''

    for fruit_chosen in ingredients_list: #for every fruit in the ingredients list
        ingredients_string += fruit_chosen + ' ' #add every selection to the string
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)  
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect() #execute this code       
        st.success('Your Smoothie is ordered!', icon="✅") #show up that it's successfully ordered


