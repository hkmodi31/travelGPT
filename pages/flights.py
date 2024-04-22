import streamlit as st
from datetime import date
from flightInfo import getAirportName, getFlightPrices

st.set_page_config(
    page_title="Flights",
    page_icon="👋",
)

# Set the title of the app
st.title("Travel Itinerary Planner")
st.write("Hey! Planning a trip? Let me help you create a customized itinerary plan for your plan to travel to")

origin = st.text_input("Origin", placeholder="Boston")
destination = st.text_input("Destination", placeholder="New York City")

# Create user input field for departure date
departureDate = st.date_input("Date of Departure", format="YYYY-MM-DD")

# Calculate the minimum acceptable date for arrival
min_arrival_date = max(departureDate, date.today())

# Create user input field for arrival date
arrivalDate = st.date_input("Date of Arrival", format="YYYY-MM-DD")

# Adjust the arrival date automatically if it's before the departure date
if departureDate > arrivalDate:
    arrivalDate = departureDate
    st.warning('Arrival date was set to the same as departure date because it cannot be earlier.')

if st.button('Submit'):
    if(len(origin)!=0 and len(destination)!=0):
        originAirportName, originAirportID, destinationAirportName, destinationAirportID = getAirportName(origin, destination)
        st.write(f"Suggest airport location of origin : {originAirportName}")
        st.write(f"Suggest airport location of destination : {destinationAirportName}")

        st.write("Some suggested cheapest flights based on your dates selected!")
        st.write(getFlightPrices(originAirportID, destinationAirportID, departureDate, arrivalDate))