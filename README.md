VORTEX: The Antifragile Framework for Python 🛡️
"Stop catching exceptions. Start inverting them."
VORTEX is a lightweight Python framework designed to implement Kinetic Vector Inversion—the philosophy that system failures should be treated as energy for redirection, not program crashes.
It combines Structural Integrity (via Pydantic) and Antifragile Retries (via Tenacity) into a single, cohesive workflow.
🚀 Key Features
1. Kinetic Vector Inversion (vortex_flow)
Define your Primary Vector (risky task) and your Fallback Vector (safe recovery). If the primary task fails, the system automatically redirects execution to the fallback, ensuring continuity.
result = await vortex_flow(
    primary=lambda: fetch_data_from_cloud(),
    fallback=load_data_from_disk
)


2. Antifragile Tasks (@vortex_task)
Wrap any asynchronous function with this decorator to grant it immediate resilience. The function will automatically retry up to 3 times (by default) with exponential backoff upon encountering transient errors.
@vortex_task(retries=3)
async def unstable_network_call():
    # ...


3. Structural Integrity (VortexData)
Data reliability starts at the source. By inheriting from VortexData, all data objects are automatically validated against their type schemas before execution, preventing runtime errors caused by corrupted or malformed inputs.
X Installation & Usage
1. Install Dependencies:
pip install pydantic tenacity
2. Run the Example:
python vortex.py
* Philosophy
VORTEX is not just code; it is a mindset. We believe that robust systems are built by assuming failure is inevitable, and designing the flow to capitalize on it.
