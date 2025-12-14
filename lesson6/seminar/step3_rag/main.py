import asyncio
import sys
from src.animation_pipeline import AnimationPipeline

async def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "танец макарена"
    pipeline = AnimationPipeline()
    await pipeline.run(query)

if __name__ == "__main__":
    asyncio.run(main())