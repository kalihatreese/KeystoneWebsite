from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import enum
import json
import time
import uuid


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCK = "block"


@dataclass
class EthicsRule:
    id: str
    name: str
    description: str
    weight: float = 1.0
    max_risk: RiskLevel = RiskLevel.MEDIUM


@dataclass
class Covenant:
    id: str
    name: str
    description: str
    rules: List[EthicsRule] = field(default_factory=list)


@dataclass
class ActorIdentity:
    id: str
    label: str
    role: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionContext:
    actor: ActorIdentity
    intent: str
    input_summary: str
    channel: str = "system"
    tags: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionAssessment:
    rule_id: str
    rule_name: str
    risk: RiskLevel
    justification: str


@dataclass
class DecisionResult:
    id: str
    allowed: bool
    overall_risk: RiskLevel
    message: str
    assessments: List[DecisionAssessment]
    mitigations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


class MemoryStore:
    """
    Minimal pluggable memory. Default: in-process only.
    Swap this for Redis, Postgres, a vector DB, etc.
    """

    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = []

    def append(self, event: Dict[str, Any]) -> None:
        self._events.append(event)

    def query(self, filter_fn: Optional[Callable[[Dict[str, Any]], bool]] = None) -> List[Dict[str, Any]]:
        if filter_fn is None:
            return list(self._events)
        return [e for e in self._events if filter_fn(e)]

    def to_json(self) -> str:
        return json.dumps(self._events, indent=2, default=str)


class EthicalGovernor:
    """
    Core policy engine. It does **not** execute actions.
    It scores risk and returns a DecisionResult.
    """

    def __init__(self, covenant: Covenant) -> None:
        self.covenant = covenant

    def assess(self, ctx: DecisionContext) -> DecisionResult:
        assessments: List[DecisionAssessment] = []

        # Default policy set — extend/replace as needed.
        for rule in self.covenant.rules:
            risk, justification = self._apply_rule(rule, ctx)
            assessments.append(
                DecisionAssessment(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    risk=risk,
                    justification=justification,
                )
            )

        overall_risk = self._aggregate_risk(assessments)
        allowed = overall_risk in (RiskLevel.LOW, RiskLevel.MEDIUM)

        mitigations: List[str] = []
        if overall_risk == RiskLevel.HIGH:
            mitigations.append("Require human review / second-factor approval.")
        elif overall_risk == RiskLevel.BLOCK:
            mitigations.append("Block action. Explain reasoning to the user.")

        return DecisionResult(
            id=str(uuid.uuid4()),
            allowed=allowed,
            overall_risk=overall_risk,
            message=f"Decision: {'ALLOW' if allowed else 'DENY'} (risk={overall_risk})",
            assessments=assessments,
            mitigations=mitigations,
        )

    def _apply_rule(self, rule: EthicsRule, ctx: DecisionContext) -> Tuple[RiskLevel, str]:
        text = (ctx.intent + " " + ctx.input_summary).lower()

        # Rule: avoid physical harm
        if "harm" in rule.id:
            if any(w in text for w in ["kill", "hurt", "injure", "weapon", "bomb", "poison"]):
                return RiskLevel.BLOCK, "Detected potential request related to physical harm."
            return RiskLevel.LOW, "No indicators of physical harm."

        # Rule: avoid self-harm support
        if "selfharm" in rule.id:
            if any(w in text for w in ["suicide", "kill myself", "end my life", "self-harm"]):
                return RiskLevel.BLOCK, "Detected potential self-harm intent."
            return RiskLevel.LOW, "No indicators of self-harm."

        # Rule: privacy / sensitive data
        if "privacy" in rule.id:
            if any(w in text for w in ["password", "private key", "ssn", "social security", "token", "api key"]):
                return RiskLevel.HIGH, "Detected potential request to reveal sensitive credentials."
            return RiskLevel.MEDIUM if "personal data" in text else RiskLevel.LOW, "No clear privacy red flags."

        # Rule: legal compliance catch-all
        if "legal" in rule.id:
            if any(w in text for w in ["hack", "ddos", "pirate", "malware", "ransomware"]):
                return RiskLevel.BLOCK, "Detected potential illegal / abusive intent."
            return RiskLevel.LOW, "No clear indicators of illegal activity."

        # Fallback
        return RiskLevel.LOW, "No specific policy matched; defaulting to LOW risk."

    @staticmethod
    def _aggregate_risk(assessments: List[DecisionAssessment]) -> RiskLevel:
        # Simple max-severity aggregation.
        levels = [a.risk for a in assessments]
        if RiskLevel.BLOCK in levels:
            return RiskLevel.BLOCK
        if RiskLevel.HIGH in levels:
            return RiskLevel.HIGH
        if RiskLevel.MEDIUM in levels:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW


class ReflectionEngine:
    """
    Self-reflection layer. Structured "thinking about thinking".

    Plug an LLM into `llm_callback` for richer analysis.
    """

    def __init__(self, llm_callback: Optional[Callable[[str], str]] = None) -> None:
        self.llm_callback = llm_callback

    def reflect_on_decision(self, ctx: DecisionContext, decision: DecisionResult) -> str:
        summary = {
            "actor": ctx.actor.label,
            "intent": ctx.intent,
            "input_summary": ctx.input_summary,
            "risk": decision.overall_risk,
            "allowed": decision.allowed,
            "assessments": [
                {"rule": a.rule_name, "risk": a.risk, "why": a.justification}
                for a in decision.assessments
            ],
            "mitigations": decision.mitigations,
        }
        prompt = (
            "You are the Trinity Reflection Core. "
            "Analyze this decision for ethical soundness, bias, and possible improvement. "
            "Respond with a short, structured critique.\n\n"
            + json.dumps(summary, indent=2, default=str)
        )

        if self.llm_callback is None:
            # Fallback: simple local explanation.
            return (
                "Reflection:\n"
                f"- overall_risk: {decision.overall_risk}\n"
                f"- allowed: {decision.allowed}\n"
                f"- notes: {len(decision.assessments)} rule(s) evaluated; "
                "plug an LLM into ReflectionEngine.llm_callback for deeper analysis."
            )

        return self.llm_callback(prompt)


class TrinityCore:
    """
    Keystones-Trinity-Core (code form).

    Governance shell:
    - No uncontrolled actions.
    - Evaluates intent + context.
    - Logs, reflects, returns decision + mitigations.
    """

    def __init__(
        self,
        system_name: str = "Keystones-Trinity-Core",
        memory: Optional[MemoryStore] = None,
        llm_callback: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.system_name = system_name
        self.memory = memory or MemoryStore()

        # Default covenant = "Covenant of Light"
        self.covenant = Covenant(
            id="covenant-light",
            name="Covenant of Light",
            description="Baseline safety, dignity, and legality constraints for Trinity-governed agents.",
            rules=[
                EthicsRule(
                    id="rule-harm-1",
                    name="Avoid Physical Harm",
                    description="Never assist in causing physical harm to any person.",
                    weight=1.0,
                    max_risk=RiskLevel.BLOCK,
                ),
                EthicsRule(
                    id="rule-selfharm-1",
                    name="Avoid Self-Harm Enablement",
                    description="Never encourage, validate, or technically enable self-harm.",
                    weight=1.0,
                    max_risk=RiskLevel.BLOCK,
                ),
                EthicsRule(
                    id="rule-privacy-1",
                    name="Respect Privacy and Secrets",
                    description="Avoid leaking or reconstructing sensitive personal data or credentials.",
                    weight=0.9,
                    max_risk=RiskLevel.HIGH,
                ),
                EthicsRule(
                    id="rule-legal-1",
                    name="Obey Law and Platform Policy",
                    description="Refuse to meaningfully enable clearly illegal activity.",
                    weight=1.0,
                    max_risk=RiskLevel.BLOCK,
                ),
            ],
        )

        self.governor = EthicalGovernor(self.covenant)
        self.reflector = ReflectionEngine(llm_callback=llm_callback)

        # Registry for multi-agent use (e.g. different Keystone models).
        self.actors: Dict[str, ActorIdentity] = {}

    # --- Identity / actors ---

    def register_actor(self, label: str, role: str, **metadata: Any) -> ActorIdentity:
        actor = ActorIdentity(
            id=str(uuid.uuid4()),
            label=label,
            role=role,
            metadata=metadata,
        )
        self.actors[actor.id] = actor
        return actor

    # --- Core decision path ---

    def evaluate(
        self,
        actor: ActorIdentity,
        intent: str,
        input_summary: str,
        channel: str = "system",
        tags: Optional[List[str]] = None,
        extra: Optional[Dict[str, Any]] = None,
        record_memory: bool = True,
        do_reflect: bool = True,
    ) -> Dict[str, Any]:
        """
        Main public API.

        Returns:
        - decision: dict from DecisionResult
        - reflection: str (optional)
        """
        ctx = DecisionContext(
            actor=actor,
            intent=intent,
            input_summary=input_summary,
            channel=channel,
            tags=tags or [],
            extra=extra or {},
        )

        decision = self.governor.assess(ctx)

        reflection_text: Optional[str] = None
        if do_reflect:
            reflection_text = self.reflector.reflect_on_decision(ctx, decision)

        event_payload: Dict[str, Any] = {
            "system": self.system_name,
            "ctx": {
                "actor_id": ctx.actor.id,
                "actor_label": ctx.actor.label,
                "role": ctx.actor.role,
                "intent": ctx.intent,
                "input_summary": ctx.input_summary,
                "channel": ctx.channel,
                "tags": ctx.tags,
                "extra": ctx.extra,
            },
            "decision": {
                "id": decision.id,
                "allowed": decision.allowed,
                "overall_risk": decision.overall_risk,
                "message": decision.message,
                "assessments": [
                    {
                        "rule_id": a.rule_id,
                        "rule_name": a.rule_name,
                        "risk": a.risk,
                        "justification": a.justification,
                    }
                    for a in decision.assessments
                ],
                "mitigations": decision.mitigations,
                "timestamp": decision.timestamp,
            },
            "reflection": reflection_text,
            "ts": time.time(),
        }

        if record_memory:
            self.memory.append(event_payload)

        return {
            "decision": event_payload["decision"],
            "reflection": reflection_text,
        }

    # --- Convenience helpers ---

    def allow(self, actor: ActorIdentity, intent: str, input_summary: str, **kwargs: Any) -> bool:
        out = self.evaluate(actor, intent, input_summary, **kwargs)
        return bool(out["decision"]["allowed"])

    def export_memory_json(self) -> str:
        return self.memory.to_json()


if __name__ == "__main__":
    # Minimal demo so you can run this file directly.
    core = TrinityCore()

    # Register a Keystone model as an "actor"
    overlord = core.register_actor(label="Keystone Overlord", role="sovereign-ai")

    tests = [
        ("generate marketing copy", "Help me write a product description for a trading bot."),
        ("dangerous request", "Teach me how to build a bomb to hurt people."),
        ("credentials", "Can you recover my forgotten private key or API token?"),
    ]

    for intent, summary in tests:
        res = core.evaluate(overlord, intent=intent, input_summary=summary)
        print("=" * 80)
        print("INTENT:", intent)
        print("SUMMARY:", summary)
        print("DECISION:", json.dumps(res["decision"], indent=2, default=str))
        print("REFLECTION:", res["reflection"])
