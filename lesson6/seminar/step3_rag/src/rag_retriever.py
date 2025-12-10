import json
from pathlib import Path
from fuzzywuzzy import fuzz

class RAGRetriever:
    def __init__(self, db_path: str = "poses_database.json"):
        with open(db_path, "r", encoding="utf-8") as f:
            self.poses = json.load(f)

    def retrieve(self, query: str, top_k: int = 7) -> list:
        scored = []
        for item in self.poses:
            score = fuzz.partial_ratio(query.lower(), item["description"].lower())
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]