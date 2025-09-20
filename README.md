# Advance-financial-account-assistant
An AI-powered data science assistant built on a Mixture-of-Experts (MOE) framework. The chatbot interface triggers specialized agents for data collection, preprocessing, analysis, feature engineering, model training, evaluation, and optimization. Implemented using OpenAI SDK and Xero MCP Server, with Google AI Studio API integration.
n AI-powered accounting and financial task automation system with a Mixture-of-Experts (MoE) architecture. This application leverages Google AI Studio API and Xero MCP Server for intelligent accounting operations.

## 🚀 Features

- **Mixture-of-Experts Architecture**: Multiple specialized AI agents for different accounting tasks
- **Google AI Studio Integration**: Uses Google's Gemini models for AI processing
- **Xero Integration**: MCP server for seamless Xero accounting data access
- **Specialized Agents**:
  - 📊 **Financial Summary Agent**: Generates P&L reports, balance sheets, and financial insights
  - 🏷️ **Transaction Categorizer**: Automatically categorizes and analyzes transactions
  - 💰 **Cash Flow Analyzer**: Analyzes cash flow patterns and provides forecasting
  - 🔍 **Account Reconciler**: Handles bank reconciliation and discrepancy detection
- **Web Interface**: FastAPI-based chatbot with real-time WebSocket support
- **REST API**: Complete API for integration with other systems

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Advanced Accounts Agent                  │
├─────────────────────────────────────────────────────────────┤
│  Web Interface (FastAPI)  │  REST API  │  WebSocket API    │
├─────────────────────────────────────────────────────────────┤
│              MoE Orchestrator (Query Router)               │
├─────────────────────────────────────────────────────────────┤
│ Financial │ Transaction │ Cash Flow │ Account              │
│ Summary   │ Categorizer │ Analyzer  │ Reconciler           │
│ Agent     │ Agent       │ Agent     │ Agent                │
├─────────────────────────────────────────────────────────────┤
│        Google AI Studio API        │    Xero MCP Server    │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.12+
- Google AI Studio API key
- Xero Client ID and Secret (for Xero integration)
- `.env` file with required environment variables

## 🛠️ Installation

### Quick Start

1. **Install dependencies**:
   ```bash
   python install.py
   ```

2. **Set up environment variables**:
   ```bash
   python setup_env.py
   ```

3. **Test the installation**:
   ```bash
   python demo_mode.py
   ```

### Manual Installation

1. **Install dependencies**:
   ```bash
   pip install -e .
   pip install pydantic-settings
   ```

2. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```env
   # Google AI Studio Configuration
   GOOGLE_AI_STUDIO_API_KEY=your_google_ai_studio_api_key_here
   GOOGLE_AI_MODEL=gemini-1.5-flash
   
   # Xero Configuration
   XERO_CLIENT_ID=your_xero_client_id_here
   XERO_CLIENT_SECRET=your_xero_client_secret_here
   XERO_TENANT_ID=your_xero_tenant_id_here
   
   # Application Configuration
   APP_NAME=Advanced Accounts Agent
   APP_VERSION=1.0.0
   DEBUG=false
   HOST=0.0.0.0
   PORT=8000
   
   # Agent Configuration
   MAX_RETRIES=3
   TIMEOUT_SECONDS=30
   ```

## 🚀 Usage

### 1. Run the Chatbot Interface (Default)
```bash
python main.py
# or
python main.py chatbot
```
Access the web interface at: `http://localhost:8000`

### 2. Run the Demo
```bash
python main.py demo
```
This will run through example queries for all agents.

### 3. Run the MCP Server
```bash
python main.py mcp
```
Starts the MCP server for Xero integration.

### 4. Run Examples
```bash
python examples.py
```
Comprehensive examples of all agent capabilities.

## 🌐 Web Interface

The web interface provides:
- **Real-time Chat**: WebSocket-based chat interface
- **Agent Information**: View all available agents and their capabilities
- **Statistics**: Monitor system performance and usage
- **API Documentation**: Built-in Swagger/OpenAPI documentation

### API Endpoints

- `GET /` - Web chat interface
- `POST /chat` - Send chat messages
- `GET /agents` - List all agents
- `GET /stats` - System statistics
- `GET /examples` - Example queries
- `POST /examples/demo` - Run demo
- `WebSocket /ws` - Real-time chat

## 🤖 Agent Capabilities

### Financial Summary Agent
- Generate P&L summaries
- Create balance sheet analysis
- Provide financial health insights
- Compare financial periods
- Generate executive summaries

**Example Queries**:
- "Generate a financial summary for this month"
- "Create a profit and loss report"
- "What's our financial health status?"

### Transaction Categorizer Agent
- Auto-categorize transactions
- Detect spending patterns
- Identify unusual transactions
- Generate spending reports
- Suggest budget optimizations

**Example Queries**:
- "Categorize these transactions"
- "Analyze my spending patterns"
- "What categories are my expenses in?"

### Cash Flow Analyzer Agent
- Analyze cash flow patterns
- Generate cash flow forecasts
- Identify liquidity risks
- Monitor cash flow trends
- Provide cash management recommendations

**Example Queries**:
- "Analyze our cash flow trends"
- "Generate a cash flow forecast"
- "What are our liquidity risks?"

### Account Reconciler Agent
- Reconcile bank accounts
- Detect transaction discrepancies
- Match transactions between systems
- Identify missing transactions
- Generate reconciliation reports

**Example Queries**:
- "Reconcile my bank account"
- "Find missing transactions"
- "Detect discrepancies in my accounts"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_AI_STUDIO_API_KEY` | Google AI Studio API key | Required |
| `GOOGLE_AI_MODEL` | AI model to use | `gemini-1.5-flash` |
| `XERO_CLIENT_ID` | Xero client ID | Required |
| `XERO_CLIENT_SECRET` | Xero client secret | Required |
| `XERO_TENANT_ID` | Xero tenant ID | Optional |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `false` |
| `MAX_RETRIES` | Max retries for AI calls | `3` |
| `TIMEOUT_SECONDS` | Request timeout | `30` |

## 📊 Example Usage

### Python API Usage

```python
import asyncio
from orchestrator import MoEOrchestrator

async def main():
    orchestrator = MoEOrchestrator()
    
    # Process a query
    response = await orchestrator.process_query(
        "Generate a financial summary for this month"
    )
    
    print(f"Agent: {response.agent_type}")
    print(f"Response: {response.message}")
    print(f"Success: {response.success}")

asyncio.run(main())
```

### REST API Usage

```bash
# Send a chat message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Generate a financial summary for this month",
    "user_id": "user123",
    "session_id": "session456"
  }'

# Get agent information
curl "http://localhost:8000/agents"

# Get system statistics
curl "http://localhost:8000/stats"
```

## 🔌 MCP Server Integration

The MCP server provides tools for Xero integration:

- `get_xero_contacts` - Retrieve contacts
- `get_xero_invoices` - Retrieve invoices
- `get_xero_transactions` - Retrieve bank transactions
- `get_xero_accounts` - Retrieve chart of accounts
- `get_xero_financial_summary` - Get financial summaries
- `create_xero_invoice` - Create new invoices

## 🧪 Testing

Run the examples to test all functionality:

```bash
python examples.py
```

This will demonstrate:
- Individual agent capabilities
- Orchestrator routing
- Multi-agent queries
- Error handling
- Custom context usage

## 📁 Project Structure

```
advance-account-agent/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── orchestrator.py        # MoE orchestrator
├── mcp_server.py          # Xero MCP server
├── chatbot_interface.py   # FastAPI web interface
├── examples.py            # Usage examples
├── agents/                # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── financial_summary_agent.py
│   ├── transaction_categorizer_agent.py
│   ├── cash_flow_analyzer_agent.py
│   └── account_reconciler_agent.py
├── pyproject.toml         # Project dependencies
└── README.md             # This file
```

## 🚀 Deployment

### Development
```bash
python main.py
```

### Production
```bash
# Install production dependencies
pip install -e .[dev]

# Run with production settings
DEBUG=false python main.py
```

### Docker (Optional)
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["python", "main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support & Troubleshooting

### Common Issues

**1. Pydantic Import Error**
```
PydanticImportError: `BaseSettings` has been moved to the `pydantic-settings` package
```
**Solution**: Install the missing package:
```bash
pip install pydantic-settings
```

**2. Missing Environment Variables**
```
Missing required environment variables: GOOGLE_AI_STUDIO_API_KEY, XERO_CLIENT_ID, XERO_CLIENT_SECRET
```
**Solution**: Run the setup script:
```bash
python setup_env.py
```

**3. Module Import Errors**
**Solution**: Install dependencies:
```bash
python install.py
```

### Testing Without API Keys

If you want to test the application without setting up API keys:
```bash
python demo_mode.py
```

### Getting Help

For support and questions:
1. Check the examples in `examples.py`
2. Review the API documentation at `http://localhost:8000/docs`
3. Check the logs for error details
4. Ensure all environment variables are properly set
5. Run `python demo_mode.py` to test without API keys

## 🔮 Future Enhancements

- [ ] Additional specialized agents (Tax Agent, Budget Agent, etc.)
- [ ] Machine learning model training for better categorization
- [ ] Integration with more accounting systems
- [ ] Advanced reporting and visualization
- [ ] Multi-tenant support
- [ ] Audit trail and compliance features
