from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from app.core.state import get_state, set_state, reset_state
from app.core.engine import Engine
from app.models.domain import SimulationConfig, WorldState, AgentConfig
import json

# Load environment variables from .env file
# Find the backend directory (parent of app directory)
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'

# Try loading from explicit path first, then fallback to default behavior
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback: try current directory and parent directories
    load_dotenv()

# Verify API key is loaded (for debugging)
# Configure logging to ensure console output
# Get root logger and configure it
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove existing handlers to avoid duplicates
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# Also configure basicConfig as fallback
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[console_handler],
    force=True
)

logger = logging.getLogger(__name__)
# Test that logging works
import sys
print("=" * 60, file=sys.stderr)
print("SERVER STARTUP: Logging configured", file=sys.stderr)
print("=" * 60, file=sys.stderr)
sys.stderr.flush()
logger.info("Server logging initialized - errors should be visible")
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    logger.info(f"GEMINI_API_KEY loaded successfully (length: {len(api_key)})")
else:
    logger.error(f"GEMINI_API_KEY not found! Checked path: {env_path.absolute()}")
    logger.error("Make sure .env file exists in the backend directory with GEMINI_API_KEY set")

# Global engine instance
engine = Engine(ticks_per_day=10)  # Default: 10 ticks per day
simulation_task: asyncio.Task | None = None


async def simulation_loop():
    """Background task that runs the simulation loop"""
    logger = logging.getLogger(__name__)
    import sys
    print("[SIMULATION LOOP] Started", file=sys.stderr, flush=True)
    logger.info("Simulation loop started")
    
    while True:
        try:
            state = get_state()
            if state.is_running:
                print(f"[SIMULATION LOOP] Tick {state.current_tick}, Day {state.current_day}, is_running={state.is_running}", file=sys.stderr, flush=True)
                # Run one tick first (updates tick counter, day, etc.)
                # This creates a copy of the state
                updated_state = engine.tick(state)
                
                # Process trading for all agents on the updated state
                # This will modify the agent dictionaries in updated_state
                print(f"[SIMULATION LOOP] About to call process_trading", file=sys.stderr, flush=True)
                trading_events = await engine.process_trading(updated_state)
                print(f"[SIMULATION LOOP] process_trading returned {len(trading_events)} events", file=sys.stderr, flush=True)
                
                # Add trading events to event log
                updated_state.event_log.extend(trading_events)
                
                set_state(updated_state)
                # Sleep for a short duration (e.g., 1 second per tick)
                await asyncio.sleep(1)
            else:
                # If not running, check every second
                await asyncio.sleep(1)
        except Exception as e:
            import traceback
            print(f"[SIMULATION LOOP ERROR] {e}", file=sys.stderr, flush=True)
            print(f"[SIMULATION LOOP ERROR] Traceback:\n{traceback.format_exc()}", file=sys.stderr, flush=True)
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
    import sys
    state = get_state()
    print(f"[HEALTH CHECK] State: is_running={state.is_running}, agents={len(state.agents) if state.agents else 0}", file=sys.stderr, flush=True)
    logger.info(f"Health check - is_running={state.is_running}, agents={len(state.agents) if state.agents else 0}")
    return {
        "status": "online",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "simulation_running": state.is_running,
        "agent_count": len(state.agents) if state.agents else 0
    }


@app.get("/api/state")
async def get_world_state():
    """Get current world state"""
    state = get_state()
    # FastAPI automatically serializes Pydantic models
    return state


@app.post("/api/config")
async def set_simulation_config(config: SimulationConfig):
    """Set simulation configuration and initialize world state"""
    logger = logging.getLogger(__name__)
    
    try:
        # Reset existing state
        reset_state()
        # Clear agent instance cache when reconfiguring
        engine.clear_agent_cache()
        
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
    import sys
    print("[START ENDPOINT] Starting simulation", file=sys.stderr, flush=True)
    logger.info("Start simulation endpoint called")
    
    state = get_state()
    if not state.agents:
        print("[START ENDPOINT] ERROR: No agents configured", file=sys.stderr, flush=True)
        return {"status": "error", "message": "No agents configured. Please configure simulation first."}
    
    # Create a copy to avoid mutating the shared state
    from copy import deepcopy
    updated_state = deepcopy(state)
    updated_state.is_running = True
    set_state(updated_state)
    
    print(f"[START ENDPOINT] Simulation started. Agents: {len(updated_state.agents)}, is_running: {updated_state.is_running}", file=sys.stderr, flush=True)
    logger.info(f"Simulation started with {len(updated_state.agents)} agents")
    
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

