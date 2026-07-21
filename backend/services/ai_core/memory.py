import time
import json
import os
from typing import Dict, Any, List, Optional

class MemoryEngine:
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        
        self.short_term_memory: List[Dict[str, Any]] = []
        self.long_term_memory: List[Dict[str, Any]] = self._load_json("long_term.json")
        self.episodic_memory: List[Dict[str, Any]] = self._load_json("episodic.json")
        self.user_preferences: Dict[str, Any] = self._load_json("preferences.json", default={"voice_enabled": True, "theme": "dark_cyber", "default_agent": "manager"})

    def _load_json(self, filename: str, default: Any = None) -> Any:
        file_path = os.path.join(self.storage_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return default if default is not None else []

    def _save_json(self, filename: str, data: Any):
        file_path = os.path.join(self.storage_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Memory Engine] Error saving {filename}: {e}")

    def add_short_term(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        entry = {
            "timestamp": time.time(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.short_term_memory.append(entry)
        # Keep last 50 turns in short-term buffer
        if len(self.short_term_memory) > 50:
            self.short_term_memory.pop(0)

    def add_long_term_fact(self, key: str, value: Any, category: str = "general"):
        fact = {
            "key": key,
            "value": value,
            "category": category,
            "timestamp": time.time()
        }
        self.long_term_memory.append(fact)
        self._save_json("long_term.json", self.long_term_memory)

    def record_episode(self, goal: str, steps: List[Dict[str, Any]], outcome: str, success: bool):
        episode = {
            "id": f"ep_{int(time.time()*1000)}",
            "timestamp": time.time(),
            "goal": goal,
            "steps_taken": len(steps),
            "outcome": outcome,
            "success": success
        }
        self.episodic_memory.append(episode)
        self._save_json("episodic.json", self.episodic_memory)

    def get_context_summary(self) -> Dict[str, Any]:
        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_facts_count": len(self.long_term_memory),
            "episodic_count": len(self.episodic_memory)
        }

    def get_memory_stats(self) -> Dict[str, int]:
        return {
            "short_term_entries": len(self.short_term_memory),
            "long_term_facts": len(self.long_term_memory),
            "episodic_episodes": len(self.episodic_memory),
            "user_preferences": len(self.user_preferences)
        }

memory_engine = MemoryEngine(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "storage", "memory"))
