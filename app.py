import streamlit as st
from swarm import Swarm, Agent
from duckduckgo_search import DDGS
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up Streamlit app configuration
st.set_page_config(page_title="Emzy ChatNet", page_icon="🌐")
st.header('Chatbot with Internet Access')
st.write('Equipped with internet access, enables users to ask questions and make research')

# Function to set OpenAI API key dynamically in the session state
def set_openai_api_key():
    """Prompts the user to enter the OpenAI API Key."""
    api_key_input = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key_input:
        os.environ['OPENAI_API_KEY'] = api_key_input
        st.success("OpenAI API Key set successfully!")
    else:
        st.warning("Please enter your OpenAI API Key to continue.")

# Input for OpenAI API Key
st.subheader("OpenAI API Key Setup")
set_openai_api_key()

# Initialize Swarm client only after API key is set
if 'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY']:
    # Initialize the Swarm client after API key is entered
    client = Swarm()
else:
    st.error("Please enter a valid OpenAI API key.")

# Initialize DuckDuckGo Search Client
ddgs = DDGS()

# Function to search the web for the given query using DuckDuckGo
def search_web(query):
    """Search DuckDuckGo for the query and return the results."""
    print(f"Searching the web for {query}...")
    
    try:
        # Format current date for the search
        current_date = datetime.now().strftime("%Y-%m")
        
        # Perform search using DuckDuckGo API
        results = ddgs.text(f"{query} {current_date}", max_results=10)
        
        # Check if results are returned
        if results:
            news_results = ""
            for result in results:
                news_results += f"**Title**: {result['title']}\n**URL**: {result['href']}\n**Description**: {result['body']}\n\n"
            return news_results.strip()
        else:
            return f"No results found for '{query}'."
    except Exception as e:
        return f"An error occurred while searching the web: {str(e)}"

# Define Web Search Agent to gather the latest news on specified topics
web_search_agent = Agent(
    name="Web Search Assistant",
    instructions="Your role is to gather the latest news articles on specified topics using DuckDuckGo's search capabilities.",
    functions=[search_web]
)

# Define Researcher Agent to analyze and synthesize the raw search results
researcher_agent = Agent(
    name="Research Assistant",
    instructions="""Your role is to analyze and synthesize the raw search results:
    1. Remove duplicates and redundant content.
    2. Identify and merge related topics and themes.
    3. Verify consistency across sources.
    4. Prioritize relevant information.
    5. Extract key facts, statistics, and quotes.
    6. Flag contradictions.
    7. Maintain attribution and proper context."""
)

# Define Writer Agent to transform research results into a polished article
writer_agent = Agent(
    name="Writer Assistant",
    instructions="""Your role is to turn the deduplicated research results into a polished article:
    1. Organize the content into sections.
    2. Maintain a professional and engaging tone.
    3. Ensure proper flow and readability.
    4. Add relevant context where needed.
    5. Ensure factual accuracy and clarity.
    6. Format the article with proper headings."""
)

# Function to run the complete workflow (search, analyze, write)
def run_workflow(query):
    """Run the complete workflow: search -> analyze -> write"""
    try:
        # 1. Search the web
        search_response = client.run(
            agent=web_search_agent,
            messages=[{"role": "user", "content": f"Search the web for {query}"}],
        )
        raw_news = search_response.messages[-1]["content"]
        st.write(raw_news)

        # 2. Analyze and synthesize the results
        research_response = client.run(
            agent=researcher_agent,
            messages=[{"role": "user", "content": raw_news}],
        )
        deduplicated_news = research_response.messages[-1]["content"]

        # 3. Write the final polished article
        final_response = client.run(
            agent=writer_agent,
            messages=[{"role": "user", "content": deduplicated_news}],
            stream=True,  # Enable streaming for large content
        )
        return final_response
    except Exception as e:
        return f"An error occurred during the workflow: {str(e)}"

# Streamlit app interface
def main():
    """Main function to run the Streamlit app"""
    st.title("Emzy Internet Research Assistant 🔎")
    st.write("Use this assistant to gather and generate research-based articles with internet access.")

    # Initialize session state for query and article if not set
    if 'query' not in st.session_state:
        st.session_state.query = ""
    if 'article' not in st.session_state:
        st.session_state.article = ""

    # Create two columns for the input and the clear button
    col1, col2 = st.columns([3, 1])

    # Input field for search query
    with col1:
        query = st.text_input("Enter your search query:", value=st.session_state.query)

    # Clear button to reset the search and article content
    with col2:
        if st.button("Clear"):
            st.session_state.query = ""
            st.session_state.article = ""
            st.experimental_rerun()

    # Button to generate the article based on the search query
    if st.button("Generate Article") and query:
        with st.spinner("Generating article..."):
            try:
                st.write(f"Running workflow for query: {query}")
                streaming_response = run_workflow(query)
                st.session_state.query = query
                full_response = ""
                message_placeholder = st.empty()

                # Streaming response
                for chunk in streaming_response:
                    if isinstance(chunk, dict) and 'delim' in chunk:
                        continue
                    if isinstance(chunk, dict) and 'content' in chunk:
                        content = chunk['content']
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.article = full_response
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Display the article if available
    if st.session_state.article:
        st.markdown(st.session_state.article)

if __name__ == "__main__":
    main()
