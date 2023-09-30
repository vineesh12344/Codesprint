import streamlit as st
from datetime import datetime

import os
import sys
# Get the absolute path to the directory containing this script (app.py)
current_directory = os.path.dirname(os.path.realpath(__file__))

# Add the 'modules' directory to sys.path
# LLM_directory = os.path.join(current_directory, 'llm')
# Supabase_directory = os.path.join(current_directory, 'Supabase')
# utils_directory = os.path.join(current_directory, 'utils')
# sys.path.append(Supabase_directory)
# sys.path.append(LLM_directory)
# sys.path.append(utils_directory)

# Get the OpenAI API key 
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
LANGCHAIN_TRACING_V2 = st.secrets["LANGCHAIN_TRACING_V2"]
LANGCHAIN_ENDPOINT = st.secrets["LANGCHAIN_ENDPOINT"]
LANGCHAIN_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
LANGCHAIN_PROJECT = st.secrets["LANGCHAIN_PROJECT"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT


st.set_page_config(page_title="Disruption Monitoring (Mirxes)", page_icon=":robot_face:")


