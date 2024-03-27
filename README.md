# Chat With a Websites from URL
This GitHub repository hosts the Chat With Websites project. It is a chatbot capable of interacting with websites, extracting information, and communicating in a user-friendly manner. The project seamlessly integrates the powerful capabilities of LangChain with a Streamlit graphical user interface to enhance the overall user experience.

## Features
- **Website Interaction**: The chatbot uses the latest version of LangChain to interact with and extract information from various websites.
- **Intelligent Communication**: Communicate with the chatbot naturally and receive relevant responses.
- **Streamlit GUI**: A clean and intuitive user interface built with Streamlit, making it accessible for users with varying levels of technical expertise.
- **Python-based**: Entirely coded in Python.

## How it Looks and Works 
##### For demo play video!
https://github.com/Shashank1130/Chat-With-Websites/assets/107529934/8c266f39-033b-41b7-bb58-fbeec24c9dba


## Brief explanation of how RAG works

A RAG bot is short for Retrieval-Augmented Generation. This means that we are going to "augment" the knowledge of our LLM with new information that we are going to pass in our prompt. We first vectorize all the text that we want to use as "augmented knowledge" and then look through the vectorized text to find the most similar text to our prompt. We then pass this text to our LLM as a prefix.

![Untitled design](https://github.com/Shashank1130/Chat-With-Websites/assets/107529934/9d3db91c-36f8-430b-8061-436f6d678699)

## Installation

Ensure you have Python installed on your system. Then clone this repository:

```bash
git clone https://github.com/your-username/chat-with-websites.git
cd chat-with-websites
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create your own .env file with the following variables:

```bash
OPENAI_API_KEY=[your-openai-api-key]
```

## Usage
To run the Streamlit app:

```bash
streamlit run app.py
```


