# test Gurobi installation
import gurobipy as gp
from gurobipy import GRB
from eventlet.timeout import Timeout

# import auxillary packages
import re
import requests  # for loading the example source code
import openai
import os

# import flaml and autogen
from flaml import autogen
from flaml.autogen.agentchat import Agent, UserProxyAgent
from optiguide.optiguide import OptiGuideAgent

autogen.oai.ChatCompletion.start_logging()
current_directory = os.path.dirname(os.path.abspath(__file__))


from .Agent import user,agent
class PsaOptiguide:
    """
    Main Wrapper class for the OptiGuideAgent for the PSA Port Operations use case.
    """

    @classmethod
    def ask(cls,message:str):
        """Main method for asking questions to the OptiGuideAgent """
        output = user.initiate_chat(agent, message=f"{message}")
        return output
