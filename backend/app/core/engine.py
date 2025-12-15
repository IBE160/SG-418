from typing import Optional, Dict, Any, List
import logging
from app.models.domain import WorldState
from app.agents.implementation import GeminiAgent

logger = logging.getLogger(__name__)


class Engine:
    """Core simulation engine managing ticks and day advancement"""
    
    def __init__(self, ticks_per_day: int = 10):
        """
        Initialize the engine.
        
        Args:
            ticks_per_day: Number of ticks that constitute one simulation day
        """
        self.ticks_per_day = ticks_per_day
        # Cache for agent instances to avoid recreating them every tick
        self._agent_instance_cache: Dict[str, GeminiAgent] = {}
    
    def _calculate_total_economic_value(self, agents: list) -> float:
        """Calculate total economic value from all agent inventories"""
        total = 0.0
        for agent in agents:
            inventory = agent.get('inventory', {})
            if isinstance(inventory, dict):
                total += sum(inventory.values())
        return total
    
    def _create_agent_instance(self, agent_dict: Dict[str, Any]) -> Optional[GeminiAgent]:
        """Create or retrieve a cached GeminiAgent instance from an agent dictionary"""
        agent_id = agent_dict.get('id')
        if not agent_id:
            logger.error("Agent dictionary missing 'id' field")
            return None
        
        # Check cache first
        if agent_id in self._agent_instance_cache:
            agent = self._agent_instance_cache[agent_id]
            # Sync inventory from dict to agent instance (inventory changes every tick)
            agent.inventory = dict(agent_dict.get('inventory', {}))
            return agent
        
        # Create new instance if not in cache
        try:
            agent = GeminiAgent(
                agent_id=agent_id,
                job=agent_dict['job'],
                culture=agent_dict.get('culture', 'Neutral'),
                needs=agent_dict.get('needs', {}),
                wants=agent_dict.get('wants', {}),
                income=agent_dict.get('income', 0)
            )
            # Sync inventory from dict to agent instance
            agent.inventory = dict(agent_dict.get('inventory', {}))
            # Cache the instance for future use
            self._agent_instance_cache[agent_id] = agent
            return agent
        except ValueError as e:
            # Log the actual error for debugging
            logger.error(f"ValueError creating GeminiAgent instance for {agent_id}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Failed to create GeminiAgent instance for {agent_id}: {e}", exc_info=True)
            logger.error(f"Error type: {type(e).__name__}")
            return None
    
    def _sync_agent_dict_from_instance(self, agent_dict: Dict[str, Any], agent_instance: GeminiAgent):
        """Sync agent dictionary with changes from agent instance"""
        agent_dict['inventory'] = dict(agent_instance.inventory)
        agent_dict['last_action'] = agent_instance.last_action
    
    async def _process_agent_turn(self, agent_dict: Dict[str, Any], all_agents: List[Dict[str, Any]], tick: int, day: int) -> Dict[str, Any]:
        """Process a single agent's trading turn"""
        import sys
        print(f"[ENGINE DEBUG] _process_agent_turn START for agent {agent_dict.get('id')}", file=sys.stderr, flush=True)
        agent_instance = self._create_agent_instance(agent_dict)
        if not agent_instance:
            return {
                "tick": tick,
                "day": day,
                "agent_id": agent_dict.get('id'),
                "action": "SKIP",
                "details": "Failed to create agent instance",
                "result": "error"
            }
        
        try:
            # Step 1: Select trade partner
            import sys
            print(f"[ENGINE DEBUG] Step 1: Selecting trade partner for agent {agent_dict.get('id')}", file=sys.stderr, flush=True)
            partner_id = await agent_instance.select_trade_partner(all_agents)
            print(f"[ENGINE DEBUG] Selected partner: {partner_id} for agent {agent_dict.get('id')}", file=sys.stderr, flush=True)
            if not partner_id:
                agent_instance.last_action = "WAIT"
                self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                return {
                    "tick": tick,
                    "day": day,
                    "agent_id": agent_dict.get('id'),
                    "action": "WAIT",
                    "details": "No suitable trade partner found",
                    "result": "success"
                }
            
            # Find partner agent
            partner_dict = next((a for a in all_agents if a.get('id') == partner_id), None)
            if not partner_dict:
                agent_instance.last_action = "WAIT"
                self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                return {
                    "tick": tick,
                    "day": day,
                    "agent_id": agent_dict.get('id'),
                    "action": "WAIT",
                    "details": f"Partner {partner_id} not found",
                    "result": "error"
                }
            
            # Step 2: Generate offer
            import sys
            print(f"[ENGINE DEBUG] Calling generate_offer for agent {agent_dict.get('id')} with partner {partner_id} (job: {partner_dict.get('job', '')})", file=sys.stderr, flush=True)
            offer = await agent_instance.generate_offer(partner_id, partner_dict.get('job', ''))
            print(f"[ENGINE DEBUG] generate_offer returned: {offer}", file=sys.stderr, flush=True)
            if not offer:
                agent_instance.last_action = "WAIT"
                self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                # Check if agent has inventory to provide more context
                inventory_summary = {k: v for k, v in agent_instance.inventory.items() if v > 0} if agent_instance.inventory else {}
                if not inventory_summary:
                    details = "Failed to generate offer: Agent has no resources in inventory"
                else:
                    details = f"Failed to generate offer: Agent has inventory {inventory_summary} but offer generation failed (check terminal/logs for error details)"
                # Log error to console and logger - MAKE IT VERY VISIBLE
                import sys
                error_msg = f"Agent {agent_dict.get('id')} failed to generate offer. Inventory: {agent_instance.inventory}"
                print(f"\n{'='*70}", file=sys.stderr, flush=True)
                print(f"[ENGINE ERROR] OFFER GENERATION FAILED!", file=sys.stderr, flush=True)
                print(f"[ENGINE ERROR] {error_msg}", file=sys.stderr, flush=True)
                print(f"[ENGINE ERROR] This is the error you're seeing in the browser!", file=sys.stderr, flush=True)
                print(f"{'='*70}\n", file=sys.stderr, flush=True)
                logger.error("="*70)
                logger.error("OFFER GENERATION FAILED!")
                logger.error(error_msg)
                logger.error("="*70)
                return {
                    "tick": tick,
                    "day": day,
                    "agent_id": agent_dict.get('id'),
                    "action": "WAIT",
                    "details": details,
                    "result": "error"
                }
            
            # Step 3: Evaluate offer (create partner agent instance)
            partner_instance = self._create_agent_instance(partner_dict)
            if not partner_instance:
                agent_instance.last_action = "WAIT"
                self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                return {
                    "tick": tick,
                    "day": day,
                    "agent_id": agent_dict.get('id'),
                    "action": "WAIT",
                    "details": f"Failed to create partner instance for {partner_id}",
                    "result": "error"
                }
            
            response = await partner_instance.evaluate_offer(offer, agent_dict.get('id'))
            
            # Step 4: Execute trade if accepted
            if response.get('decision') == 'ACCEPT':
                # Execute the trade
                offered_resource = offer.get('offered_resource')
                offered_amount = offer.get('offered_amount', 0)
                requested_resource = offer.get('requested_resource')
                requested_amount = offer.get('requested_amount', 0)
                
                # Check if both agents have the required resources
                if (offered_resource in agent_instance.inventory and 
                    agent_instance.inventory[offered_resource] >= offered_amount and
                    requested_resource in partner_instance.inventory and
                    partner_instance.inventory[requested_resource] >= requested_amount):
                    
                    # Execute trade
                    agent_instance.inventory[offered_resource] -= offered_amount
                    if requested_resource not in agent_instance.inventory:
                        agent_instance.inventory[requested_resource] = 0
                    agent_instance.inventory[requested_resource] += requested_amount
                    
                    partner_instance.inventory[requested_resource] -= requested_amount
                    if offered_resource not in partner_instance.inventory:
                        partner_instance.inventory[offered_resource] = 0
                    partner_instance.inventory[offered_resource] += offered_amount
                    
                    # Sync back to dictionaries
                    self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                    self._sync_agent_dict_from_instance(partner_dict, partner_instance)
                    
                    agent_instance.last_action = "TRADE_ACCEPTED"
                    return {
                        "tick": tick,
                        "day": day,
                        "agent_id": agent_dict.get('id'),
                        "action": "TRADE",
                        "details": f"Traded {offered_amount} {offered_resource} for {requested_amount} {requested_resource} with {partner_id}",
                        "result": "success"
                    }
                else:
                    agent_instance.last_action = "TRADE_FAILED"
                    self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                    return {
                        "tick": tick,
                        "day": day,
                        "agent_id": agent_dict.get('id'),
                        "action": "TRADE_FAILED",
                        "details": "Insufficient resources for trade",
                        "result": "error"
                    }
            elif response.get('decision') == 'REJECT':
                agent_instance.last_action = "TRADE_REJECTED"
                self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                return {
                    "tick": tick,
                    "day": day,
                    "agent_id": agent_dict.get('id'),
                    "action": "TRADE_REJECTED",
                    "details": f"Trade offer rejected by {partner_id}: {response.get('reasoning', 'No reason given')}",
                    "result": "success"
                }
            else:  # COUNTER
                agent_instance.last_action = "TRADE_COUNTERED"
                self._sync_agent_dict_from_instance(agent_dict, agent_instance)
                return {
                    "tick": tick,
                    "day": day,
                    "agent_id": agent_dict.get('id'),
                    "action": "TRADE_COUNTERED",
                    "details": f"Trade offer countered by {partner_id}",
                    "result": "success"
                }
                
        except Exception as e:
            import traceback
            import sys
            error_msg = f"Error processing turn for agent {agent_dict.get('id')}: {e}"
            full_traceback = traceback.format_exc()
            
            # Print to stderr for immediate visibility
            print(f"\n[ENGINE ERROR] {error_msg}", file=sys.stderr)
            print(f"[ENGINE ERROR] Full traceback:\n{full_traceback}", file=sys.stderr)
            sys.stderr.flush()
            
            # Also log using logger
            logger.error(error_msg, exc_info=True)
            
            agent_instance.last_action = "ERROR"
            self._sync_agent_dict_from_instance(agent_dict, agent_instance)
            return {
                "tick": tick,
                "day": day,
                "agent_id": agent_dict.get('id'),
                "action": "ERROR",
                "details": f"Error during trading: {str(e)}",
                "result": "error"
            }
    
    def clear_agent_cache(self):
        """Clear the agent instance cache (useful when agents are reconfigured)"""
        self._agent_instance_cache.clear()
    
    async def process_trading(self, state: WorldState) -> List[Dict[str, Any]]:
        """Process trading for all agents in the current tick"""
        import sys
        print(f"[ENGINE DEBUG] process_trading called. is_running={state.is_running}, agents_count={len(state.agents) if state.agents else 0}", file=sys.stderr, flush=True)
        if not state.is_running or not state.agents:
            print(f"[ENGINE DEBUG] Skipping trading: is_running={state.is_running}, has_agents={bool(state.agents)}", file=sys.stderr, flush=True)
            return []
        
        # Check if we can create agent instances (e.g., API key check)
        # Try to create one agent instance to verify setup
        if not self._agent_instance_cache and state.agents:
            test_agent_dict = state.agents[0]
            test_instance = self._create_agent_instance(test_agent_dict)
            if not test_instance:
                # If we can't create agents, skip trading for this tick
                # This prevents repeated error messages
                # If we can't create agents, skip trading for this tick
                # Log the actual error for debugging
                logger.error(f"Failed to create test agent instance. Check server logs for details.")
                return [{
                    "tick": state.current_tick,
                    "day": state.current_day,
                    "agent_id": None,
                    "action": "TRADING_DISABLED",
                    "details": "Cannot create agent instances. Check server logs for error details.",
                    "result": "error"
                }]
        
        events = []
        # Process each agent's turn
        import sys
        for agent_dict in state.agents:
            print(f"[ENGINE DEBUG] Processing turn for agent {agent_dict.get('id')}", file=sys.stderr, flush=True)
            event = await self._process_agent_turn(
                agent_dict, 
                state.agents, 
                state.current_tick, 
                state.current_day
            )
            print(f"[ENGINE DEBUG] Agent {agent_dict.get('id')} turn result: action={event.get('action')}, details={event.get('details')}", file=sys.stderr, flush=True)
            events.append(event)
        
        return events
    
    def tick(self, state: WorldState) -> WorldState:
        """
        Advance the simulation by one tick.
        
        Args:
            state: Current world state
            
        Returns:
            Updated world state (new instance)
        """
        if not state.is_running:
            return state
        
        # Create a copy of the state to avoid mutating the original
        # This prevents race conditions when multiple requests access state concurrently
        from copy import deepcopy
        updated_state = deepcopy(state)
        
        # Increment tick counter
        updated_state.current_tick += 1
        
        # Check if we've reached a new day
        if updated_state.current_tick % self.ticks_per_day == 0:
            updated_state.current_day += 1
            # Reset daily event budgets for all agents (to be implemented in Epic 3)
            # This is a placeholder for future agent budget reset logic
            
            # Add day transition event
            updated_state.event_log.append({
                "tick": updated_state.current_tick,
                "day": updated_state.current_day,
                "agent_id": None,
                "action": "DAY_TRANSITION",
                "details": f"Day {updated_state.current_day} begins",
                "result": "success"
            })
        
        # Calculate and update market history (total economic value)
        total_value = self._calculate_total_economic_value(updated_state.agents)
        updated_state.market_history.append({
            "tick": updated_state.current_tick,
            "day": updated_state.current_day,
            "total_value": total_value
        })
        
        # Generate periodic events to show activity
        # Every 5 ticks, add a simulation progress event
        if updated_state.current_tick % 5 == 0 and updated_state.agents:
            agent_count = len(updated_state.agents)
            updated_state.event_log.append({
                "tick": updated_state.current_tick,
                "day": updated_state.current_day,
                "agent_id": None,
                "action": "SIMULATION_TICK",
                "details": f"Simulation running: {agent_count} agents active, total value: {total_value:.2f}",
                "result": "success"
            })
        
        # Update timestamp
        from datetime import datetime
        updated_state.last_updated = datetime.now().timestamp()
        
        return updated_state

