import streamlit as st
from datetime import datetime

import os
import sys
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from llm.LLM import PsaOptiguide
# Get the absolute path to the directory containing this script (app.py)
current_directory = os.path.dirname(os.path.realpath(__file__))

# Add the 'modules' directory to sys.path
LLM_directory = os.path.join(current_directory, 'llm')
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


st.set_page_config(page_title="CargoLingo Advisor 🚢", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>CargoLingo Advisor 🚢</h1>", unsafe_allow_html=True)
from utils.Visualizer import Visualizer

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(string)  # Pass the new output directly
            return ret

        stdout.write = new_write
        yield

# Container box for Messages in
# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100,placeholder ="Why did the system make decision x related to supplier/demand selection,time, and location?")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        
        with st.spinner(f"Running Psa-LLM Agent {user_input}"):
            # Set 1 second timeout

            with st.expander("Show LLM Output"):
                with st_capture(st.write):
                    if user_input == "Visualize":
                        fig = Visualizer.plot_current_warehouse_capacity()
                        st.plotly_chart(fig)
                    else:
                        try:
                            output = PsaOptiguide.ask(user_input)
                        except Exception as e:
                            st.error(f"Error: {e}")
                            st.stop()



#         # Display the json output
#         st.write(f'Results: {results}')
#         st.write(f'Type of Results: {type(results)}')


#         st.session_state['past'].append(user_input)
#         st.session_state['generated'].append(results)
#         st.session_state['model_name'].append(model_name)

#         # from https://openai.com/pricing#language-models

# if st.session_state['generated']:
#     with response_container:
#         for i in range(len(st.session_state['generated'])):
#             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
#             message(st.session_state["generated"][i], key=str(i))
#             st.write(
#                 f"Model used: {st.session_state['model_name'][i]};")