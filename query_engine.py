import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.messages import AIMessage, HumanMessage

def get_agent_response(api_key, df, chat_history, user_query):
    """
    Initializes a LangChain Pandas Agent and gets a response.
    The agent is given only the *scoped_df* to ensure RBAC.
    """
    
    # Initialize the LLM
    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-3.5-turbo",
        temperature=0
    )
    
    # Create the Pandas DataFrame Agent
    # We remove the 'agent_type' parameter.
    # The agent will automatically use the correct type (OpenAI Functions)
    # because the LLM supports it.
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True # Required for pandas agent
    )
    
    # Format the chat history for the agent
    history_messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            history_messages.append(HumanMessage(content=msg["content"]))
        else:
            history_messages.append(AIMessage(content=msg["content"]))

    try:
        # Invoke the agent with the query and history
        response = agent.invoke({
            "input": user_query,
            "chat_history": history_messages
        })
        
        return response["output"]

    except Exception as e:
        print(f"Error invoking agent: {e}")
        return "Sorry, I encountered an error while processing your request."