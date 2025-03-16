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
def plot_simple_temperature(df_obs, df_recon, show_old_times=True, show_new_times=True, show_star=True):
    fig, ax = plt.subplots(figsize=(8, 5))  # Slightly larger as we removed some content
    
    # Plot the old temperatures (blue)
    if show_old_times:
        ax.plot(df_recon["Year"], df_recon["Temperature"], color="#6495ED", lw=2, label="Old Times")
    
    # Plot the new temperatures (red)
    if show_new_times:
        ax.plot(df_obs["Year"], df_obs["Temperature"], color="#FF6347", lw=3, label="New Times")
    
    # Add a horizontal line at zero
    ax.axhline(0, color="black", linestyle="--", alpha=0.5)
    
    # Mark "NOW" with a star
    if show_star and show_new_times:
        latest_year = df_obs["Year"].max()
        latest_temp = df_obs.loc[df_obs["Year"] == latest_year, "Temperature"].values[0]
        ax.scatter([latest_year], [latest_temp], color="gold", s=150, marker="*", zorder=5)
        ax.annotate("NOW!", xy=(latest_year, latest_temp), xytext=(latest_year-50, latest_temp+0.2),
                    fontsize=12, fontweight="bold", color="purple")
    
    # Styling
    ax.set_title("Earth's Temperature Story", fontsize=16, fontweight="bold")
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Is Earth Getting Warmer?", fontsize=12)
    
    # Simplify the y-axis
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["Cooler", "Normal", "Warmer"], fontsize=12)
    
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
    
    # SIDEBAR WITH SIMPLE TOGGLES ONLY
    with st.sidebar:
        st.title("Play with the Chart!")
        
        # Simple toggles for lines with fun language
        st.subheader("🎨 Show or Hide")
        show_old = st.checkbox("Show OLD times (Blue line)", value=True)
        show_new = st.checkbox("Show NEW times (Red line)", value=True)
        show_star_now = st.checkbox("Show golden star ⭐", value=True)

    # Two column layout for main content
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Simple explanation
        st.markdown('<p class="big-text">This picture shows how Earth\'s temperature has changed over a very long time.</p>', unsafe_allow_html=True)
        
        # Display the simple graph with filter options applied
        fig = plot_simple_temperature(df_obs, df_recon, show_old, show_new, show_star_now)
        st.pyplot(fig)
    
    with col_right:
        # Explanation buttons with emoji - vertical stack
        st.subheader("Click to learn more!")
        
        # Compact buttons layout
        if st.button("🔎 What Do We See?", key="what"):
            st.markdown("""
            <div style="background-color:#E6F9FF; padding:10px; border-radius:10px;">
            <p style="font-size:16px">
            • Blue line shows how Earth was long ago.<br>
            • Red line shows how Earth is now.<br> 
            • See the red line going up? Earth is getting warmer!
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
            🌳 Plant trees • 🚶 Walk more • 💡 Turn off lights<br>
            🚿 Take shorter showers • ♻️ Recycle
            </p>
            </div>
            """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
