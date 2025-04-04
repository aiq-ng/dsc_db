from fastapi import HTTPException
from modules.shared.db import db
import json

class SuggestionManager:
    async def create_suggestion(self, title: str, description: str | None, user_id: int):
        query = """
            INSERT INTO suggestions (title, description, user_id)
            VALUES ($1, $2, $3)
            RETURNING *
        """
        result = await db.fetchrow(query, title, description, user_id)
        return {
            "id": result["id"],
            "title": result["title"],
            "description": result["description"],
            "user_id": result["user_id"],
            "created_at": result["created_at"].isoformat()
        }

    async def get_suggestion(self, suggestion_id: int):
        query = "SELECT * FROM suggestions WHERE id = $1"
        result = await db.fetchrow(query, suggestion_id)
        if not result:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        return {
            "id": result["id"],
            "title": result["title"],
            "description": result["description"],
            "user_id": result["user_id"],
            "created_at": result["created_at"].isoformat()
        }

    async def get_all_suggestions(self, skip: int = 0, limit: int = 100):
        count_query = "SELECT COUNT(*) FROM suggestions"
        total = await db.fetchval(count_query)
        query = "SELECT * FROM suggestions ORDER BY created_at DESC OFFSET $1 LIMIT $2"
        results = await db.fetch(query, skip, limit)
        data = [{
            "id": r["id"],
            "title": r["title"],
            "description": r["description"],
            "user_id": r["user_id"],
            "created_at": r["created_at"].isoformat()
        } for r in results]
        next_page = f"/suggestions/?skip={skip + limit}&limit={limit}" if skip + limit < total else None
        previous_page = f"/suggestions/?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None
        return {"data": data, "total": total, "next_page": next_page, "previous_page": previous_page}