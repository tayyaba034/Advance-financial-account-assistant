"""
Demo mode for Advanced Accounts Agent.
This allows you to test the application without setting up API keys.
"""

import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoMode:
    """Demo mode that simulates agent responses without API calls."""
    
    def __init__(self):
        self.logger = logger
    
    async def run_demo(self):
        """Run a demonstration of all agents in demo mode."""
        self.logger.info("🚀 Advanced Accounts Agent - Demo Mode")
        self.logger.info("=" * 60)
        self.logger.info("This demo shows what the agents can do without API calls.")
        self.logger.info("=" * 60)
        
        demo_queries = [
            {
                "query": "Generate a financial summary for this month",
                "agent": "FinancialSummaryAgent",
                "response": "Based on your financial data, here's your monthly summary:\n\n📊 **Executive Summary**\nYour business shows strong performance with a 15% increase in revenue compared to last month.\n\n💰 **Key Metrics**\n- Total Revenue: $125,000\n- Total Expenses: $95,000\n- Net Profit: $30,000\n- Profit Margin: 24%\n\n📈 **Performance Analysis**\n- Revenue growth is driven by increased customer acquisition\n- Operating expenses are well controlled\n- Cash flow is positive and improving\n\n🎯 **Recommendations**\n- Continue current growth strategies\n- Monitor expense ratios closely\n- Consider investing in marketing for further growth"
            },
            {
                "query": "Categorize my recent transactions",
                "agent": "TransactionCategorizerAgent", 
                "response": "I've successfully categorized your transactions:\n\n🏷️ **Categorization Results**\n- Office Supplies: $1,500 (15 transactions)\n- Marketing: $3,200 (8 transactions)\n- Travel: $2,100 (12 transactions)\n- Meals: $800 (20 transactions)\n- Software: $450 (5 transactions)\n\n📊 **Spending Analysis**\n- Total categorized: $8,050\n- Most active category: Meals (20 transactions)\n- Highest spending: Marketing ($3,200)\n\n💡 **Insights**\n- Marketing spend is 40% of total expenses\n- Consider bulk purchasing for office supplies\n- Travel expenses are within budget"
            },
            {
                "query": "Analyze our cash flow trends",
                "agent": "CashFlowAnalyzerAgent",
                "response": "Here's your cash flow analysis:\n\n💰 **Cash Flow Summary**\n- Current Balance: $45,000\n- Monthly Inflows: $125,000\n- Monthly Outflows: $95,000\n- Net Cash Flow: $30,000\n\n📈 **Trend Analysis**\n- 6-month average net flow: $28,500\n- Cash flow volatility: Low (12%)\n- Trend direction: Improving\n- Positive months: 5/6\n\n🔮 **6-Month Forecast**\n- Projected monthly growth: 5%\n- Expected balance in 6 months: $180,000\n- Confidence level: 85%\n\n⚠️ **Risk Assessment**\n- Risk level: Low\n- Months of cash: 4.5\n- Liquidity ratio: 1.3\n- Recommendation: Maintain current cash management strategy"
            },
            {
                "query": "Reconcile my bank account",
                "agent": "AccountReconcilerAgent",
                "response": "Bank reconciliation completed successfully!\n\n🔍 **Reconciliation Results**\n- Total bank transactions: 150\n- Total accounting transactions: 148\n- Matched transactions: 145\n- Match rate: 96.7%\n\n⚠️ **Discrepancies Found**\n- 3 unmatched bank transactions\n- 2 unmatched accounting transactions\n- 1 low confidence match\n\n📋 **Discrepancy Details**\n1. Bank fee ($15) - Missing in accounting\n2. Interest earned ($25) - Missing in accounting\n3. Check #1234 ($500) - Not yet cleared\n\n✅ **Recommendations**\n- Add missing bank fee and interest to accounting\n- Verify check #1234 status\n- Review low confidence match manually"
            }
        ]
        
        for i, demo in enumerate(demo_queries, 1):
            self.logger.info(f"\n📝 Demo Query {i}: {demo['query']}")
            self.logger.info(f"🤖 Agent: {demo['agent']}")
            self.logger.info(f"⏱️  Processing time: 0.5s")
            self.logger.info(f"✅ Response:")
            
            # Print response with proper formatting
            for line in demo['response'].split('\n'):
                if line.strip():
                    self.logger.info(f"   {line}")
            
            # Add delay between demos
            await asyncio.sleep(1)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("🎉 Demo completed successfully!")
        self.logger.info("=" * 60)
        self.logger.info("To use the full application with real AI capabilities:")
        self.logger.info("1. Run: python setup_env.py")
        self.logger.info("2. Enter your API keys")
        self.logger.info("3. Run: python main.py")
        self.logger.info("=" * 60)

async def main():
    """Run the demo."""
    demo = DemoMode()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
