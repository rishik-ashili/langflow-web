import streamlit as st
import pandas as pd
import altair as alt
import requests
from typing import Optional
import time
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

# Add this function after the imports
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Constants for API
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a251ca29-c516-4b2d-b0a8-dc39c2749687"
FLOW_ID = "6d5828af-a6a8-4f2a-8117-1b580b738600"
APPLICATION_TOKEN = "AstraCS:zIMiMHfACfDXmrduRByGfNwD:c2631f6e5d03624c1363432bc44679a76195623944816dfb6ddcb2cedeeb2d98"
TWEAKS = {
    "ChatInput-9vauS": {},
    "ChatOutput-TojAu": {},
    "OpenAIModel-SPpeb": {},
    "File-pcWQi": {},
    "AstraDB-H0bkV": {},
    "OpenAIEmbeddings-59oyL": {},
    "Prompt-4Mipb": {},
    "ParseData-fWDBv": {},
    "AstraDB-Rk1Mh": {},
    "OpenAIEmbeddings-diXrs": {},
    "SplitText-Qz9ua": {}
}

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'history' not in st.session_state:
    st.session_state.history = []

# API Function
def run_flow(message: str, endpoint: str, output_type: str = "chat", input_type: str = "chat", 
             tweaks: Optional[dict] = None, application_token: Optional[str] = None) -> dict:
    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
        payload = {
            "input_value": message,
            "output_type": output_type,
            "input_type": input_type,
        }
        if tweaks:
            payload["tweaks"] = tweaks
        headers = {
            "Authorization": f"Bearer {application_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Page config
st.set_page_config(page_title="Media-matic", layout="wide")

# Modified get_data function
@st.cache_data
def get_data(period='last_30_days'):
    current_date = datetime.now()
    
    if period == 'last_30_days':
        days = 30
    elif period == 'last_90_days':
        days = 90
    else:
        days = 7
        
    dates = pd.date_range(end=current_date, periods=days)
    
    data = []
    post_types = ['Reel', 'Static Image', 'Carousel']
    
    for date in dates:
        for post_type in post_types:
            data.append({
                'Date': date,
                'Post Type': post_type,
                'Likes': np.random.randint(500, 5000),
                'Comments': np.random.randint(50, 500),
                'Shares': np.random.randint(1000, 50000),
                'Views': np.random.randint(1000, 10000)
            })
    
    return pd.DataFrame(data)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Dashboard", "Analysis", "Visualization", "Templates", "Settings"],
        icons=['house', 'graph-up', 'bar-chart', 'file-text', 'gear'],
        menu_icon="cast",
        default_index=0,
    )
    
    if st.button('Toggle Theme'):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    
    period = st.selectbox(
        "Select Time Period",
        ["Last 7 days", "Last 30 days", "Last 90 days"],
        key="time_period"
    )

# Dynamic styling based on theme
theme_bg_color = "#1E1E1E" if st.session_state.theme == 'dark' else "#ffffff"
theme_text_color = "#ffffff" if st.session_state.theme == 'dark' else "#000000"
container_bg_color = "#2D2D2D" if st.session_state.theme == 'dark' else "#f0f2f6"

# Header styling
st.markdown(f"""
    <style>
    .title {{
        text-align: center;
        padding: 20px;
        color: {theme_text_color};
    }}
    .stButton > button {{
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: #45a049;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    .input-container {{
        background-color: {container_bg_color};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    .analysis-container {{
        background-color: {container_bg_color};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    </style>
    <div class="title">
        <h1>Media-matic</h1>
        <h3>AI-powered Social Media Analyst</h3>
    </div>
    """, unsafe_allow_html=True)

# Main content based on selection
if selected == "Dashboard":
    # Loading animation
    with st.spinner("Loading dashboard..."):
        lottie_loading = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_x62chJ.json")
        st_lottie(lottie_loading, speed=1, height=200, key="loading")
    
    df = get_data(period.lower().replace(" ", "_"))
    
    # Enhanced Metrics Summary with animations
    st.markdown("### 📊 Key Metrics Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("👍 Total Likes", df['Likes'].sum()),
        ("💭 Total Comments", df['Comments'].sum()),
        ("🔄 Total Shares", df['Shares'].sum()),
        ("👀 Total Views", df['Views'].sum())
    ]
    
    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.metric(
                label=label,
                value=f"{value:,}",
                delta=f"{np.random.randint(-10, 20)}% vs last period"
            )

    # Trend Analysis
    st.markdown("### 📈 Trend Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Time series chart
        fig_trend = px.line(
            df.groupby('Date')[['Likes', 'Comments', 'Shares']].mean().reset_index(),
            x='Date',
            y=['Likes', 'Comments', 'Shares'],
            title='Engagement Metrics Over Time'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Post type performance
        fig_performance = px.bar(
            df.groupby('Post Type')[['Likes', 'Comments', 'Shares']].mean().reset_index(),
            x='Post Type',
            y=['Likes', 'Comments', 'Shares'],
            title='Average Performance by Post Type',
            barmode='group'
        )
        st.plotly_chart(fig_performance, use_container_width=True)

    # Engagement Distribution
    st.markdown("### 📊 Engagement Distribution")
    fig_dist = px.box(
        df,
        y=['Likes', 'Comments', 'Shares'],
        title='Engagement Metrics Distribution'
    )
    st.plotly_chart(fig_dist, use_container_width=True)

elif selected == "Analysis":
    # Header section with styling
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #1f1f1f;'>🤖 AI-Powered Content Analysis</h2>
            <p style='color: #4f4f4f;'>Enter your prompt below to get AI-powered insights about your social media content.</p>
        </div>
    """, unsafe_allow_html=True)

    # Input container with consistent styling
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Add the analysis animation
    lottie_analysis = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
    st_lottie(lottie_analysis, height=200, key="analysis_animation")
    
    # Input area
    message = st.text_area("💭 Enter your prompt:", height=100, 
                          placeholder="e.g., Analyze the performance of my recent Instagram posts...")
    
    # Center the analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze", use_container_width=True)
    
    if analyze_button and message:
        try:
            with st.spinner("🤔 Analyzing your content..."):
                response = run_flow(
                    message=message,
                    endpoint=FLOW_ID,
                    output_type="chat",
                    input_type="chat",
                    tweaks=TWEAKS,
                    application_token=APPLICATION_TOKEN
                )

                if "error" in response:
                    st.error("❌ Analysis failed. Please try again.")
                else:
                    st.success("✅ Analysis complete!")
                    
                    # Extract and display results
                    try:
                        final_output = (
                            response.get("outputs", [{}])[0]
                            .get("outputs", [{}])[0]
                            .get("results", {})
                            .get("message", {})
                            .get("text", "No analysis available.")
                        )
                        
                        # Results container
                        st.markdown("""
                            <div style='background-color: #ffffff; 
                                      padding: 20px; 
                                      border-radius: 10px; 
                                      box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                                      margin-top: 20px;'>
                                <h3 style='color: #1f1f1f; margin-bottom: 20px;'>
                                    <span style='margin-right: 10px;'>🎯</span>Analysis Results
                                </h3>
                                <div style='background-color: #f8f9fa; 
                                          padding: 20px; 
                                          border-radius: 10px; 
                                          color: #1f1f1f; 
                                          font-size: 16px; 
                                          line-height: 1.6;'>
                        """, unsafe_allow_html=True)
                        
                        # Format and display the analysis text
                        st.markdown(final_output, unsafe_allow_html=True)
                        
                        st.markdown("</div></div>", unsafe_allow_html=True)
                        
                        # Add to history
                        st.session_state.history.append({
                            'prompt': message,
                            'response': final_output,
                            'timestamp': datetime.now()
                        })
                        
                    except Exception as e:
                        st.error(f"Error processing analysis: {str(e)}")
                        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again later.")
    
    elif analyze_button:
        st.warning("⚠️ Please enter a message")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display history section
    if st.session_state.history:
        st.markdown("""
            <div style='margin-top: 30px;'>
                <h3>📜 Previous Analyses</h3>
            </div>
        """, unsafe_allow_html=True)
        
        for item in reversed(st.session_state.history[-5:]):
            with st.expander(f"Analysis from {item['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                st.markdown("**Prompt:**")
                st.write(item['prompt'])
                st.markdown("**Response:**")
                st.markdown(item['response'], unsafe_allow_html=True)

elif selected == "Visualization":
    st.markdown("### 📊 Data Visualization")
    
    data = get_data(period.lower().replace(" ", "_"))
    df = pd.DataFrame(data)

    # Download options in sidebar
    st.sidebar.markdown("### 📥 Download Options")
    
    # Download full data
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="📄 Download Full Data (CSV)",
        data=csv,
        file_name='social_media_metrics.csv',
        mime='text/csv',
    )
    
    # Download specific metrics
    metric_options = st.sidebar.multiselect(
        "Select metrics to download:",
        ['Likes', 'Comments', 'Shares', 'Views'],
        default=['Likes', 'Comments']
    )
    
    if metric_options:
        selected_data = df[['Date', 'Post Type'] + metric_options].to_csv(index=False)
        st.sidebar.download_button(
            label="📄 Download Selected Metrics (CSV)",
            data=selected_data,
            file_name='selected_metrics.csv',
            mime='text/csv',
        )

    # Metrics Summary with enhanced styling
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: #1f1f1f;'>📈 Key Metrics Summary</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👍 Total Likes", f"{df['Likes'].sum():,}", 
                 delta=f"{np.random.randint(-10, 20)}% vs last period")
    with col2:
        st.metric("💭 Total Comments", f"{df['Comments'].sum():,}", 
                 delta=f"{np.random.randint(-10, 20)}% vs last period")
    with col3:
        st.metric("🔄 Total Shares", f"{df['Shares'].sum():,}", 
                 delta=f"{np.random.randint(-10, 20)}% vs last period")
    with col4:
        st.metric("👀 Total Views", f"{df['Views'].sum():,}", 
                 delta=f"{np.random.randint(-10, 20)}% vs last period")

    # Charts with enhanced styling and loading animation
    with st.spinner('✨ Generating visualizations...'):
        time.sleep(1)
        
        # First row of charts
        st.markdown("### 📊 Engagement Metrics by Post Type")
        col1, col2 = st.columns(2)

        with col1:
            likes_chart = alt.Chart(df).mark_bar().encode(
                x='Post Type',
                y='Likes',
                color=alt.Color('Post Type', scale=alt.Scale(scheme='category10')),
                tooltip=['Post Type', 'Likes']
            ).properties(
                title='Average Likes by Post Type',
                height=300
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            st.altair_chart(likes_chart, use_container_width=True)

        with col2:
            comments_chart = alt.Chart(df).mark_bar().encode(
                x='Post Type',
                y='Comments',
                color=alt.Color('Post Type', scale=alt.Scale(scheme='category10')),
                tooltip=['Post Type', 'Comments']
            ).properties(
                title='Average Comments by Post Type',
                height=300
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            st.altair_chart(comments_chart, use_container_width=True)

        # Second row of charts
        st.markdown("### 📈 Performance Metrics")
        col3, col4 = st.columns(2)

        with col3:
            shares_chart = alt.Chart(df).mark_bar().encode(
                x='Post Type',
                y='Shares',
                color=alt.Color('Post Type', scale=alt.Scale(scheme='category10')),
                tooltip=['Post Type', 'Shares']
            ).properties(
                title='Average Shares by Post Type',
                height=300
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            st.altair_chart(shares_chart, use_container_width=True)

        with col4:
            views_chart = alt.Chart(df).mark_bar().encode(
                x='Post Type',
                y='Views',
                color=alt.Color('Post Type', scale=alt.Scale(scheme='category10')),
                tooltip=['Post Type', 'Views']
            ).properties(
                title='Average Views by Post Type',
                height=300
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            st.altair_chart(views_chart, use_container_width=True)

        # Time series analysis
        st.markdown("### 📅 Trend Analysis")
        trend_chart = alt.Chart(df).mark_line().encode(
            x='Date:T',
            y='Likes:Q',
            color='Post Type:N',
            tooltip=['Date', 'Post Type', 'Likes']
        ).properties(
            title='Engagement Trends Over Time',
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        st.altair_chart(trend_chart, use_container_width=True)

        # Interactive metrics selector
        st.markdown("### 🔍 Custom Metric Analysis")
        selected_metric = st.selectbox(
            "Choose metric to analyze:",
            ['Likes', 'Comments', 'Shares', 'Views']
        )
        
        custom_chart = alt.Chart(df).mark_bar().encode(
            x='Post Type:N',
            y=f'{selected_metric}:Q',
            color=alt.Color('Post Type', scale=alt.Scale(scheme='category10')),
            tooltip=['Post Type', selected_metric]
        ).properties(
            title=f'{selected_metric} by Post Type',
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        st.altair_chart(custom_chart, use_container_width=True)

elif selected == "Templates":
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #1f1f1f;'>📑 Analysis Templates</h2>
            <p style='color: #4f4f4f;'>Choose a template to quickly analyze specific aspects of your social media performance.</p>
        </div>
    """, unsafe_allow_html=True)

    # Simplified templates with specific prompts
    templates = {
        "Engagement Analysis": {
            "description": "Analyze engagement metrics across different post types and time periods",
            "prompt": "Analyze the engagement metrics for our social media posts including engagement rates, best performing content, and trends over time."
        },
        "Content Performance": {
            "description": "Evaluate how different content types perform across metrics",
            "prompt": "Evaluate the performance comparison between Reels, Images, and Carousels, including views, shares, and engagement metrics."
        },
        "Audience Insights": {
            "description": "Understand audience behavior and preferences",
            "prompt": "Analyze our audience behavior including engagement patterns and content preferences."
        },
        "Competitor Analysis": {
            "description": "Compare performance against industry benchmarks",
            "prompt": "Compare our social media performance with industry standards including engagement rates and content strategy."
        }
    }

    # Template selection
    template_type = st.selectbox(
        "Select Analysis Template",
        list(templates.keys())
    )
    
    # Display template description
    st.markdown(f"""
        <div style='background-color: #ffffff; padding: 15px; border-radius: 10px; margin: 10px 0;'>
            <p style='color: #1f1f1f; margin: 0;'><strong>Description:</strong> {templates[template_type]['description']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Display and allow editing of the template prompt
    template_prompt = st.text_area(
        "Customize Template Prompt:",
        templates[template_type]['prompt'],
        height=100
    )

    # Process template
    if st.button("📊 Run Template Analysis", use_container_width=True):
        try:
            with st.spinner("🔄 Processing template analysis..."):
                response = run_flow(
                    message=template_prompt,
                    endpoint=FLOW_ID,
                    output_type="chat",
                    input_type="chat",
                    tweaks=TWEAKS,
                    application_token=APPLICATION_TOKEN
                )

                if "error" in response:
                    st.error("❌ Template analysis failed. Please try again.")
                else:
                    st.success("✅ Template analysis complete!")
                    
                    # Extract and display results
                    final_output = (
                        response.get("outputs", [{}])[0]
                        .get("outputs", [{}])[0]
                        .get("results", {})
                        .get("message", {})
                        .get("text", "No analysis available.")
                    )
                    
                    # Display results in a formatted container
                    st.markdown("""
                        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px;'>
                            <h3 style='color: #1f1f1f; margin-bottom: 20px;'>
                                <span style='margin-right: 10px;'>📈</span>Template Analysis Results
                            </h3>
                            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; color: #1f1f1f; font-size: 16px; line-height: 1.6;'>
                    """, unsafe_allow_html=True)
                    
                    # Simply display the text with basic formatting
                    st.markdown(final_output)
                    
                    st.markdown("""
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add to history
                    st.session_state.history.append({
                        'prompt': f"Template: {template_type}",
                        'response': final_output,
                        'timestamp': datetime.now()
                    })
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again later.")
elif selected == "Settings":
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #1f1f1f;'>⚙️ Settings</h2>
            <p style='color: #4f4f4f;'>Customize your Media-matic experience</p>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for different settings categories
    settings_tab1, settings_tab2, settings_tab3, settings_tab4 = st.tabs([
        "🎨 Appearance", "🔑 API Configuration", "🔔 Notifications", "📊 Analysis Preferences"
    ])

    with settings_tab1:
        st.markdown("### Appearance Settings")
        
        # Theme Settings
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            theme_mode = st.radio("🎭 Theme Mode", ["Light", "Dark"], 
                                index=0 if st.session_state.theme == 'light' else 1)
        
        with theme_col2:
            color_scheme = st.selectbox(
                "🎨 Color Scheme",
                ["Default", "Blue", "Green", "Purple", "Orange"]
            )
        
        # Chart Preferences
        st.markdown("#### 📈 Chart Preferences")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            default_chart_type = st.selectbox(
                "Default Chart Type",
                ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot"]
            )
        with chart_col2:
            chart_animation = st.checkbox("Enable Chart Animations", value=True)
        
        # Font Settings
        st.markdown("#### 📝 Font Settings")
        font_col1, font_col2 = st.columns(2)
        with font_col1:
            font_size = st.select_slider(
                "Font Size",
                options=["Small", "Medium", "Large"],
                value="Medium"
            )
        with font_col2:
            font_family = st.selectbox(
                "Font Family",
                ["System Default", "Arial", "Roboto", "Open Sans"]
            )

    with settings_tab2:
        st.markdown("### API Configuration")
        
        # API Settings
        api_col1, api_col2 = st.columns(2)
        with api_col1:
            api_key = st.text_input("🔑 API Key", value=APPLICATION_TOKEN, type="password")
        with api_col2:
            api_environment = st.selectbox(
                "🌐 API Environment",
                ["Production", "Development", "Testing"]
            )
        
        # Advanced API Settings
        st.markdown("#### Advanced Settings")
        adv_api_col1, adv_api_col2 = st.columns(2)
        with adv_api_col1:
            request_timeout = st.number_input("Request Timeout (seconds)", 
                                            min_value=1, max_value=60, value=30)
        with adv_api_col2:
            max_retries = st.number_input("Max Retries", 
                                        min_value=0, max_value=5, value=3)

    with settings_tab3:
        st.markdown("### Notification Settings")
        
        # Email Notifications
        st.markdown("#### 📧 Email Notifications")
        email_col1, email_col2 = st.columns(2)
        with email_col1:
            email_notifications = st.checkbox("Enable email notifications")
            if email_notifications:
                email_address = st.text_input("Email Address")
        with email_col2:
            if email_notifications:
                notification_frequency = st.select_slider(
                    "Notification Frequency",
                    options=["Real-time", "Daily", "Weekly"],
                    value="Daily"
                )
        
        # In-App Notifications
        st.markdown("#### 🔔 In-App Notifications")
        notify_col1, notify_col2 = st.columns(2)
        with notify_col1:
            analysis_complete = st.checkbox("Analysis Complete Notifications", value=True)
            error_notifications = st.checkbox("Error Notifications", value=True)
        with notify_col2:
            system_updates = st.checkbox("System Updates", value=True)
            performance_alerts = st.checkbox("Performance Alerts", value=True)

    with settings_tab4:
        st.markdown("### Analysis Preferences")
        
        # Analysis Settings
        analysis_col1, analysis_col2 = st.columns(2)
        with analysis_col1:
            default_period = st.selectbox(
                "📅 Default Analysis Period",
                ["Last 7 days", "Last 30 days", "Last 90 days"]
            )
            metrics_display = st.multiselect(
                "📊 Default Metrics to Display",
                ["Likes", "Comments", "Shares", "Views", "Engagement Rate"],
                default=["Likes", "Comments"]
            )
        
        with analysis_col2:
            auto_refresh = st.checkbox("🔄 Auto-refresh Analysis", value=False)
            if auto_refresh:
                refresh_interval = st.select_slider(
                    "Refresh Interval",
                    options=["5 min", "15 min", "30 min", "1 hour"],
                    value="30 min"
                )
        
        # Export Settings
        st.markdown("#### 📤 Export Settings")
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            default_export_format = st.selectbox(
                "Default Export Format",
                ["CSV", "Excel", "JSON", "PDF"]
            )
        with export_col2:
            include_charts = st.checkbox("Include Charts in Exports", value=True)

    # Save Settings Button with Animation
    st.markdown("<br>", unsafe_allow_html=True)
    save_col1, save_col2, save_col3 = st.columns([1, 2, 1])
    with save_col2:
        if st.button("💾 Save Settings", use_container_width=True):
            with st.spinner("Saving settings..."):
                time.sleep(1)  # Simulate saving
                st.success("✅ Settings saved successfully!")
                st.balloons()

    # Reset Settings
    with save_col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            with st.spinner("Resetting settings..."):
                time.sleep(1)  # Simulate resetting
                st.success("✅ Settings reset to defaults!")

    # Display current settings summary
    st.markdown("### 📑 Current Settings Summary")
    with st.expander("View Settings Summary"):
        st.json({
            "appearance": {
                "theme": theme_mode,
                "color_scheme": color_scheme,
                "font_size": font_size
            },
            "api": {
                "environment": api_environment,
                "timeout": request_timeout,
                "max_retries": max_retries
            },
            "notifications": {
                "email_enabled": email_notifications,
                "notification_types": {
                    "analysis_complete": analysis_complete,
                    "errors": error_notifications,
                    "updates": system_updates
                }
            },
            "analysis": {
                "default_period": default_period,
                "metrics": metrics_display,
                "auto_refresh": auto_refresh
            }
        })

# Footer
st.markdown("---")
st.markdown("© 2024 Media-matic")