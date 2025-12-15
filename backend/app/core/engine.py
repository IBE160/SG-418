from typing import Optional
from app.models.domain import WorldState


class Engine:
    """Core simulation engine managing ticks and day advancement"""
    
    def __init__(self, ticks_per_day: int = 10):
        """
        Initialize the engine.
        
        Args:
            ticks_per_day: Number of ticks that constitute one simulation day
        """
        self.ticks_per_day = ticks_per_day
    
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
        
        # Update timestamp
        from datetime import datetime
        updated_state.last_updated = datetime.now().timestamp()
        
        return updated_state

