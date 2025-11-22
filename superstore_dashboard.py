import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Superstore Sales Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stMetric {
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric label {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 700 !important;
    }
    h1 {color: #1f77b4; text-align: center;}
    h2 {color: #2c3e50;}
    h3 {color: #34495e;}
    </style>
    """, unsafe_allow_html=True)

# LOAD DATA FUNCTION
@st.cache_data
def load_data():


    df = pd.read_csv('./DATASET/superstore_cleaned.csv')
    
    
    np.random.seed(42)
    dates = pd.date_range('2014-01-01', '2017-12-31', freq='D')
    
    data = {
        'Order_Date': np.random.choice(dates, 10000),
        'Category': np.random.choice(['Furniture', 'Office Supplies', 'Technology'], 10000),
        'Sub_Category': np.random.choice(['Chairs', 'Tables', 'Paper', 'Binders', 'Phones', 'Accessories'], 10000),
        'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], 10000),
        'State': np.random.choice(['California', 'New York', 'Texas', 'Florida', 'Pennsylvania'], 10000),
        'City': np.random.choice(['Los Angeles', 'New York City', 'Houston', 'Philadelphia', 'San Francisco'], 10000),
        'Sales': np.random.uniform(10, 5000, 10000),
        'Quantity': np.random.randint(1, 10, 10000),
        'Discount': np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5], 10000),
        'Profit': np.random.uniform(-1000, 2000, 10000),
        'Ship_Mode': np.random.choice(['Standard Class', 'Second Class', 'First Class', 'Same Day'], 10000)
    }
    
    df = pd.DataFrame(data)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month
    df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
    
    return df

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    
    # Title
    st.markdown("<h1>📊 Superstore Sales Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    with st.spinner('⏳ Loading data...'):
        df = load_data()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['Order_Date'].min()
    max_date = df['Order_Date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Category filter
    categories = st.sidebar.multiselect(
        "Select Categories",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )
    
    # Segment filter
    segments = st.sidebar.multiselect(
        "Select Segments",
        options=df['Segment'].unique(),
        default=df['Segment'].unique()
    )
    
    # State filter
    states = st.sidebar.multiselect(
        "Select States",
        options=sorted(df['State'].unique()),
        default=sorted(df['State'].unique())
    )
    
    # Apply filters
    if len(date_range) == 2:
        df_filtered = df[
            (df['Order_Date'].dt.date >= date_range[0]) &
            (df['Order_Date'].dt.date <= date_range[1]) &
            (df['Category'].isin(categories)) &
            (df['Segment'].isin(segments)) &
            (df['State'].isin(states))
        ]
    else:
        df_filtered = df[
            (df['Category'].isin(categories)) &
            (df['Segment'].isin(segments)) &
            (df['State'].isin(states))
        ]
    
    # ========================================================================
    # KEY METRICS (KPIs)
    # ========================================================================
    st.markdown("<h2>📈 Key Performance Indicators</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    total_sales = df_filtered['Sales'].sum()
    total_profit = df_filtered['Profit'].sum()
    total_orders = len(df_filtered)
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0

    st.markdown("""
    <style>
        .kpi-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin: 10px;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
            margin: 10px 0;
        }
        .kpi-label {
            font-size: 14px;
            color: #666;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

    with col1:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">💰 Total Sales</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">📊 Total Profit</div>
            <div class="kpi-value">${total_profit:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">🛒 Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">📉 Profit Margin</div>
            <div class="kpi-value">{profit_margin:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">💵 Avg Order Value</div>
            <div class="kpi-value">${avg_order_value:.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    # ========================================================================
    # SECTION 1: SALES ANALYSIS
    # ========================================================================
    st.markdown("<h2>📊 Sales Analysis</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["By Category", "By Segment", "By Time"])
    
    # Tab 1: By Category
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by Category
            category_sales = df_filtered.groupby('Category').agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Order_Date': 'count'
            }).reset_index()
            category_sales.columns = ['Category', 'Sales', 'Profit', 'Orders']
            category_sales = category_sales.sort_values('Sales', ascending=False)
            
            fig_cat = px.bar(
                category_sales,
                x='Category',
                y='Sales',
                color='Category',
                title='Sales by Category',
                text_auto='.2s',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_cat.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_cat, use_container_width=True)
            
        with col2:
            # Profit by Category
            fig_profit = px.pie(
                category_sales,
                values='Profit',
                names='Category',
                title='Profit Distribution by Category',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_profit.update_layout(height=400)
            st.plotly_chart(fig_profit, use_container_width=True)
        
        # Category Details Table
        st.markdown("### Category Performance Details")
        category_sales['Profit_Margin_%'] = (category_sales['Profit'] / category_sales['Sales'] * 100).round(2)
        st.dataframe(
            category_sales.style.format({
                'Sales': '${:,.2f}',
                'Profit': '${:,.2f}',
                'Orders': '{:,}',
                'Profit_Margin_%': '{:.2f}%'
            }),
            use_container_width=True
        )
    
    # Tab 2: By Segment
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by Segment
            segment_sales = df_filtered.groupby('Segment').agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            fig_seg = px.bar(
                segment_sales,
                x='Segment',
                y=['Sales', 'Profit'],
                title='Sales & Profit by Segment',
                barmode='group',
                color_discrete_sequence=['#3b82f6', '#10b981']
            )
            fig_seg.update_layout(height=400)
            st.plotly_chart(fig_seg, use_container_width=True)
            
        with col2:
            # Segment Distribution
            fig_seg_pie = px.pie(
                segment_sales,
                values='Sales',
                names='Segment',
                title='Sales Distribution by Segment',
                hole=0.4
            )
            fig_seg_pie.update_layout(height=400)
            st.plotly_chart(fig_seg_pie, use_container_width=True)
    
    # Tab 3: By Time
    with tab3:
        # Monthly Sales Trend
        monthly_sales = df_filtered.groupby(df_filtered['Order_Date'].dt.to_period('M')).agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        monthly_sales['Order_Date'] = monthly_sales['Order_Date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_sales['Order_Date'],
            y=monthly_sales['Sales'],
            name='Sales',
            line=dict(color='#3b82f6', width=3)
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_sales['Order_Date'],
            y=monthly_sales['Profit'],
            name='Profit',
            line=dict(color='#10b981', width=3)
        ))
        fig_trend.update_layout(
            title='Monthly Sales & Profit Trend',
            xaxis_title='Date',
            yaxis_title='Amount ($)',
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Yearly Comparison
        yearly_sales = df_filtered.groupby('Year').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order_Date': 'count'
        }).reset_index()
        yearly_sales.columns = ['Year', 'Sales', 'Profit', 'Orders']
        
        st.markdown("### Yearly Performance")
        st.dataframe(
            yearly_sales.style.format({
                'Sales': '${:,.2f}',
                'Profit': '${:,.2f}',
                'Orders': '{:,}'
            }),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 2: GEOGRAPHIC ANALYSIS
    # ========================================================================
    st.markdown("<h2>🗺️ Geographic Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 States by Sales
        state_sales = df_filtered.groupby('State')['Sales'].sum().reset_index()
        state_sales = state_sales.sort_values('Sales', ascending=False).head(10)
        
        fig_states = px.bar(
            state_sales,
            x='Sales',
            y='State',
            orientation='h',
            title='Top 10 States by Sales',
            color='Sales',
            color_continuous_scale='Blues'
        )
        fig_states.update_layout(height=500)
        st.plotly_chart(fig_states, use_container_width=True)
    
    with col2:
        # Top 10 Cities by Profit
        city_profit = df_filtered.groupby('City')['Profit'].sum().reset_index()
        city_profit = city_profit.sort_values('Profit', ascending=False).head(10)
        
        fig_cities = px.bar(
            city_profit,
            x='Profit',
            y='City',
            orientation='h',
            title='Top 10 Cities by Profit',
            color='Profit',
            color_continuous_scale='Greens'
        )
        fig_cities.update_layout(height=500)
        st.plotly_chart(fig_cities, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 3: PRODUCT ANALYSIS
    # ========================================================================
    st.markdown("<h2>📦 Product Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Sub-Categories by Sales
        subcat_sales = df_filtered.groupby('Sub_Category').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        subcat_sales = subcat_sales.sort_values('Sales', ascending=False).head(10)
        
        fig_subcat = px.bar(
            subcat_sales,
            x='Sub_Category',
            y='Sales',
            title='Top 10 Sub-Categories by Sales',
            color='Sales',
            color_continuous_scale='Viridis'
        )
        fig_subcat.update_layout(height=400)
        st.plotly_chart(fig_subcat, use_container_width=True)
    
    with col2:
        # Profit Margin by Sub-Category
        subcat_sales['Profit_Margin'] = (subcat_sales['Profit'] / subcat_sales['Sales'] * 100).round(2)
        
        fig_margin = px.scatter(
            subcat_sales,
            x='Sales',
            y='Profit_Margin',
            size='Profit',
            color='Sub_Category',
            title='Profit Margin vs Sales by Sub-Category',
            hover_data=['Sub_Category']
        )
        fig_margin.update_layout(height=400)
        st.plotly_chart(fig_margin, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 4: DISCOUNT ANALYSIS
    # ========================================================================
    st.markdown("<h2>💸 Discount Impact Analysis</h2>", unsafe_allow_html=True)
    
    discount_analysis = df_filtered.groupby('Discount').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order_Date': 'count'
    }).reset_index()
    discount_analysis.columns = ['Discount', 'Sales', 'Profit', 'Orders']
    discount_analysis['Discount'] = (discount_analysis['Discount'] * 100).astype(int).astype(str) + '%'
    discount_analysis['Profit_Margin'] = (discount_analysis['Profit'] / discount_analysis['Sales'] * 100).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_disc_sales = px.bar(
            discount_analysis,
            x='Discount',
            y='Sales',
            title='Sales by Discount Level',
            color='Sales',
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig_disc_sales, use_container_width=True)
    
    with col2:
        fig_disc_profit = px.line(
            discount_analysis,
            x='Discount',
            y='Profit_Margin',
            title='Profit Margin by Discount Level',
            markers=True,
            line_shape='spline'
        )
        fig_disc_profit.update_traces(line_color='#ef4444', marker_size=10)
        st.plotly_chart(fig_disc_profit, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 5: SHIPPING ANALYSIS
    # ========================================================================
    st.markdown("<h2>🚚 Shipping Mode Analysis</h2>", unsafe_allow_html=True)
    
    shipping = df_filtered.groupby('Ship_Mode').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order_Date': 'count'
    }).reset_index()
    shipping.columns = ['Ship_Mode', 'Sales', 'Profit', 'Orders']
    shipping = shipping.sort_values('Orders', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ship = px.pie(
            shipping,
            values='Orders',
            names='Ship_Mode',
            title='Orders Distribution by Shipping Mode',
            hole=0.4
        )
        st.plotly_chart(fig_ship, use_container_width=True)
    
    with col2:
        st.markdown("### Shipping Mode Performance")
        st.dataframe(
            shipping.style.format({
                'Sales': '${:,.2f}',
                'Profit': '${:,.2f}',
                'Orders': '{:,}'
            }),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 6: RAW DATA EXPLORER
    # ========================================================================
    with st.expander("🔍 View Raw Data"):
        st.markdown("### Filtered Dataset Preview")
        st.dataframe(df_filtered.head(100), use_container_width=True)
        
        # Download button
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_superstore_data.csv',
            mime='text/csv'
        )
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
            <p>📊 Superstore Sales Analysis Dashboard</p>
            <p>Built with Streamlit | Data Period: 2014-2017</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    main()