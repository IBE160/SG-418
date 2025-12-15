from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class GlobalConfig(BaseModel):
    """Global simulation configuration"""
    day_length_seconds: int = Field(gt=0, description="Duration of a simulation day in real-time seconds")
    max_days: int = Field(gt=0, description="Maximum number of days the simulation will run")


class JobConfig(BaseModel):
    """Job configuration"""
    job_name: str = Field(description="Name of the job (e.g., 'Woodcutter')")
    resource_produced: str = Field(description="Resource this job produces (e.g., 'Wood')")


class AgentConfig(BaseModel):
    """Agent configuration"""
    job: str = Field(description="The agent's assigned profession")
    count: int = Field(gt=0, description="Number of agents to create with this configuration")
    culture: str = Field(default="Neutral", description="Descriptive string influencing behavior (e.g., 'Cooperative', 'Aggressive')")
    needs: Dict[str, int] | str = Field(default_factory=dict, description="Essential resources and their importance (dict or JSON string)")
    wants: Dict[str, int] | str = Field(default_factory=dict, description="Desirable resources (dict or JSON string)")
    income: int = Field(gt=0, description="Daily income received by the agent")


class SimulationConfig(BaseModel):
    """Complete simulation configuration"""
    day_length_seconds: int = Field(gt=0)
    max_days: int = Field(gt=0)
    jobs: List[JobConfig]
    agents: List[AgentConfig]


class TradeOffer(BaseModel):
    """Trade offer model"""
    offered_resource: str = Field(description="Resource being offered")
    offered_amount: int = Field(gt=0, description="Amount of resource being offered")
    requested_resource: str = Field(description="Resource being requested")
    requested_amount: int = Field(gt=0, description="Amount of resource being requested")


class OfferResponse(BaseModel):
    """Response to a trade offer"""
    decision: str = Field(description="Decision: ACCEPT, REJECT, or COUNTER")
    reasoning: str = Field(description="Reasoning for the decision")
    counter_offer: Optional[TradeOffer] = Field(default=None, description="Counter offer if decision is COUNTER")


class WorldState(BaseModel):
    """Global simulation state"""
    current_tick: int = 0
    current_day: int = 1
    is_running: bool = False
    last_updated: float = Field(default_factory=lambda: datetime.now().timestamp())
    # Placeholders for future epics
    agents: List = Field(default_factory=list)
    event_log: List = Field(default_factory=list)
    market_history: List = Field(default_factory=list)

