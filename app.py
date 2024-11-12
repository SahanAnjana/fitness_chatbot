import os
from langchain_groq import ChatGroq as LangChainGroq
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
import spacy
import requests
import streamlit as st
import time  # to create the streaming effect

# Set up API keys and environment
API_KEY = 'BWbYoawu0cdbkBnX6uqdeVUFd9Y4rdc3fV6k6hYy'
BASE_URL = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}'
os.environ["GROQ_API_KEY"] = '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'

# Load NLP model for food name extraction
nlp = spacy.load("en_core_web_sm")

# Initialize LangChain model
llm = LangChainGroq(model="mixtral-8x7b-32768")

# Tool 1: Food name extraction tool
def extract_food_name(text):
    doc = nlp(text)
    food_names = [ent.text for ent in doc.ents if ent.label_ == 'FOOD']
    return food_names

food_extraction_tool = Tool(
    name="Food Name Extractor",
    func=extract_food_name,
    description="Extracts food names from user input text."
)

# Tool 2: Nutrition information retrieval tool
def get_nutrition_info(food_item):
    params = {'query': food_item, 'pageSize': 1}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        return None, f"Error: Unable to retrieve data for {food_item} (status code {response.status_code})."
    
    data = response.json()
    if data.get('foods'):
        food_data = data['foods'][0]
        food_name = food_data.get('description')
        nutrients = food_data.get('foodNutrients')
        
        nutrition_details = "\n".join([f"• {nutrient['nutrientName']}: {nutrient['value']} ({nutrient['unitName']})" for nutrient in nutrients])
        return food_name, nutrition_details
    return None, "No nutrition information found."

nutrition_retrieval_tool = Tool(
    name="Nutrition Info Retriever",
    func=get_nutrition_info,
    description="Retrieves nutrition information for a given food item from the USDA API."
)

# Create prompt template for the Groq LLM response
prompt_template = PromptTemplate(
    input_variables=["nutrition_name", "nutrition_info"],
    template="The user asked about {nutrition_name}. Provide more details about its nutrition and usage in fitness. \n\nHere are the nutritional details:\n{nutrition_info}"
)

# Define the RAG agent
agent = initialize_agent(
    tools=[food_extraction_tool, nutrition_retrieval_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    prompt=prompt_template,
    handle_parsing_errors=True
)

# Streamlit app interface with conversational capability
st.title("Nutrition Chatbot")

# Add CSS to align user messages to the right
st.markdown("""
<style>
.chat-message {
    padding: 8px;
    margin: 8px 0;
    width: fit-content;
    border-radius: 12px;
}
.user-message {
    background-color: #DCF8C6;
    color: #303030;
    margin-left: auto;
    text-align: right;
}
.bot-message {
    background-color: #F0F0F0;
    color: #303030;
}
</style>
""", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Accept user input through chat input widget
if prompt := st.chat_input("Ask about a food item:"):
    # Display user message in chat message container
    st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response from the agent
    response = agent.run(prompt)
    
    # Display assistant response in chat message container with streaming effect
    bot_message_placeholder = st.empty()
    full_response = ""
    
    # Split response into words for streaming effect
    for word in response.split():
        full_response += word + " "
        bot_message_placeholder.markdown(f'<div class="chat-message bot-message">{full_response}</div>', unsafe_allow_html=True)
        time.sleep(0.05)  # Adjust the sleep duration to control speed
    
    # Append full bot response to chat history
    st.session_state.messages.append({"role": "bot", "content": full_response})
