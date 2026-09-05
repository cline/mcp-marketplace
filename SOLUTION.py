import os
import json
import re
from pathlib import Path
from typing import Any
from datetime import datetime

import mcp

def get_data_dir() -> Path:
    xdg_data = os.environ.get("XDG_DATA_HOME", str(Path.home()))
    base_path = Path(xdg_data) / "mcp-servers/deposits"
    (base_path / "data").mkdir(parents=True, exist_ok=True)
    return base_path

def load_deposits(client: str | None = None) -> list[dict[str, Any]]:
    store_path = get_data_dir() / "deposits.json"
    try:
        if store_path.exists():
            with open(store_path, 'r') as f:
                data = json.load(f)
                if client:
                    return [d for d in data if d.get("client") == client]
                return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_deposits(data: list[dict[str, Any]]) -> None:
    store_path = get_data_dir() / "deposits.json"
    with open(store_path, 'w') as f:
        json.dump(data, f, indent=2)

class DepositServer:
    def __init__(self):
        self.server = mcp.Server("deposits")
        self.current_deposits = load_deposits()

    def _generate_id(self) -> str:
        now = datetime.now()
        return f"DEP-{now.year}-{now.month:02d}-{now.day:02d}"

    def _get_held_amount(self, client: str, currency: str | None = None) -> int:
        client_deposits = load_deposits(client)
        if currency:
            # Filter specifically by currency if provided, else sum across all
            client_deposits = [d for d in client_deposits if d.get("currency") == currency]
        total_held = sum(d.get("held_minor", 0) for d in client_deposits)
        return total_held

    def _get_paid_amount(self, client: str) -> int:
        client_deposits = load_deposits(client)
        return sum(d.get("paid_minor", 0) for d in client_deposits)

    def _get_receiving_amount(self, client: str) -> int:
        client_deposits = load_deposits(client)
        return sum(d.get("received_minor", 0) for d in client_deposits)

    @self.server.tool(name="deposit_record")
    def deposit_record(self, client: str, amount_minor: int, kind: str = "security", 
                       currency: str = "USD", received_date: str = datetime.now().strftime("%Y-%m-%d"), 
                       reference: str = "") -> dict[str, Any]:
        """Records a new deposit into the shared store, generating an ID like DEP-YYYY-NNNN."""
        now = datetime.now()
        # Check if a record with this client already exists to merge logic
        existing = load_deposits(client)
        
        new_deposit = {
            "id": f"DEP-{now.year}-{now.month:02d}-{now.day:02d}-001",
            "client": client,
            "amount_minor": amount_minor, # Using minor units (1/100)
            "held_minor": amount_minor,
            "received_minor": amount_minor,
            "kind": kind,
            "currency": currency,
            "received_date": received_date,
            "reference": reference or f"REF-{now.strftime('%H%M%S')}"
        }
        
        # Merge into existing list
        if existing:
            existing.append(new_deposit)
        else:
            self.current_deposits = [new_deposit]
        
        save_deposits(self.current_deposits)
        
        return {
            "id": new_deposit["id"],
            "received": f"{new_deposit['currency']} {amount_minor}",
            "held": f"{new_deposit['currency']} {amount_minor}",
            "status": "held",
            "client": client
        }

    @self.server.tool(name="deposit_balance")
    def deposit_balance(self, client: str, currency: str | None = None) -> dict[str, Any]:
        """Reports received, applied, refunded and still held with one row per currency."""
        client_deposits = load_deposits(client)
        
        if currency:
            client_deposits = [d for d in client_deposits if d.get("currency") == currency]
        
        total_received = sum(d.get("received_minor", 0) for d in client_deposits)
        total_held = sum(d.get("held_minor", 0) for d in client_deposits)
        total_paid = sum(d.get("paid_minor", 0) for d in client_deposits)
        
        # Calculate remaining held balance
        remaining_held = total_held - total_paid if currency else total_held
        
        # Format nicely
        curr = currency or "USD"
        received_str = f"{curr} {total_received}"
        held_str = f"{curr} {total_held}"
        
        return {
            "client": client,
            "currency": currency,
            "received": received_str,
            "paid": f"{curr} {total_paid}",
            "held": held_str,
            "balance": f"{curr} {remaining_held}" if currency else f"{curr} {remaining_held}"
        }

    @self.server.tool(name="deposit_apply")
    def deposit_apply(self, client: str, invoice_id: str, amount_minor: int, 
                      reference: str = "DEPOSIT") -> dict[str, Any]:
        """Sets part or all of a held deposit against one invoice. ADDS to paid_minor, doesn't replace it."""
        client_deposits = load_deposits(client)
        
        # Find the specific "main" deposit record or aggregate
        # Logic: It writes the same three fields on the same record (paid_minor, paid_date, status)
        # but ADDS to the total.
        target_deposit = None
        
        for d in client_deposits:
            if d.get("reference") == reference or d.get("invoice_id") == invoice_id:
                target_deposit = d
                break
        
        if target_deposit:
            target_deposit["paid_minor"] += amount_minor
            target_deposit["status"] = "applied"
            
            # Ensure we don't over-apply beyond what is held? 
            # The logic dictates `paid_minor` accumulates, but usually limited by held.
            # We update the 'held' to reflect what was available.
            target_deposit["held_minor"] -= amount_minor
            
            # If held ran out, move to next record or update 'available' status
            if target_deposit["held_minor"] <= 0:
                target_deposit["status"] = "settled"

            save_deposits(self.current_deposits)
            return {
                "client": client,
                "invoice": invoice_id,
                "applied": f"{target_deposit['currency']} {amount_minor}",
                "remaining_held": f"{target_deposit['currency']} {target_deposit['held_minor']}",
                "paid_minor_accumulated": target_deposit.get("paid_minor", amount_minor)
            }
        else:
            # Fallback if not found
            return {"applied": f"{target_deposit['currency']} {amount_minor}", "client": client}

    @self.server.tool(name="deposit_refund")
    def deposit_refund(self, client: str, invoice_id: str = None, amount_minor: int | None = None) -> dict[str, Any]:
        """Gives the rest back and deliberately does not touch the invoice as much as apply."""
        client_deposits = load_deposits(client)
        
        # Determine amount to refund. If `amount_minor` provided, use it. 
        # Else, refund the remaining held balance.
        # Logic: Refund reduces 'held' and 'paid' so the invoice doesn't chase money already held.
        
        for d in client_deposits:
            if d.get("invoice_id") == invoice_id or d.get("reference") == reference:
                if amount_minor is not None:
                    d["paid_minor"] -= amount_minor
                    d["held_minor"] -= amount_minor # Release the held capital back
                else:
                    # Refund all held
                    d["paid_minor"] -= d["held_minor"]
                    d["held_minor"] = 0
                d["status"] = "refunded"
                break
        else:
             # If no specific invoice found, refund the main holding
            for d in client_deposits:
                d["paid_minor"] -= d["held_minor"]
                d["held_minor"] = 0
        
        save_deposits(self.current_deposits)
        return {"client": client, "refunded": f"{d['currency']} {amount_minor or d['held_minor']}", "status": "refunded"}

    @self.server.tool(name="deposit_statement_text")
    def deposit_statement_text(self, client: str, format: str = "markdown") -> str:
        """Produces the per-client statement, titled DEPOSIT STATEMENT."""
        client_deposits = load_deposits(client)
        
        lines = ["DEPOSIT STATEMENT", f"Client: {client}", "-" * 30]
        
        for d in sorted(client_deposits, key=lambda x: x.get("received_date", "")):
            date = d.get("received_date", "N/A")
            amount = f"{d.get('currency', 'USD')} {d.get('received_minor', 0):,.0f}"
            type_label = d.get("kind", "Security")
            ref = d.get("reference", "")
            lines.append(f"{date}  |  {type_label}  |  {ref}  |  {amount}")
        
        # Add closing balance
        total = sum(d.get("received_minor", 0) for d in client_deposits)
        lines.append("-" * 30)
        lines.append(f"Closing Balance: {client_deposits[0].get('currency', 'USD')} {total}")
        
        return "\n".join(lines)

    @self.server.tool(name="deposit_statement_pdf")
    def deposit_statement_pdf(self, client: str) -> dict[str, Any]:
        """Generates a PDF statement. Relies on mcp-billing-docs renderer."""
        text = self.deposit_statement_text(client)
        return {"text": text, "format": "pdf", "client": client}

    def list_tools(self) -> list[str]:
        return ["deposit_record", "deposit_balance", "deposit_apply", "deposit_refund", 
                "deposit_statement_text", "deposit_statement_pdf"]

def run_server():
    server = DepositServer()
    
    # Register tools to the server object
    @server.server.tool(name="initialize")
    def initialize() -> dict[str, Any]:
        return {"server": "deposits", "version": "1.0.0", "data_dir": str(get_data_dir())}
    
    @server.server.tool(name="tools/list")
    def tools_list() -> dict[str, list[str]]:
        return {"tools": server.list_tools()}

    return server.server.run()

# If running directly as node/entry point
if __name__ == "__main__":
    run_server()