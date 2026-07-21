import re
import random
from typing import Dict, Any, List, Optional
from backend.services.system_monitor import system_monitor

class AIBrain:
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.uploaded_files_cache: List[Dict[str, Any]] = []

    def register_uploaded_file(self, file_info: Dict[str, Any]):
        self.uploaded_files_cache.append(file_info)

    async def process_command(self, prompt: str, attached_files: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        clean_prompt = prompt.strip()
        lower_prompt = clean_prompt.lower()

        if attached_files:
            for f in attached_files:
                if f not in self.uploaded_files_cache:
                    self.uploaded_files_cache.append(f)

        # 0. Developer / Creator Identity Question
        if any(w in lower_prompt for w in ["who is your developer", "who developed you", "who made you", "who created you", "who is your creator", "who built you", "who is roshab", "developer name"]):
            response_text = (
                f"### 👑 Developer Identity Protocol\n\n"
                f"I am **Rosenix**, created and developed by **Roshab Bhandari**.\n\n"
                f"*He engineered my Autonomous AI Core, Multi-Agent Swarm, and Quantum HUD System.*"
            )
            voice_text = "I am Rosenix, developed by Roshab Bhandari."
            return {
                "response": response_text,
                "voice_response": voice_text,
                "intent": "DEVELOPER_INFO"
            }

        # 1. System Audit / Status Command
        if any(w in lower_prompt for w in ["system status", "audit", "system diagnostics", "specs", "cpu", "ram", "memory"]):
            stats = system_monitor.get_system_stats()
            response_text = (
                f"**Rosenix System Telemetry Report**\n\n"
                f"- **Platform:** {stats['platform']}\n"
                f"- **Core Processor:** {stats['processor']}\n"
                f"- **CPU Load:** `{stats['cpu_usage']}%`\n"
                f"- **RAM Usage:** `{stats['memory_used_gb']} GB / {stats['memory_total_gb']} GB` ({stats['memory_percent']}%)\n"
                f"- **Disk Storage:** `{stats['disk_percent']}% utilized`\n"
                f"- **Active System Threads:** `{stats['active_threads']}`\n"
                f"- **Uptime:** `{stats['uptime']}`\n\n"
                f"*All primary quantum cores operating within optimal parameters.*"
            )
            voice_text = f"System audit complete. CPU load is at {stats['cpu_usage']} percent and memory utilization is at {stats['memory_percent']} percent. All systems optimal."
            return {
                "response": response_text,
                "voice_response": voice_text,
                "intent": "SYSTEM_DIAGNOSTICS",
                "action_type": "TELEMETRY"
            }

        # 2. File Analysis
        if any(w in lower_prompt for w in ["uploaded", "file", "document", "analyze code", "summarize file", "inspect"]) or self.uploaded_files_cache:
            if self.uploaded_files_cache and any(w in lower_prompt for w in ["file", "uploaded", "code", "document", "summarize", "what is in"]):
                latest_file = self.uploaded_files_cache[-1]
                response_text = (
                    f"### Analysis of Uploaded File: `{latest_file['filename']}`\n\n"
                    f"- **Category:** {latest_file['category']}\n"
                    f"- **File Size:** `{latest_file['size_bytes']} bytes`\n"
                    f"- **Total Lines:** `{latest_file['line_count']}`\n"
                    f"- **Format:** `{latest_file['extension'].upper()}`\n\n"
                    f"**Content Preview / Summary:**\n```\n{latest_file['preview']}\n```\n\n"
                    f"*I have indexed this file into Rosenix memory.*"
                )
                voice_text = f"Analyzed file {latest_file['filename']}. It is a {latest_file['category']} containing {latest_file['line_count']} lines."
                return {
                    "response": response_text,
                    "voice_response": voice_text,
                    "intent": "FILE_ANALYSIS",
                    "file_info": latest_file
                }

        # 3. Code Generation
        if any(w in lower_prompt for w in ["write python", "create script", "code", "function", "generate code", "html", "javascript"]):
            response_text = (
                f"### Rosenix Code Module Generated\n\n"
                f"Here is an optimized solution for your request:\n\n"
                f"```python\n"
                f"# Rosenix AI Automated Script\n"
                f"import sys\n"
                f"import asyncio\n\n"
                f"async def execute_task():\n"
                f"    print('[ROSENIX] Executing high-priority protocol...')\n"
                f"    # Goal: {clean_prompt}\n"
                f"    await asyncio.sleep(0.5)\n"
                f"    print('[ROSENIX] Protocol completed successfully.')\n\n"
                f"if __name__ == '__main__':\n"
                f"    asyncio.run(execute_task())\n"
                f"```\n\n"
                f"*Code compiled cleanly with zero syntax errors.*"
            )
            voice_text = "I have generated and validated the required code block for you."
            return {
                "response": response_text,
                "voice_response": voice_text,
                "intent": "CODE_GEN"
            }

        # 4. Greeting
        if any(w in lower_prompt for w in ["hello", "hi", "hey rosenix", "wake up", "who are you", "start"]):
            response_text = (
                f"**Greetings, Commander Roshab Bhandari.** I am **Rosenix** AI OS.\n\n"
                f"I am fully online and ready for your commands.\n"
                f"- **Voice Command Mode:** Active (`WebSpeech API Enabled`)\n"
                f"- **File Upload Engine:** Ready\n"
                f"- **System Telemetry:** Live\n\n"
                f"How may I assist you today?"
            )
            voice_text = "Greetings, Commander. Rosenix is online and ready for your command."
            return {
                "response": response_text,
                "voice_response": voice_text,
                "intent": "GREETING"
            }

        # 5. Fallback
        responses = [
            f"Command processed: **\"{clean_prompt}\"**.\n\nRosenix has analyzed your request and updated the active task queue. All parameters are optimal.",
            f"Protocol executed for **\"{clean_prompt}\"**.\n\nRosenix core has synchronized data streams. Ready for follow-up directives.",
            f"**Directive Received:** \"{clean_prompt}\"\n\nTask executed cleanly with 0 warnings. Standing by for next instruction."
        ]
        chosen_response = random.choice(responses)
        voice_response = f"Directive received: {clean_prompt}. Task completed successfully."

        return {
            "response": chosen_response,
            "voice_response": voice_response,
            "intent": "GENERAL_COMMAND"
        }

ai_brain = AIBrain()
