# app.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

# Set page configuration
st.set_page_config(
    page_title="InnBucks Zimbabwe Dashboard Proof of concept by Takundanashe moyo",
    page_icon="🏦",
    layout="wide"
)

# Generate synthetic data for InnBucks Zimbabwe
def generate_innbucks_data():
    np.random.seed(42)
    
    # Zimbabwe-specific data
    branches = ['Harare CBD', 'Bulawayo Central', 'Mutare', 'Gweru']
    mobile_networks = ['Econet', 'NetOne', 'Telecel']
    
    # Customer data
    n_customers = 1000
    customer_ids = [f'INN{i:04d}' for i in range(1, n_customers+1)]
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'customer_type': np.random.choice(['Individual', 'Agent', 'Merchant'], n_customers, p=[0.85, 0.1, 0.05]),
        'region': np.random.choice(['Harare', 'Bulawayo', 'Midlands', 'Masvingo'], n_customers),
        'branch': np.random.choice(branches, n_customers),
        'mobile_network': np.random.choice(mobile_networks, n_customers, p=[0.7, 0.2, 0.1]),
        'kyc_status': np.random.choice(['Verified', 'Pending'], n_customers, p=[0.8, 0.2])
    })
    
    # Account data
    accounts_data = []
    for cust_id in customer_ids:
        usd_balance = max(10, np.random.lognormal(5, 1.2))
        
        accounts_data.append({
            'customer_id': cust_id,
            'account_id': f'ACC{cust_id}',
            'usd_balance': usd_balance,
            'account_status': 'Active'
        })
    
    accounts_df = pd.DataFrame(accounts_data)
    
    # Transaction data (last 30 days)
    transactions_data = []
    start_date = datetime.datetime.now() - timedelta(days=30)
    
    for account in accounts_data:
        n_transactions = np.random.poisson(15)
        
        for i in range(n_transactions):
            transaction_date = start_date + timedelta(
                days=np.random.randint(0, 30), 
                hours=np.random.randint(0, 24)
            )
            transaction_type = np.random.choice(
                ['Send Money', 'Cash In', 'Cash Out', 'Bill Payment', 'Airtime'], 
                p=[0.4, 0.2, 0.15, 0.15, 0.1]
            )
            
            amount = abs(np.random.lognormal(3.5, 1.0))
            channel = np.random.choice(['Mobile App', 'USSD', 'Agent'], p=[0.6, 0.3, 0.1])
            
            transactions_data.append({
                'transaction_id': f'TXN{account["account_id"]}{i}',
                'account_id': account['account_id'],
                'transaction_date': transaction_date,
                'amount_usd': amount,
                'transaction_type': transaction_type,
                'channel': channel,
                'status': 'Completed'
            })
    
    transactions_df = pd.DataFrame(transactions_data)
    
    return customers_df, accounts_df, transactions_df

# Calculate KPIs
def calculate_kpis(customers_df, accounts_df, transactions_df):
    total_customers = customers_df['customer_id'].nunique()
    total_transactions = len(transactions_df)
    total_volume = transactions_df['amount_usd'].sum()
    total_deposits = accounts_df['usd_balance'].sum()
    kyc_completion_rate = (customers_df['kyc_status'] == 'Verified').mean()
    avg_transaction_size = transactions_df['amount_usd'].mean()
    
    # Weekly growth (simulated)
    weekly_growth = np.random.uniform(0.05, 0.15)
    
    return {
        'total_customers': total_customers,
        'total_transactions': total_transactions,
        'total_volume': total_volume,
        'total_deposits': total_deposits,
        'kyc_completion_rate': kyc_completion_rate,
        'avg_transaction_size': avg_transaction_size,
        'weekly_growth': weekly_growth
    }

# Generate data
customers_df, accounts_df, transactions_df = generate_innbucks_data()
kpis = calculate_kpis(customers_df, accounts_df, transactions_df)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Main background and text colors */
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #262730;
    }
    
    /* Metric cards styling */
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin: 10px 0;
        color: #FAFAFA;
    }
    
    /* Section headers */
    .section-header {
        color: #FF4B4B;
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 10px;
        margin: 20px 0;
        font-weight: bold;
    }
    
    /* Dataframe styling */
    .dataframe {
        background-color: #262730;
        color: #FAFAFA;
    }
    
    /* Streamlit metric styling */
    [data-testid="stMetricValue"] {
        color: #FAFAFA;
    }
    
    [data-testid="stMetricLabel"] {
        color: #FF4B4B;
    }
    
    [data-testid="stMetricDelta"] {
        color: #00FF00;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #262730;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B;
    }
    
    /* Header styling */
    .main-header {
        color: #FF4B4B;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        color: #FAFAFA;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .author-credit {
        color: #FF4B4B;
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main dashboard with dark theme
st.markdown('<h1 class="main-header">🏦 InnBucks Zimbabwe Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<div class="author-credit">Proof of Concept by Takundanashe Moyo</div>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-header">Digital Financial Services Analytics</h3>', unsafe_allow_html=True)

# KPI Metrics
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers", 
        f"{kpis['total_customers']:,}",
        f"+{int(kpis['total_customers'] * kpis['weekly_growth'])} weekly"
    )

with col2:
    st.metric(
        "Total Transactions", 
        f"{kpis['total_transactions']:,}",
        f"+{int(kpis['total_transactions'] * kpis['weekly_growth'])} weekly"
    )

with col3:
    st.metric(
        "Total Volume", 
        f"${kpis['total_volume']:,.0f}",
        f"+${int(kpis['total_volume'] * kpis['weekly_growth']):,} weekly"
    )

with col4:
    st.metric(
        "Customer Deposits", 
        f"${kpis['total_deposits']:,.0f}",
        "Liquidity"
    )

# Second row of KPIs
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("KYC Completion", f"{kpis['kyc_completion_rate']:.1%}")

with col6:
    st.metric("Avg Transaction", f"${kpis['avg_transaction_size']:.1f}")

with col7:
    st.metric("Active Accounts", f"{len(accounts_df):,}")

with col8:
    success_rate = 0.98  # Simulated success rate
    st.metric("Success Rate", f"{success_rate:.1%}")

# Transaction Analytics
st.markdown('<div class="section-header">📊 Transaction Analytics</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Types")
    txn_types = transactions_df['transaction_type'].value_counts()
    st.dataframe(
        txn_types.reset_index().rename(columns={'index': 'Type', 'transaction_type': 'Count'}),
        use_container_width=True
    )
    
    # Simple bar chart using st.bar_chart
    st.subheader("Transaction Volume by Type")
    txn_volume = transactions_df.groupby('transaction_type')['amount_usd'].sum().sort_values(ascending=False)
    st.bar_chart(txn_volume)

with col2:
    st.subheader("Channel Usage")
    channel_usage = transactions_df['channel'].value_counts()
    st.dataframe(
        channel_usage.reset_index().rename(columns={'index': 'Channel', 'channel': 'Count'}),
        use_container_width=True
    )
    
    # Channel distribution
    st.subheader("Transactions by Channel")
    st.bar_chart(channel_usage)

# Customer Analytics
st.markdown('<div class="section-header">👥 Customer Analytics</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Customer Distribution by Region")
    regional_dist = customers_df['region'].value_counts()
    st.dataframe(
        regional_dist.reset_index().rename(columns={'index': 'Region', 'region': 'Count'}),
        use_container_width=True
    )
    st.bar_chart(regional_dist)

with col4:
    st.subheader("Customer Types")
    customer_types = customers_df['customer_type'].value_counts()
    st.dataframe(
        customer_types.reset_index().rename(columns={'index': 'Type', 'customer_type': 'Count'}),
        use_container_width=True
    )
    
    st.subheader("Mobile Network Distribution")
    network_dist = customers_df['mobile_network'].value_counts()
    st.dataframe(
        network_dist.reset_index().rename(columns={'index': 'Network', 'mobile_network': 'Count'}),
        use_container_width=True
    )

# Daily Trends
st.markdown('<div class="section-header">📈 Daily Transaction Trends</div>', unsafe_allow_html=True)

# Create daily volume data
transactions_df['date'] = transactions_df['transaction_date'].dt.date
daily_volume = transactions_df.groupby('date')['amount_usd'].sum().reset_index()
daily_count = transactions_df.groupby('date')['transaction_id'].count().reset_index()

col5, col6 = st.columns(2)

with col5:
    st.subheader("Daily Transaction Volume (USD)")
    st.line_chart(daily_volume.set_index('date')['amount_usd'])

with col6:
    st.subheader("Daily Transaction Count")
    st.line_chart(daily_count.set_index('date')['transaction_id'])

# Data tables with filters
st.markdown('<div class="section-header">📋 Detailed Data Views</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Customer Data", "Transaction Data", "Account Summary"])

with tab1:
    st.subheader("Customer Database")
    
    # Filters for customer data
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_region = st.selectbox("Filter by Region", ['All'] + list(customers_df['region'].unique()))
    with col2:
        selected_type = st.selectbox("Filter by Customer Type", ['All'] + list(customers_df['customer_type'].unique()))
    with col3:
        selected_kyc = st.selectbox("Filter by KYC Status", ['All'] + list(customers_df['kyc_status'].unique()))
    
    filtered_customers = customers_df.copy()
    if selected_region != 'All':
        filtered_customers = filtered_customers[filtered_customers['region'] == selected_region]
    if selected_type != 'All':
        filtered_customers = filtered_customers[filtered_customers['customer_type'] == selected_type]
    if selected_kyc != 'All':
        filtered_customers = filtered_customers[filtered_customers['kyc_status'] == selected_kyc]
    
    st.dataframe(filtered_customers, use_container_width=True)
    st.download_button(
        "Download Customer Data",
        filtered_customers.to_csv(index=False),
        "innbucks_customers.csv",
        "text/csv"
    )

with tab2:
    st.subheader("Recent Transactions")
    
    # Transaction filters
    col1, col2 = st.columns(2)
    with col1:
        selected_txn_type = st.selectbox("Filter by Type", ['All'] + list(transactions_df['transaction_type'].unique()))
    with col2:
        selected_channel = st.selectbox("Filter by Channel", ['All'] + list(transactions_df['channel'].unique()))
    
    filtered_transactions = transactions_df.copy()
    if selected_txn_type != 'All':
        filtered_transactions = filtered_transactions[filtered_transactions['transaction_type'] == selected_txn_type]
    if selected_channel != 'All':
        filtered_transactions = filtered_transactions[filtered_transactions['channel'] == selected_channel]
    
    # Show recent transactions
    recent_txns = filtered_transactions.sort_values('transaction_date', ascending=False).head(100)
    st.dataframe(recent_txns, use_container_width=True)

with tab3:
    st.subheader("Account Summary")
    
    # Merge customer and account data
    account_summary = accounts_df.merge(customers_df, on='customer_id')
    
    st.metric("Total Accounts", len(account_summary))
    st.metric("Average Balance", f"${account_summary['usd_balance'].mean():.2f}")
    st.metric("Total Wallet Size", f"${account_summary['usd_balance'].sum():,.0f}")
    
    st.dataframe(account_summary, use_container_width=True)

# System Alerts
st.markdown('<div class="section-header">🚨 System Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("🟢 System Normal")
with col2:
    st.info("📊 Data Updated")
with col3:
    st.warning("⚠️ 2 Pending KYC")
with col4:
    st.success("✅ All Services Active")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #FF4B4B; font-weight: bold;'>"
    "InnBucks Zimbabwe Digital Banking Dashboard • Proof of Concept by Takundanashe Moyo • "
    "Last Updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") +
    "</div>", 
    unsafe_allow_html=True
)
