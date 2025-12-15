import os
import logging
from typing import Dict, Any, List
from pydantic_ai import Agent as PydanticAIAgent
from pydantic_ai.models.gemini import GeminiModel
from pydantic import BaseModel, Field
from app.agents.base import Agent
from app.models.domain import TradeOffer, OfferResponse


class TargetSelection(BaseModel):
    """Model for trade partner selection"""
    agent_id: str = Field(description="ID of the selected trade partner")


class GeminiAgent(Agent):
    """LLM-powered agent using Google Gemini"""
    
    def __init__(self, agent_id: str, job: str, culture: str, needs: Dict[str, int], wants: Dict[str, int], income: int):
        super().__init__(agent_id, job, culture, needs, wants, income)
        
        logger = logging.getLogger(__name__)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            error_msg = "GEMINI_API_KEY environment variable is not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            model = GeminiModel('gemini-1.5-flash', api_key=api_key)
            self.llm_agent = PydanticAIAgent(model, result_type=TargetSelection)
            self.offer_agent = PydanticAIAgent(model, result_type=TradeOffer)
            self.evaluate_agent = PydanticAIAgent(model, result_type=OfferResponse)
        except Exception as e:
            logger.error(f"Failed to initialize GeminiAgent {agent_id}: {e}", exc_info=True)
            raise
    
    async def select_trade_partner(self, available_agents: List[Dict[str, Any]]) -> str:
        """Select a trade partner using LLM"""
        try:
            from pydantic import ValidationError
            # Filter out self
            other_agents = [a for a in available_agents if a.get('id') != self.id]
            
            if not other_agents:
                return ""
            
            prompt = f"""You are an agent in an economic simulation.
Your ID: {self.id}
Your Job: {self.job}
Your Culture: {self.culture}
Your Needs: {self.needs}
Your Inventory: {self.inventory}

Available agents to trade with:
{self._format_agents_list(other_agents)}

Based on your needs and the jobs of other agents, select the best trade partner.
Return the agent_id of your chosen partner."""
            
            result = await self.llm_agent.run(prompt)
            return result.data.agent_id
        except Exception as e:
            from pydantic import ValidationError
            if isinstance(e, ValidationError):
                print(f"ValidationError in select_trade_partner for {self.id}: {e}")
            else:
                print(f"Error in select_trade_partner for {self.id}: {e}")
            # Return first available agent as fallback (Penalty Box: Action.WAIT equivalent)
            other_agents = [a for a in available_agents if a.get('id') != self.id]
            return other_agents[0].get('id', '') if other_agents else ''
    
    async def generate_offer(self, target_agent_id: str, target_job: str) -> Dict[str, Any]:
        """Generate a trade offer using LLM"""
        try:
            # Find what resource the target job produces
            # This would ideally come from the world state, but for now we'll infer from job name
            target_resource = target_job.lower().replace('er', '').replace('man', '').capitalize()
            
            prompt = f"""You are an agent in an economic simulation making a trade offer.
Your ID: {self.id}
Your Job: {self.job}
Your Culture: {self.culture}
Your Needs: {self.needs}
Your Wants: {self.wants}
Your Inventory: {self.inventory}

Target Agent: {target_agent_id} (Job: {target_job})
Target Agent likely produces: {target_resource}

Based on your needs and what you have in inventory, create a trade offer.
You can offer resources from your inventory and request resources you need.
Make sure the offered_amount doesn't exceed what you have in inventory.

Return a trade offer with:
- offered_resource: A resource you have
- offered_amount: How much you're offering (must be <= your inventory)
- requested_resource: A resource you need (likely {target_resource} which {target_job} produces)
- requested_amount: How much you're requesting"""
            
            result = await self.offer_agent.run(prompt)
            offer = result.data
            
            # Validate offer against inventory
            if offer.offered_resource in self.inventory:
                if offer.offered_amount > self.inventory[offer.offered_resource]:
                    offer.offered_amount = self.inventory[offer.offered_resource]
            else:
                # If resource not in inventory, set amount to 0
                offer.offered_amount = 0
            
            return offer.model_dump()
        except Exception as e:
            from pydantic import ValidationError
            if isinstance(e, ValidationError):
                print(f"ValidationError in generate_offer for {self.id}: {e}")
            else:
                print(f"Error in generate_offer for {self.id}: {e}")
            # Penalty Box: Return None to indicate failure (Action.WAIT equivalent)
            return None
    
    async def evaluate_offer(self, offer: Dict[str, Any], offerer_id: str) -> Dict[str, Any]:
        """Evaluate an incoming trade offer using LLM"""
        try:
            prompt = f"""You are an agent in an economic simulation evaluating a trade offer.
Your ID: {self.id}
Your Job: {self.job}
Your Culture: {self.culture}
Your Needs: {self.needs}
Your Wants: {self.wants}
Your Inventory: {self.inventory}

Incoming Offer from {offerer_id}:
- They offer: {offer.get('offered_amount', 0)} {offer.get('offered_resource', '')}
- They request: {offer.get('requested_amount', 0)} {offer.get('requested_resource', '')}

Evaluate this offer based on:
1. Do you have the requested resource?
2. Do you need/want the offered resource?
3. Is the trade fair?

Respond with:
- decision: ACCEPT, REJECT, or COUNTER
- reasoning: Your reasoning
- counter_offer: If COUNTER, provide a counter offer"""
            
            result = await self.evaluate_agent.run(prompt)
            response = result.data
            
            return response.model_dump()
        except Exception as e:
            from pydantic import ValidationError
            if isinstance(e, ValidationError):
                print(f"ValidationError in evaluate_offer for {self.id}: {e}")
            else:
                print(f"Error in evaluate_offer for {self.id}: {e}")
            # Penalty Box: Reject offer and continue (Action.WAIT equivalent)
            return {
                "decision": "REJECT",
                "reasoning": f"Error evaluating offer: {str(e)}",
                "counter_offer": None,
            }
    
    def _format_agents_list(self, agents: List[Dict[str, Any]]) -> str:
        """Format agents list for prompt"""
        lines = []
        for agent in agents:
            lines.append(f"- {agent.get('id', 'unknown')}: Job={agent.get('job', 'unknown')}")
        return '\n'.join(lines)

