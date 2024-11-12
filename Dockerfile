# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY ./app_streamlit.py .
COPY ./requirements.txt .

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install --no-cache-dir -r requirements.txt

ENV GROQ_API_KEY=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
ENV API_KEY=BWbYoawu0cdbkBnX6uqdeVUFd9Y4rdc3fV6k6hYy
ENV STREAMLIT_SERVER_PORT=8010
ENV STREAMLIT_SERVER_ADDRESS="0.0.0.0"

# Step 5: Run the application
CMD ["streamlit", "run", "app_streamlit.py"]
