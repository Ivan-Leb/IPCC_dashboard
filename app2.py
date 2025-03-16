import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to prepare the data
def prepare_data():
    try:
        # Load the observed data (1850-2020)
        df_obs = pd.read_csv("/Users/ivanleboucher/Desktop/Cours/data_viz/assessment_IPCC/SPM1_1850-2020_obs.csv", skiprows=15, encoding="latin1")
        df_obs = df_obs.rename(columns={"1": "Year", "2": "Temperature"}).drop(columns=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"])  
        df_obs["Temperature"] = pd.to_numeric(df_obs["Temperature"], errors="coerce")
        df_obs["Source"] = "Observed"

        # Load the reconstructed data (1-2000)
        df_recon = pd.read_csv("/Users/ivanleboucher/Desktop/Cours/data_viz/assessment_IPCC/SPM1_1-2000_recon.csv", skiprows=19, encoding="latin1")
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
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the old temperatures (blue)
    ax.plot(df_recon["Year"], df_recon["Temperature"], color="#6495ED", lw=2, label="Old Times")
    
    # Plot the new temperatures (red)
    ax.plot(df_obs["Year"], df_obs["Temperature"], color="#FF6347", lw=3, label="New Times")
    
    # Add a horizontal line at zero
    ax.axhline(0, color="black", linestyle="--", alpha=0.5)
    
    # Mark "NOW" with a star
    latest_year = df_obs["Year"].max()
    latest_temp = df_obs.loc[df_obs["Year"] == latest_year, "Temperature"].values[0]
    ax.scatter([latest_year], [latest_temp], color="gold", s=200, marker="*", zorder=5)
    ax.annotate("NOW!", xy=(latest_year, latest_temp), xytext=(latest_year-50, latest_temp+0.2),
                fontsize=14, fontweight="bold", color="purple")
    
    # Styling
    ax.set_title("Earth's Temperature Story", fontsize=20, fontweight="bold")
    ax.set_xlabel("Time", fontsize=16)
    ax.set_ylabel("Is Earth Getting Warmer?", fontsize=16)
    
    # Simplify the y-axis
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["Cooler ❄️", "Normal", "Warmer 🔥"], fontsize=14)
    
    # Set background color
    ax.set_facecolor("#F0F8FF")  # Light blue background
    
    # Make grid child-friendly
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.3)
    
    # Add a legend with large font
    ax.legend(fontsize=14, loc="upper left")
    
    # Set limits
    ax.set_xlim(df_recon["Year"].min(), df_obs["Year"].max())
    
    return fig

# Streamlit App
def main():
    # Set page config
    st.set_page_config(
        page_title="Earth's Temperature for Kids",
        page_icon="🌍",
        layout="wide"
    )
    
    # Apply a custom style with larger, more readable text
    st.markdown("""
        <style>
        .big-text {font-size: 24px !important;}
        button {font-size: 20px !important; padding: 15px !important;}
        </style>
        """, unsafe_allow_html=True)
    
    # Prepare the data
    df_obs, df_recon = prepare_data()
    
    # Check if data is loaded correctly
    if df_obs.empty or df_recon.empty:
        st.error("Could not load the datasets. Please check file paths and try again.")
        return
    
    # Title with emoji
    st.title("🌍 Our Earth is Getting Warmer")
    
    # Simple explanation
    st.markdown('<p class="big-text">This picture shows how Earth\'s temperature has changed over a very long time.</p>', unsafe_allow_html=True)
    
    # Display the simple graph
    fig = plot_simple_temperature(df_obs, df_recon)
    st.pyplot(fig)
    
    # Explanation buttons with emoji
    st.subheader("Click the buttons to learn more!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔎 What Do We See?", key="what"):
            st.markdown("""
            <div style="background-color:#E6F9FF; padding:15px; border-radius:10px;">
            <p style="font-size:18px">
            The blue line shows how warm or cool Earth was a long time ago.
            <br><br>
            The red line shows how warm Earth is now. 
            <br><br>
            See how the red line goes up? That means Earth is getting warmer!
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("❓ Why Is This Happening?", key="why"):
            st.markdown("""
            <div style="background-color:#FFF9E6; padding:15px; border-radius:10px;">
            <p style="font-size:18px">
            Cars, factories, and things we use make something called "pollution."
            <br><br>
            This pollution makes a blanket around Earth that traps heat.
            <br><br>
            It's like when you put on too many blankets and get too hot!
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🌱 How Can We Help?", key="help"):
            st.markdown("""
            <div style="background-color:#E6FFE6; padding:15px; border-radius:10px;">
            <p style="font-size:18px">
            🌳 Plant trees<br>
            🚶 Walk more<br>
            💡 Turn off lights<br>
            🚿 Take shorter showers<br>
            ♻️ Recycle
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Images section
    st.subheader("Touch to see what these mean!")
    
    image_col1, image_col2, image_col3 = st.columns(3)
    
    with image_col1:
        if st.button("🧊 Cold Earth"):
            st.markdown("""
            <div style="background-color:#E6F9FF; padding:15px; border-radius:10px; text-align:center;">
            <p style="font-size:18px">
            Long ago, Earth was sometimes colder.<br>
            There was more ice and snow!
            </p>
            </div>
            """, unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1478719059408-592965723cbc?ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80", caption="Ice and Snow")
    
    with image_col2:
        if st.button("🌡️ Hot Earth"):
            st.markdown("""
            <div style="background-color:#FFE6E6; padding:15px; border-radius:10px; text-align:center;">
            <p style="font-size:18px">
            Earth is getting warmer now.<br>
            Ice is melting and weather is changing.
            </p>
            </div>
            """, unsafe_allow_html=True)
            # UPDATED HOT WEATHER IMAGE - showing drought/dry land
            st.image("https://images.unsplash.com/photo-1504809982868-33c5eacc6026?ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80", caption="Hot and Dry Earth")
    
    with image_col3:
        if st.button("🌳 Happy Earth"):
            st.markdown("""
            <div style="background-color:#E6FFE6; padding:15px; border-radius:10px; text-align:center;">
            <p style="font-size:18px">
            We can help keep Earth happy<br>
            by taking care of nature!
            </p>
            </div>
            """, unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1552799446-159ba9523315?ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80", caption="Green Nature")

# Run the app
if __name__ == "__main__":
    main()
