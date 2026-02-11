import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Wio Bank Performance 2024", layout="wide")

# 2. Custom CSS Branding (Wio Dark Theme + Skyline Background)
st.markdown("""
    <style>
    /* Gradient Background inspired by Abu Dhabi Skyline Branding */
    .stApp {
        background: linear-gradient(180deg, #050A18 0%, #0B1221 100%);
        color: #FFFFFF;
    }
    
    /* Header & Metric Styling */
    h1, h2, h3, [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Neon Cyan Metric Values */
    [data-testid="stMetricValue"] {
        color: #00E5FF !important;
        font-weight: 700 !important;
    }
    
    /* Metric Card Containers */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #050A18;
        border-right: 1px solid rgba(0, 229, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
# Skyline Banner Placeholder - Reflecting the Abu Dhabi towers in your branding doc
st.image("https://images.unsplash.com/photo-1512453979798-5eaad0ff3b0d?auto=format&fit=crop&w=1400&q=80", use_container_width=True)
st.title("🏦 Wio Bank PJSC") [cite: 1]
st.markdown("## Strategic Product Performance Dashboard")
st.caption("Derived from the Annual Financial Statements for the year ended 31 December 2024 [cite: 2, 3]")

st.write("---")

# 4. Load & Process Data
@st.cache_data
def load_data():
    df = pd.read_csv('wio_data.csv')
    return df

try:
    df = load_data()
    
    # 5. Sidebar Navigation & Filters
    st.sidebar.title("Dashboard Controls")
    selected_segment = st.sidebar.multiselect("Select Segment", options=df["Segment"].unique(), default=df["Segment"].unique())
    month_filter = st.sidebar.select_slider("Select Time Range", options=df["Month"].unique(), value=("Jan", "Dec"))
    
    filtered_df = df[df["Segment"].isin(selected_segment)]
    
    # 6. KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Portfolio Volume", f"AED {filtered_df['Total Volume (AED)'].sum()/1e9:.1f}B")
    with col2:
        st.metric("Weighted Avg NIM", f"{filtered_df['NIM (%)'].mean():.2f}%")
    with col3:
        asset_npl = filtered_df[filtered_df["Product Type"] == "Asset"]["NPL Ratio (%)"].mean()
        st.metric("Portfolio Risk (NPL)", f"{asset_npl:.2f}%")
    with col4:
        st.metric("Active Customer Base", f"{filtered_df['Active Customers'].sum():,}")

    st.write("### Sector Deep Dive")
    
    # 7. Visual Analytics
    row1_c1, row1_c2 = st.columns(2)

    with row1_c1:
        # Risk vs Reward Bubble Chart
        st.write("#### NIM (%) vs. Risk (NPL Ratio)")
        fig_bubble = px.scatter(
            filtered_df, x="NPL Ratio (%)", y="NIM (%)", 
            size="Total Volume (AED)", color="Segment",
            hover_name="Product Name", template="plotly_dark",
            color_discrete_map={"Corporate": "#007BFF", "SME": "#00E5FF", "Retail": "#FF007A"}
        )
        fig_bubble.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bubble, use_container_width=True)
        

    with row1_c2:
        # Monthly Volume Trajectory
        st.write("#### Monthly Asset & Liability Growth")
        fig_line = px.line(
            filtered_df.groupby(["Month", "Product Type"])["Total Volume (AED)"].sum().reset_index(),
            x="Month", y="Total Volume (AED)", color="Product Type",
            markers=True, template="plotly_dark",
            color_discrete_sequence=["#00E5FF", "#7000FF"]
        )
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)

    # 8. Data Table
    with st.expander("📝 View Full Transactional Log"):
        st.dataframe(filtered_df.style.format({"Total Volume (AED)": "{:,.0f}"}), use_container_width=True)

except FileNotFoundError:
    st.error("Please ensure 'wio_data.csv' is in the same directory as this script.")