"""
Advanced Accounts Agent - Main Application Entry Point
AI-powered accounting and financial task automation with Mixture-of-Experts architecture.
"""

import asyncio
import logging
import sys
from typing import Optional

from config import get_settings, validate_environment
from orchestrator import MoEOrchestrator
from chatbot_interface import app
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AdvancedAccountsAgent:
    """
    Main application class for the Advanced Accounts Agent.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.settings = get_settings()
        self.orchestrator = MoEOrchestrator()
        self.logger = logger
        
    async def initialize(self):
        """Initialize the application components."""
        try:
            self.logger.info("Initializing Advanced Accounts Agent...")
            
            # Validate environment
            if not validate_environment():
                raise Exception("Environment validation failed")
            
            # Initialize orchestrator
            await self.orchestrator.get_agent_info()
            
            self.logger.info("✅ Advanced Accounts Agent initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize: {str(e)}")
            return False
    
    async def run_demo(self):
        """Run a demonstration of the system capabilities."""
        self.logger.info("🚀 Running Advanced Accounts Agent Demo...")
        
        demo_queries = [
            "Generate a financial summary for this month",
            "Categorize my recent transactions and analyze spending patterns",
            "Analyze our cash flow trends and provide a forecast",
            "Reconcile my bank account and detect any discrepancies"
        ]
        
        for i, query in enumerate(demo_queries, 1):
            self.logger.info(f"\n📝 Demo Query {i}: {query}")
            
            try:
                response = await self.orchestrator.process_query(query)
                
                if response.success:
                    self.logger.info(f"✅ Response from {response.agent_type}:")
                    self.logger.info(f"   {response.message}")
                    
                    if response.data and "orchestrator_metadata" in response.data:
                        metadata = response.data["orchestrator_metadata"]
                        self.logger.info(f"   Routing confidence: {metadata.get('routing_confidence', 'N/A')}")
                        self.logger.info(f"   Processing time: {metadata.get('processing_time', 'N/A'):.2f}s")
                else:
                    self.logger.warning(f"⚠️  Query failed: {response.message}")
                    
            except Exception as e:
                self.logger.error(f"❌ Error processing query: {str(e)}")
            
            # Add delay between queries
            await asyncio.sleep(1)
        
        self.logger.info("\n🎉 Demo completed!")
    
    async def run_chatbot(self):
        """Run the chatbot interface."""
        self.logger.info(f"🌐 Starting chatbot interface on {self.settings.host}:{self.settings.port}")
        
        config = uvicorn.Config(
            app,
            host=self.settings.host,
            port=self.settings.port,
            log_level="info",
            reload=self.settings.debug
        )
        
        server = uvicorn.Server(config)
        await server.serve()
    
    async def run_mcp_server(self):
        """Run the MCP server for Xero integration."""
        self.logger.info("🔌 Starting MCP server for Xero integration...")
        
        from mcp_server import main as mcp_main
        await mcp_main()


async def main():
    """Main entry point."""
    agent = AdvancedAccountsAgent()
    
    # Initialize the application
    if not await agent.initialize():
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            await agent.run_demo()
        elif command == "mcp":
            await agent.run_mcp_server()
        elif command == "chatbot":
            await agent.run_chatbot()
        else:
            print("Usage: python main.py [demo|mcp|chatbot]")
            print("  demo    - Run demonstration of all agents")
            print("  mcp     - Run MCP server for Xero integration")
            print("  chatbot - Run chatbot web interface (default)")
            sys.exit(1)
    else:
        # Default: run chatbot interface
        await agent.run_chatbot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Shutting down Advanced Accounts Agent...")
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        sys.exit(1)
