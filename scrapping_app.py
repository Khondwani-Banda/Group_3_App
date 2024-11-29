import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit.components.v1 as components

st.markdown("<h1 style='text-align: center; color: orange;'>GROUP 3 DAKAR AUTO WEBSCRAPER APP</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="color: orange;">
<h1>🚗 Explore the World of Cars, Motorcycles and Some Rented Cars with Ease!</h1>

Welcome to our app, your ultimate tool for seamless <strong>web scraping</strong> from <strong>Dakar-Auto</strong>, a premier platform for car enthusiasts!  
We've designed this app to make your data exploration and analysis effortless and exciting. Here's what you can do:  

✨ <strong>Features at a Glance</strong>:  
<ul>
<li>Scrape <strong>detailed car listings</strong> across multiple pages from Dakar-Auto.</li>  
<li>Instantly <strong>download uncleaned data</strong> directly from the app—no scraping required.</li>  
</ul>

🔧 <strong>Powered by Cutting-Edge Tools</strong>:  
Our app leverages the magic of Python, built with the following robust libraries:  
<ul>
<li><strong>`seaborn`</strong> for stunning data visualizations.</li>  
<li><strong>`pandas`</strong> for efficient data manipulation.</li>  
<li><strong>`requests`</strong> and <strong>`bs4`</strong> (Beautiful Soup) for powerful web scraping.</li>  
<li><strong>`streamlit`</strong> for an intuitive and interactive user experience.</li>  
<li><strong>`base64`</strong> for quick data encoding.</li>  
</ul>

🌐 <strong>Data Source</strong>:  
Dive into the treasure trove of automotive data at <a href="https://dakar-auto.com/" style="color: blue;"><strong>Dakar-Auto</strong></a>.  

Unleash the power of data and fuel your insights today! 🚀  
</div>
""", unsafe_allow_html=True)


st.markdown(
    """
    <style>
    /* Header background with complementary dark color */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #1C1F26, #292D33);
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.5); /* Subtle shadow */
    }

    /* Text color inside header */
    header[data-testid="stHeader"] * {
        color: #E0E0E0;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)





# Background function 
def add_bg_from_local(image_file):
        
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
        background-image: url(data:image/jpg;base64,{encoded_string.decode()});
        background-size: cover;
        background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# background image 
add_bg_from_local("circles-background-dark-tones_60389-166.jpg") 

 

# CSS to style the sidebar navigation
st.markdown(
    """
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #4CAF50;  /* Green background */
        color: black;  /* White text */
    }

    /* Sidebar header style */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white;  /* Set headers in the sidebar to white */
    }

    /* Button styles in the sidebar */
    .stButton>button {
        font-size: 14px;
        height: 3em;
        width: 100%;
        background-color: #3e8e41;  /* Darker green */
        color: black;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;  /* Lighter green on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)



def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def pick(dataframe, title, key, key1) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key1):
        # st.header(title)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key = key)





# Scraping functions
def scrape_vehicles(pages):
    """Scrape vehicle data from URL 1."""
    df = pd.DataFrame()
    for p in range(1, pages + 1):
        url = f'https://dakar-auto.com/senegal/voitures-4?&page={p}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')
        data = []
        for container in containers:
            try:
                gen_inf = container.find('h2', class_='listing-card__header__title mb-md-2 mb-0').text.split()
                brand = gen_inf[0]
                year = gen_inf[-1]
                price = container.find('h3', class_='listing-card__header__price font-weight-bold text-uppercase mb-0').text.strip().replace('\u202f', '').replace(' F CFA', '')
                address = container.find('span', class_='province font-weight-bold d-inline-block').text.strip()
                gen_inf2 = container.find_all('li', class_='listing-card__attribute list-inline-item')
                km_driven = gen_inf2[1].text.strip().replace(' km', '')
                gearbox = gen_inf2[2].text.strip()
                fuel = gen_inf2[3].text.strip()
                owner = container.find('p', class_='time-author m-0').text.strip()
                data.append({'brand': brand, 'year': year, 'price': price, 'address': address, 'kilometrage': km_driven, 'gearbox': gearbox, 'fuel': fuel, 'owner': owner})
            except Exception:
                pass
        df = pd.concat([df, pd.DataFrame(data)], axis=0).reset_index(drop=True)
    return df

def scrape_motorcycles(pages):
    """Scrape motorcycle data from URL 2."""
    df = pd.DataFrame()
    for p in range(1, pages + 1):
        url = f'https://dakar-auto.com/senegal/motos-and-scooters-3?&page={p}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')
        data = []
        for container in containers:
            try:
                gen_info = container.find('h2', class_='listing-card__header__title mb-md-2 mb-0').text.strip().split()
                brand = gen_info[0]
                year = gen_info[-1]
                price = container.find('h3', class_='listing-card__header__price font-weight-bold text-uppercase mb-0').text.strip().replace('\u202f', '').replace(' F CFA', '')
                address = container.find('div', class_='col-12 entry-zone-address').text.strip().replace('\n', '')
                kms_driven = container.find_all('li', class_='listing-card__attribute list-inline-item')[1].text.strip().replace(' km', '')
                owner = container.find('p', class_='time-author m-0').text.strip()
                data.append({'brand': brand, 'year': year, 'price': price, 'address': address, 'kms_driven': kms_driven, 'owner': owner})
            except Exception:
                pass
        df = pd.concat([df, pd.DataFrame(data)], axis=0).reset_index(drop=True)
    return df

def scrape_rentals(pages):
    """Scrape rental car data from URL 3."""
    data = []
    for page in range(1, pages + 1):
        url = f"https://dakar-auto.com/senegal/location-de-voitures-19?page={page}"
        res = get(url)
        if res.status_code != 200:
            continue
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')
        for container in containers:
            try:
                brand = container.find('h2', class_='listing-card__header__title mb-md-2 mb-0').text.strip().split()[0]
                year = container.find('h2', class_='listing-card__header__title mb-md-2 mb-0').text.strip().split()[-1]
                address = container.find('div', class_='col-12 entry-zone-address').text.strip().replace('\n', '')
                owner = container.find('p', class_='time-author m-0').text.strip().replace('Par', '').split()
                owner = ' '.join(owner)
                price = container.find('h3', class_='listing-card__header__price font-weight-bold text-uppercase mb-0').text.strip().replace(' F CFA', '').replace('\u202f', '')
                data.append({'brand': brand, 'year': year, 'price': price, 'address': address, 'owner': owner})
            except Exception:
                pass
    return pd.DataFrame(data)










# Sidebar Options
st.sidebar.header('Navigation Options')
option = st.sidebar.selectbox(
    "Choose an action:",
    [
        'Scrape Data with BeautifulSoup and View Cleaned Data',
        'Download Uncleaned Data',
        'View Dashboard',
        'Fill App Evaluation Form'
    ]
)






st.sidebar.header('Scraping Parameters')
pages_to_scrape = st.sidebar.number_input(
    "Number of Pages to Scrape", min_value=1, max_value=2753, step=1
)

# Actions
if option == 'Scrape Data with BeautifulSoup and View Cleaned Data':
    

    vehicle_data = scrape_vehicles(pages_to_scrape)
    motorcycle_data = scrape_motorcycles(pages_to_scrape)
    rental_data = scrape_rentals(pages_to_scrape)

    pick(vehicle_data, 'Vehicle Data', '1', '200')
    pick(motorcycle_data, 'Motor Cycles Data', '2', '202')
    pick(rental_data, 'Rental Cars Data', '3', '203')

elif option == 'Download Uncleaned Data':
    Vehicles = pd.read_csv('vehicles.csv')
    Motors = pd.read_csv('motors.csv')
    Rented = pd.read_csv('rented.csv')

    pick(Vehicles, 'Vehicle Data', '1', '200')
    pick(Motors, 'Motor Cycles Data', '2', '202')
    pick(Rented, 'Rental Cars Data', '3', '203')


elif option == 'View Dashboard': 
    # Load data
    df1 = pd.read_csv('Vehicle_data.csv')
    df2 = pd.read_csv('Motors_data.csv')
    df3 = pd.read_csv('Rented_data.csv')

    # classification of condition of car based on the mileage
    
    df1['condition'] = df1['kilometrage'].apply(lambda x: 'almost_new' if x < 50000 else 'used')
    df2['condition'] = df2['kms_driven'].apply(lambda x: 'almost_new' if x < 50000 else 'used')


    # Set Seaborn style
    sns.set_style("whitegrid")
    
    # Create dashboard layout
    col1, col2 = st.columns(2)

    # Top 5 Vehicle Brands Sold
    with col1:
        plot1 = plt.figure(figsize=(10, 6))
        sns.barplot(
            x=df1["brand"].value_counts()[:5].index, 
            y=df1["brand"].value_counts()[:5].values, 
            palette="viridis"
        )
        plt.title("Top 5 Most Sold Vehicle Brands", fontsize=14)
        plt.xlabel("Brand", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        st.pyplot(plot1)

    # Top 5 Motorcycle Brands Sold
    with col2:
        plot2 = plt.figure(figsize=(10, 6))
        sns.barplot(
            x=df2["brand"].value_counts()[:5].index, 
            y=df2["brand"].value_counts()[:5].values, 
            palette="rocket"
        )
        plt.title("Top 5 Most Sold Motorcycle Brands", fontsize=14)
        plt.xlabel("Brand", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        st.pyplot(plot2)

    # Next row
    col3, col4 = st.columns(2)

    # Price Trend Over the Years for Vehicles
    with col3:
        plot3 = plt.figure(figsize=(10, 6))
        sns.lineplot(data=df1, x="year", y="price", hue="condition", palette="muted")
        plt.title("Price Variation by Year (Vehicles)", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Price", fontsize=12)
        plt.legend(title="Condition")
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        st.pyplot(plot3)

    # Price Trend Over the Years for Motorcycles
    with col4:
        plot4 = plt.figure(figsize=(10, 6))
        sns.lineplot(data=df2, x="year", y="price", hue="condition", palette="coolwarm")
        plt.title("Price Variation by Year (Motorcycles)", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Price", fontsize=12)
        plt.legend(title="Condition")
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        st.pyplot(plot4)

    # Additional Visualizations
    col5, col6 = st.columns(2)

    # Distribution of Vehicle Prices
    with col5:
        plot5 = plt.figure(figsize=(10, 6))
        sns.histplot(data=df1, x="price", kde=True, bins=30, color="teal")
        plt.title("Distribution of Vehicle Prices", fontsize=14)
        plt.xlabel("Price", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        st.pyplot(plot5)

    # Distribution of Motorcycle Prices
    with col6:
        plot6 = plt.figure(figsize=(10, 6))
        sns.histplot(data=df2, x="price", kde=True, bins=30, color="purple")
        plt.title("Distribution of Motorcycle Prices", fontsize=14)
        plt.xlabel("Price", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        st.pyplot(plot6)


else:
    
    st.header("App Evaluation Form")
    components.html("""
    <iframe src=https://ee.kobotoolbox.org/i/Q9BVJrI0 width="800" height="600"></iframe>
    """,height=1100,width=800)
