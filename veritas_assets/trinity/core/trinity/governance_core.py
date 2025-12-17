from core.council.council import CouncilOfTwelve
from core.ethics.ethical_engine import EthicalEngine
from core.reflection.self_reflection import SelfReflectionLoop

class TrinityGovernanceCore:
    """
    Central orchestrator that ties the Twelve, the Ethics Engine,
    and the Reflection Loop into one aligned decision architecture.
    """

    def __init__(self):
        self.council = CouncilOfTwelve()
        self.ethics = EthicalEngine()
        self.reflection = SelfReflectionLoop()

    def evaluate(self, question: str, action: dict):
        # 1. Council deliberates (multi-lens reasoning)
        council_reports = self.council.deliberate(question)

        # 2. Ethical engine checks constraints
        ethics_report = self.ethics.evaluate(action)

        # 3. Reflection loop checks for drift
        reflection_report = self.reflection.reflect(
            logs=[{"question": question, "action": action, "flags": []}],
            doctrine=list(self.ethics.RULES.keys())
        )

        return {
            "council": [r.__dict__ for r in council_reports],
            "ethics": ethics_report,
            "reflection": reflection_report,
        }
