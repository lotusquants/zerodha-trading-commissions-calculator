import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Zerodha Trading Commissions Calculator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .highlight {
        background-color: #ffd700;
        padding: 5px;
        border-radius: 5px;
        font-weight: bold;
    }
    .profit-positive {
        color: green;
        font-weight: bold;
    }
    .profit-negative {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">📊 Zerodha Trading Commissions Calculator</h1>', unsafe_allow_html=True)

# Sidebar for file upload and instructions
with st.sidebar:
    st.header("Instructions")
    st.info("""
    1. Upload your trades CSV file
    2. The app will automatically process your trades
    3. View commissions, P&L, and breakdown
    """)
    
    uploaded_file = st.file_uploader("Upload orders.csv", type="csv")
    
    st.header("Commission Rates")
    st.write("Brokerage: 0.03% (Max ₹20 per order)")
    st.write("Transaction Charges: 0.00297%")
    st.write("GST: 18% on (Brokerage + Transaction Charges)")
    st.write("SEBI Charges: 0.0001%")
    st.write("STT: 0.025% on sell value")
    st.write("Stamp Duty: 0.003% on buy value")

# Commissions class
class Commissions:
    def __init__(self):
        self.Total_value = 0
        self.commission_breakdown = {}

    def calculate_commissions(self, buy_value, sell_value):
        self.brokerage = min(((0.03 / 100) * (buy_value + sell_value)), 20)
        self.TrnChg = (0.00297 / 100) * (buy_value + sell_value)
        self.GST = (18 / 100) * (self.brokerage + self.TrnChg)
        self.sebi = (10 / 10000000) * (buy_value + sell_value)
        self.STT = (0.025 / 100) * sell_value
        self.stampduty = (0.002 / 100) * buy_value  # Only on buy value
        
        # Store breakdown
        self.commission_breakdown = {
            "Brokerage": self.brokerage,
            "Transaction Charges": self.TrnChg,
            "GST": self.GST,
            "SEBI Charges": self.sebi,
            "STT": self.STT,
            "Stamp Duty": self.stampduty
        }
        
        self.calculate_total()

    def calculate_total(self):
        self.Total_value = sum(self.commission_breakdown.values())

# Function to process the data
def process_trades_data(orders):
    # Initialize variables for calculations
    Total_commissions = 0
    total_buy_value = 0
    total_sell_value = 0
    total_buy_quantity = 0
    total_sell_quantity = 0
    commission_breakdown = {
        "Brokerage": 0,
        "Transaction Charges": 0,
        "GST": 0,
        "SEBI Charges": 0,
        "STT": 0,
        "Stamp Duty": 0
    }
    
    # Create a list to store processed trades
    processed_trades = []
    
    # Process each order
    for index, order in orders.iterrows():
        # Skip cancelled orders
        if order['Status'] == 'CANCELLED':
            continue
            
        # Extract quantity (handle the "X/X" format)
        try:
            qty_str = str(order['Qty.'])
            if '/' in qty_str:
                qty = int(qty_str.split('/')[0])
            else:
                qty = int(qty_str)
        except:
            qty = 0
            
        # Skip if quantity is zero
        if qty == 0:
            continue
            
        # Get price and calculate trade value
        price_str = str(order['Avg. price'])
        try:
            # Extract first numeric value before '/' or any non-numeric
            price = float(price_str.split('/')[0].replace(',', '').strip())
        except:
            price = 0.0
            
        trade_value = qty * price
        
        # Initialize commission calculator
        C = Commissions()
        
        # Calculate based on trade type
        if order['Type'] == 'BUY':
            C.calculate_commissions(trade_value, 0)
            total_buy_value += trade_value
            total_buy_quantity += qty
            pnl = 0  # P&L will be calculated when we match with sells
        elif order['Type'] == 'SELL':
            C.calculate_commissions(0, trade_value)
            total_sell_value += trade_value
            total_sell_quantity += qty
            pnl = 0  # P&L will be calculated when we match with buys
        
        Total_commissions += C.Total_value
        
        # Add to commission breakdown
        for key in commission_breakdown:
            commission_breakdown[key] += C.commission_breakdown[key]
        
        # Store processed trade
        processed_trades.append({
            'Time': order['Time'],
            'Type': order['Type'],
            'Instrument': order['Instrument'],
            'Qty': qty,
            'Price': price,
            'Value': trade_value,
            'Commission': C.Total_value,
            'P&L': pnl
        })
    
    # Calculate net profit/loss
    net_profit_before_commissions = total_sell_value - total_buy_value
    net_profit_after_commissions = net_profit_before_commissions - Total_commissions
    
    # Create DataFrame from processed trades
    processed_df = pd.DataFrame(processed_trades)
    
    return {
        'total_buy_value': total_buy_value,
        'total_sell_value': total_sell_value,
        'total_buy_quantity': total_buy_quantity,
        'total_sell_quantity': total_sell_quantity,
        'total_commissions': Total_commissions,
        'commission_breakdown': commission_breakdown,
        'net_profit_before_commissions': net_profit_before_commissions,
        'net_profit_after_commissions': net_profit_after_commissions,
        'processed_trades': processed_df
    }

# Main app logic
if uploaded_file is not None:
    try:
        # Read the CSV file
        orders = pd.read_csv(uploaded_file)
        
        # Clean up column names
        orders.columns = orders.columns.str.strip()
        
        # Display the raw data
        st.subheader("Uploaded Trades Data")
        st.dataframe(orders, use_container_width=True)
        
        # Process the data
        results = process_trades_data(orders)
        
        # Display results in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Buy Value", f"₹{results['total_buy_value']:,.2f}")
            st.metric("Total Buy Quantity", f"{results['total_buy_quantity']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Sell Value", f"₹{results['total_sell_value']:,.2f}")
            st.metric("Total Sell Quantity", f"{results['total_sell_quantity']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Gross P&L", f"₹{results['net_profit_before_commissions']:,.2f}", 
                     delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Commissions", f"₹{results['total_commissions']:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col5:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            # Determine the class for coloring
            net_pnl_value = results['net_profit_after_commissions']
            delta_color = "normal"
            if net_pnl_value >= 0:
                delta_color = "off"  # disables delta color change
                net_pnl_display = f"🟢 ₹{net_pnl_value:,.2f}"
            else:
                delta_color = "off"
                net_pnl_display = f"🔴 ₹{net_pnl_value:,.2f}"

            st.metric("Net P&L", net_pnl_display, delta=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col6:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            turnover = results['total_buy_value'] + results['total_sell_value']
            if turnover > 0:
                commission_percentage = (results['total_commissions'] / turnover) * 100
                st.metric("Commission % of Turnover", f"{commission_percentage:.4f}%")
            else:
                st.metric("Commission % of Turnover", "0%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display commission breakdown
        st.subheader("Commission Breakdown")
        breakdown_df = pd.DataFrame.from_dict(results['commission_breakdown'], orient='index', columns=['Amount (₹)'])
        breakdown_df['Percentage'] = (breakdown_df['Amount (₹)'] / results['total_commissions']) * 100
        st.dataframe(breakdown_df.style.format({
            'Amount (₹)': '₹{:,.2f}',
            'Percentage': '{:.2f}%'
        }), use_container_width=True)
        
        # Display processed trades
        st.subheader("Processed Trades")
        st.dataframe(results['processed_trades'], use_container_width=True)
        
        # Display summary
        st.subheader("Summary")
        if results['net_profit_after_commissions'] >= 0:
            st.success(f"🎉 Your net profit after commissions is ₹{results['net_profit_after_commissions']:,.2f}")
        else:
            st.error(f"📉 Your net loss after commissions is ₹{abs(results['net_profit_after_commissions']):,.2f}")
            
        if results['net_profit_before_commissions'] != 0:
            commission_impact = (abs(results['total_commissions'] / results['net_profit_before_commissions']) * 100)
            st.info(f"💡 Commissions reduced your P&L by {commission_impact:.2f}%")
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please check that your CSV file has the correct format and try again.")
else:
    # Show instructions before file upload
    st.info("👈 Please upload your trades CSV file using the sidebar to get started.")
    
    # Sample data format based on your file
    st.subheader("Expected CSV Format")
    sample_data = pd.DataFrame({
        "Time": ["2025-09-10 14:08:24", "2025-09-10 14:00:58"],
        "Type": ["BUY", "SELL"],
        "Instrument": ["AVANTIFEED", "AVANTIFEED"],
        "Product": ["MIS", "MIS"],
        "Qty.": ["10/10", "10/10"],
        "Avg. price": [745.55, 753.7],
        "Status": ["COMPLETE", "COMPLETE"],
        "Unnamed: 7": ["", ""]
    })
    st.dataframe(sample_data, use_container_width=True)