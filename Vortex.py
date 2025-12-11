import asyncio
import logging
import random
from typing import Any, Callable, TypeVar, Optional

# [Dependency Check]
# Checks for required libraries (pydantic, tenacity) and provides an error if missing.
try:
    from pydantic import BaseModel, ValidationError
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError:
    print("❌ Critical Error: Missing dependencies.")
    print("👉 Please install required packages: pip install pydantic tenacity")
    exit(1)

# [Logging Setup] - Standardized and Clean Logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | [%(levelname)s] %(name)s: %(message)s', 
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("VORTEX_CORE")

# ======================================================
# VORTEX FRAMEWORK (v1.0)
# Philosophy: Kinetic Vector Inversion (Fault Tolerance)
# ======================================================

# 1. Structural Integrity (Data Safety via Pydantic)
class VortexData(BaseModel):
    """
    Base Schema for VORTEX data objects.
    Ensures runtime type validation and data consistency.
    """
    class Config:
        arbitrary_types_allowed = True

# 2. Antifragile Task Decorator
def vortex_task(retries: int = 3, min_wait: int = 1, max_wait: int = 4):
    """
    [Decorator] Transforms a standard function into a resilient task.
    Automatically absorbs shocks (errors) and retries with exponential backoff.
    """
    return retry(
        stop=stop_after_attempt(retries),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        reraise=True
    )

T = TypeVar("T")

# 3. Kinetic Flow Control (The Core Logic)
async def vortex_flow(
    primary: Callable[[], T], 
    fallback: Callable[[], T] = None,
    context: str = "Unknown Context"
) -> T:
    """
    Executes the 'Kinetic Vector Inversion' logic.
    If the Primary Vector fails, energy is redirected to the Fallback Vector.
    """
    try:
        logger.info(f"Executing Vector: {context}")
        return await primary()
    
    except Exception as e:
        logger.warning(f"⚠️ Vector Instability detected in [{context}]: {e}")
        
        if fallback:
            logger.info("   🔄 Inverting Vector -> Engaging Fallback Protocol...")
            try:
                result = await fallback()
                logger.info("   ✅ System Stabilized via Fallback.")
                return result
            except Exception as fb_e:
                logger.error(f"   ❌ Fallback also failed: {fb_e}")
                raise fb_e
        
        else:
            logger.error("   ❌ Critical Failure: No fallback vector defined.")
            raise e

# ======================================================
# DEMONSTRATION (Example Usage)
# ======================================================
if __name__ == "__main__":
    
    # [Scenario]: Secure Data Fetching with Auto-Recovery
    
    # 1. Define Data Structure
    class NetworkConfig(VortexData):
        url: str
        timeout: int
        active: bool = True

    # 2. Define Primary Task (Simulated Unstable Network)
    @vortex_task(retries=3)
    async def fetch_from_cloud(cfg: NetworkConfig):
        logger.info(f"Connecting to uplink: {cfg.url} (Timeout: {cfg.timeout}ms)")
        await asyncio.sleep(0.5)
        
        # Simulate Random Failure (Entropy)
        if random.random() < 0.7:
            logger.debug("Network Jitter detected.")
            raise ConnectionError("Connection Reset by Peer")
        
        return "CLOUD_DATA_PACKET_V1"

    # 3. Define Fallback Task (Safe Local Data)
    async def load_local_backup():
        logger.info("Accessing Local Secure Storage...")
        await asyncio.sleep(0.1)
        return "LOCAL_DATA_PACKET_BACKUP"

    # 4. Execution Routine
    async def main():
        print("\n🚀 INITIALIZING VORTEX FRAMEWORK...\n")
        
        try:
            config = NetworkConfig(url="https://api.vortex-secure.com", timeout=5000)
            
            # Execute with Kinetic Vector Inversion
            final_data = await vortex_flow(
                primary=lambda: fetch_from_cloud(config),
                fallback=load_local_backup,
                context="Data Synchronization"
            )
            
            print(f"\n👑 [OPERATION RESULT]: {final_data}")
            
        except ValidationError as ve:
            print(f"❌ Configuration Invalid: {ve}")
        except Exception as e:
            print(f"❌ System Halted: {e}")

    # Run Async Loop
    asyncio.run(main())

