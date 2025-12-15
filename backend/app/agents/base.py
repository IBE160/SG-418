from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Agent(ABC):
    """Abstract base class for agents"""
    
    def __init__(self, agent_id: str, job: str, culture: str, needs: Dict[str, int], wants: Dict[str, int], income: int):
        self.id = agent_id
        self.job = job
        self.culture = culture
        self.needs = needs
        self.wants = wants
        self.income = income
        self.inventory: Dict[str, int] = {}
        self.last_action: Optional[str] = None
    
    @abstractmethod
    async def select_trade_partner(self, available_agents: list) -> str:
        """Select a trade partner from available agents"""
        pass
    
    @abstractmethod
    async def generate_offer(self, target_agent_id: str, target_job: str) -> Dict[str, Any]:
        """Generate a trade offer"""
        pass
    
    @abstractmethod
    async def evaluate_offer(self, offer: Dict[str, Any], offerer_id: str) -> Dict[str, Any]:
        """Evaluate an incoming trade offer"""
        pass

