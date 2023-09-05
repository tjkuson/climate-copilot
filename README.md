# Climate Copilot

A climate change chatbot powered by Pinecone and OpenAI. This application is for demonstration purposes only, and is not intended for production use.

## Features

- Ask about climate change via single questions or conversationally 
- Information from the [Climate Change Committee](https://www.theccc.org.uk/)

## Get started

## Installing

Clone the repository and install the Python dependencies:

```bash
pip install -r requirements.txt
```

## API keys

You will need access to a Pinecone and OpenAI API key. Save these as environment variables. For example,

```bash
export PINECONE_API_KEY=your_pinecone_api_key
export OPENAI_API_KEY=your_openai_api_key
```

Save your Pinecone vector database information as environment variables. For example,

```bash
export PINECONE_INDEX_NAME=your_index_name
export PINECONE_ENVIRONMENT=your_index_environment
```


## Load data

Before the application can be run, you will need to load the data into Pinecone. To do this, run the following command:

```bash
python climate_copilot --load-resources
```

This will require your Pinecone and OpenAI accounts, and may take a few minutes to complete.

## Running the application

To ask a question:

```bash
python climate_copilot --ask "What is the best way to reduce my carbon footprint?"
```

To run the application in a conversational mode:

```bash
python climate_copilot
```

# Acknowledgements

Training data (found in the resources directory) is from and copyright of the [Climate Change Committee](https://www.theccc.org.uk/).

# Licence

[MIT](LICENCE)
