# Nutrition Chatbot

This repository contains a Nutrition Chatbot built using Streamlit, LangChain, and the USDA Food Data Central API. The chatbot helps users retrieve nutritional information about various food items and provides detailed information on their nutritional content and fitness-related benefits.

## Features

- **NLP-powered Food Name Extraction**: Extracts food names from user inputs using Spacy.
- **Nutrition Information Retrieval**: Fetches nutrition details from the USDA Food Composition Database API.
- **Conversational Interface**: Utilizes LangChain for RAG-based conversational capabilities.
- **Streaming Responses**: Provides a streaming response effect in the chatbot UI.
- **Dockerized Deployment**: Deploy the application on any server with Docker.

## Technologies Used

- **Streamlit**: For creating a user-friendly chatbot interface.
- **LangChain**: For managing and running conversational responses.
- **Spacy**: For extracting food names from user input.
- **USDA Food Data Central API**: For retrieving food nutritional information.
- **Docker**: For easy deployment in a containerized environment.

## Setup

### Prerequisites

- **Python 3.8+** installed on your local machine.
- **Docker** installed for containerized deployment.
- **API Key** for USDA Food Data Central (register and obtain at [USDA API](https://fdc.nal.usda.gov/api-key-signup.html)).

### Clone the Repository

```bash
git clone https://github.com/SahanAnjana/fitness_chatbot.git
cd fitness_chatbot
```

### Install Requirements

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Environment Variables

Add your API keys as environment variables:

- **USDA API Key**: Add your USDA Food Data Central API key in the `API_KEY` variable.
- **LangChain API Key**: Add your LangChain API key in the `GROQ_API_KEY` variable.

Alternatively, you can set these environment variables in a `.env` file.

### Run the Application Locally

Run the Streamlit application:

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` to use the chatbot.

## Docker Deployment

The Docker setup enables you to deploy the chatbot on any server with Docker installed.

### Build Docker Image

```bash
docker build -t nutrition-chatbot .
```

### Run Docker Container

```bash
docker run -d -p 8501:8501 --env GROQ_API_KEY=<your_groq_api_key> --env API_KEY=<your_usda_api_key> nutrition-chatbot
```

### Access the Application

Once the container is running, access the chatbot at `http://your-server-ip:8501`.

## Project Structure

```plaintext
.
├── app.py                 # Main Streamlit app file
├── Dockerfile             # Dockerfile for containerized deployment
├── requirements.txt       # Project dependencies
└── README.md              # Documentation (this file)
```

## Configuration

In the Dockerfile, `enableCORS` and `enableXsrfProtection` have been disabled to allow cross-origin requests and prevent XSRF issues. This is intended for controlled environments; enable them in production for better security.

## Troubleshooting

### CORS or XSRF Issues

If you encounter CORS or XSRF issues, make sure your environment settings are correct or configure your reverse proxy to handle these restrictions.

### LangChain Errors

Ensure that your `GROQ_API_KEY` and USDA `API_KEY` are correctly set and have the required permissions.

## License

This project is licensed under the MIT License.

---
