"""
Mixture-of-Experts (MoE) Orchestrator for Advanced Accounts Agent.
Routes user queries to the most appropriate specialized agent.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

from agents import (
    FinancialSummaryAgent,
    TransactionCategorizerAgent,
    CashFlowAnalyzerAgent,
    AccountReconcilerAgent,
    AgentRequest,
    AgentResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MoEOrchestrator:
    """
    Mixture-of-Experts Orchestrator that routes queries to specialized agents.
    """
    
    def __init__(self):
        """Initialize the orchestrator with all available agents."""
        self.agents = {
            "financial_summary": FinancialSummaryAgent(),
            "transaction_categorizer": TransactionCategorizerAgent(),
            "cash_flow_analyzer": CashFlowAnalyzerAgent(),
            "account_reconciler": AccountReconcilerAgent()
        }
        
        self.logger = logging.getLogger(f"{__name__}.MoEOrchestrator")
        self.request_history = []
        
        self.logger.info(f"Initialized MoE Orchestrator with {len(self.agents)} agents")
    
    async def process_query(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AgentResponse:
        """
        Process a user query by routing it to the most appropriate agent.
        
        Args:
            query: User query
            context: Additional context
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            AgentResponse: Response from the selected agent
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Processing query: {query[:100]}...")
            
            # Create agent request
            request = AgentRequest(
                query=query,
                context=context,
                user_id=user_id,
                session_id=session_id
            )
            
            # Find the best agent for this query
            selected_agent = await self._select_best_agent(query, context)
            
            if not selected_agent:
                return self._create_fallback_response(query)
            
            # Process the request with the selected agent
            response = await selected_agent.process_request(request)
            
            # Log the request for learning
            self._log_request(query, selected_agent.name, response.success)
            
            # Add orchestrator metadata
            response.data = response.data or {}
            response.data["orchestrator_metadata"] = {
                "selected_agent": selected_agent.name,
                "agent_capabilities": selected_agent.get_capabilities(),
                "routing_confidence": self._calculate_routing_confidence(query, selected_agent),
                "processing_time": (datetime.now() - start_time).total_seconds()
            }
            
            self.logger.info(f"Query processed by {selected_agent.name} - Success: {response.success}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return self._create_error_response(str(e))
    
    async def _select_best_agent(self, query: str, context: Optional[Dict[str, Any]]) -> Optional[Any]:
        """
        Select the best agent for the given query.
        
        Args:
            query: User query
            context: Additional context
            
        Returns:
            Selected agent or None if no suitable agent found
        """
        # Score each agent based on their ability to handle the query
        agent_scores = {}
        
        for agent_name, agent in self.agents.items():
            try:
                # Check if agent can handle the query
                can_handle = agent.can_handle(query)
                
                if can_handle:
                    # Calculate confidence score
                    confidence = await self._calculate_agent_confidence(agent, query, context)
                    agent_scores[agent_name] = {
                        "agent": agent,
                        "confidence": confidence,
                        "can_handle": True
                    }
                else:
                    agent_scores[agent_name] = {
                        "agent": agent,
                        "confidence": 0.0,
                        "can_handle": False
                    }
                    
            except Exception as e:
                self.logger.warning(f"Error evaluating agent {agent_name}: {str(e)}")
                agent_scores[agent_name] = {
                    "agent": agent,
                    "confidence": 0.0,
                    "can_handle": False
                }
        
        # Select agent with highest confidence
        best_agent = None
        best_confidence = 0.0
        
        for agent_name, score_data in agent_scores.items():
            if score_data["can_handle"] and score_data["confidence"] > best_confidence:
                best_agent = score_data["agent"]
                best_confidence = score_data["confidence"]
        
        self.logger.info(f"Selected agent: {best_agent.name if best_agent else 'None'} (confidence: {best_confidence:.2f})")
        return best_agent
    
    async def _calculate_agent_confidence(self, agent: Any, query: str, context: Optional[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for an agent handling a specific query.
        
        Args:
            agent: The agent to evaluate
            query: User query
            context: Additional context
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.5  # Base confidence
        
        # Keyword matching boost
        query_lower = query.lower()
        agent_capabilities = [cap.lower() for cap in agent.get_capabilities()]
        
        keyword_matches = 0
        for capability in agent_capabilities:
            if any(word in query_lower for word in capability.split()):
                keyword_matches += 1
        
        if keyword_matches > 0:
            confidence += min(0.3, keyword_matches * 0.1)
        
        # Context-based boost
        if context:
            if "analysis_type" in context and context["analysis_type"] in agent_capabilities:
                confidence += 0.2
            
            if "report_type" in context and context["report_type"] in agent_capabilities:
                confidence += 0.2
        
        # Historical performance boost (if available)
        historical_performance = self._get_historical_performance(agent.name)
        if historical_performance > 0.8:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _calculate_routing_confidence(self, query: str, selected_agent: Any) -> float:
        """Calculate confidence in the routing decision."""
        # Simple confidence based on agent's ability to handle the query
        if selected_agent.can_handle(query):
            return 0.8
        else:
            return 0.3
    
    def _get_historical_performance(self, agent_name: str) -> float:
        """Get historical performance score for an agent."""
        if not self.request_history:
            return 0.5
        
        agent_history = [req for req in self.request_history if req["agent"] == agent_name]
        if not agent_history:
            return 0.5
        
        success_rate = sum(1 for req in agent_history if req["success"]) / len(agent_history)
        return success_rate
    
    def _log_request(self, query: str, agent_name: str, success: bool):
        """Log request for learning and performance tracking."""
        self.request_history.append({
            "query": query[:100],  # Truncate for storage
            "agent": agent_name,
            "success": success,
            "timestamp": datetime.now()
        })
        
        # Keep only last 1000 requests
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
    
    def _create_fallback_response(self, query: str) -> AgentResponse:
        """Create a fallback response when no agent can handle the query."""
        return AgentResponse(
            success=False,
            message="I'm sorry, but I couldn't find a suitable agent to handle your request. Please try rephrasing your query or contact support.",
            agent_type="MoEOrchestrator",
            data={
                "available_agents": list(self.agents.keys()),
                "agent_capabilities": {
                    agent_name: agent.get_capabilities() 
                    for agent_name, agent in self.agents.items()
                }
            }
        )
    
    def _create_error_response(self, error_message: str) -> AgentResponse:
        """Create an error response."""
        return AgentResponse(
            success=False,
            message=f"An error occurred while processing your request: {error_message}",
            agent_type="MoEOrchestrator",
            data={"error": error_message}
        )
    
    async def get_agent_info(self) -> Dict[str, Any]:
        """Get information about all available agents."""
        return {
            agent_name: agent.get_info() 
            for agent_name, agent in self.agents.items()
        }
    
    async def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        if not self.request_history:
            return {
                "total_requests": 0,
                "agent_performance": {},
                "recent_activity": []
            }
        
        # Calculate agent performance
        agent_performance = {}
        for agent_name in self.agents.keys():
            agent_requests = [req for req in self.request_history if req["agent"] == agent_name]
            if agent_requests:
                success_rate = sum(1 for req in agent_requests if req["success"]) / len(agent_requests)
                agent_performance[agent_name] = {
                    "total_requests": len(agent_requests),
                    "success_rate": success_rate,
                    "last_used": max(req["timestamp"] for req in agent_requests).isoformat()
                }
        
        return {
            "total_requests": len(self.request_history),
            "agent_performance": agent_performance,
            "recent_activity": [
                {
                    "query": req["query"],
                    "agent": req["agent"],
                    "success": req["success"],
                    "timestamp": req["timestamp"].isoformat()
                }
                for req in self.request_history[-10:]  # Last 10 requests
            ]
        }
    
    async def process_multi_agent_query(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> List[AgentResponse]:
        """
        Process a query that might benefit from multiple agents.
        
        Args:
            query: User query
            context: Additional context
            
        Returns:
            List of responses from relevant agents
        """
        responses = []
        
        # Find all agents that can handle the query
        relevant_agents = []
        for agent_name, agent in self.agents.items():
            if agent.can_handle(query):
                relevant_agents.append(agent)
        
        # Process with each relevant agent
        for agent in relevant_agents:
            try:
                request = AgentRequest(query=query, context=context)
                response = await agent.process_request(request)
                responses.append(response)
            except Exception as e:
                self.logger.warning(f"Error processing with agent {agent.name}: {str(e)}")
        
        return responses
