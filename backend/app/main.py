from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import logging
from app.core.state import get_state, set_state, reset_state
from app.core.engine import Engine
from app.models.domain import SimulationConfig, WorldState, AgentConfig
import json

# Global engine instance
engine = Engine(ticks_per_day=10)  # Default: 10 ticks per day
simulation_task: asyncio.Task | None = None


async def simulation_loop():
    """Background task that runs the simulation loop"""
    logger = logging.getLogger(__name__)
    while True:
        try:
            state = get_state()
            if state.is_running:
                # Run one tick
                updated_state = engine.tick(state)
                set_state(updated_state)
                # Sleep for a short duration (e.g., 1 second per tick)
                await asyncio.sleep(1)
            else:
                # If not running, check every second
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}", exc_info=True)
            # Continue running even if there's an error
            await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for background tasks"""
    # Startup
    global simulation_task
    simulation_task = asyncio.create_task(simulation_loop())
    yield
    # Shutdown
    if simulation_task:
        simulation_task.cancel()
        try:
            await simulation_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="AIES API", version="0.1.0", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AIES API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "GET /health": "Health check",
            "GET /api/state": "Get world state",
            "POST /api/config": "Set simulation configuration",
            "POST /api/control/start": "Start simulation",
            "POST /api/control/stop": "Stop simulation",
            "GET /api/export": "Export event log as CSV"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }


@app.get("/api/state")
async def get_world_state():
    """Get current world state"""
    state = get_state()
    return state.model_dump()


@app.post("/api/config")
async def set_simulation_config(config: SimulationConfig):
    """Set simulation configuration and initialize world state"""
    logger = logging.getLogger(__name__)
    
    try:
        # Reset existing state
        reset_state()
        
        # Create a mapping of job names to resources produced
        job_to_resource = {job.job_name: job.resource_produced for job in config.jobs}
        
        # Create agents from configuration
        agents = []
        agent_id_counter = 1
        
        for agent_config in config.agents:
            # Validate that the job exists in config.jobs
            if agent_config.job not in job_to_resource:
                logger.warning(f"Agent job '{agent_config.job}' not found in jobs configuration. Skipping agent creation.")
                continue
            
            # Parse needs and wants - handle both dict and JSON string
            needs = agent_config.needs
            wants = agent_config.wants
            
            # If needs/wants are strings, try to parse as JSON
            if isinstance(needs, str):
                try:
                    needs = json.loads(needs) if needs else {}
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in needs for job '{agent_config.job}'. Using empty dict.")
                    needs = {}
            if isinstance(wants, str):
                try:
                    wants = json.loads(wants) if wants else {}
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in wants for job '{agent_config.job}'. Using empty dict.")
                    wants = {}
            
            # Get the resource produced by this job
            resource_produced = job_to_resource[agent_config.job]
            
            # Create multiple agents based on count
            for i in range(agent_config.count):
                # Initialize inventory with starting amount of produced resource
                # Agents start with some of their produced resource to enable trading
                initial_inventory = {resource_produced: 10}  # Starting amount
                
                # Create independent copies of needs and wants for each agent
                # to prevent shared mutable state across agents
                agent_needs = dict(needs) if needs else {}
                agent_wants = dict(wants) if wants else {}
                
                agent = {
                    "id": f"agent-{agent_id_counter}",
                    "job": agent_config.job,
                    "culture": agent_config.culture,
                    "needs": agent_needs,
                    "wants": agent_wants,
                    "income": agent_config.income,
                    "inventory": initial_inventory,
                    "last_action": None,
                }
                agents.append(agent)
                agent_id_counter += 1
        
        # Initialize world state with configuration
        state = WorldState(
            current_tick=0,
            current_day=1,
            is_running=False,
            agents=agents,
            event_log=[],
            market_history=[],
        )
        
        set_state(state)
        
        return {"status": "ok", "message": "Configuration applied", "agent_count": len(agents)}
    except Exception as e:
        logger.error(f"Error setting simulation config: {e}", exc_info=True)
        return {"status": "error", "message": f"Failed to apply configuration: {str(e)}", "agent_count": 0}


@app.post("/api/control/start")
async def start_simulation():
    """Start the simulation"""
    state = get_state()
    if not state.agents:
        return {"status": "error", "message": "No agents configured. Please configure simulation first."}
    
    # Create a copy to avoid mutating the shared state
    from copy import deepcopy
    updated_state = deepcopy(state)
    updated_state.is_running = True
    set_state(updated_state)
    return {"status": "ok", "message": "Simulation started"}


@app.post("/api/control/stop")
async def stop_simulation():
    """Stop the simulation"""
    state = get_state()
    # Create a copy to avoid mutating the shared state
    from copy import deepcopy
    updated_state = deepcopy(state)
    updated_state.is_running = False
    set_state(updated_state)
    return {"status": "ok", "message": "Simulation stopped"}


@app.get("/api/export")
async def export_event_log():
    """Export event log as CSV"""
    import csv
    from io import StringIO
    
    state = get_state()
    events = state.event_log or []
    
    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Tick", "Day", "AgentID", "Action", "Details", "Result"])
    
    for event in events:
        writer.writerow([
            event.get("tick", ""),
            event.get("day", ""),
            event.get("agent_id", ""),
            event.get("action", ""),
            event.get("details", ""),
            event.get("result", ""),
        ])
    
    from fastapi.responses import Response
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=event-log.csv"}
    )

