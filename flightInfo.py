import requests
import pandas as pd

headers = {
	"X-RapidAPI-Key": "d9544c65f7msh5ce45305800d6fcp102505jsnb24c2b82a436",
	"X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
}


def getAirportName(origin, destination):
    urlAutoComplete = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    originQuery = {"query":origin,"market":"US","locale":"en-US"}
    destinationQuery = {"query":destination,"market":"US","locale":"en-US"}

    responseOrigin = requests.get(urlAutoComplete, headers=headers, params=originQuery)
    responseDestination = requests.get(urlAutoComplete, headers=headers, params=destinationQuery)

    originAirport = responseOrigin.json()["data"][0]["presentation"]["suggestionTitle"]
    originAirportID = responseOrigin.json()["data"][0]["id"]

    destinationAirport = responseDestination.json()["data"][0]["presentation"]["suggestionTitle"]
    destinationAirportID = responseDestination.json()["data"][0]["id"]

    return originAirport, originAirportID, destinationAirport, destinationAirportID


def getFlightPrices(originID, destinationID, departDate, returnDate):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

    querystring = {"fromId":originID,
                "toId":destinationID,
                "departDate":departDate,
                "returnDate":returnDate,
                "adults":"1",
                "currency":"USD",
                "market":"US",
                "locale":"en-US"}

    responseFlights = requests.get(url, headers=headers, params=querystring)

    data = responseFlights.json()["data"]

    # Creating DataFrame
    operating_carrier_names = []
    flight_fares = []
    departure_dates = []
    departure_times = []

    for itinerary in data['itineraries']:
        for leg in itinerary['legs']:
            for carrier in leg['carriers']['marketing']:
                operating_carrier_names.append(carrier['name'])
                flight_fares.append(itinerary['price']['raw'])  # Store raw price for comparison
                departure_dates.append(leg['departure'].split('T')[0])
                departure_times.append(leg['departure'].split('T')[1][:5])  # Extracting only HH:MM part

    # Creating DataFrame
    df = pd.DataFrame({
        'Operating Carrier': operating_carrier_names,
        'Flight Fare': flight_fares,
        'Departure Date': departure_dates,
        'Departure Time': departure_times
    })

    # Find the lowest fare for each operating carrier
    df_min_fares = df.groupby('Operating Carrier')['Flight Fare'].min().reset_index()
    df_min_fares = df_min_fares.rename(columns={'Flight Fare': 'Lowest Fare'})

    # Merge back with original DataFrame to get complete rows
    df_unique_min_fares = pd.merge(df_min_fares, df, on=['Operating Carrier'])

    # Filter only rows where the fare matches the lowest fare
    df_unique_min_fares = df_unique_min_fares[df_unique_min_fares['Flight Fare'] == df_unique_min_fares['Lowest Fare']]
    df_unique_min_fares.reset_index(inplace=True)

    return df_unique_min_fares
