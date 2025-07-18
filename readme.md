# **AI Product Intelligence Agent (Gemini Edition)**

A streamlined intelligence hub for Go-To-Market (GTM) and Product Marketing teams, powered by a multi-agent system running on Google's Gemini model.

This application transforms scattered public web data into concise, actionable launch insights. It leverages a coordinated team of specialized AI agents, built with **LangChain/LangGraph**, to perform deep analysis on competitor launches, market sentiment, and performance metrics.

## **✨ Features**

* **Multi-Agent Coordination**: A sophisticated team of AI agents works together, managed by a supervisor who delegates tasks and synthesizes results.  
* **Specialized Roles**:  
  * **🔍 Product Launch Analyst**: Delivers an evidence-backed breakdown of a rival's launch strategy, including positioning, differentiators, and channel mix.  
  * **💬 Market Sentiment Specialist**: Consolidates social media chatter and review themes, highlighting key positive and negative drivers.  
  * **📈 Launch Metrics Specialist**: Scours the web for publicly available KPIs like adoption numbers, press coverage, and user engagement signals.  
* **Powered by Gemini**: Utilizes Google's powerful **Gemini 1.5 Pro** model for high-quality analysis and reasoning.  
* **Live Web Access**: Integrates with **Firecrawl** to search and scrape real-time data from the web, ensuring insights are current and relevant.  
* **Interactive UI**: A clean and intuitive user interface built with **Streamlit**, allowing for easy interaction and clear presentation of results.  
* **Secure API Key Handling**: Standard sidebar inputs for securely providing API keys.

## **🛠️ How It Works: The Multi-Agent Architecture**

This application uses **LangGraph** to create a cyclic, stateful graph that represents the team of agents. This allows for more complex and realistic agent interactions than a simple chain.

1. **The Supervisor**: Acts as the team lead. When a user makes a request, the Supervisor is the first to see it. Its job is to analyze the request and delegate it to the most appropriate specialist agent.  
2. **The Specialists**: Each specialist (Launch Analyst, Sentiment Specialist, Metrics Specialist) is an expert in its domain. It receives the task from the Supervisor, uses its tools (Search and Crawl) to gather information from the web, and then formulates a detailed report.  
3. **The Final Report**: The specialist's report is sent back to the Supervisor. The Supervisor reviews the report and, if it meets the requirements, formats it into a final, polished response for the user. This ensures the output is consistent and high-quality.

This coordinated workflow allows the system to handle complex queries by breaking them down and assigning them to the right "expert," mimicking how a real human intelligence team operates.

## **🚀 Tech Stack**

* **Frontend**: [Streamlit](https://streamlit.io/)  
* **Backend & Agent Framework**: [LangChain](https://www.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)  
* **LLM**: [Google Gemini 1.5 Pro](https://deepmind.google/technologies/gemini/)  
* **Web Scraping/Crawling**: [Firecrawl](https://firecrawl.dev/)  
* **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/)

## **⚙️ Setup and Installation**

Follow these steps to run the application on your local machine.

### **1\. Clone the Repository**

git clone https://github.com/ZidanMau24/Product_Intelegent_Agent
cd /Product_Intelegent_Agent

### **2\. Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage dependencies.

\# For Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

### **3\. Install Dependencies**

Install all the required Python packages from the requirements.txt file.

pip install \-r requirements.txt

### **4\. Configure API Keys**

The application requires API keys for Google AI (Gemini) and Firecrawl.

Create a file named .env in the root of your project directory and add your keys in the following format:

GOOGLE\_API\_KEY="your\_google\_ai\_api\_key\_here"  
FIRECRAWL\_API\_KEY="your\_firecrawl\_api\_key\_here"

Alternatively, you can enter the keys directly into the application's sidebar when you run it.

## **▶️ How to Run**

Once the setup is complete, you can launch the Streamlit application with the following command:

streamlit run product\_launch\_intelligence\_agent.py

The application will open in your default web browser, ready for you to start analyzing\!
