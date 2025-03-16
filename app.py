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
def plot_simple_temperature(df_obs, df_recon):
    fig, ax = plt.subplots(figsize=(8, 4))  # REDUCED SIZE
    
    # Plot the old temperatures (blue)
    ax.plot(df_recon["Year"], df_recon["Temperature"], color="#6495ED", lw=2, label="Old Times")
    
    # Plot the new temperatures (red)
    ax.plot(df_obs["Year"], df_obs["Temperature"], color="#FF6347", lw=3, label="New Times")
    
    # Add a horizontal line at zero
    ax.axhline(0, color="black", linestyle="--", alpha=0.5)
    
    # Mark "NOW" with a star
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
    ax.set_yticklabels(["Cooler ❄️", "Normal", "Warmer"], fontsize=12)
    
    # Set background color
    ax.set_facecolor("#F0F8FF")  # Light blue background
    
    # Make grid child-friendly
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.3)
    
    # Add a legend with large font
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
    
    # Two column layout for main content
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Simple explanation
        st.markdown('<p class="big-text">This picture shows how Earth\'s temperature has changed over a very long time.</p>', unsafe_allow_html=True)
        
        # Display the simple graph
        fig = plot_simple_temperature(df_obs, df_recon)
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
    
    # Images section - 3 column layout
    st.subheader("Touch to see these pictures!")
    
    image_col1, image_col2, image_col3 = st.columns(3)
    


    with image_col1:
        if st.button("🧊 Cold Earth", key="cold"):
            # More reliable image URL with https
            st.image("https://images.unsplash.com/photo-1478719059408-592965723cbc?ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80", 
                   caption="Ice and Snow", width=300)
            st.markdown("""<p style="font-size:14px; text-align:center">Long ago, Earth had more ice and snow!</p>""", 
                      unsafe_allow_html=True)
    
    with image_col2:
        if st.button("🌡️ Hot Earth", key="hot"):
            # FIXED: New reliable image URL from a different source
            st.image("science.adl5889-fa.jpg", 
                   caption="Hot and Dry Earth", width=300)
            st.markdown("""<p style="font-size:14px; text-align:center">Earth is getting too hot and dry now!</p>""", 
                      unsafe_allow_html=True)
    
    with image_col3:
        if st.button("🌳 Happy Earth", key="happy"):
            # More reliable image URL
            st.image("https://cdn.pixabay.com/photo/2015/12/01/20/28/green-1072828_1280.jpg", 
                   caption="Green Nature", width=300)
            st.markdown("""<p style="font-size:14px; text-align:center">We can help keep Earth happy!</p>""", 
                      unsafe_allow_html=True)















    # with image_col1:
    #     if st.button("🧊 Cold Earth", key="cold"):
    #         # Made image smaller to fit better
    #         st.image("https://images.unsplash.com/photo-1478719059408-592965723cbc", 
    #                caption="Ice and Snow", width=300)
    #         st.markdown("""<p style="font-size:14px; text-align:center">Long ago, Earth had more ice and snow!</p>""", 
    #                   unsafe_allow_html=True)
    
    # with image_col2:
    #     if st.button("🌡️ Hot Earth", key="hot"):
    #         # Made image smaller to fit better
    #         st.image("https://images.unsplash.com/photo-1504809982868-33c5eacc6026", 
    #                caption="Hot and Dry Earth", width=300)
    #         st.markdown("""<p style="font-size:14px; text-align:center">Earth is getting too hot and dry now!</p>""", 
    #                   unsafe_allow_html=True)
    
    # with image_col3:
    #     if st.button("🌳 Happy Earth", key="happy"):
    #         # Made image smaller to fit better
    #         st.image("https://images.unsplash.com/photo-1552799446-159ba9523315", 
    #                caption="Green Nature", width=300)
    #         st.markdown("""<p style="font-size:14px; text-align:center">We can help keep Earth happy!</p>""", 
    #                   unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()