from typing import Optional
from app.models.domain import WorldState


class StateManager:
    """Singleton state manager for WorldState"""
    
    _instance: Optional['StateManager'] = None
    _state: WorldState = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance._state = WorldState()
        return cls._instance
    
    def get_state(self) -> WorldState:
        """Get the current world state"""
        return self._state
    
    def set_state(self, state: WorldState) -> None:
        """Set the world state"""
        self._state = state
    
    def reset_state(self) -> None:
        """Reset the world state to initial values"""
        self._state = WorldState()


# Global singleton instance
_state_manager = StateManager()


def get_state() -> WorldState:
    """Get the current world state singleton"""
    return _state_manager.get_state()


def set_state(state: WorldState) -> None:
    """Set the world state singleton"""
    _state_manager.set_state(state)


def reset_state() -> None:
    """Reset the world state singleton"""
    _state_manager.reset_state()

