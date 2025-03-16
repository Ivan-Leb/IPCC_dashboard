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

# Define cartoon character explanations - RENAMED CHARACTERS WITH QUICKER INTROS
def get_cartoon_explanations():
    # Shorter explanations with renamed characters
    what_explanation = """
    <div style="background-color:#E6F9FF; padding:12px; border-radius:15px; border:2px dashed #6495ED;">
    <div style="display:flex; align-items:center;">
    <div style="font-size:50px; margin-right:12px;">👩‍🏫</div>
    <div>
    <p style="font-size:16px; font-weight:bold;">Professor Tina says:</p>
    <p style="font-size:14px;">
    • <span style="color:blue">Blue line</span>: Earth's temperature long ago<br>
    • <span style="color:red">Red line</span>: Recent temperatures<br>
    • The red line shoots up at the end - Earth is warming fast!
    </p>
    </div>
    </div>
    </div>
    """
    
    why_explanation = """
    <div style="background-color:#FFF9E6; padding:12px; border-radius:15px; border:2px dashed #FFB347;">
    <div style="display:flex; align-items:center;">
    <div style="font-size:50px; margin-right:12px;">👨‍🔬</div>
    <div>
    <p style="font-size:16px; font-weight:bold;">Professor Theo says:</p>
    <p style="font-size:14px;">
    • Cars, factories, and homes burn fuels that release gases.<br><br>
    • These gases work like a blanket around Earth, trapping heat.<br><br>
    • More gases = warmer planet!
    </p>
    </div>
    </div>
    </div>
    """
    
    help_explanation = """
    <div style="background-color:#E6FFE6; padding:12px; border-radius:15px; border:2px dashed #4CAF50;">
    <div style="display:flex; align-items:center;">
    <div style="font-size:50px; margin-right:12px;">🦸‍♀️</div>
    <div>
    <p style="font-size:16px; font-weight:bold;">Captain Climate says:</p>
    <p style="font-size:14px;">
    🌳 Plant trees • 🚶‍♂️ Walk more • 🚲 Ride bikes<br>
    💡 Save energy • ♻️ Recycle • 🥕 Eat plants<br>
    🚿 Save water • 📚 Learn more
    </p>
    </div>
    </div>
    </div>
    """
    
    return what_explanation, why_explanation, help_explanation

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
    
    with col_right:
        # Get cartoon character explanations
        what_explanation, why_explanation, help_explanation = get_cartoon_explanations()
        
        # Explanation buttons with emoji
        st.subheader("Click to learn more!")
        
        # Compact buttons layout with cartoon character responses
        if st.button("🔎 What Do We See?", key="what"):
            st.markdown(what_explanation, unsafe_allow_html=True)
        
        if st.button("❓ Why Is This Happening?", key="why"):
            st.markdown(why_explanation, unsafe_allow_html=True)
        
        if st.button("🌱 How Can We Help?", key="help"):
            st.markdown(help_explanation, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
