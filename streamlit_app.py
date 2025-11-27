# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col #import a function from snowpark to show one column instead of the whole table
import requests # this a Python package library called requests.  The requests library allows us to build and sent REST API calls
#----------------------
# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie! :cup_with_straw: ")
st.write(  """Choose the fruits you want in your custom smoothie !  """)
#----------------------
name_on_order = st.text_input("Name of Smoothie: ")
st.write("The name on your Smoothie will be: ", name_on_order)
#------------------------
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))#show only fruit name column.
#st.dataframe(data=my_dataframe, use_container_width=True)
#---------------------
ingredients_list = st.multiselect (
    'choose up to 5 ingredients :'
    ,my_dataframe
    ,max_selections=5
)
#---------------------
if ingredients_list: 
    ingredients_string = ''

    for fruit_chosen in ingredients_list: #for every fruit in the ingredients list
        ingredients_string += fruit_chosen + ' ' #add every selection to the string
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)  
    
    #st.write(ingredients_list) #show finale selection into [] and with ID
    #insert into table (SQL code)
    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients) 
    #        values ('""" + ingredients_string + """')"""

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    #Code below to insert into the table for every selection :
    # if ingredients_string:  #if the ingredient list is not null then do the below
    #    session.sql(my_insert_stmt).collect() #execute this code
    #    st.success('Your Smoothie is ordered!', icon="✅") #show up that it's successfully ordered
    ###############################
    
    time_to_insert = st.button('submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect() #execute this code
            
        st.success('Your Smoothie is ordered!', icon="✅") #show up that it's successfully ordered


