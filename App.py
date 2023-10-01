import streamlit as st
from datetime import datetime

import os
import sys
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from llm.LLM import PsaOptiguide
from llm.Agent_main import AgentMain
from plotly import graph_objects as go

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

# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
# os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
# os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
# os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT


st.set_page_config(page_title="CargoLingo Advisor 🚢", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>CargoLingo Advisor 🚢</h1>", unsafe_allow_html=True)


@contextmanager
def st_capture():
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            # output_func(string)  # Pass the new output directly

            with open("./logs/output.txt", "w") as f:
                f.write(string)

            return ret

        stdout.write = new_write
        yield

        # write stdout to file
        with open("./logs/output.txt", "w") as f:
            f.write(stdout.getvalue())

@contextmanager
def st_capture2(output_func):
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
            with st.expander("Show LLM Output",expanded=True):
                with st_capture2(st.markdown):
                    try:
                        question_output = AgentMain.ask(user_input)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.stop()

            if isinstance(question_output, go.Figure):
                # Return Streamlit plotly figure
                st.plotly_chart(question_output)
                        
            elif question_output == user_input:
                with st_capture():
                    try:
                        output = PsaOptiguide.ask(user_input)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.stop()

                with open("./logs/output.txt", "r") as f:
                    output = f.read()
                    output = output.split("--------------------------------------------------------------------------------")


                    seen = []
                    for i in range(len(output) - 1):
                        if(output[i] in seen):
                            continue

                        seen.append(output[i])
                        if("to user" in output[i]):
                            with st.expander(f"Final answer to human"):
                                st.write(output[i])

                            break
                        elif("Gurobi" in output[i]):
                            with st.expander(f"Gurobi optimizer output"):
                                st.write(output[i])

                        elif("safeguard" in output[i]):
                            with st.expander(f"Checking if code is safe to run"):
                                st.markdown(f'''```python {output[i]} ''')

                        else:
                            with st.expander(f"Intermediate thought {i + 1}"):
                                st.write(output[i])

            else:
                """Means its non relevant question"""
                st.write(f"**{question_output}**")

            



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
