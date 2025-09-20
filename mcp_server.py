"""
MCP Server for Xero integration in the Advanced Accounts Agent.
Provides tools for interacting with Xero accounting data.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, 
    Tool, 
    TextContent, 
    ImageContent, 
    EmbeddedResource,
    LoggingLevel
)

from config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Initialize MCP server
server = Server("xero-accounting-server")


class XeroMCPServer:
    """
    MCP Server for Xero integration.
    Provides tools for accessing Xero accounting data.
    """
    
    def __init__(self):
        self.server = server
        self.settings = settings
        self.logger = logger
        self._setup_tools()
        self._setup_resources()
    
    def _setup_tools(self):
        """Set up MCP tools for Xero operations."""
        
        @server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available Xero tools."""
            return [
                Tool(
                    name="get_xero_contacts",
                    description="Retrieve contacts from Xero",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of contacts to retrieve",
                                "default": 100
                            },
                            "search": {
                                "type": "string",
                                "description": "Search term for contact names"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_xero_invoices",
                    description="Retrieve invoices from Xero",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "description": "Invoice status filter",
                                "enum": ["DRAFT", "SUBMITTED", "AUTHORISED", "PAID", "VOIDED"]
                            },
                            "date_from": {
                                "type": "string",
                                "description": "Start date for invoice search (YYYY-MM-DD)"
                            },
                            "date_to": {
                                "type": "string", 
                                "description": "End date for invoice search (YYYY-MM-DD)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of invoices to retrieve",
                                "default": 100
                            }
                        }
                    }
                ),
                Tool(
                    name="get_xero_transactions",
                    description="Retrieve bank transactions from Xero",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "bank_account_id": {
                                "type": "string",
                                "description": "Bank account ID to retrieve transactions for"
                            },
                            "date_from": {
                                "type": "string",
                                "description": "Start date for transaction search (YYYY-MM-DD)"
                            },
                            "date_to": {
                                "type": "string",
                                "description": "End date for transaction search (YYYY-MM-DD)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of transactions to retrieve",
                                "default": 100
                            }
                        }
                    }
                ),
                Tool(
                    name="get_xero_accounts",
                    description="Retrieve chart of accounts from Xero",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "account_type": {
                                "type": "string",
                                "description": "Filter by account type",
                                "enum": ["REVENUE", "EXPENSE", "ASSET", "LIABILITY", "EQUITY"]
                            }
                        }
                    }
                ),
                Tool(
                    name="get_xero_financial_summary",
                    description="Get financial summary data from Xero",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date_from": {
                                "type": "string",
                                "description": "Start date for financial summary (YYYY-MM-DD)"
                            },
                            "date_to": {
                                "type": "string",
                                "description": "End date for financial summary (YYYY-MM-DD)"
                            },
                            "summary_type": {
                                "type": "string",
                                "description": "Type of financial summary",
                                "enum": ["profit_loss", "balance_sheet", "cash_flow"],
                                "default": "profit_loss"
                            }
                        }
                    }
                ),
                Tool(
                    name="create_xero_invoice",
                    description="Create a new invoice in Xero",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "contact_id": {
                                "type": "string",
                                "description": "Contact ID for the invoice"
                            },
                            "line_items": {
                                "type": "array",
                                "description": "Invoice line items",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "description": {"type": "string"},
                                        "quantity": {"type": "number"},
                                        "unit_amount": {"type": "number"},
                                        "account_code": {"type": "string"}
                                    }
                                }
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Invoice due date (YYYY-MM-DD)"
                            }
                        },
                        "required": ["contact_id", "line_items"]
                    }
                )
            ]
        
        @server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "get_xero_contacts":
                    return await self._get_xero_contacts(arguments)
                elif name == "get_xero_invoices":
                    return await self._get_xero_invoices(arguments)
                elif name == "get_xero_transactions":
                    return await self._get_xero_transactions(arguments)
                elif name == "get_xero_accounts":
                    return await self._get_xero_accounts(arguments)
                elif name == "get_xero_financial_summary":
                    return await self._get_xero_financial_summary(arguments)
                elif name == "create_xero_invoice":
                    return await self._create_xero_invoice(arguments)
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
            except Exception as e:
                self.logger.error(f"Error calling tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    def _setup_resources(self):
        """Set up MCP resources."""
        
        @server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available Xero resources."""
            return [
                Resource(
                    uri="xero://contacts",
                    name="Xero Contacts",
                    description="Access to Xero contacts data",
                    mimeType="application/json"
                ),
                Resource(
                    uri="xero://invoices",
                    name="Xero Invoices", 
                    description="Access to Xero invoices data",
                    mimeType="application/json"
                ),
                Resource(
                    uri="xero://transactions",
                    name="Xero Transactions",
                    description="Access to Xero bank transactions",
                    mimeType="application/json"
                ),
                Resource(
                    uri="xero://accounts",
                    name="Xero Chart of Accounts",
                    description="Access to Xero chart of accounts",
                    mimeType="application/json"
                )
            ]
        
        @server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read Xero resource data."""
            try:
                if uri == "xero://contacts":
                    return await self._get_contacts_data()
                elif uri == "xero://invoices":
                    return await self._get_invoices_data()
                elif uri == "xero://transactions":
                    return await self._get_transactions_data()
                elif uri == "xero://accounts":
                    return await self._get_accounts_data()
                else:
                    return json.dumps({"error": f"Unknown resource: {uri}"})
            except Exception as e:
                self.logger.error(f"Error reading resource {uri}: {str(e)}")
                return json.dumps({"error": str(e)})
    
    async def _get_xero_contacts(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get Xero contacts."""
        # In a real implementation, this would call the Xero API
        # For now, we'll return sample data
        limit = arguments.get("limit", 100)
        search = arguments.get("search", "")
        
        sample_contacts = [
            {
                "ContactID": "12345678-1234-1234-1234-123456789012",
                "Name": "ABC Corporation",
                "EmailAddress": "contact@abccorp.com",
                "IsCustomer": True,
                "IsSupplier": False,
                "ContactStatus": "ACTIVE"
            },
            {
                "ContactID": "87654321-4321-4321-4321-210987654321",
                "Name": "XYZ Suppliers Ltd",
                "EmailAddress": "orders@xyzsuppliers.com",
                "IsCustomer": False,
                "IsSupplier": True,
                "ContactStatus": "ACTIVE"
            }
        ]
        
        # Filter by search term if provided
        if search:
            sample_contacts = [
                contact for contact in sample_contacts 
                if search.lower() in contact["Name"].lower()
            ]
        
        # Apply limit
        sample_contacts = sample_contacts[:limit]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "contacts": sample_contacts,
                "total": len(sample_contacts),
                "message": "Sample Xero contacts data (replace with actual Xero API call)"
            }, indent=2)
        )]
    
    async def _get_xero_invoices(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get Xero invoices."""
        status = arguments.get("status")
        date_from = arguments.get("date_from")
        date_to = arguments.get("date_to")
        limit = arguments.get("limit", 100)
        
        sample_invoices = [
            {
                "InvoiceID": "inv-001",
                "InvoiceNumber": "INV-2024-001",
                "Type": "ACCREC",
                "Status": "AUTHORISED",
                "Date": "2024-01-15",
                "DueDate": "2024-02-15",
                "Total": 1500.00,
                "AmountPaid": 0.00,
                "AmountDue": 1500.00,
                "Contact": {
                    "ContactID": "12345678-1234-1234-1234-123456789012",
                    "Name": "ABC Corporation"
                }
            },
            {
                "InvoiceID": "inv-002", 
                "InvoiceNumber": "INV-2024-002",
                "Type": "ACCREC",
                "Status": "PAID",
                "Date": "2024-01-10",
                "DueDate": "2024-02-10",
                "Total": 2500.00,
                "AmountPaid": 2500.00,
                "AmountDue": 0.00,
                "Contact": {
                    "ContactID": "87654321-4321-4321-4321-210987654321",
                    "Name": "XYZ Suppliers Ltd"
                }
            }
        ]
        
        # Apply filters
        if status:
            sample_invoices = [inv for inv in sample_invoices if inv["Status"] == status]
        
        # Apply limit
        sample_invoices = sample_invoices[:limit]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "invoices": sample_invoices,
                "total": len(sample_invoices),
                "filters": {
                    "status": status,
                    "date_from": date_from,
                    "date_to": date_to
                },
                "message": "Sample Xero invoices data (replace with actual Xero API call)"
            }, indent=2)
        )]
    
    async def _get_xero_transactions(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get Xero bank transactions."""
        bank_account_id = arguments.get("bank_account_id")
        date_from = arguments.get("date_from")
        date_to = arguments.get("date_to")
        limit = arguments.get("limit", 100)
        
        sample_transactions = [
            {
                "TransactionID": "txn-001",
                "BankAccount": {
                    "AccountID": bank_account_id or "bank-001",
                    "Name": "Business Checking"
                },
                "Date": "2024-01-15",
                "Reference": "Office supplies purchase",
                "Amount": -150.00,
                "Type": "SPEND",
                "Status": "RECONCILED"
            },
            {
                "TransactionID": "txn-002",
                "BankAccount": {
                    "AccountID": bank_account_id or "bank-001", 
                    "Name": "Business Checking"
                },
                "Date": "2024-01-14",
                "Reference": "Customer payment - ABC Corp",
                "Amount": 5000.00,
                "Type": "RECEIVE",
                "Status": "RECONCILED"
            }
        ]
        
        # Apply limit
        sample_transactions = sample_transactions[:limit]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "transactions": sample_transactions,
                "total": len(sample_transactions),
                "filters": {
                    "bank_account_id": bank_account_id,
                    "date_from": date_from,
                    "date_to": date_to
                },
                "message": "Sample Xero transactions data (replace with actual Xero API call)"
            }, indent=2)
        )]
    
    async def _get_xero_accounts(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get Xero chart of accounts."""
        account_type = arguments.get("account_type")
        
        sample_accounts = [
            {
                "AccountID": "acc-001",
                "Code": "4000",
                "Name": "Sales Revenue",
                "Type": "REVENUE",
                "Class": "REVENUE",
                "Status": "ACTIVE"
            },
            {
                "AccountID": "acc-002",
                "Code": "5000",
                "Name": "Office Supplies",
                "Type": "EXPENSE",
                "Class": "EXPENSE",
                "Status": "ACTIVE"
            },
            {
                "AccountID": "acc-003",
                "Code": "1000",
                "Name": "Business Checking",
                "Type": "BANK",
                "Class": "ASSET",
                "Status": "ACTIVE"
            }
        ]
        
        # Filter by account type if provided
        if account_type:
            sample_accounts = [acc for acc in sample_accounts if acc["Type"] == account_type]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "accounts": sample_accounts,
                "total": len(sample_accounts),
                "filters": {"account_type": account_type},
                "message": "Sample Xero accounts data (replace with actual Xero API call)"
            }, indent=2)
        )]
    
    async def _get_xero_financial_summary(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get Xero financial summary."""
        date_from = arguments.get("date_from", "2024-01-01")
        date_to = arguments.get("date_to", "2024-01-31")
        summary_type = arguments.get("summary_type", "profit_loss")
        
        if summary_type == "profit_loss":
            summary_data = {
                "revenue": {
                    "total": 125000.00,
                    "accounts": [
                        {"name": "Sales Revenue", "amount": 120000.00},
                        {"name": "Service Revenue", "amount": 5000.00}
                    ]
                },
                "expenses": {
                    "total": 95000.00,
                    "accounts": [
                        {"name": "Office Supplies", "amount": 5000.00},
                        {"name": "Rent", "amount": 20000.00},
                        {"name": "Salaries", "amount": 60000.00},
                        {"name": "Utilities", "amount": 10000.00}
                    ]
                },
                "net_profit": 30000.00
            }
        else:
            summary_data = {"message": f"Summary type {summary_type} not implemented in sample data"}
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "summary_type": summary_type,
                "period": {"from": date_from, "to": date_to},
                "data": summary_data,
                "message": "Sample Xero financial summary (replace with actual Xero API call)"
            }, indent=2)
        )]
    
    async def _create_xero_invoice(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Create a new Xero invoice."""
        contact_id = arguments["contact_id"]
        line_items = arguments["line_items"]
        due_date = arguments.get("due_date")
        
        # In a real implementation, this would create an invoice in Xero
        # For now, we'll return a success response with sample data
        
        invoice_data = {
            "InvoiceID": f"inv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "InvoiceNumber": f"INV-{datetime.now().strftime('%Y%m%d')}-001",
            "ContactID": contact_id,
            "LineItems": line_items,
            "DueDate": due_date,
            "Status": "DRAFT",
            "Total": sum(item.get("quantity", 1) * item.get("unit_amount", 0) for item in line_items)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "invoice": invoice_data,
                "message": "Invoice created successfully (sample data - replace with actual Xero API call)"
            }, indent=2)
        )]
    
    async def _get_contacts_data(self) -> str:
        """Get contacts data for resource."""
        return json.dumps(await self._get_xero_contacts({}))
    
    async def _get_invoices_data(self) -> str:
        """Get invoices data for resource."""
        return json.dumps(await self._get_xero_invoices({}))
    
    async def _get_transactions_data(self) -> str:
        """Get transactions data for resource."""
        return json.dumps(await self._get_xero_transactions({}))
    
    async def _get_accounts_data(self) -> str:
        """Get accounts data for resource."""
        return json.dumps(await self._get_xero_accounts({}))


async def main():
    """Main function to run the MCP server."""
    xero_server = XeroMCPServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="xero-accounting-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
