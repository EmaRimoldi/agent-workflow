"""Communication primitives for coordinated agent modes."""

from agentops_lab.communication.blackboard import SharedMemory
from agentops_lab.communication.coordinator import Coordinator

__all__ = ["Coordinator", "SharedMemory"]
