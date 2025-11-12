import streamlit as st
import pandas as pd
from auth import get_user_details, get_available_users
from query_engine import get_agent_response

# --- Page Configuration ---
st.set_page_config(
    page_title="Dumroo.ai Admin Panel",
    page_icon="🤖",
    layout="wide"
)

# --- Helper Functions ---
@st.cache_data
def load_full_data():
    """Loads the complete dataset from the CSV."""
    try:
        return pd.read_csv("sample_data.csv")
    except FileNotFoundError:
        st.error("Error: sample_data.csv not found.")
        return pd.DataFrame()

def filter_data_by_scope(full_df, user_details):
    """
    Filters the main DataFrame based on the user's scope.
    This is the core RBAC logic[cite: 16].
    """
    if user_details is None:
        return pd.DataFrame() # Return empty if no user

    scope_type = user_details["scope_type"]
    scope_value = user_details["scope_value"]

    if scope_type == "grade":
        # Ensure 'grade' column is treated as integer for comparison
        full_df['grade'] = full_df['grade'].astype(int)
        return full_df[full_df["grade"] == int(scope_value)].copy()
    
    elif scope_type == "region":
        return full_df[full_df["region"] == scope_value].copy()
    
    # In a real app, you might have a 'all' scope for super-admins
    # But per the prompt, we are assuming no super-admins [cite: 12]
    else:
        return pd.DataFrame() # Default to empty if scope is unknown

# --- Main Application ---
st.title("🤖 Dumroo.ai Admin Panel")
st.markdown("Ask questions about your students in plain English. [cite: 7]")

# --- Sidebar: Authentication & Scoping ---
st.sidebar.title("Admin Controls")
st.sidebar.markdown("This simulates logging in as different users with specific permissions. [cite: 13]")

# API Key Input
openai_api_key = st.sidebar.text_input(
    "sk-...FqkA", type="password",
    help="Your key is required to power the AI agent."
)

# User Selection
available_users = get_available_users()
selected_user_name = st.sidebar.selectbox(
    "Select Admin User:",
    options=available_users,
    index=0 # Default to the first user
)

# Load and display user's scope
current_user = get_user_details(selected_user_name)
st.sidebar.info(f"""
    **User:** {selected_user_name}  
    **Role:** {current_user['role']}  
    **Scope:** `{current_user['scope_type']}` = `{current_user['scope_value']}`
    """)

# Load and filter data based on selected user's scope
full_data = load_full_data()
scoped_data = filter_data_by_scope(full_data, current_user)

# (Demo Feature) Show the admin what data they are allowed to see
with st.sidebar.expander("View Your Scoped Data"):
    st.markdown("The AI agent can **only** see this filtered data. This enforces your access role.")
    st.dataframe(scoped_data)

# --- Chat Interface (Bonus ) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# When the user changes, reset the chat
if "current_user_id" not in st.session_state or st.session_state.current_user_id != current_user["user_id"]:
    st.session_state.messages = []
    st.session_state.current_user_id = current_user["user_id"]
    st.info(f"Chat reset. You are now logged in as {selected_user_name}.")

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask a question about your students..."):
    
    # 1. Check for API key
    if not openai_api_key:
        st.error("Please enter your OpenAI API Key in the sidebar to chat.")
    # 2. Check if scoped data is empty
    elif scoped_data.empty:
        st.warning(f"No data available for your scope ({current_user['scope_type']} = {current_user['scope_value']}). Cannot answer questions.")
    # 3. Process the query
    else:
        # Add user message to UI and state
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from AI agent
        with st.spinner("The AI agent is thinking..."):
            response = get_agent_response(
                openai_api_key,
                scoped_data,
                st.session_state.messages[:-1], # Pass history *before* new prompt
                prompt
            )
        
        # Add AI response to UI and state
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})