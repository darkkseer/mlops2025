import os
import asyncio
import httpx
import base64
from pathlib import Path
from .rag_retriever import RAGRetriever
from .animation_agent import AnimationAgent
from .gif_generator import create_gif, base64_to_image

class AnimationPipeline:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.agent = AnimationAgent()
        self.pose_api_url = "http://localhost:8001"

    async def _visualize_pose(self, pose: dict) -> str:
        """Отправляет позу в Pose API, возвращает base64 PNG"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self.pose_api_url}/visualize",
                json={"pose": pose}
            )
            if resp.status_code != 200:
                raise RuntimeError(f"Pose API error: {resp.text}")
            return resp.json()["image"]

    async def run(self, query: str) -> str:
        print(f"🎬 Generating animation for: {query}")
        
        # 1. RAG: найти релевантные позы
        candidates = self.retriever.retrieve(query)
        print(f"🔍 Retrieved {len(candidates)} candidate poses")

        # 2. LLM: выбрать последовательность
        sequence = await self.agent.select_sequence(query, candidates)
        print(f"🤖 LLM selected {len(sequence)} poses for animation")

        # 3. Визуализация кадров
        frames_b64 = []
        for i, pose in enumerate(sequence):
            print(f"🖼️  Rendering frame {i+1}/{len(sequence)}...")
            b64 = await self._visualize_pose(pose["pose"])
            frames_b64.append(b64)

        # 4. Сборка GIF
        images = [base64_to_image(b64) for b64 in frames_b64]
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{query.replace(' ', '_')}.gif"
        create_gif(images, str(output_path), duration=600)
        
        print(f"✅ Animation saved to: {output_path}")
        return str(output_path)