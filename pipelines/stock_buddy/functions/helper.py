from vnstock3 import Vnstock
from langchain_core.messages import HumanMessage, AIMessage
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI

# Helper function to create a pandas dataframe agent
def create_dataframe_agent(df, **kwargs):
    return create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0.1, model="gpt-4o-mini"),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True,
        **kwargs
    )

# Helper function to get the last human message from the state
def get_last_human_message(state):
    return next((m for m in reversed(state['messages']) if isinstance(m, HumanMessage)), None)



# Function to invoke the agent with the dataframe
def invoke_agent_with_dataframe(state, df, **kwargs):
    agent = create_dataframe_agent(df, **kwargs)
    last_human_message = get_last_human_message(state)
    answer = agent.invoke({
        "input": last_human_message.content,
        "chat_history": state['messages']
    })
    return answer
