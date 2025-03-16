import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
def plot_simple_temperature(df_obs, df_recon, time_markers=None, show_old_times=True, show_new_times=True):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot the old temperatures (blue)
    if show_old_times:
        ax.plot(df_recon["Year"], df_recon["Temperature"], color="#6495ED", lw=2, label="Long Ago (Blue)")
    
    # Plot the new temperatures (red)
    if show_new_times:
        ax.plot(df_obs["Year"], df_obs["Temperature"], color="#FF6347", lw=3, label="Now (Red)")
    
    # Add a horizontal line at zero
    ax.axhline(0, color="black", linestyle="--", alpha=0.5)
    
    # Add time markers if provided
    if time_markers and time_markers.any():
        for marker in time_markers:
            if marker['show']:
                year = marker['year']
                # Check if the year is within the visible range
                if ((show_old_times and year < 1850) or 
                    (show_new_times and year >= 1850)):
                    # Draw a vertical line at the marker year
                    ax.axvline(x=year, color=marker['color'], linestyle='-', alpha=0.3, linewidth=10)
                    # Add an annotation above the chart
                    ax.annotate(marker['label'], xy=(year, ax.get_ylim()[1]), 
                                xytext=(0, 10), textcoords='offset points',
                                ha='center', fontsize=9,
                                bbox=dict(boxstyle="round,pad=0.3", fc=marker['color'], alpha=0.3))
    
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
    ax.set_xlim(df_recon["Year"].min(), df_obs["Year"].max())
    
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
        
        # Simple toggles for lines
        st.subheader("🎨 Show or Hide Lines")
        show_old = st.checkbox("Show Blue Line (Long Ago)", value=True)
        show_new = st.checkbox("Show Red Line (Now)", value=True)
        
        # Time period markers with images
        st.subheader("📅 Show Important Times")
        
        # Define markers for different periods
        time_markers = [
            {
                'name': 'dinosaurs',
                'year': 100,  # Arbitrary year for visual representation
                'label': '🦕 Dinosaur Times',
                'color': 'green',
                'show': st.checkbox('🦕 Dinosaur Times', value=False)
            },
            {
                'name': 'ice_age',
                'year': 500,
                'label': '❄️ Ice Age',
                'color': 'lightblue',
                'show': st.checkbox('❄️ Ice Age', value=False)
            },
            {
                'name': 'roman',
                'year': 1000,
                'label': '🏛️ Roman Times',
                'color': 'sandybrown',
                'show': st.checkbox('🏛️ Roman Times', value=False)
            },
            {
                'name': 'industry_begins',
                'year': 1850,
                'label': '🏭 Factories Begin',
                'color': 'darkgray',
                'show': st.checkbox('🏭 Factories Begin', value=False)
            },
            {
                'name': 'cars',
                'year': 1920,
                'label': '🚗 Cars Everywhere',
                'color': 'darkgray',
                'show': st.checkbox('🚗 Cars Everywhere', value=False)
            },
            {
                'name': 'modern',
                'year': 1980,
                'label': '💻 Modern Times',
                'color': 'purple',
                'show': st.checkbox('💻 Modern Times', value=False)
            }
        ]

    # Two column layout for main content
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Simple explanation
        st.markdown('<p class="big-text">This picture shows how Earth\'s temperature has changed over a very long time.</p>', unsafe_allow_html=True)
        
        # Display temperature graph
        fig = plot_simple_temperature(
            df_obs, 
            df_recon,
            time_markers=time_markers,
            show_old_times=show_old,
            show_new_times=show_new
        )
        st.pyplot(fig)
        
        # Show explanation for selected time periods
        active_markers = [marker for marker in time_markers if marker['show']]
        
        if active_markers:
            st.markdown("### About the times you selected:")
            for marker in active_markers:
                if marker['name'] == 'dinosaurs':
                    st.markdown("🦕 **Dinosaur Times**: Earth was much warmer! Dinosaurs lived in a hot world with no ice at the poles.")
                elif marker['name'] == 'ice_age':
                    st.markdown("❄️ **Ice Age**: Earth was much colder. Giant ice sheets covered much of North America and Europe.")
                elif marker['name'] == 'roman':
                    st.markdown("🏛️ **Roman Times**: Temperature was fairly stable. The Roman Empire flourished in this climate.")
                elif marker['name'] == 'industry_begins':
                    st.markdown("🏭 **Factories Begin**: People started burning lots of coal. This is when the temperature started rising faster.")
                elif marker['name'] == 'cars':
                    st.markdown("🚗 **Cars Everywhere**: More cars and factories meant more pollution and warming.")
                elif marker['name'] == 'modern':
                    st.markdown("💻 **Modern Times**: Our world today is warming very quickly because of all the energy we use.")
    
    with col_right:
        # Explanation buttons with emoji
        st.subheader("Click to learn more!")
        
        # Compact buttons layout
        if st.button("🔎 What Do We See?", key="what"):
            st.markdown("""
            <div style="background-color:#E6F9FF; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            • Blue line shows how Earth was long ago.<br>
            • Red line shows how Earth is now.<br> 
            • See the red line going up? Earth is getting warmer!<br>
            • The colored markers show important times in history.
            </p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("❓ Why Is This Happening?", key="why"):
            st.markdown("""
            <div style="background-color:#FFF9E6; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            Cars, factories, and things we use make pollution. This pollution makes a blanket around Earth that traps heat - like too many blankets on your bed!
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
        
        # Show image explanation for each time period
        st.markdown("### Time Period Icons:")
        
        # Display all time period icons in a grid
        icon_cols = st.columns(2)
        
        with icon_cols[0]:
            st.markdown("🦕 = Dinosaur Times")
            st.markdown("❄️ = Ice Age")
            st.markdown("🏛️ = Roman Times")
        
        with icon_cols[1]:
            st.markdown("🏭 = Factories Begin")
            st.markdown("🚗 = Cars Everywhere")
            st.markdown("💻 = Modern Times")

# Run the app
if __name__ == "__main__":
    main()
