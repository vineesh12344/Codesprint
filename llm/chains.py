import openai
import numpy as np
import os
from dotenv import load_dotenv
import os
from collections import deque
from typing import Dict, List, Optional, Any
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
# Langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain ,LLMCheckerChain
from langchain.callbacks import wandb_tracing_enabled
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    StringPromptTemplate
)

from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)


path_to_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print('path_to_root: ', path_to_root)

# Load variables from the .env file
load_dotenv(os.path.join(path_to_root, '.env'))

# Access the variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2=os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT=os.getenv("LANGCHAIN_ENDPOINT")
# Access the variables

# Set the environment variables
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT

classifier_llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=1)
classifier_article_schema = {
    "name": "binary_classifier_article_schema",
    "description": "Binary Classifier Schema for Article, is a disruption event or not",
    "type": "object",
    "properties": {
      "isDisruptionEvent": {
        "type": "boolean"
      },
      "disruptionType":{
        "type": "string",
        "description": "Type of disruption event. Must be one of the example the Full list given in conditions"
      },
      "Reason": {
        "type": "string",
        "description": "Reason for your decision"
      }
    },
    "required": ["isDisruptionEvent","disruptionType","Reason"]
  }

classifierprompt = PromptTemplate(
    template = """Role:You are a Binary Classifier,your goal is to classify if the given news article is a vaild disruption event article or not.
    Conditions:
    1. A disruption event can be defined as "An event that potentially impacts the supply chain and have a vaild disruption type".
    Full List of possible disruption types: a) Airport Disruption b) Bankruptcy c) Business Spin-off d) Business Sale e) Chemical Spill f) Corruption g) Company Split h) Cyber Attack i) FDA/EMA/OSHA Action j) Factory Fire k) Fine l) Geopolitical m) Leadership Transition n) Legal Action o) Merger & Acquisition p) Port Disruption q) Protest/Riot r) Supply Shortage a) Earthquake b) Extreme Weather c) Flood d) Hurricane e) Tornado f) Volcano g) Human Health h) Power Outage.
    2. The disruption event the news article is reporting, must be a 'live' event, meaning it is currently happening. Not an article reporting on a past event.

    Article Title:{articleTitle}\n{articleText}\nEnd of article\n\nFeedback:{feedback}\n

    TASK: Given youre Role and the Conditions, Classify if the given news article is a vaild disruption event article or not.A vaild disruption event article is classified as "An event that potentially impacts the supply chain and have a vaild disruption type",  Select the disruption type only based on the given full list of possible disruption types. Think through and give reasoning for your decision. Must Output boolean value for isDisruptionEvent.
    """,
    input_variables=["articleTitle","articleText","feedback"]
)

articleClassifier = create_structured_output_chain(output_schema=classifier_article_schema,llm = classifier_llm,prompt=classifierprompt)