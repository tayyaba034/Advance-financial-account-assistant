"""
FastAPI-based chatbot interface for the Advanced Accounts Agent.
Provides REST API endpoints for interacting with the accounting agents.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from orchestrator import MoEOrchestrator
from config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Accounts Agent",
    description="AI-powered accounting and financial task automation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = MoEOrchestrator()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


# Pydantic models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    user_id: Optional[str] = Field(default=None, description="User identifier")
    session_id: Optional[str] = Field(default=None, description="Session identifier")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool = Field(description="Whether the request was successful")
    message: str = Field(description="Response message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    agent_type: str = Field(description="Agent that processed the request")
    timestamp: datetime = Field(default_factory=datetime.now)


class AgentInfo(BaseModel):
    """Model for agent information."""
    name: str = Field(description="Agent name")
    description: str = Field(description="Agent description")
    capabilities: List[str] = Field(description="Agent capabilities")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(description="Service version")


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Serve the chat interface HTML."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Advanced Accounts Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }
            .chat-container { height: 400px; overflow-y: auto; padding: 20px; border-bottom: 1px solid #eee; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user-message { background: #3498db; color: white; text-align: right; }
            .bot-message { background: #ecf0f1; color: #2c3e50; }
            .input-container { padding: 20px; display: flex; gap: 10px; }
            .input-field { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .send-button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .send-button:hover { background: #2980b9; }
            .status { padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Advanced Accounts Agent</h1>
                <p>AI-powered accounting and financial task automation</p>
            </div>
            <div class="status" id="status">Connecting...</div>
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    Welcome! I'm your Advanced Accounts Agent. I can help you with:
                    <ul>
                        <li>📊 Financial summaries and reports</li>
                        <li>🏷️ Transaction categorization</li>
                        <li>💰 Cash flow analysis</li>
                        <li>🔍 Account reconciliation</li>
                    </ul>
                    How can I assist you today?
                </div>
            </div>
            <div class="input-container">
                <input type="text" class="input-field" id="messageInput" placeholder="Ask me about your accounting needs..." />
                <button class="send-button" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            let ws;
            const chatContainer = document.getElementById('chatContainer');
            const messageInput = document.getElementById('messageInput');
            const status = document.getElementById('status');

            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
                
                ws.onopen = function() {
                    status.textContent = 'Connected';
                    status.style.background = '#d4edda';
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    addMessage(data.message, 'bot');
                };
                
                ws.onclose = function() {
                    status.textContent = 'Disconnected';
                    status.style.background = '#f8d7da';
                    setTimeout(connectWebSocket, 3000);
                };
            }

            function addMessage(message, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = message;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function sendMessage() {
                const message = messageInput.value.trim();
                if (message && ws.readyState === WebSocket.OPEN) {
                    addMessage(message, 'user');
                    ws.send(JSON.stringify({message: message}));
                    messageInput.value = '';
                }
            }

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            connectWebSocket();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for processing user messages."""
    try:
        logger.info(f"Processing chat request: {request.message[:100]}...")
        
        # Process the request through the orchestrator
        response = await orchestrator.process_query(
            query=request.message,
            context=request.context,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        # Convert to API response format
        return ChatResponse(
            success=response.success,
            message=response.message,
            data=response.data,
            agent_type=response.agent_type,
            timestamp=response.timestamp
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents", response_model=List[AgentInfo])
async def get_agents():
    """Get information about all available agents."""
    try:
        agent_info = await orchestrator.get_agent_info()
        
        agents = []
        for agent_name, info in agent_info.items():
            agents.append(AgentInfo(
                name=info["name"],
                description=info["description"],
                capabilities=info["capabilities"]
            ))
        
        return agents
        
    except Exception as e:
        logger.error(f"Error getting agent info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_orchestrator_stats():
    """Get orchestrator statistics."""
    try:
        stats = await orchestrator.get_orchestrator_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting orchestrator stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/batch")
async def chat_batch(requests: List[ChatRequest]):
    """Process multiple chat requests in batch."""
    try:
        responses = []
        
        for request in requests:
            response = await orchestrator.process_query(
                query=request.message,
                context=request.context,
                user_id=request.user_id,
                session_id=request.session_id
            )
            
            responses.append(ChatResponse(
                success=response.success,
                message=response.message,
                data=response.data,
                agent_type=response.agent_type,
                timestamp=response.timestamp
            ))
        
        return {"responses": responses}
        
    except Exception as e:
        logger.error(f"Error processing batch chat requests: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message:
                continue
            
            # Process the message through the orchestrator
            response = await orchestrator.process_query(
                query=user_message,
                context=message_data.get("context"),
                user_id=message_data.get("user_id"),
                session_id=message_data.get("session_id")
            )
            
            # Send response back to client
            await manager.send_personal_message(
                json.dumps({
                    "message": response.message,
                    "success": response.success,
                    "agent_type": response.agent_type,
                    "data": response.data,
                    "timestamp": response.timestamp.isoformat()
                }),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)


# Example usage endpoints
@app.get("/examples")
async def get_examples():
    """Get example queries for each agent."""
    return {
        "financial_summary": [
            "Generate a financial summary for this month",
            "Create a profit and loss report",
            "Show me the balance sheet analysis",
            "What's our financial health status?"
        ],
        "transaction_categorizer": [
            "Categorize these transactions",
            "Analyze my spending patterns",
            "What categories are my expenses in?",
            "Generate an expense report"
        ],
        "cash_flow_analyzer": [
            "Analyze our cash flow trends",
            "Generate a cash flow forecast",
            "What are our liquidity risks?",
            "Show me cash flow patterns"
        ],
        "account_reconciler": [
            "Reconcile my bank account",
            "Find missing transactions",
            "Detect discrepancies in my accounts",
            "Match transactions between systems"
        ]
    }


@app.post("/examples/demo")
async def run_demo():
    """Run a demonstration of all agents."""
    demo_queries = [
        "Generate a financial summary for this month",
        "Categorize my recent transactions",
        "Analyze our cash flow trends",
        "Reconcile my bank account"
    ]
    
    results = []
    for query in demo_queries:
        try:
            response = await orchestrator.process_query(query)
            results.append({
                "query": query,
                "response": {
                    "success": response.success,
                    "message": response.message,
                    "agent_type": response.agent_type
                }
            })
        except Exception as e:
            results.append({
                "query": query,
                "error": str(e)
            })
    
    return {"demo_results": results}


if __name__ == "__main__":
    import uvicorn
    
    # Validate environment before starting
    from config import validate_environment
    if not validate_environment():
        logger.error("Environment validation failed. Please check your .env file.")
        exit(1)
    
    logger.info(f"Starting Advanced Accounts Agent on {settings.host}:{settings.port}")
    uvicorn.run(
        "chatbot_interface:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
