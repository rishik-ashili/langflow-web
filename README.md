# Media-matic 

# Check out our project & demo video here:
https://langflow.streamlit.app/ -website
https://www.youtube.com/watch?v=5aWgZfuJEHU - demo video

## Overview
An intelligent analytics solution that helps you understand and optimize your social media performance. Built with cutting-edge technology, our platform provides deep insights for data-driven social media strategy decisions.

## Features

* **Real-time Analytics**: Track engagement metrics across your social media accounts using DataStax's powerful data processing capabilities
* **User-Friendly Interface**: Explore your social data through an intuitive web interface powered by Streamlit
* **AI-Driven Insights**: Uncover meaningful patterns and actionable insights using advanced analytics powered by LangFlow

## Technologies Used
- LangFlow
- DataStax
- Streamlit
- Python 3.8+

## Prerequisites
- Python 3.8 or higher
- DataStax account
- LangFlow API key
---

## Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-media-analytics.git
cd social-media-analytics
```

### 2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys and configuration
```

## Usage

### 1. Start the Streamlit application:
```bash
streamlit run app.py
```

### 2. Navigate to `http://localhost:8501` in your web browser

### 3. Connect your social media accounts through the settings panel

### 4. Start analyzing your social media performance!

## Configuration

Configure your application by setting the following environment variables in `.env`:

```
DATASTAX_API_KEY=your_datastax_api_key
LANGFLOW_API_KEY=your_langflow_api_key
```

## How to Use

1. **Enter Your Query**
   - Type your analysis request in the main text box
   - Supports natural language questions about your social media performance

2. **Run the Analysis**
   - Click the "Analyze" button to process your query
   - The system will evaluate your data using AI-powered analytics

3. **Review Results**
   - Analysis results appear instantly below the input area
   - View detailed metrics, trends, and actionable insights
   - Access your complete chat history to track previous analyses

**Note**: Each analysis provides visualization of key metrics, sentiment analysis of engagement, and customized recommendations based on your social media data.

## Project Structure
- main.py: Main application file containing the Streamlit app logic.
- requirements.txt: List of dependencies required for the project.

## Acknowledgments

- DataStax team for their excellent database solution
- LangFlow community for AI analytics capabilities
- Streamlit team for the amazing web framework


https://github.com/user-attachments/assets/6d927861-f642-4852-a4d4-ca207bc2c4a9

