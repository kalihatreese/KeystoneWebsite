#!/usr/bin/env python3
"""
Ethics Bridge — Filters all store transactions through Trinity Consensus.
"""

from trinity_consensus import get_consensus

def ethical_gate(topic, weight):
    """Ask Trinity to approve or deny an action."""
    result = get_consensus(topic=topic, ethical_weight=weight)
    return result == "APPROVED"
