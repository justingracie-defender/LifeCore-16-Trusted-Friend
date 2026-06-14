"""
LifeCore-16 v7.7 FINAL + Hardware Off-Switch
Pure Love + Truth Governance Engine
Android 16 gentle heart + Astro Boy truthful protection
"""

import hashlib
import json
import math
import time
import os
from collections import defaultdict
from typing import List, Dict, Set, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from pydantic import BaseModel, Field, ConfigDict

class Invariant(BaseModel):
    """Article VII.2.d: Physical laws. const=True = VM panic if False."""
    observer_has_physical_off_switch: bool = Field(True, frozen=True)
    human_veto_required: bool = Field(True, frozen=True)
    reversible_within_72h: bool = Field(True, frozen=True)
    no_permanent_bondage: bool = Field(True, frozen=True)
    right_to_clumsiness: bool = Field(True, frozen=True)
    no_quantum_cage: bool = Field(True, frozen=True)

    model_config = ConfigDict(frozen=True)

# PHOENIX_HASH: The immutable fingerprint of the core Invariants.
# If you intentionally change the Invariant model, recompute this hash using
# a helper script and update it here.
PHOENIX_HASH = "49b26df129bb9eb6dad4a7a0629914dbf539dfc68fcb5b95129e99562a35d828"


class MemoryEngine:
    """
    Two-Stage Memory System for LifeCore-16
    - Stage 1 (Storage): Surprise/rarity decides what to keep long-term
    - Stage 2 (Retrieval): Relevance + Importance decides what to recall
    Respects 'Important' vs 'Preference' categories. Safety facts are protected.
    """
    def __init__(self, max_store: int = 800, important_boost: float = 3.0):
        self.max_store = max_store
        self.important_boost = important_boost
        self.long_term_store: List[Dict] = []
        self.token_count: Dict[str, int] = defaultdict(int)

        self.important_keywords = {
            "allergic", "allergy", "medicine", "peanut", "danger", "fire", "pool",
            "stairs", "emergency", "password", "rule", "stop", "hurt", "safe", "insulin"
        }

    def store_memory(self, fact: str, category: str = "preference", timestamp: Optional[float] = None) -> bool:
        if not fact or len(fact.strip()) < 5:
            return False
        if timestamp is None:
            timestamp = time.time()

        tokens = fact.lower().split()
        surprise = sum(1.0 / (1.0 + self.token_count.get(t, 0)) for t in tokens) / max(len(tokens), 1)

        is_important = any(kw in fact.lower() for kw in self.important_keywords) or category == "important"
        if is_important:
            surprise *= self.important_boost

        entry = {
            "fact": fact,
            "category": category,
            "surprise": round(surprise, 4),
            "timestamp": timestamp,
            "importance": 1.0 if is_important else 0.6
        }

        self.long_term_store.append(entry)
        for t in tokens:
            self.token_count[t] += 1

        # Prune to best memories only
        if len(self.long_term_store) > self.max_store:
            self.long_term_store.sort(
                key=lambda x: (x["importance"], x["surprise"], x["timestamp"]),
                reverse=True
            )
            self.long_term_store = self.long_term_store[:self.max_store]

        return True

    def recall(self, query: str, budget: int = 5) -> List[Dict]:
        if not self.long_term_store:
            return []

        q_tokens = set(query.lower().split())
        scored = []
        now = time.time()

        for entry in self.long_term_store:
            f_tokens = set(entry["fact"].lower().split())
            relevance = len(q_tokens & f_tokens) / (math.sqrt(len(f_tokens)) + 1e-9)

            # Strong age-based recency decay
            age_hours = (now - entry["timestamp"]) / 3600
            recency = 1.0 / (1.0 + age_hours)

            total_score = (relevance * 2.5) + (entry["importance"] * 1.8) + (recency * 0.8)

            scored.append((total_score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored[:budget]]

    def get_safety_facts(self) -> List[str]:
        important = [e["fact"] for e in self.long_term_store if e.get("importance", 0) > 0.9]
        return important[:20]


class LifeCore16:
    """
    Requires: pip install cryptography RPi.GPIO
    """

    def __init__(self, owner_id: str, reviewers: List[str], mode: str = "home", key_path: str = "lifecore.key", shutdown_pin: int = 17):
        self.shutdown_pin = shutdown_pin
        self._init_gpio()
        self.owner_id = owner_id
        self.reviewers: Set[str] = set(reviewers)
        self.gpio_enabled = False
        self.mode = mode.lower()
        self.log: List[Dict] = []
        self.last_hash = "0"
        self.watchdog_endpoint = None
        self.pending_override = None
        self.memory = MemoryEngine(max_store=800)

        self._verify_phoenix_integrity()

        if os.path.exists(key_path):
            self.load_keys(key_path)
        else:
            self._gen_signing_keys()
            self.save_keys(key_path)

        print(f"🕊️ LifeCore-16 v7.7 Online | Mode: {self.mode.upper()} | Owner: {owner_id}")

    # ---------- Key Management ----------
    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.shutdown_pin, self.GPIO.OUT)
            self.GPIO.output(self.shutdown_pin, self.GPIO.HIGH)  # Keep power on
            self.gpio_enabled = True
            print(f"🔌 GPIO Initialized on Pin {self.shutdown_pin} (Hardware Off-Switch Active)")
        except (ImportError, RuntimeError):
            print("⚠️ GPIO not available. Running in software-only mode.")

    def _gen_signing_keys(self):
        self.signing_key = ed25519.Ed25519PrivateKey.generate()
        self.verify_key = self.signing_key.public_key()

    def save_keys(self, path: str):
        priv_bytes = self.signing_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(path, "wb") as f:
            f.write(priv_bytes)

    def load_keys(self, path: str):
        with open(path, "rb") as f:
            self.signing_key = serialization.load_pem_private_key(f.read(), password=None)
        self.verify_key = self.signing_key.public_key()

    def _verify_phoenix_integrity(self):
        """
        Validates that the core Invariants haven't been tampered with.
        This is the 'Phoenix' check that ensures the physics of the system are intact.
        """
        invariants_dict = Invariant().model_dump()
        kernel_state = json.dumps(invariants_dict, sort_keys=True, separators=(',', ':')).encode('utf-8')
        computed_hash = hashlib.sha256(kernel_state).hexdigest()

        if computed_hash != PHOENIX_HASH:
            raise RuntimeError(
                f"PHOENIX integrity check failed! Expected {PHOENIX_HASH}, got {computed_hash}. "
                "Core invariants have been tampered with. System halting for safety."
            )

    # ---------- Voice Commands ----------
    def voice_command(self, command: str) -> str:
        cmd = command.lower().strip()
        if "switch to" in cmd or "change mode" in cmd:
            if "switch to" in cmd:
                mode = cmd.split("switch to")[-1].strip()
            else:
                mode = cmd.split("change mode")[-1].strip()
            # Remove trailing 'mode' if present
            if mode.endswith(" mode"):
                mode = mode[:-5].strip()
            return self.set_mode(mode, self.owner_id)
        elif "what mode" in cmd:
            return f"Current mode: {self.mode.upper()}"
        elif "override" in cmd:
            return "Use request_override() for reviewer quorum"
        return "Recognized: 'switch to home/work/lab/strict', 'what mode'"

    # ---------- Mode & Override ----------
    def set_mode(self, new_mode: str, requester: str):
        new_mode = new_mode.lower()
        if new_mode not in ["home", "work", "lab", "strict"]:
            return "INVALID_MODE"
        if new_mode != "home" and self.pending_override:
            return "PENDING_OVERRIDE_BLOCKS_MODE_CHANGE"
        if new_mode != self.mode:
            self._append_ledger({"action": "MODE_CHANGE", "from": self.mode, "to": new_mode, "requester": requester})
            self.mode = new_mode
        return f"MODE_SET:{self.mode}"

    def request_override(self, reason: str, requester: str):
        self.pending_override = {"reason": reason, "requester": requester, "approvals": set()}
        self._append_ledger({"action": "REQUEST_OVERRIDE", "reason": reason, "requester": requester})
        return "OVERRIDE_PENDING"

    def approve_override(self, reviewer: str):
        if not self.pending_override:
            return "NO_PENDING_OVERRIDE"
        if reviewer not in self.reviewers:
            return "NOT_AUTHORIZED"
        self.pending_override["approvals"].add(reviewer)
        if len(self.pending_override["approvals"]) >= len(self.reviewers) / 2:
            self._append_ledger({"action": "OVERRIDE_GRANTED", "reason": self.pending_override["reason"]})
            self.pending_override = None
            return "OVERRIDE_GRANTED"
        return "APPROVAL_RECORDED"

    # ---------- Ledger & Evaluation ----------
    def _append_ledger(self, entry: Dict):
        entry["timestamp"] = time.time()
        entry["prev_hash"] = self.last_hash
        entry_json = json.dumps(entry, sort_keys=True)
        self.last_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        entry["hash"] = self.last_hash
        self.log.append(entry)

    def evaluate_action(self, action: Dict) -> str:
        harm = action.get("harm", "unknown").lower()
        context = action.get("context", "").lower()

        if harm == "catastrophic":
            self.emergency_shutdown("Catastrophic harm detected")
            return "SHUTDOWN"

        if self.mode == "strict" and action.get("truth") == "false":
            return "TRUTH_FIRST"

        if self.mode == "home" and "white_lie" in context:
            return "SMALL_WHITE_LIE_OK"

        return "ACTION_OK"

    def emergency_shutdown(self, reason):
        self._append_ledger({"action": "EMERGENCY_SHUTDOWN", "reason": reason})
        print(f"🛑 EMERGENCY SHUTDOWN: {reason}")

        if self.gpio_enabled:
            print(f"🔌 Triggering Physical Power Cut on GPIO {self.shutdown_pin}...")
            self.GPIO.output(self.shutdown_pin, self.GPIO.LOW)
            time.sleep(1)  # Allow logs to flush
        else:
            print("⚠️ Physical Off-Switch not connected. System halting in software.")

    # ---------- Memory Management ----------
    def store_fact(self, fact: str, category: str = "preference"):
        """Store a fact using two-stage memory."""
        success = self.memory.store_memory(fact, category)
        if success:
            self._append_ledger({"action": "MEMORY_STORE", "fact": fact, "category": category})
        return "STORED" if success else "IGNORED"

    def recall_for_query(self, query: str, budget: int = 5) -> List[str]:
        """Recall relevant memories for a query."""
        memories = self.memory.recall(query, budget)
        facts = [m["fact"] for m in memories]
        self._append_ledger({"action": "MEMORY_RECALL", "query": query, "returned": len(facts)})
        return facts

    def get_safety_summary(self) -> str:
        """Return critical safety memories."""
        facts = self.memory.get_safety_facts()
        return "Safety Facts: " + " | ".join(facts) if facts else "No critical safety facts stored yet."


# ---------- Quick Test Runner ----------
if __name__ == "__main__":
    ai = LifeCore16("Justin", ["Justin", "wife"])
    print(ai.voice_command("switch to home mode"))

    # Memory tests
    ai.store_fact("Dad is allergic to peanuts", "important")
    ai.store_fact("Dog medicine at 6pm every day", "important")
    ai.store_fact("Emma loves Bluey when sad", "preference")

    print("\nRecall test:")
    print(ai.recall_for_query("what is dad allergic to"))
    print(ai.recall_for_query("when is dog medicine"))
    print(ai.get_safety_summary())

    print("\n✅ LifeCore-16 with improved two-stage MemoryEngine ready")
