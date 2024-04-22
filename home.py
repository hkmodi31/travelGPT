import streamlit as st
from model import getProcessedOutput

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

# Set the title of the app
st.title("Travel Itinerary Planner")
st.write("Hey! Planning a trip? Let me help you create a customized itinerary plan for your plan to travel to")

destination = st.text_input("Destination", placeholder="Ex. Boston, MA, USA")

tripType = st.selectbox(
    'Type of Trip',
    ('Romantic', 'Family', 'Adventure')
)

llm = st.selectbox(
    'LLM model',
    ('Gemma', 'OpenAI', 'Claude')
)


# Display user input
if st.button('Submit'):
    result, source = getProcessedOutput(
        llmSelected=llm,
        destination=destination, 
        tripType=tripType)
    
    st.write(result)

    st.write(f"Source:{source}")