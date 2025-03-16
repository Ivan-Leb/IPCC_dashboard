import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to prepare the data
def prepare_data():
    try:
        # Load the observed data (1850-2020)
        df_obs = pd.read_csv("SPM1_1850-2020_obs.csv", skiprows=15, encoding="latin1")
        df_obs = df_obs.rename(columns={"1": "Year", "2": "Temperature"}).drop(columns=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"])  
        df_obs["Temperature"] = pd.to_numeric(df_obs["Temperature"], errors="coerce")
        df_obs["Source"] = "Observed"

        # Load the reconstructed data (1-2000)
        df_recon = pd.read_csv("SPM1_1-2000_recon.csv", skiprows=19, encoding="latin1")
        df_recon = df_recon.rename(columns={"1": "Year", "2": "Temperature"}).drop(columns=["Unnamed: 4", "3", "4"])
        df_recon["Temperature"] = pd.to_numeric(df_recon["Temperature"], errors="coerce")
        df_recon["Source"] = "Reconstructed"
        
        # Convert to numeric values
        df_recon["Year"] = pd.to_numeric(df_recon["Year"], errors="coerce")
        df_obs["Year"] = pd.to_numeric(df_obs["Year"], errors="coerce")
        
        return df_obs, df_recon
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Function to create a simple temperature plot
def plot_simple_temperature(df_obs, df_recon, show_old_times=True, show_new_times=True, 
                           show_grid=True, highlight_range=None, show_trend=False, chart_theme="default"):
    # Set style colors based on theme
    if chart_theme == "default":
        old_color = "#6495ED"  # Classic blue
        new_color = "#FF6347"  # Red
        bg_color = "#F0F8FF"   # Light blue
        grid_color = "gray"
    elif chart_theme == "dark":
        old_color = "#4682B4"  # Steel blue
        new_color = "#CD5C5C"  # Indian red
        bg_color = "#2F4F4F"   # Dark slate
        grid_color = "#DCDCDC"
    elif chart_theme == "pastel":
        old_color = "#ADD8E6"  # Light blue
        new_color = "#FFB6C1"  # Light pink
        bg_color = "#F0FFF0"   # Honeydew
        grid_color = "#D3D3D3"
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot the old temperatures
    if show_old_times:
        ax.plot(df_recon["Year"], df_recon["Temperature"], color=old_color, lw=2, label="Long Ago (Past)")
    
    # Plot the new temperatures
    if show_new_times:
        ax.plot(df_obs["Year"], df_obs["Temperature"], color=new_color, lw=3, label="Recent Times")
    
    # Add a horizontal line at zero
    ax.axhline(0, color="black", linestyle="--", alpha=0.5)
    
    # Highlight a time range if specified
    if highlight_range and len(highlight_range) == 2:
        start_year, end_year = highlight_range
        ax.axvspan(start_year, end_year, color="yellow", alpha=0.2)
        ax.text(start_year + (end_year-start_year)/2, ax.get_ylim()[1]*0.9, 
                f"Highlighted: {start_year}-{end_year}", 
                ha="center", fontsize=10, bbox=dict(facecolor="yellow", alpha=0.3))
    
    # Add trend line for the recent data if requested
    if show_trend and show_new_times:
        # Simple linear trend for recent years
        x = df_obs["Year"].values
        y = df_obs["Temperature"].values
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "k--", alpha=0.7, label="Warming Trend")
        
        # Add trend slope information
        slope_per_decade = z[0] * 10  # degrees per decade
        ax.text(x.mean(), ax.get_ylim()[1]*0.8, 
                f"Warming rate: {slope_per_decade:.2f}°C per decade", 
                ha="center", fontsize=10, bbox=dict(facecolor="white", alpha=0.7))
    
    # Styling
    ax.set_title("Earth's Temperature Story", fontsize=16, fontweight="bold")
    ax.set_xlabel("Time (Years)", fontsize=12)
    ax.set_ylabel("Temperature Change (°C)", fontsize=12)
    
    # Simplify the y-axis
    ax.set_yticks([-1, -0.5, 0, 0.5, 1, 1.5])
    ax.set_yticklabels(["1°C Cooler", "0.5°C Cooler", "Normal", "0.5°C Warmer", "1°C Warmer", "1.5°C Warmer"], fontsize=10)
    
    # Set background color
    ax.set_facecolor(bg_color)
    
    # Make grid child-friendly
    if show_grid:
        ax.grid(color=grid_color, linestyle="--", linewidth=0.5, alpha=0.3)
    else:
        ax.grid(False)
    
    # Add a legend with large font if at least one line is shown
    if show_old_times or show_new_times or show_trend:
        ax.legend(fontsize=10, loc="upper left")
    
    # Set limits
    ax.set_xlim(df_recon["Year"].min() if show_old_times else df_obs["Year"].min(), 
               df_obs["Year"].max())
    
    plt.tight_layout()
    
    return fig

# Streamlit App
def main():
    # Set page config
    st.set_page_config(
        page_title="Earth's Temperature for Kids",
        page_icon="🌍",
        layout="wide"
    )
    
    # Apply a custom style with more compact elements
    st.markdown("""
        <style>
        .big-text {font-size: 20px !important;}
        button {font-size: 16px !important; padding: 8px !important;}
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        h1 {margin-top: 0px; margin-bottom: 5px;}
        h3 {margin-top: 10px; margin-bottom: 5px;}
        .stButton>button {width: 100%;}
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .sidebar .stRadio > label {
            font-size: 18px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Prepare the data
    df_obs, df_recon = prepare_data()
    
    # Check if data is loaded correctly
    if df_obs.empty or df_recon.empty:
        st.error("Could not load the datasets. Please check file paths and try again.")
        return
    
    # Title with emoji - more compact
    st.title("🌍 Our Earth is Getting Warmer")
    
    # SIDEBAR WITH MORE USEFUL FILTERS
    with st.sidebar:
        st.title("Explore the Data")
        
        # Data selection
        st.subheader("📊 Choose What to Show")
        show_old = st.checkbox("Show Long Ago Data (Blue line)", value=True)
        show_new = st.checkbox("Show Recent Data (Red line)", value=True)
        
        # Time range selector
        st.subheader("⏱️ Time Range")
        time_periods = {
            "All Time": None,
            "Last 100 Years": [1920, 2020],
            "Last 50 Years": [1970, 2020],
            "Industrial Age": [1850, 2020],
            "Middle Ages": [500, 1500],
            "Roman Era": [0, 500]
        }
        selected_period = st.selectbox("Show a specific time period:", list(time_periods.keys()))
        highlight_range = time_periods[selected_period]
        
        # Visual options
        st.subheader("🎨 Visual Options")
        show_grid = st.checkbox("Show Grid Lines", value=True)
        show_trend = st.checkbox("Show Warming Trend Line", value=False)
        
        chart_theme = st.radio(
            "Chart Color Theme:",
            ["default", "dark", "pastel"],
            format_func=lambda x: {
                "default": "Standard Colors",
                "dark": "Dark Theme",
                "pastel": "Pastel Colors"
            }[x]
        )
        
        # Advanced options (collapsed by default)
        with st.expander("📈 Advanced Options"):
            y_axis_scale = st.radio("Y-Axis Scale:", ["default", "extended"])
            if y_axis_scale == "extended":
                st.info("Extended scale shows more extreme temperature variations")

    # Two column layout for main content
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Simple explanation
        st.markdown('<p class="big-text">This chart shows how Earth\'s temperature has changed over time. Scientists measure how much warmer or cooler Earth is compared to normal temperatures.</p>', unsafe_allow_html=True)
        
        # Import missing numpy for trend line
        import numpy as np
        
        # Display the graph with filter options applied
        fig = plot_simple_temperature(
            df_obs, df_recon, 
            show_old_times=show_old, 
            show_new_times=show_new,
            show_grid=show_grid,
            highlight_range=highlight_range,
            show_trend=show_trend,
            chart_theme=chart_theme
        )
        st.pyplot(fig)
        
        # Show data explanation based on the period selected
        if selected_period == "Last 50 Years":
            st.info("📌 The last 50 years show the fastest warming in Earth's recent history!")
        elif selected_period == "Industrial Age":
            st.info("📌 This is when humans started using lots of machines and burning fossil fuels.")
        elif selected_period == "Middle Ages":
            st.info("📌 During this time, Earth's temperature changed more slowly and naturally.")
    
    with col_right:
        # Explanation buttons with emoji - vertical stack
        st.subheader("Click to learn more!")
        
        # Compact buttons layout
        if st.button("🔎 What Do We See?", key="what"):
            st.markdown("""
            <div style="background-color:#E6F9FF; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            • Blue line shows how Earth's temperature changed long ago.<br>
            • Red line shows more recent temperature changes.<br> 
            • When the lines go up, Earth is getting warmer!<br>
            • Notice how much faster it's warming in recent years.
            </p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("❓ Why Is This Happening?", key="why"):
            st.markdown("""
            <div style="background-color:#FFF9E6; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            Cars, factories, and things we use make greenhouse gases. These gases trap heat in Earth's atmosphere - like a blanket that's getting too thick.
            </p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🌱 How Can We Help?", key="help"):
            st.markdown("""
            <div style="background-color:#E6FFE6; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            🌳 Plant trees • 🚶 Walk more • 🚲 Ride bikes<br>
            💡 Save energy • ♻️ Recycle • 🥕 Eat more plants<br>
            🚿 Save water • 📚 Learn about climate science
            </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section for data insights
        if st.button("📊 Interesting Facts", key="facts"):
            st.markdown("""
            <div style="background-color:#F5E6FF; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            • Earth has warmed about 1°C since 1850.<br>
            • The 10 warmest years on record have all occurred since 2005.<br>
            • Scientists can learn about ancient temps from tree rings and ice cores.<br>
            • Even small temperature changes can have big effects on plants, animals, and weather.
            </p>
            </div>
            """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
