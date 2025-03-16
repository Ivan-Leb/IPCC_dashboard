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
    if time_markers and len(time_markers) > 0:
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
    ax.set_xlim(0, 2020)  # Set to exactly the 0-2020 range we have data for
    
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
        
        # Time period markers with more historically accurate periods
        st.subheader("📅 Show Important Historical Periods")
        
        # Define markers for different periods - using historically accurate periods within the 0-2000 CE range
        time_markers = [
            {
                'name': 'roman_empire',
                'year': 100,
                'label': '🏛️ Roman Empire',
                'color': 'gold',
                'show': st.checkbox('🏛️ Roman Empire (100 CE)', value=False)
            },
            {
                'name': 'medieval_warm',
                'year': 1000,
                'label': '☀️ Medieval Warm Period',
                'color': 'orange',
                'show': st.checkbox('☀️ Medieval Warm Period (1000 CE)', value=False)
            },
            {
                'name': 'little_ice_age',
                'year': 1650,
                'label': '❄️ Little Ice Age',
                'color': 'lightblue',
                'show': st.checkbox('❄️ Little Ice Age (1650 CE)', value=False)
            },
            {
                'name': 'industrial_revolution',
                'year': 1850,
                'label': '🏭 Industrial Revolution',
                'color': 'darkgray',
                'show': st.checkbox('🏭 Industrial Revolution (1850 CE)', value=False)
            },
            {
                'name': 'great_acceleration',
                'year': 1950,
                'label': '🚀 Great Acceleration',
                'color': 'indianred',
                'show': st.checkbox('🚀 Great Acceleration (1950 CE)', value=False)
            },
            {
                'name': 'recent_warming',
                'year': 2000,
                'label': '🔥 Recent Rapid Warming',
                'color': 'crimson',
                'show': st.checkbox('🔥 Recent Rapid Warming (2000 CE)', value=False)
            }
        ]

    # Two column layout for main content
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Simple explanation
        st.markdown('<p class="big-text">This picture shows how Earth\'s temperature has changed over the last 2000 years.</p>', unsafe_allow_html=True)
        
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
            st.markdown("### About the periods you selected:")
            for marker in active_markers:
                if marker['name'] == 'roman_empire':
                    st.markdown("🏛️ **Roman Empire (100 CE)**: This was a relatively warm period when the Roman Empire was at its height. Temperatures were similar to or slightly warmer than the long-term average.")
                elif marker['name'] == 'medieval_warm':
                    st.markdown("☀️ **Medieval Warm Period (1000 CE)**: Parts of the world experienced unusually warm temperatures during this time. Vikings settled in Greenland and crops grew in northern regions.")
                elif marker['name'] == 'little_ice_age':
                    st.markdown("❄️ **Little Ice Age (1650 CE)**: A cooler period when glaciers grew larger. Rivers would freeze in winter, and crops sometimes failed due to shorter growing seasons.")
                elif marker['name'] == 'industrial_revolution':
                    st.markdown("🏭 **Industrial Revolution (1850 CE)**: This is when people began burning large amounts of coal to power factories. This marks the beginning of rapidly increasing carbon dioxide in the atmosphere.")
                elif marker['name'] == 'great_acceleration':
                    st.markdown("🚀 **Great Acceleration (1950 CE)**: After World War II, there was an enormous increase in car use, energy consumption, and manufacturing worldwide, causing much more pollution.")
                elif marker['name'] == 'recent_warming':
                    st.markdown("🔥 **Recent Rapid Warming (2000 CE)**: The 21st century has seen record-breaking temperatures. Most of the 20 warmest years on record have occurred since 2000.")
    
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
            • See the red line going up quickly? Earth is warming faster than it has for thousands of years!<br>
            • The colored markers show important periods in history.
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
