import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner!')

st.header('Breakfast Favourites!')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-boiled Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Import pandas
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

# Create the repeatable code block called a function
def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error(str(e))

# Snowflake-related functions
st.header("The fruit load list contains:")
def get_fruit_load_list(connection):
    with connection.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# Add button to load the fruit
if st.button('Get Fruit Load List'):
    snowflake_connection = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(snowflake_connection)
    st.dataframe(my_data_rows)

