# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!
    """)

Name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", Name_on_order)

#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
    ,max_selections=5
)

ingredients_string = ''
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.ORDERS(INGREDIENTS,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+Name_on_order+"""')"""

#st.write(my_insert_stmt)
#st.write(ingredients_string)
#st.stop()

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

#New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
