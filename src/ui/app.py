# src/ui/app.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path to import from other modules
sys.path.append(str(Path(__file__).parent.parent))
from data.mock_data_generator import HealthDataGenerator
from pathway_processing.stream_processor import HealthDataProcessor

class HealthAdvisoryUI:
    def __init__(self):
        st.set_page_config(
            page_title="Team SAM - Health Advisory System",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        self.data_generator = HealthDataGenerator()
        self.processor = HealthDataProcessor()
        
        # Initialize session state
        if 'health_data' not in st.session_state:
            st.session_state.health_data = []
        if 'selected_user' not in st.session_state:
            st.session_state.selected_user = None

    def run(self):
        self._render_sidebar()
        self._render_main_content()

    def _render_sidebar(self):
        with st.sidebar:
            st.title("🏥 Team Sam - Health Advisory")
            st.subheader("Patient Selection")
            
            # User selection dropdown
            users = self.data_generator.get_user_profiles()
            selected_user = st.selectbox(
                "Select User",
                options=users,
                format_func=lambda x: x['name']
            )
            st.session_state.selected_user = selected_user

            # Display user profile
            if selected_user:
                st.subheader("User Profile")
                st.write(f"Age: {selected_user['age']}")
                st.write(f"Weight: {selected_user['weight']} kg")
                st.write(f"Height: {selected_user['height']} cm")
                st.write("Medical Conditions:")
                for condition in selected_user['conditions']:
                    st.write(f"- {condition}")

    def _render_main_content(self):
        if not st.session_state.selected_user:
            st.info("Please select a user from the sidebar to begin monitoring.")
            return

        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        # Simulate real-time data
        new_data = self.data_generator.generate_health_data(
            st.session_state.selected_user['user_id']
        )
        st.session_state.health_data.append(new_data)
        
        # Keep only last 100 data points
        if len(st.session_state.health_data) > 100:
            st.session_state.health_data = st.session_state.health_data[-100:]

        # Convert to DataFrame for easier processing
        df = pd.DataFrame(st.session_state.health_data)

        # Display current metrics
        with col1:
            self._render_metric_card(
                "Heart Rate",
                f"{new_data['heart_rate']} bpm",
                "❤️",
                self._get_heart_rate_color(new_data['heart_rate'])
            )

        with col2:
            self._render_metric_card(
                "SpO₂",
                f"{new_data['spo2']}%",
                "🫁",
                self._get_spo2_color(new_data['spo2'])
            )

        with col3:
            self._render_metric_card(
                "Steps",
                f"{new_data['steps']:,}",
                "👣",
                "#1f77b4"
            )

        # Create two columns for charts
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            self._render_line_chart(df, "Heart Rate Over Time", "heart_rate", "bpm")

        with chart_col2:
            self._render_activity_pie_chart(df)

        # Render recommendations
        st.subheader("🎯 Personalized Recommendations")
        self._render_recommendations(new_data)

    def _render_metric_card(self, title, value, emoji, color):
        st.markdown(
            f"""
            <div style="
                padding: 20px;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            ">
                <h3 style="
                    color: {color};
                    margin: 0;
                    font-size: 1.2em;
                ">{emoji} {title}</h3>
                <p style="
                    color: {color};
                    font-size: 2em;
                    font-weight: bold;
                    margin: 10px 0 0 0;
                ">{value}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def _render_line_chart(self, df, title, metric, unit):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df['timestamp']),
            y=df[metric],
            mode='lines+markers',
            name=metric,
            line=dict(width=3)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title=unit,
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_activity_pie_chart(self, df):
        activity_counts = df['activity_level'].value_counts()
        
        fig = px.pie(
            values=activity_counts.values,
            names=activity_counts.index,
            title="Activity Level Distribution"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_recommendations(self, data):
        recommendations = [
            {
                "title": "Activity Level",
                "message": "Based on your current activity level, consider taking a short walk to reach your daily step goal.",
                "icon": "🚶‍♂️"
            },
            {
                "title": "Heart Rate",
                "message": f"Your heart rate is {data['heart_rate']} bpm. Remember to stay hydrated and maintain steady breathing.",
                "icon": "❤️"
            },
            {
                "title": "Stress Management",
                "message": "Your stress level indicates you might benefit from a brief meditation session.",
                "icon": "🧘‍♀️"
            }
        ]

        for rec in recommendations:
            st.markdown(
                f"""
                <div style="
                    padding: 20px;
                    border-radius: 10px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                ">
                    <h4 style="
                        color: #1f77b4;
                        margin: 0;
                    ">{rec['icon']} {rec['title']}</h4>
                    <p style="
                        margin: 10px 0 0 0;
                        color: #2c3e50;
                    ">{rec['message']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    @staticmethod
    def _get_heart_rate_color(value):
        if value < 60 or value > 100:
            return "#ff4b4b"
        return "#28a745"

    @staticmethod
    def _get_spo2_color(value):
        if value < 95:
            return "#ff4b4b"
        return "#28a745"

if __name__ == "__main__":
    app = HealthAdvisoryUI()
    app.run()