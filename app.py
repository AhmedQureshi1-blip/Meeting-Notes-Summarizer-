"""
Meeting Notes Summarizer - Streamlit Web Application
A user-friendly web interface for summarizing meeting notes with batch processing,
token tracking, and cost estimation.
"""

import streamlit as st
import os
import json
from datetime import datetime
from typing import List, Dict
import pandas as pd

from summarizer import MeetingSummarizer, TokenTracker


# Page configuration
st.set_page_config(
    page_title="Meeting Notes Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stat-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'summarizer' not in st.session_state:
        st.session_state.summarizer = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'summaries' not in st.session_state:
        st.session_state.summaries = []
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = []


def sidebar_config():
    """Configure sidebar with API key and settings."""
    st.sidebar.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your OpenAI API key. Leave empty to use environment variable."
    )
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.session_state.summarizer = MeetingSummarizer(api_key if api_key else None)
    
    # Initialize summarizer if not already done
    if st.session_state.summarizer is None:
        st.session_state.summarizer = MeetingSummarizer(api_key if api_key else None)
    
    st.sidebar.markdown("---")
    
    # Usage statistics
    st.sidebar.header("📊 Session Statistics")
    if st.session_state.summarizer:
        stats = st.session_state.summarizer.tracker.get_session_stats()
        
        st.sidebar.metric(
            "Total Tokens",
            f"{stats['total_tokens']:,}",
            delta=None
        )
        
        st.sidebar.metric(
            "Session Cost",
            f"${stats['cost']:.4f}",
            delta=None
        )
        
        # Monthly estimate
        monthly_estimate = st.session_state.summarizer.tracker.get_monthly_estimate(stats)
        st.sidebar.markdown(f"**Estimated Monthly Cost:** ${monthly_estimate['estimated_monthly_cost']:.2f}")
    
    st.sidebar.markdown("---")
    
    # Reset button
    if st.sidebar.button("🔄 Reset Session", help="Clear session statistics"):
        if st.session_state.summarizer:
            st.session_state.summarizer.tracker.reset_session()
        st.session_state.summaries = []
        st.session_state.batch_results = []
        st.sidebar.success("Session reset successfully!")


def single_summary_mode():
    """Handle single meeting note summarization."""
    st.header("📝 Single Summary Mode")
    st.markdown("Paste your meeting notes below to generate a summary.")
    
    # Text input
    meeting_text = st.text_area(
        "Meeting Notes",
        height=200,
        placeholder="Paste your meeting notes here...",
        help="Enter the meeting notes you want to summarize (minimum 50 characters)"
    )
    
    # Summary length options
    col1, col2 = st.columns([1, 3])
    with col1:
        summary_length = st.selectbox(
            "Summary Length",
            ["short", "medium", "long"],
            index=1,
            help="Choose the length of the summary"
        )
    
    # Summarize button
    if st.button("✨ Generate Summary", type="primary", use_container_width=True):
        if not meeting_text.strip():
            st.error("⚠️ Please enter meeting notes before generating a summary.")
            return
        
        with st.spinner("Generating summary..."):
            try:
                result = st.session_state.summarizer.summarize(meeting_text, summary_length)
                
                if result['success']:
                    st.session_state.summaries.append({
                        'timestamp': datetime.now().isoformat(),
                        'summary': result['summary'],
                        'stats': result['stats']
                    })
                    
                    # Display success message
                    st.markdown('<div class="success-box">✅ Summary generated successfully!</div>', unsafe_allow_html=True)
                    
                    # Display summary
                    st.subheader("📄 Summary")
                    st.write(result['summary'])
                    
                    # Display statistics
                    st.subheader("📊 Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Input Tokens", f"{result['stats']['input_tokens']:,}")
                    with col2:
                        st.metric("Output Tokens", f"{result['stats']['output_tokens']:,}")
                    with col3:
                        st.metric("Cost", f"${result['stats']['cost']:.4f}")
                    
                    # Download button
                    st.download_button(
                        "📥 Download Summary",
                        result['summary'],
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.markdown(f'<div class="error-box">❌ {result["error"]}</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ An unexpected error occurred: {str(e)}</div>', unsafe_allow_html=True)


def batch_mode():
    """Handle batch processing of multiple meeting notes."""
    st.header("📚 Batch Processing Mode")
    st.markdown("Process multiple meeting notes at once.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a text file with multiple meeting notes",
        type=['txt'],
        help="Each meeting note should be separated by '---' on its own line"
    )
    
    # Text input for batch
    st.markdown("Or paste multiple meeting notes below (separated by '---'):")
    batch_text = st.text_area(
        "Batch Meeting Notes",
        height=300,
        placeholder="Meeting 1 text...\n---\nMeeting 2 text...\n---\nMeeting 3 text...",
        help="Separate each meeting note with '---' on its own line"
    )
    
    # Summary length
    summary_length = st.selectbox(
        "Summary Length",
        ["short", "medium", "long"],
        index=1,
        key="batch_length"
    )
    
    # Process button
    if st.button("🚀 Process Batch", type="primary", use_container_width=True):
        # Get input text
        if uploaded_file is not None:
            batch_text = uploaded_file.read().decode('utf-8')
        
        if not batch_text.strip():
            st.error("⚠️ Please provide meeting notes for batch processing.")
            return
        
        # Split by '---'
        meetings = [m.strip() for m in batch_text.split('---') if m.strip()]
        
        if len(meetings) == 0:
            st.error("⚠️ No valid meeting notes found. Please separate meetings with '---'.")
            return
        
        st.info(f"Found {len(meetings)} meeting notes to process.")
        
        # Process with progress bar
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, meeting in enumerate(meetings):
            status_text.text(f"Processing meeting {i+1} of {len(meetings)}...")
            
            try:
                result = st.session_state.summarizer.summarize(meeting, summary_length)
                result['index'] = i
                result['original_length'] = len(meeting)
                results.append(result)
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e),
                    'summary': None,
                    'stats': None,
                    'index': i,
                    'original_length': len(meeting)
                })
            
            progress_bar.progress((i + 1) / len(meetings))
        
        status_text.text("Batch processing complete!")
        st.session_state.batch_results = results
        
        # Display results
        st.subheader("📊 Batch Results")
        
        # Summary statistics
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Processed", len(results))
        with col2:
            st.metric("Successful", successful, delta_color="normal")
        with col3:
            st.metric("Failed", failed, delta_color="inverse")
        
        # Detailed results
        st.subheader("📋 Detailed Results")
        
        for i, result in enumerate(results):
            with st.expander(f"Meeting {i+1} - {'✅ Success' if result['success'] else '❌ Failed'}"):
                if result['success']:
                    st.write(f"**Original Length:** {result['original_length']:,} characters")
                    st.write(f"**Summary:**")
                    st.write(result['summary'])
                    st.write(f"**Tokens:** {result['stats']['total_tokens']:,}")
                    st.write(f"**Cost:** ${result['stats']['cost']:.4f}")
                else:
                    st.error(f"Error: {result['error']}")
        
        # Download all results
        if st.button("📥 Download All Results as JSON"):
            results_json = json.dumps(results, indent=2)
            st.download_button(
                "Download JSON",
                results_json,
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


def history_view():
    """Display history of summaries."""
    st.header("📜 Summary History")
    
    if not st.session_state.summaries:
        st.info("No summaries generated yet.")
        return
    
    # Display as table
    df_data = []
    for i, summary in enumerate(st.session_state.summaries):
        df_data.append({
            '#': i + 1,
            'Timestamp': summary['timestamp'],
            'Preview': summary['summary'][:100] + '...',
            'Tokens': summary['stats']['total_tokens'],
            'Cost': f"${summary['stats']['cost']:.4f}"
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📝 Meeting Notes Summarizer</h1>', unsafe_allow_html=True)
    st.markdown("Transform your meeting notes into concise summaries with AI-powered analysis.")
    
    # Sidebar
    sidebar_config()
    
    # Mode selection
    tab1, tab2, tab3 = st.tabs(["Single Summary", "Batch Processing", "History"])
    
    with tab1:
        single_summary_mode()
    
    with tab2:
        batch_mode()
    
    with tab3:
        history_view()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Built with Streamlit • Uses GPT-3.5-turbo • Token tracking enabled</p>
        <p>Cost: $0.0005/1K input tokens, $0.0015/1K output tokens</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
