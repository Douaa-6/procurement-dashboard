import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="Procurement Intelligence Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #1f77b4;
}
.buy-card { border-left-color: #2ca02c; }
.wait-card { border-left-color: #ff7f0e; }
.avoid-card { border-left-color: #d62728; }
.neutral-card { border-left-color: #7f7f7f; }

.alert-box {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
.alert-critical { background-color: #ffebee; border-left: 5px solid #f44336; }
.alert-warning { background-color: #fff3e0; border-left: 5px solid #ff9800; }
.alert-success { background-color: #e8f5e8; border-left: 5px solid #4caf50; }
</style>
""", unsafe_allow_html=True)

class StreamlitProcurementDashboard:
    def __init__(self):
        # Sample data based on your analysis results
        self.current_recommendations = {
            'Concrete': {'price': 201.86, 'action': 'BUY NOW', 'savings': 3.23, 'month': 'October 2025'},
            'Timber': {'price': 3812.31, 'action': 'BUY NOW', 'savings': 289.74, 'month': 'October 2025'},
            'Cabling': {'price': 47.80, 'action': 'NEUTRAL', 'savings': 0, 'month': 'October 2025'},
            'Cement': {'price': 13.45, 'action': 'BUY NOW', 'savings': 0.16, 'month': 'October 2025'}
        }
        
        self.forecasts = {
            'Timber': [
                {'month': 'Oct 2025', 'price': 3812.31, 'action': 'BUY NOW', 'savings': 289.74},
                {'month': 'Nov 2025', 'price': 3833.51, 'action': 'WAIT', 'savings': 291.35},
                {'month': 'Dec 2025', 'price': 3841.10, 'action': 'WAIT', 'savings': 291.92},
                {'month': 'Jan 2026', 'price': 3844.61, 'action': 'WAIT', 'savings': 292.19},
                {'month': 'Feb 2026', 'price': 3884.60, 'action': 'WAIT', 'savings': 295.23},
                {'month': 'Mar 2026', 'price': 3912.03, 'action': 'WAIT', 'savings': 297.31}
            ],
            'Concrete': [
                {'month': 'Oct 2025', 'price': 201.86, 'action': 'BUY NOW', 'savings': 3.23},
                {'month': 'Nov 2025', 'price': 201.98, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Dec 2025', 'price': 201.76, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Jan 2026', 'price': 203.30, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Feb 2026', 'price': 202.98, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Mar 2026', 'price': 203.00, 'action': 'NEUTRAL', 'savings': 0}
            ],
            'Cabling': [
                {'month': 'Oct 2025', 'price': 47.80, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Nov 2025', 'price': 48.42, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Dec 2025', 'price': 48.62, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Jan 2026', 'price': 47.89, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Feb 2026', 'price': 48.08, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Mar 2026', 'price': 48.36, 'action': 'NEUTRAL', 'savings': 0}
            ],
            'Cement': [
                {'month': 'Oct 2025', 'price': 13.45, 'action': 'BUY NOW', 'savings': 0.16},
                {'month': 'Nov 2025', 'price': 13.51, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Dec 2025', 'price': 13.52, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Jan 2026', 'price': 13.60, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Feb 2026', 'price': 13.59, 'action': 'NEUTRAL', 'savings': 0},
                {'month': 'Mar 2026', 'price': 13.58, 'action': 'NEUTRAL', 'savings': 0}
            ]
        }
        
        self.risk_levels = {
            'Cabling': {'level': 'CRITICAL', 'volatility': 15.5, 'color': '#d62728'},
            'Timber': {'level': 'HIGH', 'volatility': 12.1, 'color': '#ff7f0e'},
            'Concrete': {'level': 'MODERATE', 'volatility': 6.9, 'color': '#2ca02c'},
            'Cement': {'level': 'LOW', 'volatility': 3.8, 'color': '#1f77b4'}
        }

    def display_header(self):
        st.title("🏗️ Procurement Intelligence Dashboard")
        st.markdown("**Strategic Material Procurement Guidance | September 2025**")
        st.markdown("---")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Potential Savings", "4.1%", "Portfolio Optimization")
        with col2:
            st.metric("Highest Savings Material", "Timber", "$289.74 per unit")
        with col3:
            st.metric("Critical Risk Material", "Cabling", "15.5% volatility")
        with col4:
            st.metric("Optimal Window", "October 2025", "75% of materials")

    def display_current_recommendations(self):
        st.header("📋 Current Month Recommendations")
        
        cols = st.columns(4)
        
        for idx, (material, data) in enumerate(self.current_recommendations.items()):
            with cols[idx]:
                action_color = {
                    'BUY NOW': '#2ca02c',
                    'WAIT': '#ff7f0e', 
                    'AVOID': '#d62728',
                    'NEUTRAL': '#7f7f7f'
                }.get(data['action'], '#7f7f7f')
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{material}</h4>
                    <h3>${data['price']:,.2f}</h3>
                    <p style="color: {action_color}; font-weight: bold;">{data['action']}</p>
                    <p>{data['month']}</p>
                    {f"<p style='color: #2ca02c;'>💰 ${data['savings']:.2f} savings</p>" if data['savings'] > 0 else ""}
                </div>
                """, unsafe_allow_html=True)

    def display_risk_alerts(self):
        st.header("⚠️ Risk Alerts & Early Warnings")
        
        # Critical alerts
        st.markdown("""
        <div class="alert-box alert-critical">
            <strong>🚨 CRITICAL: Cabling</strong><br>
            15.5% volatility requires immediate hedging strategies. Consider 6-month forward contracts.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-box alert-warning">
            <strong>⚠️ HIGH RISK: Timber</strong><br>
            12.1% volatility with highest financial impact. Strategic timing essential for October window.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-box alert-success">
            <strong>✅ OPPORTUNITY: October Window</strong><br>
            Optimal buying period opens in 1 month for 75% of materials. Plan bulk purchases now.
        </div>
        """, unsafe_allow_html=True)

    def display_interactive_forecasts(self):
        st.header("📈 Interactive Price Forecasts")
        
        # Material selector
        selected_material = st.selectbox(
            "Select Material for Detailed Forecast:",
            options=list(self.forecasts.keys()),
            index=1  # Default to Timber (highest impact)
        )
        
        # Display forecast table
        forecast_data = self.forecasts[selected_material]
        df = pd.DataFrame(forecast_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"{selected_material} 6-Month Forecast")
            
            # Style the dataframe
            def style_action(val):
                color_map = {
                    'BUY NOW': 'background-color: #d4edda; color: #155724;',
                    'WAIT': 'background-color: #fff3cd; color: #856404;',
                    'AVOID': 'background-color: #f8d7da; color: #721c24;',
                    'NEUTRAL': 'background-color: #e2e3e5; color: #383d41;'
                }
                return color_map.get(val, '')
            
            styled_df = df.style.applymap(style_action, subset=['action'])
            st.dataframe(styled_df, use_container_width=True)
        
        with col2:
            st.subheader("Key Insights")
            risk_info = self.risk_levels[selected_material]
            
            st.markdown(f"""
            **Risk Level:** {risk_info['level']}  
            **Volatility:** {risk_info['volatility']}%  
            **Best Action:** {forecast_data[0]['action']}  
            **Next Month Price:** ${forecast_data[0]['price']:,.2f}
            """)
            
            if forecast_data[0]['savings'] > 0:
                st.success(f"💰 Potential savings: ${forecast_data[0]['savings']:.2f} per unit")

    def display_savings_calculator(self):
        st.header("💰 Savings Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calc_material = st.selectbox(
                "Material:",
                options=list(self.current_recommendations.keys()),
                key="calc_material"
            )
            
            purchase_quantity = st.number_input(
                "Purchase Quantity:",
                min_value=1,
                value=100,
                step=1
            )
            
            purchase_month = st.selectbox(
                "Purchase Month:",
                options=["October 2025 (Optimal)", "November 2025", "December 2025", "January 2026"],
                key="calc_month"
            )
        
        with col2:
            material_data = self.current_recommendations[calc_material]
            
            if "Optimal" in purchase_month:
                unit_price = material_data['price']
                savings_per_unit = material_data['savings']
            else:
                # Simulate non-optimal pricing
                unit_price = material_data['price'] * 1.02  # 2% higher
                savings_per_unit = 0
            
            total_cost = unit_price * purchase_quantity
            total_savings = savings_per_unit * purchase_quantity
            
            st.metric("Unit Price", f"${unit_price:.2f}")
            st.metric("Total Cost", f"${total_cost:,.2f}")
            
            if total_savings > 0:
                st.metric("Total Savings", f"${total_savings:,.2f}", f"vs non-optimal timing")
                st.success(f"Save ${total_savings:,.2f} by purchasing in optimal window!")
            else:
                st.warning("Consider waiting for optimal purchase window")

    def display_price_trends_chart(self):
        st.header("📊 Price Trends Visualization")
        
        # Create interactive chart
        fig = go.Figure()
        
        # Add lines for each material
        materials = ['Timber', 'Concrete', 'Cabling', 'Cement']
        colors = ['#d62728', '#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, material in enumerate(materials):
            forecast = self.forecasts[material]
            months = [item['month'] for item in forecast]
            prices = [item['price'] for item in forecast]
            
            fig.add_trace(go.Scatter(
                x=months,
                y=prices,
                mode='lines+markers',
                name=material,
                line=dict(color=colors[i], width=3),
                marker=dict(size=8),
                hovertemplate=f"<b>{material}</b><br>Month: %{{x}}<br>Price: $%{{y:,.2f}}<extra></extra>"
            ))
        
        fig.update_layout(
            title="6-Month Price Forecast Comparison",
            xaxis_title="Month",
            yaxis_title="Price ($)",
            hovermode='x unified',
            template="plotly_white",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def display_sidebar_controls(self):
        st.sidebar.header("Dashboard Controls")
        
        # Update data button
        if st.sidebar.button("🔄 Refresh Data", help="Update with latest price data"):
            st.sidebar.success("Data refreshed!")
            st.experimental_rerun()
        
        # Download options
        st.sidebar.header("Export Options")
        
        if st.sidebar.button("📊 Export to Excel"):
            # Create sample Excel data
            excel_data = pd.DataFrame(self.current_recommendations).T
            st.sidebar.download_button(
                label="📥 Download Excel Report",
                data=excel_data.to_csv(),
                file_name="procurement_recommendations.csv",
                mime="text/csv"
            )
        
        # Settings
        st.sidebar.header("Settings")
        
        show_advanced = st.sidebar.checkbox("Show Advanced Analytics", value=False)
        auto_refresh = st.sidebar.checkbox("Auto Refresh (5 min)", value=False)
        
        if auto_refresh:
            st.sidebar.info("Auto-refresh enabled")
            # In real implementation, you'd set up periodic refresh
        
        # Help section
        st.sidebar.header("Help & Info")
        
        with st.sidebar.expander("How to Use"):
            st.write("""
            1. **Current Recommendations**: View immediate buy/wait/avoid guidance
            2. **Interactive Forecasts**: Select materials for detailed analysis
            3. **Savings Calculator**: Calculate ROI for different purchase scenarios
            4. **Price Trends**: Visualize 6-month forecasts
            """)
        
        with st.sidebar.expander("Data Sources"):
            st.write("""
            - Historical price data: 2013-2022 (472 records)
            - Statistical modeling: Trend + seasonal analysis
            - Risk assessment: Volatility-based classification
            - Correlation analysis: 72% accuracy early warning system
            """)
        
        return show_advanced

def main():
    dashboard = StreamlitProcurementDashboard()
    
    # Display sidebar
    show_advanced = dashboard.display_sidebar_controls()
    
    # Main dashboard content
    dashboard.display_header()
    
    # Current recommendations
    dashboard.display_current_recommendations()
    
    st.markdown("---")
    
    # Risk alerts
    dashboard.display_risk_alerts()
    
    st.markdown("---")
    
    # Interactive forecasts
    dashboard.display_interactive_forecasts()
    
    st.markdown("---")
    
    # Savings calculator
    dashboard.display_savings_calculator()
    
    st.markdown("---")
    
    # Price trends chart
    dashboard.display_price_trends_chart()
    
    # Advanced analytics (if enabled)
    if show_advanced:
        st.markdown("---")
        st.header("🔬 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Correlation Matrix")
            # Sample correlation data
            corr_data = {
                'Material': ['Concrete', 'Timber', 'Cabling', 'Cement'],
                'Concrete': [1.000, 0.404, 0.560, 0.893],
                'Timber': [0.404, 1.000, 0.823, 0.331],
                'Cabling': [0.560, 0.823, 1.000, 0.543],
                'Cement': [0.893, 0.331, 0.543, 1.000]
            }
            corr_df = pd.DataFrame(corr_data)
            st.dataframe(corr_df, use_container_width=True)
        
        with col2:
            st.subheader("Risk Metrics")
            risk_data = []
            for material, risk_info in dashboard.risk_levels.items():
                risk_data.append({
                    'Material': material,
                    'Risk Level': risk_info['level'],
                    'Volatility (%)': risk_info['volatility']
                })
            risk_df = pd.DataFrame(risk_data)
            st.dataframe(risk_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>Last Updated:</strong> September 2025 | <strong>Next Update:</strong> October 2025</p>
        <p>Based on 9+ years of historical price analysis and statistical modeling</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()