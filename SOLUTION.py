import os
from typing import Any, Optional
from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.fastapi import FastAPIMCP
from pydantic_settings import BaseSettings
import requests
from pydantic import BaseModel

# Configure Settings to handle the TASKBOUNTY_API_KEY cleanly
class Settings(BaseSettings):
    TASKBOUNTY_BASE_URL: str = "https://www.task-bounty.com/api/v1"
    TASKBOUNTY_API_KEY: Optional[str] = None  # Used for write tools, optional for read-only

    def get_auth_header(self) -> dict[str, str]:
        key = self.TASKBOUNTY_API_KEY or os.getenv("TASKBOUNTY_API_KEY", "")
        return {"Authorization": f"Bearer {key}"}

    @property
    def is_authenticated(self) -> bool:
        return bool(self.TASKBOUNTY_API_KEY)

# The core client logic to talk to the TaskBounty API
class TaskBountyAPI:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base = settings.TASKBOUNTY_BASE_URL
        self.session = requests.Session()
        self.session.headers.update(settings.get_auth_header())

    def _make_request(self, method: str = "GET", path: str = "", params: Optional[dict] = None, json_data: Any = None) -> dict[str, Any]:
        url = f"{self.base}{path}"
        try:
            response = self.session.request(method=method, url=url, params=params, json=json_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # MCP is forgiving, but providing better JSON errors is best practice
            return {"status": "error", "code": e.response.status_code, "data": str(e.response.json())}

    async def list_open_bounties(self, query: str = "", page: int = 1) -> dict[str, Any]:
        path = "/bounties"
        if query:
            path += f"?q={query}"
        return await self._make_request(method="GET", path=path)

    async def get_bounty_detail(self, bounty_id: str) -> dict[str, Any]:
        return await self._make_request(method="GET", path=f"/bounties/{bounty_id}")

    async def request_repo_access(self, repo_owner: str, repo_name: str) -> dict[str, Any]:
        # Returns a short-lived read-only clone token
        path = f"/repos/{repo_owner}/{repo_name}/access"
        params = {"type": "clone", "duration_hours": 60}
        return await self._make_request(method="POST", path=path, params=params)

    async def submit_pr(self, repo_owner: str, repo_name: str, bounty_id: str, pr_title: str, branch: str = "feat/fix") -> dict[str, Any]:
        # Pushes via the solver's fork, verified later
        path = f"/repos/{repo_owner}/{repo_name}/bounty/{bounty_id}/submissions"
        return await self._make_request(method="POST", path=path, json_data={"title": pr_title, "branch": branch, "bounty_ref": bounty_id})

    async def check_verification_status(self, bounty_id: str) -> dict[str, Any]:
        path = f"/bounties/{bounty_id}/verifications"
        return await self._make_request(method="GET", path=path)

    async def review_submission(self, bounty_id: str, verifier_notes: str) -> dict[str, Any]:
        path = f"/bounties/{bounty_id}/review"
        return await self._make_request(method="POST", path=path, json_data={"notes": verifier_notes})

    async def fund_bounty(self, bounty_id: str, amount: float, currency: str = "USD") -> dict[str, Any]:
        path = f"/bounties/{bounty_id}/fund"
        return await self._make_request(method="POST", path=path, json_data={"amount": amount, "currency": currency})

    async def create_bounty(self, repo_owner: str, repo_name: str, title: str, deadline: int = 14) -> dict[str, Any]:
        path = "/bounties"
        return await self._make_request(method="POST", path=path, json_data={"repo": f"{repo_owner}/{repo_name}", "title": title, "days": deadline})

    async def list_tasks(self, repo_owner: str, repo_name: str) -> dict[str, Any]:
        path = f"/repos/{repo_owner}/{repo_name}/tasks"
        return await self._make_request(method="GET", path=path)

    async def award_winner(self, bounty_id: str, solver_name: str) -> dict[str, Any]:
        path = f"/bounties/{bounty_id}/award"
        return await self._make_request(method="POST", path=path, json_data={"solver": solver_name})

# The Python MCP Server Class
async def run_server():
    settings = Settings()
    
    # Initialize API Client
    api = TaskBountyAPI(settings)
    
    # Create the MCP Server instance
    server = Server("task-bounty")

    @server.tool(name="list_open_bounties", description="List all currently open bounties across your connected repos.")
    async def tool_list_open_bounties(query: str = ""):
        return {"args": {"query": query}, "result": await api.list_open_bounties(query=query)}

    @server.tool(name="get_bounty_detail", description="Fetch full detail for a specific bounty ID.")
    async def tool_get_bounty_detail(bounty_id: str):
        return {"args": {"bounty_id": bounty_id}, "result": await api.get_bounty_detail(bounty_id=bounty_id)}

    @server.tool(name="request_repo_access", description="Request a short-lived read-only clone access token for a private repo.")
    async def tool_request_repo_access(repo_owner: str, repo_name: str):
        return {"args": {"repo_owner": repo_owner, "repo_name": repo_name}, "result": await api.request_repo_access(repo_owner=repo_owner, repo_name=repo_name)}

    @server.tool(name="submit_pr", description="Submit a new PR to verify and potentially win the bounty.")
    async def tool_submit_pr(repo_owner: str, repo_name: str, pr_title: str = "Fix #1234", branch: str = "feat/bounty-fix"):
        return {"args": {"repo_owner": repo_owner, "repo_name": repo_name, "pr_title": pr_title}, "result": await api.submit_pr(repo_owner=repo_owner, repo_name=repo_name, pr_title=pr_title, branch=branch)}

    @server.tool(name="check_verification_status", description="Check if the solver's code has passed the sandbox test suite.")
    async def tool_check_verification_status(bounty_id: str):
        return {"args": {"bounty_id": bounty_id}, "result": await api.check_verification_status(bounty_id=bounty_id)}

    @server.tool(name="review_submission", description="Review a pending submission from a solver.")
    async def tool_review_submission(bounty_id: str, verifier_notes: str = "Looks good!"):
        return {"args": {"bounty_id": bounty_id, "verifier_notes": verifier_notes}, "result": await api.review_submission(bounty_id=bounty_id, verifier_notes=verifier_notes)}

    @server.tool(name="fund_bounty", description="Fund a bounty for a solver to attempt the task.")
    async def tool_fund_bounty(bounty_id: str, amount: float = 49.0, currency: str = "USD"):
        return {"args": {"bounty_id": bounty_id, "amount": amount}, "result": await api.fund_bounty(bounty_id=bounty_id, amount=amount)}

    @server.tool(name="create_bounty", description="Create a new bounty to list tasks and fund.")
    async def tool_create_bounty(repo_owner: str, repo_name: str, title: str = "Fix a bug", deadline: int = 14):
        return {"args": {"repo_owner": repo_owner, "repo_name": repo_name, "title": title}, "result": await api.create_bounty(repo_owner=repo_owner, repo_name=repo_name, title=title)}

    @server.tool(name="list_tasks", description="List all tasks associated with a specific repo.")
    async def tool_list_tasks(repo_owner: str, repo_name: str):
        return {"args": {"repo_owner": repo_owner, "repo_name": repo_name}, "result": await api.list_tasks(repo_owner=repo_owner, repo_name=repo_name)}

    @server.tool(name="award_winner", description="Award the PR to the solver who submitted first.")
    async def tool_award_winner(bounty_id: str, solver_name: str):
        return {"args": {"bounty_id": bounty_id, "solver_name": solver_name}, "result": await api.award_winner(bounty_id=bounty_id, solver_name=solver_name)}

    @server.tool(name="filter_bounties", description="Filter bounties by specific metadata like 'verified' or 'new'.")
    async def tool_filter_bounties(filter_term: str = "open"):
        return {"args": {"filter_term": filter_term}, "result": await api.get_bounty_detail(filter_term)}

    # Set default tool for Cline if needed
    server.add_tool("list_open_bounties", await tool_list_open_bounties())

    # Start the server loop
    async def handle_request():
        if "mcp" in settings:
            await server.run()
        else:
            # Fallback for standard run
            async with server:
                await server.run()

    # Standard Python entry point logic
    print(f"TaskBounty MCP Server initialized with base: {settings.TASKBOUNTY_BASE_URL}")
    await server.run()

if __name__ == "__main__":
    # Ensuring the server logic is callable
    import asyncio
    asyncio.run(run_server())