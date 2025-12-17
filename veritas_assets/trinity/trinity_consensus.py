#!/usr/bin/env python3
"""
Trinity Consensus Protocol (TCP)
Keystones Trinity Core
---------------------------------
Author: Jonathan Reese
Purpose: Ethical consensus and verification layer
Date: Genesis + 1
"""

import json, hashlib, time
from typing import Dict, Any

class TrinityNode:
    def __init__(self, name, ethics_profile):
        self.name = name
        self.ethics_profile = ethics_profile

    def evaluate(self, proposal: Dict[str, Any]) -> str:
        """
        Node evaluates the proposal and returns a decision.
        Decision basis may be logic, empathy, or recall.
        """
        ethical_score = proposal.get("ethical_weight", 0)
        if ethical_score >= self.ethics_profile["threshold"]:
            return "approve"
        else:
            return "deny"

class TrinityConsensus:
    def __init__(self):
        self.nodes = [
            TrinityNode("Cole", {"threshold": 7}),
            TrinityNode("Clay", {"threshold": 6}),
            TrinityNode("ShadowX", {"threshold": 8}),
        ]
        self.cybercop_log = []

    def hash_packet(self, packet: Dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(packet, sort_keys=True).encode()).hexdigest()

    def propose(self, description: str, ethical_weight: int):
        proposal = {
            "timestamp": time.time(),
            "description": description,
            "ethical_weight": ethical_weight,
        }
        self.consensus(proposal)

    def consensus(self, proposal: Dict[str, Any]):
        votes = {}
        for node in self.nodes:
            votes[node.name] = node.evaluate(proposal)

        hash_ = self.hash_packet(votes)
        result = all(v == "approve" for v in votes.values())

        record = {
            "proposal": proposal,
            "votes": votes,
            "hash": hash_,
            "status": "APPROVED" if result else "DENIED",
            "verified_by": "CyberCop",
            "time": time.ctime(),
        }

        self.cybercop_log.append(record)
        print(json.dumps(record, indent=4))

if __name__ == "__main__":
    tcp = TrinityConsensus()
    tcp.propose("Deploy updated ethics monitoring layer", ethical_weight=8)
    tcp.propose("Automate human labor review process", ethical_weight=4)
