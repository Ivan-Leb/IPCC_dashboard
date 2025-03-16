import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import base64

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
def plot_simple_temperature(df_obs, df_recon, show_old_times=True, show_new_times=True):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot the old temperatures (blue)
    if show_old_times:
        ax.plot(df_recon["Year"], df_recon["Temperature"], color="#6495ED", lw=2, label="Long Ago (Blue)")
    
    # Plot the new temperatures (red)
    if show_new_times:
        ax.plot(df_obs["Year"], df_obs["Temperature"], color="#FF6347", lw=3, label="Now (Red)")
    
    # Add a horizontal line at zero
    ax.axhline(0, color="black", linestyle="--", alpha=0.5)
    
    # Styling
    ax.set_title("Earth's Temperature Story", fontsize=16, fontweight="bold")
    ax.set_xlabel("Time (Years)", fontsize=12)
    ax.set_ylabel("Temperature Change (°C)", fontsize=12)
    
    # Simplify the y-axis
    ax.set_yticks([-1, -0.5, 0, 0.5, 1, 1.5])
    ax.set_yticklabels(["Cooler", "", "Normal", "", "Warmer", "Much Warmer"], fontsize=10)
    
    # Set background color
    ax.set_facecolor("#F0F8FF")  # Light blue background
    
    # Make grid child-friendly
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.3)
    
    # Add a legend with large font if at least one line is shown
    if show_old_times or show_new_times:
        ax.legend(fontsize=12, loc="upper left")
    
    # Set limits
    ax.set_xlim(0, 2020)  # Set to exactly the 0-2020 range we have data for
    
    plt.tight_layout()
    
    return fig

# Define cartoon character explanation components
def get_cartoon_explanations():
    # Since we can't actually include images in this response, 
    # we'll use emoji as placeholders. In a real implementation, 
    # you'd replace these with actual cartoon character images.
    
    x_axis_explanation = """
    <div style="background-color:#FFE6E6; padding:15px; border-radius:15px; border:2px dashed #FF6347;">
    <div style="display:flex; align-items:center;">
    <div style="font-size:60px; margin-right:15px;">👧</div>
    <div>
    <p style="font-size:18px; font-weight:bold;">What does the Time (x-axis) show?</p>
    <p style="font-size:16px;">
    Hi! I'm Tina Time! The bottom of the chart shows <b>years</b> from a long time ago (year 0) 
    until now (year 2020). As you move from left to right, you're traveling through time like a time machine!
    <br><br>
    The <span style="color:blue">blue line</span> shows temperature from a long time ago.
    The <span style="color:red">red line</span> shows more recent temperatures.
    </p>
    </div>
    </div>
    </div>
    """
    
    y_axis_explanation = """
    <div style="background-color:#E6F9FF; padding:15px; border-radius:15px; border:2px dashed #6495ED;">
    <div style="display:flex; align-items:center;">
    <div style="font-size:60px; margin-right:15px;">🧒</div>
    <div>
    <p style="font-size:18px; font-weight:bold;">What does the Temperature (y-axis) show?</p>
    <p style="font-size:16px;">
    Hey there! I'm Theo Thermo! The side of the chart shows how the Earth's temperature has changed.
    <br><br>
    The middle line (0) is the normal temperature. When the line goes up ↑, Earth is getting warmer.
    When the line goes down ↓, Earth is getting cooler.
    <br><br>
    See how the red line shoots up at the end? That means Earth is getting much warmer very quickly!
    </p>
    </div>
    </div>
    </div>
    """
    
    return x_axis_explanation, y_axis_explanation

# Streamlit App
def main():
    # Set page config
    st.set_page_config(
        page_title="Earth's Temperature for Kids",
        page_icon="🌍",
        layout="wide"
    )
    
    # Apply a custom style
    st.markdown("""
        <style>
        .big-text {font-size: 20px !important;}
        button {font-size: 16px !important; padding: 8px !important;}
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        h1 {margin-top: 0px; margin-bottom: 5px;}
        h3 {margin-top: 10px; margin-bottom: 5px;}
        .stButton>button {width: 100%;}
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
    
    # SIDEBAR
    with st.sidebar:
        st.title("Play with the Chart!")
        
        # Simple toggles for lines - ONLY KEEPING THESE TWO FILTERS
        st.subheader("🎨 Show or Hide Lines")
        show_old = st.checkbox("Show Blue Line (Long Ago)", value=True)
        show_new = st.checkbox("Show Red Line (Now)", value=True)

    # Two column layout for main content
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Simple explanation
        st.markdown('<p class="big-text">This picture shows how Earth\'s temperature has changed over the last 2000 years.</p>', unsafe_allow_html=True)
        
        # Display temperature graph
        fig = plot_simple_temperature(
            df_obs, 
            df_recon,
            show_old_times=show_old,
            show_new_times=show_new
        )
        st.pyplot(fig)
        
        # Get cartoon character explanations
        x_axis_explanation, y_axis_explanation = get_cartoon_explanations()
        
        # Buttons to show cartoon character explanations
        st.markdown("### Click to get help from our cartoon friends!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👧 Help me understand the Time axis!", key="time_axis"):
                st.markdown(x_axis_explanation, unsafe_allow_html=True)
        
        with col2:
            if st.button("🧒 Help me understand the Temperature axis!", key="temp_axis"):
                st.markdown(y_axis_explanation, unsafe_allow_html=True)
    
    with col_right:
        # Explanation buttons with emoji
        st.subheader("Click to learn more!")
        
        # Compact buttons layout
        if st.button("🔎 What Do We See?", key="what"):
            st.markdown("""
            <div style="background-color:#E6F9FF; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            • Blue line shows Earth's temperature long ago.<br>
            • Red line shows more recent temperatures.<br> 
            • See the red line going up quickly? Earth is warming faster than it has for thousands of years!
            </p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("❓ Why Is This Happening?", key="why"):
            st.markdown("""
            <div style="background-color:#FFF9E6; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            Since the Industrial Revolution (around 1850), humans have been burning fossil fuels like coal, oil, and natural gas. This releases greenhouse gases that trap heat in our atmosphere, like a blanket getting thicker and thicker around our planet.
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

# Run the app
if __name__ == "__main__":
    main()
