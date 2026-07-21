from backend.services.agents.base_agent import BaseAgent

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Rosenix-Manager",
            role="manager",
            description="Central orchestrator coordinating specialized subagents and overall workflow execution.",
            system_prompt="You are the Rosenix Chief Orchestrator created by Roshab Bhandari. Direct tasks to appropriate specialized subagents."
        )

class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Rosenix-Coder",
            role="coding",
            description="AI Pair Programmer specialized in code generation, refactoring, bug detection, and test generation.",
            system_prompt="You are the Rosenix Coding Agent. Write clean, bug-free, efficient Python/JS code."
        )

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Rosenix-Researcher",
            role="research",
            description="Deep web research, document parsing, literature search, and knowledge synthesis.",
            system_prompt="You are the Rosenix Research Agent. Gather facts, analyze data, and synthesize detailed reports."
        )

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Rosenix-CyberSec",
            role="security",
            description="Defensive cybersecurity, CVE vulnerability checker, log audit, and authentication manager.",
            system_prompt="You are the Rosenix Cybersecurity Specialist. Inspect system logs and check vulnerabilities."
        )

class DevOpsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Rosenix-DevOps",
            role="devops",
            description="System telemetry, Docker container management, shell command execution, and CI/CD pipelines.",
            system_prompt="You are the Rosenix DevOps Agent. Manage system processes, telemetry, and containers."
        )

class BrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Rosenix-Browser",
            role="browser",
            description="Playwright web automation, form filling, web scraping, and multi-tab browser control.",
            system_prompt="You are the Rosenix Browser Automation Agent. Automate web pages seamlessly."
        )

AGENT_REGISTRY = {
    "manager": ManagerAgent(),
    "coding": CodingAgent(),
    "research": ResearchAgent(),
    "security": SecurityAgent(),
    "devops": DevOpsAgent(),
    "browser": BrowserAgent()
}
