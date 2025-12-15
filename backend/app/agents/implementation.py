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
        
        # Ensure logger has console handler
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        # Hardcoded API key for development - set as environment variable
        # GeminiModel reads from GEMINI_API_KEY or GOOGLE_API_KEY environment variable
        api_key = "your api key here"
        os.environ['GEMINI_API_KEY'] = api_key
        os.environ['GOOGLE_API_KEY'] = api_key  # Some versions use this
        
        try:
            model = GeminiModel('gemini-2.5-flash')
            self.llm_agent = PydanticAIAgent(model, output_type=TargetSelection)
            self.offer_agent = PydanticAIAgent(model, output_type=TradeOffer)
            self.evaluate_agent = PydanticAIAgent(model, output_type=OfferResponse)
        except Exception as e:
            self.logger.error(f"Failed to initialize GeminiAgent {agent_id}: {e}", exc_info=True)
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
            return result.output.agent_id
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
        import sys
        print(f"[OFFER DEBUG] Agent {self.id} generating offer for target {target_agent_id} (job: {target_job}). Inventory: {self.inventory}", file=sys.stderr, flush=True)
        self.logger.info(f"Agent {self.id} generating offer for target {target_agent_id} (job: {target_job}). Inventory: {self.inventory}")
        try:
            # Pre-check: Agent must have some inventory to make an offer
            if not self.inventory or all(amount <= 0 for amount in self.inventory.values()):
                print(f"[OFFER DEBUG] Agent {self.id} has no inventory to offer. Inventory: {self.inventory}", file=sys.stderr, flush=True)
                self.logger.info(f"Agent {self.id} has no inventory to offer. Inventory: {self.inventory}")
                return None
            
            # Find what resource the target job produces
            # This would ideally come from the world state, but for now we'll infer from job name
            target_resource = target_job.lower().replace('er', '').replace('man', '').capitalize()
            
            # Format available resources for the prompt
            available_resources = {k: v for k, v in self.inventory.items() if v > 0}
            resources_list = ", ".join([f"{k}: {v}" for k, v in available_resources.items()])
            
            prompt = f"""You are an agent in an economic simulation making a trade offer.
Your ID: {self.id}
Your Job: {self.job}
Your Culture: {self.culture}
Your Needs: {self.needs}
Your Wants: {self.wants}

Your Available Inventory (resources you can offer):
{resources_list}

Target Agent: {target_agent_id} (Job: {target_job})
Target Agent likely produces: {target_resource}

IMPORTANT: You can ONLY offer resources from your available inventory listed above.
You MUST choose an offered_resource that exists in your inventory with amount > 0.
The offered_amount must be between 1 and the amount you have in inventory.

Create a trade offer with:
- offered_resource: MUST be one of: {list(available_resources.keys())}
- offered_amount: Must be between 1 and your available amount for that resource
- requested_resource: A resource you need (likely {target_resource} which {target_job} produces)
- requested_amount: How much you're requesting (must be > 0)"""
            
            # Debug: Print before LLM call
            import sys
            print(f"[OFFER DEBUG] About to call LLM for agent {self.id}", file=sys.stderr, flush=True)
            sys.stderr.flush()
            
            try:
                result = await self.offer_agent.run(prompt)
                print(f"[OFFER DEBUG] LLM call completed for agent {self.id}", file=sys.stderr, flush=True)
                sys.stderr.flush()
            except Exception as llm_error:
                import traceback
                print(f"[OFFER DEBUG] LLM call failed for agent {self.id}: {type(llm_error).__name__}: {llm_error}", file=sys.stderr, flush=True)
                print(f"[OFFER DEBUG] LLM error traceback:\n{traceback.format_exc()}", file=sys.stderr, flush=True)
                sys.stderr.flush()
                raise  # Re-raise to be caught by outer exception handler
            
            if not result:
                print(f"[OFFER DEBUG] LLM returned None result for agent {self.id}", file=sys.stderr, flush=True)
                sys.stderr.flush()
                return None
            
            if not hasattr(result, 'output') or result.output is None:
                print(f"[OFFER DEBUG] LLM result has no output for agent {self.id}. Result: {result}", file=sys.stderr, flush=True)
                sys.stderr.flush()
                return None
            
            offer = result.output
            
            # Log the raw offer for debugging
            print(f"[OFFER DEBUG] Agent {self.id} LLM generated offer: offered_resource='{offer.offered_resource}', offered_amount={offer.offered_amount}, requested_resource='{offer.requested_resource}', requested_amount={offer.requested_amount}", file=sys.stderr, flush=True)
            self.logger.info(f"Agent {self.id} LLM generated offer: offered_resource='{offer.offered_resource}', offered_amount={offer.offered_amount}, requested_resource='{offer.requested_resource}', requested_amount={offer.requested_amount}")
            
            # Handle case sensitivity: try to find resource with case-insensitive matching
            offered_resource_key = None
            for inv_key in self.inventory.keys():
                if inv_key.lower() == offer.offered_resource.lower():
                    offered_resource_key = inv_key
                    break
            
            if offered_resource_key is None:
                # Resource not in inventory - cannot make offer
                print(f"[OFFER DEBUG] Agent {self.id} tried to offer '{offer.offered_resource}' which is not in inventory. Available resources: {list(self.inventory.keys())}", file=sys.stderr, flush=True)
                self.logger.info(f"Agent {self.id} tried to offer '{offer.offered_resource}' which is not in inventory. Available resources: {list(self.inventory.keys())}")
                return None
            
            available_amount = self.inventory[offered_resource_key]
            if available_amount <= 0:
                # No available amount - cannot make offer
                self.logger.info(f"Agent {self.id} has 0 {offered_resource_key} in inventory")
                return None
            
            # Adjust amount if it exceeds inventory
            final_offered_amount = min(offer.offered_amount, available_amount)
            if offer.offered_amount > available_amount:
                self.logger.info(f"Agent {self.id} requested {offer.offered_amount} {offered_resource_key} but only has {available_amount}, adjusting to {final_offered_amount}")
            
            # Final validation: ensure amounts are still > 0 (required by TradeOffer model)
            if final_offered_amount <= 0:
                self.logger.info(f"Agent {self.id} generated invalid offer: offered_amount would be {final_offered_amount} (must be > 0)")
                return None
            
            if offer.requested_amount <= 0:
                print(f"[OFFER DEBUG] Agent {self.id} generated invalid offer: requested_amount={offer.requested_amount} (must be > 0)", file=sys.stderr, flush=True)
                self.logger.info(f"Agent {self.id} generated invalid offer: requested_amount={offer.requested_amount} (must be > 0)")
                return None
            
            # Return offer dict with corrected resource name to match inventory key exactly
            return {
                "offered_resource": offered_resource_key,  # Use exact inventory key
                "offered_amount": final_offered_amount,
                "requested_resource": offer.requested_resource,
                "requested_amount": offer.requested_amount
            }
        except Exception as e:
            import traceback
            import sys
            error_type = type(e).__name__
            error_msg = str(e)
            full_traceback = traceback.format_exc()
            
            # Always print to console with flush to ensure visibility - MAKE IT VERY VISIBLE
            print(f"\n{'='*70}", file=sys.stderr, flush=True)
            print(f"[EXCEPTION] Agent {self.id} failed to generate offer!", file=sys.stderr, flush=True)
            print(f"[EXCEPTION] Error Type: {error_type}", file=sys.stderr, flush=True)
            print(f"[EXCEPTION] Error Message: {error_msg}", file=sys.stderr, flush=True)
            print(f"[EXCEPTION] Full Traceback:\n{full_traceback}", file=sys.stderr, flush=True)
            print(f"{'='*70}\n", file=sys.stderr, flush=True)
            
            # Also log using logger
            self.logger.error("="*70)
            self.logger.error(f"EXCEPTION: Agent {self.id} failed to generate offer: {error_type}: {error_msg}")
            self.logger.error(f"Full traceback:\n{full_traceback}")
            self.logger.error("="*70)
            
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
            response = result.output
            
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

