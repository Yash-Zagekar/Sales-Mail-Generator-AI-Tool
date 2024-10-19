import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


# Function to inject custom CSS for font styling and background color
def set_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700&display=swap');

        /* Apply Quicksand font to all elements */
        html, body, [class*="css"] {
            font-family: 'Quicksand', sans-serif;
        }

        /* Background color for the entire app */
        .main {
            background-color: #0b090a; 
        }

        /* Title style */
        h2, h3 {
            font-family: 'Quicksand', sans-serif;
        }
         h1 {
            font-family: 'Jost', sans-serif;
        }
        

        /* Remove default styling for text input field */
        .stTextInput {
            border: none;  /* Remove default border */
            padding: 0;  /* Remove default padding */
        }

        /* Custom styles for input fields */
        .stTextInput input {
            font-family: 'Quicksand', sans-serif;
            border-radius: 15px;  /* Curved border */
            border: 2px solid #9d4edd;  /* Border color */
            padding: 10px;  /* Add padding for better appearance */
            outline: none;  /* Remove outline */
        }

        /* Add hover effect for input field */
        .stTextInput input:hover {
            border-color: #6a1b9a;  /* Change border color on hover */
        }
    
        
        

        </style>
        """,
        unsafe_allow_html=True
    )


def display_links():
    st.markdown(
        """
        <style>
        .box {
            border: 1px dashed #9d4edd;  /* Changed to dashed border with purple color */
            padding: 10px;
            border-radius: 8px;
            font-family: 'Quicksand', sans-serif;
            font-size: 14px;
        }
        </style>

    <div class="box">
    <strong>💡Note: </strong>
    <p style="margin: 0;">🔷Ensure the URLs you provide are valid and contain accurate descriptions of the job postings</p>
    <p style="margin: 0;">Following are test links:</p>
    <p style="margin: 0;">https://japan-dev.com/jobs/geniee/geniee-aigenerative-ai-engineer-ixsc0h</p>
    <p style="margin: 0;">https://japan-dev.com/jobs/rakuten/rakuten-project-manager---technology-platforms-office-6fals7</p>
    </div>

        """,
        unsafe_allow_html=True
    )


def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("<h1 style='font-family: Jost;color: #9d4edd;'>📧 SALES MAIL GENERATOR</h1>", unsafe_allow_html=True)

    url_input = st.text_input("Enter a URL:")
    submit_button = st.button("Submit")
    display_links()
    st.markdown("----------------------------------------------------------------------------------------------------------")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    set_custom_css()  # Call the function to set custom CSS
    create_streamlit_app(chain, portfolio, clean_text)
