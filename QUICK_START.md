# 🚀 Quick Start Guide - Advanced Accounts Agent

## ✅ All Errors Fixed!

The application has been successfully fixed and is ready to use. Here's what was resolved:

### 🔧 Issues Fixed:
1. **Pydantic Import Error**: Added `pydantic-settings` dependency
2. **Environment Variable Configuration**: Made configuration more flexible
3. **Missing Dependencies**: Created installation script
4. **Setup Complexity**: Added helper scripts for easy setup

## 🎯 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
python install.py
```

### Step 2: Set Up Environment Variables
```bash
python setup_env.py
```
*This will guide you through entering your API keys*

### Step 3: Run the Application
```bash
# Test without API keys (demo mode)
python demo_mode.py

# Run full application with API keys
python main.py
```

## 🧪 Test Without API Keys

If you want to see what the application can do without setting up API keys:
```bash
python demo_mode.py
```

This will show you:
- ✅ Financial Summary Agent capabilities
- ✅ Transaction Categorizer Agent capabilities  
- ✅ Cash Flow Analyzer Agent capabilities
- ✅ Account Reconciler Agent capabilities

## 🌐 Web Interface

Once running with API keys, access the web interface at:
- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📋 Available Commands

```bash
# Installation and setup
python install.py          # Install all dependencies
python setup_env.py        # Set up environment variables

# Running the application
python main.py             # Start web interface (default)
python main.py demo        # Run demo mode
python main.py mcp         # Start MCP server
python demo_mode.py        # Test without API keys

# Examples and testing
python examples.py         # Comprehensive examples
```

## 🔑 Required API Keys

You'll need these API keys (get them from the respective services):

1. **Google AI Studio API Key**
   - Get from: https://aistudio.google.com/
   - Used for: AI processing and responses

2. **Xero Client ID & Secret**
   - Get from: https://developer.xero.com/
   - Used for: Accounting data integration

## 🎉 What You Get

- **4 Specialized AI Agents** for different accounting tasks
- **Intelligent Query Routing** that picks the right agent
- **Web Interface** with real-time chat
- **REST API** for integration
- **MCP Server** for Xero integration
- **Comprehensive Examples** and documentation

## 🆘 Need Help?

1. **Run the demo**: `python demo_mode.py`
2. **Check the README**: Full documentation available
3. **View examples**: `python examples.py`
4. **API docs**: http://localhost:8000/docs (when running)

## ✨ Success!

Your Advanced Accounts Agent is now ready to use! The application provides AI-powered accounting automation with a sophisticated Mixture-of-Experts architecture.
