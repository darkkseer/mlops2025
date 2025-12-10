import json
import httpx
import asyncio

class AnimationAgent:
    def __init__(self, llm_url: str = "http://localhost:11434/v1"):
        self.llm_url = llm_url

    async def select_sequence(self, query: str, candidate_poses: list) -> list:
        descriptions = [p["description"] for p in candidate_poses]
        prompt = f"""
Ты — аниматор танцев. Пользователь просит: "{query}".
Вот доступные позы:
{chr(10).join(f"{i+1}. {desc}" for i, desc in enumerate(descriptions))}

Выбери оптимальную последовательность из 7 поз для анимации танца.
Верни ТОЛЬКО JSON в формате:
{{"sequence": ["описание позы 1", "описание позы 2", ...]}}
Без пояснений.
"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self.llm_url}/chat/completions",
                json={
                    "model": "qwen2.5:1.5b",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 200
                }
            )
            if resp.status_code != 200:
                raise RuntimeError(f"LLM error: {resp.text}")
            text = resp.json()["choices"][0]["message"]["content"]
        
        try:
            data = json.loads(text.strip())
            selected_descs = data["sequence"]
            # Сопоставляем описания с pose-объектами
            pose_map = {p["description"]: p for p in candidate_poses}
            return [pose_map[desc] for desc in selected_descs if desc in pose_map]
        except Exception as e:
            print(f"⚠️ Parsing error, falling back to all poses: {e}")
            return candidate_poses[:7]