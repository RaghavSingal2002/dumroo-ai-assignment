# Dumroo.ai - AI Developer Assignment

This project implements an AI-powered chat system for the Dumroo Admin Panel. It allows admins to ask natural language questions about student data, with a critical feature: **Role-Based Access Control (RBAC)**.

The system enforces RBAC by filtering the dataset *before* it is passed to the AI agent, ensuring an admin can only access data within their assigned scope (e.g., their specific grade or region).

This solution is built using Python, Streamlit, Pandas, and LangChain.

## Features

* **Natural Language Queries:** Ask questions like "how many students failed the quiz?".
* **Strict RBAC:** Admins are selected via a dropdown. The data is filtered *before* the AI sees it, guaranteeing security.
* **Streamlit Interface:** A clean, interactive web app for demo purposes (Bonus).
* **Conversational Memory:** The agent can answer follow-up questions (Bonus).
* **Modular Code:** The logic is split into `auth.py`, `query_engine.py`, and `app.py` for maintainability (Bonus).

## Setup & Running

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-link>
    cd dumroo-ai-assignment
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

5.  **Use the App:**
    * Open the app in your browser (usually `http://localhost:8501`).
    * Enter your **OpenAI API Key** in the sidebar.
    * Select a **mock admin user** from the dropdown.
    * Ask questions in the chat box!

## Example Queries 

Try these queries after selecting an admin (e.g., **Ms. Davis - Grade 8**):

* `"Which students haven't submitted their homework yet?"` 
* `"What is the average quiz score for my students?"`
* `"How many students are in class A?"`
* `"Show me the names of students who scored below 70 on the quiz."`

**To test the RBAC:**
* Log in as **Ms. Davis (Grade 8)** and ask: `"How many students are in Grade 9?"`
* The agent will correctly answer **"zero"** or **"I don't see any students in Grade 9"** because its data (the `scoped_data`) contains *only* Grade 8 students.
