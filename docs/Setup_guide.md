# Setup Guide - Product Launch Intelligence Agent

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher** ([Download Python](https://python.org/downloads/))
- **pip** (usually comes with Python)
- **Git** ([Download Git](https://git-scm.com/downloads))
- A **Google account** (for Google AI API)
- **Web browser** (Chrome, Firefox, Safari, or Edge)

## 🔑 API Keys Setup

### Step 1: Google AI API Key

1. **Visit Google AI Studio**
   - Go to [https://aistudio.google.com/](https://aistudio.google.com/)
   - Sign in with your Google account

2. **Create API Key**
   - Click **"Get API Key"** in the top navigation
   - Click **"Create API Key"**
   - Select **"Create API key in new project"** (recommended)
   - Copy the generated API key immediately
   - Store it securely (you won't be able to see it again)

3. **Verify Access**
   - The free tier includes generous limits
   - For production use, consider upgrading to paid tier

### Step 2: Firecrawl API Key

1. **Create Firecrawl Account**
   - Go to [https://firecrawl.dev/](https://firecrawl.dev/)
   - Click **"Sign Up"** or **"Get Started"**
   - Sign up using email or GitHub

2. **Get API Key**
   - After signing up, you'll be redirected to the dashboard
   - Navigate to **"API Keys"** section
   - Copy your API key
   - Note: Free tier includes 500 credits

3. **Check Limits**
   - Free: 500 credits/month
   - Paid plans available for higher usage

## 💻 Installation

### Method 1: Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/product-launch-intelligence-agent.git
cd product-launch-intelligence-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### Method 2: Manual Setup

1. **Download the Code**
   - Download ZIP from GitHub and extract
   - Or clone using Git (see Method 1)

2. **Create Virtual Environment**
   ```bash
   python -m venv product-intel-env
   cd product-intel-env
   Scripts\activate  # Windows
   # or
   source bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install streamlit==1.28.1
   pip install langchain==0.1.0
   pip install langchain-google-genai==1.0.0
   pip install langgraph==0.0.26
   pip install firecrawl-py==0.0.8
   pip install python-dotenv==1.0.0
   ```

## ⚙️ Configuration

### Step 1: Environment Variables

Create a `.env` file in the project root:

```bash
# Required API Keys
GOOGLE_API_KEY=your_google_ai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Optional Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Step 2: Verify Configuration

Create a test file `test_config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Test API keys
google_key = os.getenv("GOOGLE_API_KEY")
firecrawl_key = os.getenv("FIRECRAWL_API_KEY")

print("Google AI API Key:", "✅ Set" if google_key else "❌ Missing")
print("Firecrawl API Key:", "✅ Set" if firecrawl_key else "❌ Missing")

if google_key and firecrawl_key:
    print("🎉 Configuration complete!")
else:
    print("⚠️ Please set missing API keys in .env file")
```

Run the test:
```bash
python test_config.py
```

## 🚀 Running the Application

### Step 1: Start the Application

```bash
# Ensure virtual environment is activated
# Then run:
streamlit run product_launch_intelligence_agent.py
```

### Step 2: Access the Interface

- The application will automatically open in your browser
- If not, navigate to: `http://localhost:8501`
- You should see the **"AI Product Intelligence Agent"** interface

### Step 3: Initial Test

1. **Check API Status**
   - Look at the sidebar for "System Status"
   - Should show "✅ Gemini Intelligence Team ready"

2. **Run a Test Analysis**
   - Enter "Tesla Model 3" in the company field
   - Click "🚀 Analyze Strategy"
   - Wait for results (may take 30-60 seconds)

## 🛠️ Troubleshooting

### Common Issues

#### 1. Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt --upgrade
```

#### 2. API Key Errors
```
Error: Invalid API key
```
**Solution:**
- Verify API keys in `.env` file
- Check for extra spaces or quotes
- Regenerate keys if necessary

#### 3. Firecrawl Connection Issues
```
Error during search: Connection timeout
```
**Solution:**
- Check internet connection
- Verify Firecrawl API key
- Check Firecrawl service status

#### 4. Streamlit Port Issues
```
Port 8501 is already in use
```
**Solution:**
```bash
# Use different port
streamlit run product_launch_intelligence_agent.py --server.port 8502
```

#### 5. LangGraph Routing Issues
```
KeyError or routing errors
```
**Solution:**
- This is a known issue in the current code
- The conditional edges need fixing (see main analysis document)

### Debugging Steps

1. **Check Python Version**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Verify Package Versions**
   ```bash
   pip list | grep -E "(streamlit|langchain|firecrawl)"
   ```

3. **Test API Connections**
   ```python
   # Test Google AI
   from langchain_google_genai import ChatGoogleGenerativeAI
   llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
   print("Google AI:", llm.invoke("Hello").content)
   
   # Test Firecrawl
   from firecrawl import FirecrawlApp
   app = FirecrawlApp(api_key="your_key")
   print("Firecrawl:", app.search("test", page_options={"fetch_page_content": False}))
   ```

## 🔧 Advanced Configuration

### Custom Port and Host

```bash
# Run on different port
streamlit run product_launch_intelligence_agent.py --server.port 8502

# Run on all interfaces (for remote access)
streamlit run product_launch_intelligence_agent.py --server.address 0.0.0.0
```

### Environment-Specific Settings

Create separate `.env` files:
- `.env.development`
- `.env.production`
- `.env.testing`

### Docker Setup (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "product_launch_intelligence_agent.py"]
```

Build and run:
```bash
docker build -t product-intel-agent .
docker run -p 8501:8501 --env-file .env product-intel-agent
```

## 📊 Usage Examples

### Example 1: Competitor Analysis
```
Company: "Notion"
Analysis Type: Competitor Analysis
Expected Output: Launch strategy, positioning, pricing analysis
```

### Example 2: Market Sentiment
```
Company: "ChatGPT"
Analysis Type: Market Sentiment  
Expected Output: Social media sentiment, review analysis
```

### Example 3: Launch Metrics
```
Company: "Threads by Meta"
Analysis Type: Launch Metrics
Expected Output: User numbers, adoption rates, press coverage
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Monitor API usage** to avoid unexpected charges
5. **Use HTTPS** in production deployments

## 📈 Performance Optimization

### For Better Response Times:
- Use specific search queries
- Limit concurrent requests
- Cache frequently accessed data
- Monitor API rate limits

### Resource Management:
- Close browser tabs when not in use
- Restart application if memory usage is high
- Monitor API credit consumption

## 🆘 Getting Help

### If you encounter issues:

1. **Check the logs** in the terminal where Streamlit is running
2. **Search existing issues** on the GitHub repository
3. **Create a new issue** with:
   - Error message
   - Steps to reproduce
   - Your environment details
   - API key status (don't share actual keys)

### Useful Resources:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [Firecrawl Documentation](https://docs.firecrawl.dev/)

## ✅ Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned/downloaded
- [ ] Virtual environment created and activated
- [ ] Dependencies installed via `pip install -r requirements.txt`
- [ ] Google AI API key obtained and added to `.env`
- [ ] Firecrawl API key obtained and added to `.env`
- [ ] Configuration tested with `test_config.py`
- [ ] Application starts with `streamlit run product_launch_intelligence_agent.py`
- [ ] Can access interface at `http://localhost:8501`
- [ ] API status shows "✅ Gemini Intelligence Team ready"
- [ ] Test analysis completed successfully

**🎉 Congratulations! Your Product Launch Intelligence Agent is ready to use!**
