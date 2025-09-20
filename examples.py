"""
Example usage and demonstrations for the Advanced Accounts Agent.
Shows how to use each agent and the orchestrator.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta

from orchestrator import MoEOrchestrator
from agents import (
    FinancialSummaryAgent,
    TransactionCategorizerAgent,
    CashFlowAnalyzerAgent,
    AccountReconcilerAgent,
    AgentRequest
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedAccountsAgentExamples:
    """
    Examples demonstrating the capabilities of the Advanced Accounts Agent.
    """
    
    def __init__(self):
        """Initialize the examples."""
        self.orchestrator = MoEOrchestrator()
        self.logger = logger
    
    async def run_all_examples(self):
        """Run all example demonstrations."""
        self.logger.info("🚀 Starting Advanced Accounts Agent Examples...")
        
        examples = [
            ("Financial Summary Agent", self.example_financial_summary),
            ("Transaction Categorizer Agent", self.example_transaction_categorizer),
            ("Cash Flow Analyzer Agent", self.example_cash_flow_analyzer),
            ("Account Reconciler Agent", self.example_account_reconciler),
            ("MoE Orchestrator", self.example_orchestrator),
            ("Multi-Agent Query", self.example_multi_agent_query)
        ]
        
        for name, example_func in examples:
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"📋 {name} Example")
            self.logger.info(f"{'='*60}")
            
            try:
                await example_func()
                self.logger.info(f"✅ {name} example completed successfully!")
            except Exception as e:
                self.logger.error(f"❌ {name} example failed: {str(e)}")
            
            await asyncio.sleep(1)  # Brief pause between examples
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("🎉 All examples completed!")
        self.logger.info(f"{'='*60}")
    
    async def example_financial_summary(self):
        """Example: Financial Summary Agent."""
        agent = FinancialSummaryAgent()
        
        # Example 1: Basic financial summary
        self.logger.info("📊 Example 1: Basic Financial Summary")
        request = AgentRequest(
            query="Generate a comprehensive financial summary for this month",
            context={"period": "monthly"}
        )
        
        response = await agent.process_request(request)
        self.logger.info(f"Response: {response.message}")
        if response.data:
            self.logger.info(f"Summary generated for: {response.data.get('period', 'N/A')}")
        
        # Example 2: P&L Summary
        self.logger.info("\n📈 Example 2: Profit & Loss Summary")
        pnl_response = await agent.generate_profit_loss_summary("monthly")
        self.logger.info(f"P&L Response: {pnl_response.message}")
        
        # Example 3: Executive Summary
        self.logger.info("\n👔 Example 3: Executive Summary")
        exec_response = await agent.generate_executive_summary()
        self.logger.info(f"Executive Summary: {exec_response.message}")
    
    async def example_transaction_categorizer(self):
        """Example: Transaction Categorizer Agent."""
        agent = TransactionCategorizerAgent()
        
        # Example 1: Categorize sample transactions
        self.logger.info("🏷️ Example 1: Transaction Categorization")
        
        sample_transactions = [
            {"id": "T001", "description": "Office supplies from Staples", "amount": 150.00, "date": "2024-01-15"},
            {"id": "T002", "description": "Electricity bill payment", "amount": 250.00, "date": "2024-01-14"},
            {"id": "T003", "description": "Google Ads marketing campaign", "amount": 500.00, "date": "2024-01-13"},
            {"id": "T004", "description": "Business lunch with client", "amount": 85.00, "date": "2024-01-12"},
            {"id": "T005", "description": "Adobe Creative Suite subscription", "amount": 29.99, "date": "2024-01-11"}
        ]
        
        request = AgentRequest(
            query="Categorize these transactions and analyze spending patterns",
            context={"transactions": sample_transactions}
        )
        
        response = await agent.process_request(request)
        self.logger.info(f"Response: {response.message}")
        
        if response.data and "categorized_transactions" in response.data:
            categorized = response.data["categorized_transactions"]
            self.logger.info(f"Categorized {len(categorized)} transactions")
            
            # Show categorization results
            for tx in categorized[:3]:  # Show first 3
                self.logger.info(f"  {tx['description']} -> {tx['category']} (confidence: {tx.get('confidence', 'N/A')})")
        
        # Example 2: Single transaction categorization
        self.logger.info("\n🔍 Example 2: Single Transaction Categorization")
        single_response = await agent.categorize_single_transaction(
            "Monthly office rent payment",
            2000.00,
            "2024-01-01"
        )
        self.logger.info(f"Single transaction response: {single_response.message}")
    
    async def example_cash_flow_analyzer(self):
        """Example: Cash Flow Analyzer Agent."""
        agent = CashFlowAnalyzerAgent()
        
        # Example 1: Basic cash flow analysis
        self.logger.info("💰 Example 1: Cash Flow Analysis")
        request = AgentRequest(
            query="Analyze our cash flow patterns and provide insights",
            context={"analysis_type": "cash_flow_analysis"}
        )
        
        response = await agent.process_request(request)
        self.logger.info(f"Response: {response.message}")
        
        if response.data and "analysis" in response.data:
            analysis = response.data["analysis"]
            if "metrics" in analysis:
                metrics = analysis["metrics"]
                self.logger.info(f"Average monthly net flow: ${metrics.get('average_monthly_net_flow', 'N/A')}")
                self.logger.info(f"Cash flow volatility: {metrics.get('cash_flow_volatility', 'N/A')}")
                self.logger.info(f"Trend direction: {metrics.get('trend_direction', 'N/A')}")
        
        # Example 2: Cash flow forecast
        self.logger.info("\n🔮 Example 2: Cash Flow Forecast")
        forecast_response = await agent.generate_cash_flow_forecast(6)
        self.logger.info(f"Forecast response: {forecast_response.message}")
        
        # Example 3: Liquidity risk analysis
        self.logger.info("\n⚠️ Example 3: Liquidity Risk Analysis")
        risk_response = await agent.analyze_liquidity_risk()
        self.logger.info(f"Risk analysis response: {risk_response.message}")
    
    async def example_account_reconciler(self):
        """Example: Account Reconciler Agent."""
        agent = AccountReconcilerAgent()
        
        # Example 1: Basic account reconciliation
        self.logger.info("🔍 Example 1: Account Reconciliation")
        request = AgentRequest(
            query="Reconcile my bank account and detect discrepancies",
            context={"reconciliation_type": "bank_reconciliation"}
        )
        
        response = await agent.process_request(request)
        self.logger.info(f"Response: {response.message}")
        
        if response.data and "reconciliation_result" in response.data:
            result = response.data["reconciliation_result"]
            self.logger.info(f"Match rate: {result.get('match_rate', 'N/A'):.1f}%")
            self.logger.info(f"Matched transactions: {len(result.get('matched_transactions', []))}")
            self.logger.info(f"Unmatched bank transactions: {len(result.get('unmatched_bank_transactions', []))}")
            self.logger.info(f"Unmatched accounting transactions: {len(result.get('unmatched_accounting_transactions', []))}")
        
        if response.data and "discrepancies" in response.data:
            discrepancies = response.data["discrepancies"]
            self.logger.info(f"Discrepancies found: {len(discrepancies)}")
            
            for disc in discrepancies[:2]:  # Show first 2
                self.logger.info(f"  {disc['type']}: {disc['description']}")
        
        # Example 2: Missing transaction detection
        self.logger.info("\n🔎 Example 2: Missing Transaction Detection")
        missing_response = await agent.detect_missing_transactions()
        self.logger.info(f"Missing transactions response: {missing_response.message}")
    
    async def example_orchestrator(self):
        """Example: MoE Orchestrator routing."""
        self.logger.info("🎯 Example 1: Query Routing")
        
        test_queries = [
            "Generate a financial summary for this month",
            "Categorize my recent transactions",
            "Analyze our cash flow trends",
            "Reconcile my bank account",
            "What's our profit margin this quarter?"
        ]
        
        for query in test_queries:
            self.logger.info(f"\nQuery: {query}")
            
            response = await self.orchestrator.process_query(query)
            self.logger.info(f"Selected agent: {response.agent_type}")
            self.logger.info(f"Response: {response.message[:100]}...")
            
            if response.data and "orchestrator_metadata" in response.data:
                metadata = response.data["orchestrator_metadata"]
                self.logger.info(f"Routing confidence: {metadata.get('routing_confidence', 'N/A')}")
        
        # Example 2: Get orchestrator statistics
        self.logger.info("\n📊 Example 2: Orchestrator Statistics")
        stats = await self.orchestrator.get_orchestrator_stats()
        self.logger.info(f"Total requests processed: {stats.get('total_requests', 0)}")
        
        agent_performance = stats.get('agent_performance', {})
        for agent_name, performance in agent_performance.items():
            self.logger.info(f"  {agent_name}: {performance.get('total_requests', 0)} requests, "
                           f"{performance.get('success_rate', 0):.1%} success rate")
    
    async def example_multi_agent_query(self):
        """Example: Multi-agent query processing."""
        self.logger.info("🤝 Example: Multi-Agent Query Processing")
        
        # Query that could benefit from multiple agents
        query = "Provide a comprehensive analysis of our business finances including summaries, transaction categorization, cash flow analysis, and account reconciliation"
        
        self.logger.info(f"Complex query: {query}")
        
        # Process with multiple agents
        responses = await self.orchestrator.process_multi_agent_query(query)
        
        self.logger.info(f"Responses from {len(responses)} agents:")
        for i, response in enumerate(responses, 1):
            self.logger.info(f"  {i}. {response.agent_type}: {response.message[:80]}...")
    
    async def example_custom_context(self):
        """Example: Using custom context with agents."""
        self.logger.info("🎛️ Example: Custom Context Usage")
        
        # Custom financial data
        custom_context = {
            "financial_data": {
                "revenue": {
                    "current_period": 150000.00,
                    "previous_period": 120000.00,
                    "growth_rate": 25.0
                },
                "expenses": {
                    "operating": 100000.00,
                    "administrative": 20000.00,
                    "marketing": 15000.00,
                    "total": 135000.00
                },
                "profit": {
                    "gross": 50000.00,
                    "net": 15000.00,
                    "margin": 10.0
                }
            }
        }
        
        request = AgentRequest(
            query="Generate a financial summary with custom data",
            context=custom_context
        )
        
        response = await self.orchestrator.process_query(
            query=request.query,
            context=request.context
        )
        
        self.logger.info(f"Custom context response: {response.message}")
    
    async def example_error_handling(self):
        """Example: Error handling and edge cases."""
        self.logger.info("🛡️ Example: Error Handling")
        
        # Test with invalid query
        invalid_query = "This is not a valid accounting query at all"
        
        response = await self.orchestrator.process_query(invalid_query)
        self.logger.info(f"Invalid query response: {response.message}")
        self.logger.info(f"Success: {response.success}")
        
        # Test with empty query
        empty_response = await self.orchestrator.process_query("")
        self.logger.info(f"Empty query response: {empty_response.message}")


async def main():
    """Run all examples."""
    examples = AdvancedAccountsAgentExamples()
    await examples.run_all_examples()


if __name__ == "__main__":
    asyncio.run(main())
