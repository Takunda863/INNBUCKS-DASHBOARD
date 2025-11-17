import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="InnBucks Zimbabwe Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E3A8A;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Generate synthetic data for InnBucks Zimbabwe
def generate_innbucks_data():
    np.random.seed(42)
    
    # Zimbabwe-specific data
    branches = ['Harare CBD', 'Bulawayo Central', 'Mutare', 'Gweru', 'Masvingo', 'Chinhoyi', 'Kadoma']
    currencies = ['USD', 'ZWL']
    mobile_networks = ['Econet', 'NetOne', 'Telecel']
    
    # Customer data
    n_customers = 5000
    customer_ids = [f'INN{i:05d}' for i in range(1, n_customers+1)]
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'customer_type': np.random.choice(['Individual', 'Agent', 'Merchant'], n_customers, p=[0.85, 0.1, 0.05]),
        'region': np.random.choice(['Harare', 'Bulawayo', 'Midlands', 'Masvingo', 'Manicaland', 'Mashonaland'], n_customers),
        'branch': np.random.choice(branches, n_customers),
        'age': np.random.randint(18, 70, n_customers),
        'registration_date': pd.date_range('2020-01-01', periods=n_customers, freq='D'),
        'mobile_network': np.random.choice(mobile_networks, n_customers, p=[0.7, 0.2, 0.1]),
        'kyc_status': np.random.choice(['Verified', 'Pending', 'Expired'], n_customers, p=[0.8, 0.15, 0.05])
    })
    
    # Account data
    accounts_data = []
    for cust_id in customer_ids:
        n_accounts = 1  # Most customers have one account
        for i in range(n_accounts):
            primary_currency = np.random.choice(currencies, p=[0.7, 0.3])
            usd_balance = max(10, np.random.lognormal(5, 1.2))
            zwl_balance = usd_balance * np.random.uniform(800, 1200) if primary_currency == 'ZWL' else 0
            
            accounts_data.append({
                'customer_id': cust_id,
                'account_id': f'ACC{cust_id}',
                'primary_currency': primary_currency,
                'usd_balance': usd_balance if primary_currency == 'USD' else usd_balance,
                'zwl_balance': zwl_balance,
                'total_balance_usd': usd_balance if primary_currency == 'USD' else usd_balance,
                'account_status': 'Active'
            })
    
    accounts_df = pd.DataFrame(accounts_data)
    
    # Transaction data (last 90 days)
    transactions_data = []
    start_date = datetime.datetime.now() - timedelta(days=90)
    
    for account in accounts_data:
        account_id = account['account_id']
        n_transactions = np.random.poisson(25)  # Average transactions per account
        
        for i in range(n_transactions):
            transaction_date = start_date + timedelta(days=np.random.randint(0, 90), 
                                                    hours=np.random.randint(0, 24))
            transaction_type = np.random.choice(['Send Money', 'Cash In', 'Cash Out', 'Bill Payment', 'Airtime'], 
                                              p=[0.4, 0.2, 0.15, 0.15, 0.1])
            
            # Transaction amounts based on type
            if transaction_type == 'Send Money':
                amount = abs(np.random.lognormal(3.5, 1.0))
            elif transaction_type == 'Cash In':
                amount = abs(np.random.lognormal(4.0, 1.2))
            else:
                amount = abs(np.random.lognormal(3.0, 0.8))
            
            channel = np.random.choice(['Mobile App', 'USSD', 'Agent', 'Branch'], p=[0.6, 0.3, 0.08, 0.02])
            status = 'Completed' if np.random.random() > 0.02 else 'Failed'
            
            transactions_data.append({
                'transaction_id': f'TXN{account_id}{i}',
                'account_id': account_id,
                'transaction_date': transaction_date,
                'amount_usd': amount,
                'transaction_type': transaction_type,
                'channel': channel,
                'status': status,
                'fee_usd': amount * 0.02 if transaction_type in ['Send Money', 'Bill Payment'] else amount * 0.01
            })
    
    transactions_df = pd.DataFrame(transactions_data)
    
    # Agent network data
    agents_data = []
    n_agents = 200
    
    for i in range(n_agents):
        agent_id = f'AGT{i:04d}'
        location = np.random.choice(branches)
        status = np.random.choice(['Active', 'Inactive'], p=[0.9, 0.1])
        monthly_volume = np.random.lognormal(8, 1.0)
        
        agents_data.append({
            'agent_id': agent_id,
            'location': location,
            'status': status,
            'monthly_volume_usd': monthly_volume,
            'registration_date': pd.Timestamp('2023-01-01') + timedelta(days=np.random.randint(0, 365))
        })
    
    agents_df = pd.DataFrame(agents_data)
    
    return customers_df, accounts_df, transactions_df, agents_df

# Calculate KPIs
def calculate_innbucks_kpis(customers_df, accounts_df, transactions_df, agents_df):
    """Calculate InnBucks specific KPIs"""
    
    # Customer Metrics
    total_customers = customers_df['customer_id'].nunique()
    active_agents = agents_df[agents_df['status'] == 'Active'].shape[0]
    kyc_completion_rate = (customers_df['kyc_status'] == 'Verified').mean()
    
    # Transaction Metrics
    total_transactions = len(transactions_df)
    successful_transactions = transactions_df[transactions_df['status'] == 'Completed'].shape[0]
    success_rate = successful_transactions / total_transactions
    total_volume = transactions_df['amount_usd'].sum()
    total_fees = transactions_df['fee_usd'].sum()
    
    # Account Metrics
    total_deposits = accounts_df['total_balance_usd'].sum()
    avg_balance = accounts_df['total_balance_usd'].mean()
    
    # Recent activity (last 7 days)
    last_7_days = datetime.datetime.now() - timedelta(days=7)
    recent_txns = transactions_df[transactions_df['transaction_date'] >= last_7_days]
    weekly_volume = recent_txns['amount_usd'].sum()
    weekly_transactions = len(recent_txns)
    
    # Customer growth
    current_month = datetime.datetime.now().replace(day=1)
    new_customers_this_month = customers_df[customers_df['registration_date'] >= current_month].shape[0]
    
    return {
        'total_customers': total_customers,
        'active_agents': active_agents,
        'kyc_completion_rate': kyc_completion_rate,
        'total_transactions': total_transactions,
        'success_rate': success_rate,
        'total_volume': total_volume,
        'total_fees': total_fees,
        'total_deposits': total_deposits,
        'avg_balance': avg_balance,
        'weekly_volume': weekly_volume,
        'weekly_transactions': weekly_transactions,
        'new_customers_this_month': new_customers_this_month
    }

# Generate data
customers_df, accounts_df, transactions_df, agents_df = generate_innbucks_data()
kpis = calculate_innbucks_kpis(customers_df, accounts_df, transactions_df, agents_df)

# Main dashboard
st.markdown('<h1 class="main-header">🏦 InnBucks Zimbabwe Performance Dashboard</h1>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")
selected_region = st.sidebar.selectbox("Select Region", ['All'] + list(customers_df['region'].unique()))
selected_branch = st.sidebar.selectbox("Select Branch", ['All'] + list(customers_df['branch'].unique()))
date_range = st.sidebar.date_input("Date Range", [
    datetime.datetime.now() - timedelta(days=30),
    datetime.datetime.now()
])

# Apply filters
filtered_customers = customers_df.copy()
filtered_transactions = transactions_df.copy()

if selected_region != 'All':
    filtered_customers = filtered_customers[filtered_customers['region'] == selected_region]
    customer_ids = filtered_customers['customer_id'].tolist()
    filtered_transactions = filtered_transactions[filtered_transactions['account_id'].str[3:].isin(customer_ids)]

if selected_branch != 'All':
    filtered_customers = filtered_customers[filtered_customers['branch'] == selected_branch]
    customer_ids = filtered_customers['customer_id'].tolist()
    filtered_transactions = filtered_transactions[filtered_transactions['account_id'].str[3:].isin(customer_ids)]

# KPI Metrics Row
st.markdown('<h2 class="section-header">📈 Key Performance Indicators</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Customers",
        value=f"{kpis['total_customers']:,}",
        delta=f"+{kpis['new_customers_this_month']} this month"
    )

with col2:
    st.metric(
        label="Active Agents",
        value=kpis['active_agents'],
        delta="Network"
    )

with col3:
    st.metric(
        label="Transaction Success Rate",
        value=f"{kpis['success_rate']:.1%}",
        delta="2.1%"
    )

with col4:
    st.metric(
        label="KYC Completion",
        value=f"{kpis['kyc_completion_rate']:.1%}",
        delta="5.2%"
    )

# Second row of KPIs
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        label="Total Volume (USD)",
        value=f"${kpis['total_volume']:,.0f}",
        delta=f"${kpis['weekly_volume']:,.0f} weekly"
    )

with col6:
    st.metric(
        label="Fee Income (USD)",
        value=f"${kpis['total_fees']:,.0f}",
        delta="Revenue"
    )

with col7:
    st.metric(
        label="Customer Deposits (USD)",
        value=f"${kpis['total_deposits']:,.0f}",
        delta="Liquidity"
    )

with col8:
    st.metric(
        label="Avg Balance (USD)",
        value=f"${kpis['avg_balance']:.0f}",
        delta="Wallet size"
    )

# Charts Section
st.markdown('<h2 class="section-header">📊 Transaction Analytics</h2>', unsafe_allow_html=True)

# First row of charts
col1, col2 = st.columns(2)

with col1:
    # Transaction types distribution
    txn_types = filtered_transactions['transaction_type'].value_counts()
    fig1 = px.pie(
        values=txn_types.values,
        names=txn_types.index,
        title="Transaction Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Channel usage
    channel_usage = filtered_transactions['channel'].value_counts()
    fig2 = px.bar(
        x=channel_usage.index,
        y=channel_usage.values,
        title="Transaction Channels",
        color=channel_usage.index,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(xaxis_title="Channel", yaxis_title="Number of Transactions", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Second row of charts
col3, col4 = st.columns(2)

with col3:
    # Daily transaction volume
    daily_volume = filtered_transactions.groupby(
        filtered_transactions['transaction_date'].dt.date
    )['amount_usd'].sum().reset_index()
    
    fig3 = px.line(
        daily_volume,
        x='transaction_date',
        y='amount_usd',
        title="Daily Transaction Volume (USD)",
        markers=True
    )
    fig3.update_layout(xaxis_title="Date", yaxis_title="Volume (USD)")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Customer segmentation
    customer_segments = filtered_customers['customer_type'].value_counts()
    fig4 = px.pie(
        values=customer_segments.values,
        names=customer_segments.index,
        title="Customer Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig4, use_container_width=True)

# Third row of charts
st.markdown('<h2 class="section-header">👥 Customer & Agent Analytics</h2>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    # Regional distribution
    regional_dist = filtered_customers['region'].value_counts()
    fig5 = px.bar(
        x=regional_dist.index,
        y=regional_dist.values,
        title="Customer Distribution by Region",
        color=regional_dist.index,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig5.update_layout(xaxis_title="Region", yaxis_title="Number of Customers", showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # Mobile network distribution
    network_dist = filtered_customers['mobile_network'].value_counts()
    fig6 = px.bar(
        x=network_dist.index,
        y=network_dist.values,
        title="Mobile Network Distribution",
        color=network_dist.index,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig6.update_layout(xaxis_title="Mobile Network", yaxis_title="Number of Customers", showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

# Agent Performance
st.markdown('<h2 class="section-header">🏪 Agent Network Performance</h2>', unsafe_allow_html=True)

# Agent metrics
col7, col8, col9 = st.columns(3)

active_agents = agents_df[agents_df['status'] == 'Active']
avg_agent_volume = active_agents['monthly_volume_usd'].mean()
top_agent_volume = active_agents['monthly_volume_usd'].max()

with col7:
    st.metric("Active Agents", len(active_agents))

with col8:
    st.metric("Avg Agent Volume (USD)", f"${avg_agent_volume:,.0f}")

with col9:
    st.metric("Top Agent Volume (USD)", f"${top_agent_volume:,.0f}")

# Agent location distribution
agent_locations = agents_df['location'].value_counts()
fig7 = px.bar(
    x=agent_locations.index,
    y=agent_locations.values,
    title="Agent Distribution by Location",
    color=agent_locations.index,
    color_discrete_sequence=px.colors.qualitative.Dark2
)
fig7.update_layout(xaxis_title="Location", yaxis_title="Number of Agents", showlegend=False)
st.plotly_chart(fig7, use_container_width=True)

# Risk and Compliance Section
st.markdown('<h2 class="section-header">🛡️ Risk & Compliance</h2>', unsafe_allow_html=True)

col10, col11, col12 = st.columns(3)

# KYC status
kyc_status = filtered_customers['kyc_status'].value_counts()
failed_transactions = len(filtered_transactions[filtered_transactions['status'] == 'Failed'])

with col10:
    st.metric("Verified KYC", f"{kyc_status.get('Verified', 0):,}")

with col11:
    st.metric("Pending KYC", f"{kyc_status.get('Pending', 0):,}")

with col12:
    st.metric("Failed Transactions", f"{failed_transactions:,}")

# Data Export and Detailed Views
st.markdown('<h2 class="section-header">📋 Detailed Data Views</h2>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Customer Data", "Transaction Logs", "Agent Performance"])

with tab1:
    st.subheader("Customer Database")
    st.dataframe(filtered_customers.head(100), use_container_width=True)
    
    # Export option
    csv = filtered_customers.to_csv(index=False)
    st.download_button(
        label="Download Customer Data as CSV",
        data=csv,
        file_name="innbucks_customers.csv",
        mime="text/csv"
    )

with tab2:
    st.subheader("Recent Transactions")
    recent_txns = filtered_transactions.sort_values('transaction_date', ascending=False).head(100)
    st.dataframe(recent_txns, use_container_width=True)

with tab3:
    st.subheader("Agent Performance")
    st.dataframe(agents_df, use_container_width=True)

# Real-time alerts section
st.markdown('<h2 class="section-header">🚨 System Alerts</h2>', unsafe_allow_html=True)

# Simulate alerts
alerts = [
    {"type": "⚠️", "message": "High transaction failure rate in Bulawayo region", "time": "2 hours ago"},
    {"type": "🔔", "message": "System maintenance scheduled for tonight 10 PM", "time": "5 hours ago"},
    {"type": "✅", "message": "KYC verification backlog cleared", "time": "1 day ago"},
    {"type": "📈", "message": "Record transaction volume yesterday", "time": "1 day ago"}
]

for alert in alerts:
    with st.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            st.write(alert["type"])
        with col2:
            st.write(f"{alert['message']} - *{alert['time']}*")
        st.divider()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "InnBucks Zimbabwe Digital Banking Dashboard • Last Updated: " + 
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M") +
    "</div>", 
    unsafe_allow_html=True
)
