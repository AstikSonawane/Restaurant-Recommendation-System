import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from PIL import Image
#img = Image.open('image.png')
# Define HTML/CSS style with background image
html_style = """
<style>
    [data-testid="stAppViewContainer"]{
    background-image: url('https://images.unsplash.com/photo-1599458252573-56ae36120de1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZmluZSUyMGRpbmluZyUyMHJlc3RhdXJhbnR8ZW58MHwwfDB8fHwy');
            background-size: cover; /* Scale the background image to be as large as possible */
        background-position: center; /* Center the background image */
        height: 100%; /* Set height to 100% to cover the whole page */
    }
    }

    /* CSS styling goes here */
    body {
        font-family: Times New Roman, Serif;
        /* Set background image */
        #background-image: url('https://media.timeout.com/images/106001846/1024/576/image.webp');
        /* Set background size */
        background-size: cover;
        /* Set background position */
        background-position: center;
      
        /* Set font color to black */
        color: #ffffff;
    }

    .container {
        opacity:0.9;
        padding: 20px;
        border: 1px solid #ffffff;
        border-radius: 5px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        
    }

    h1 {
        opacity:0.9;
        color: #ffffff;
        font-size: 30px;
        margin-bottom: 20px;
        
    }

    p {
        opacity:0.9;
        color: #ffffff;
        font-size: 50px;
        line-height: 1.5;
        
    }
</style>
"""

# Render HTML/CSS style
st.markdown(html_style, unsafe_allow_html=True)

# Render Streamlit content
st.title("Restaurant Recommendation System")

# Data reading
data = pd.read_csv(r'C:\Users\HOME\Desktop\DSA\Project\resto.csv', delimiter='|')

# Displaying No of rows X No of Columns
#st.write("Data Shape:", data.shape)

# displaying first 5 contents of data by default
#st.write("Data Info:", data.info())
# Replace '-' with a default rating of 4.5
data['RATING'] = data['RATING'].replace('-', 4.5)
# EDA Process

# Data Cleaning

# Identifying duplicate values from data
data.dropna(axis=0, how='any', inplace=True)
data.drop_duplicates(inplace=True, keep=False)
data.drop(columns=['CITY', 'URL', 'PAGE NO', 'VOTES'], inplace=True)

# No null values in data now

# Renaming columns
data.rename({'CUSINE_CATEGORY': 'CUISINE', 'CUSINE TYPE': 'OUTLET_TYPE', 'RATING_TYPE': 'REVIEWS'}, axis=1, inplace=True)

# Cleaning Reviews column to English only
data['REVIEWS'].replace(to_replace='Excelente' , value='Excellent', inplace=True)
data['REVIEWS'].replace(to_replace=['Veľmi dobré','Bardzo dobrze','Muy Bueno','Velmi dobré'] , value='Very Good', inplace=True)
data['REVIEWS'].replace(to_replace=['Skvělá volba','Dobrze','Bueno','Buono','Dobré','Bom','Skvělé'] , value='Good', inplace=True)
data['REVIEWS'].replace(to_replace=['Priemer','Média','Çok iyi'] , value='Average', inplace=True)
data['REVIEWS'].replace(to_replace=['Průměr','Promedio','Ortalama','Muito Bom','İyi'] , value='Poor', inplace=True)
data['REVIEWS'].replace(to_replace=['Baik','Biasa','Media','Sangat Baik'] , value='Very Poor', inplace=True)
data['REVIEWS'].replace(to_replace=['None'] , value='Not Rated', inplace=True)

# Cleaning region column
data['REGION'] = data['REGION'].str.replace('[a-zA-Z].+-- ', '', regex=True)
data['REGION'] = data['REGION'].str.replace(' West| west| East| east', '', regex=True)

data['REGION'] = data['REGION'].str.replace('4 Bungalows|7 Andheri|Azad Nagar|Near Andheri Station|Veera Desai Area|Mahakali', 'Andheri', regex=True)
data['REGION'] = data['REGION'].str.replace('Bandra Kurla Complex', 'Bandra', regex=True)
data['REGION'] = data['REGION'].str.replace('CBD-Belapur', 'CBD Belapur', regex=True)
data['REGION'] = data['REGION'].str.replace('Girgaon Chowpatty', 'Chowpatty', regex=True)
data['REGION'] = data['REGION'].str.replace('Dadar Shivaji Park', 'Dadar', regex=True)
data['REGION'] = data['REGION'].str.replace('Flea Bazaar Café|Kamala Mills Compound', 'Lower Parel', regex=True)
data['REGION'] = data['REGION'].str.replace('Runwal Green', 'Mulund', regex=True)
data['REGION'] = data['REGION'].str.replace('Mumbai CST Area', 'Mumbai Central', regex=True)
data['REGION'] = data['REGION'].str.replace('Kopar Khairane|Seawoods|Turbhe|Ulwe', 'Navi Mumbai', regex=True)
data['REGION'] = data['REGION'].str.replace('New Panvel|Old Panvel', 'Panvel', regex=True)
data['REGION'] = data['REGION'].str.replace('Kamothe', 'Sion', regex=True)
data['REGION'] = data['REGION'].str.replace('Ghodbunder Road|Majiwada', 'Thane', regex=True)



# Change datatype of columns
data = data.astype({'NAME': str, 'PRICE': pd.Int32Dtype(), 'CUISINE': str, 'OUTLET_TYPE': 'category', 'REVIEWS': 'category', 'RATING': float})


# Testing Deployment

# Finding Restaurants!

place = st.selectbox("Enter the locality to dine in:", ['Dadar', 'Thane', 'Airoli', 'Andheri', 'Bandra','Kalyan', 'CBD Belapur', 'Lower Parel', 'Mulund', 'Mumbai Central', 'Panvel'])

place_df = data[data['REGION'].str.lower().str.contains(place.lower())]

# Sorting by user desired cuisine
cuisine_options = ['Indian', 'Chinese', 'Italian', 'Mexican', 'American', 'Japanese','Seafood', 'Thai', 'Mediterranean', 'French', 'Greek']
cuisine = st.selectbox("Select cuisine:", cuisine_options)

cuisine_df = place_df[place_df['CUISINE'].str.lower().str.contains(cuisine.lower())]

price = st.selectbox("Sort by price:", ['High to Low', 'Low to High'])

if price == 'High to Low':
    price_sort = cuisine_df.sort_values(by='PRICE', ascending=False)
elif price == 'Low to High':
    price_sort = cuisine_df.sort_values(by='PRICE', ascending=True)

price_sort.reset_index(drop=True, inplace=True)


st.write(price_sort)
