import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''
url = 'https://taxifare-419896309165.europe-west1.run.app/predict'


if url == 'https://taxifare-419896309165.europe-west1.run.app/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')
    #---------------------------------------------------
    date_time = st.date_input("Enter the date of the ride and time", value=datetime.date.today())
    t = st.time_input('Set the time for the ride on', datetime.time(8, 45))
    if date_time is not None:
       pickup_datetime = datetime.datetime.combine(date_time, t).strftime('%Y-%m-%d %H:%M:%S')
    else:
        st.error("Please select a valid date.")

    #st.write('The time of the ride is:', t)
    #st.write("The time of the ride is:", date_time)
    #---------------------------------------------------

    # Generate random data for demonstration
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"]
    )

    # Display the map for the user to view
    st.write("Map of the area")
    st.map(df)

    # Input fields for pickup location
    st.write("Enter Pickup Location")
    pickup_latitude = st.number_input("Pickup Latitude", value=37.76)
    pickup_longitude = st.number_input("Pickup Longitude", value=-122.4)

    # Input fields for dropoff location
    st.write("Enter Dropoff Location")
    dropoff_latitude = st.number_input("Dropoff Latitude", value=37.76)
    dropoff_longitude = st.number_input("Dropoff Longitude", value=-122.4)



    #---------------------------------------------------
    passenger_count = st.number_input("Passenger Count", value=1)


'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

dict_parameters = {
    "pickup_datetime": pickup_datetime,
    "pickup_latitude": pickup_latitude,
    "pickup_longitude": pickup_longitude,
    "dropoff_latitude": dropoff_latitude,
    "dropoff_longitude": dropoff_longitude,
    "passenger_count": passenger_count
}

response = requests.get(url, params=dict_parameters)

# Check if the response is successful
if response.status_code == 200:
    try:
        prediction = response.json()
        st.write("The pickup date-time is", dict_parameters['pickup_datetime'])
        st.write('The number of passengers is', dict_parameters['passenger_count'])
        st.write("The price of the ride is:", round(prediction['fare']*100, 2), "dollars")
    except ValueError:
        st.error("Error parsing the response. The response is not a valid JSON.")
else:
    st.error(f"API request failed with status code {response.status_code}.")
    st.write("Response content:", response.text)
