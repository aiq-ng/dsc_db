from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from modules.suggestions.manager import SuggestionManager
from modules.suggestions.models import SuggestionCreate, SuggestionResponse
from modules.auth.router import get_current_user

router = APIRouter()
manager = SuggestionManager()

@router.post("/")
async def create_suggestion(suggestion: SuggestionCreate, current_user=Depends(get_current_user)):
    print(current_user)
    return await manager.create_suggestion(suggestion.title, suggestion.description, current_user["current_user"]["id"])

@router.get("/{suggestion_id}")
async def get_suggestion(suggestion_id: int, current_user=Depends(get_current_user)):
    return await manager.get_suggestion(suggestion_id)

@router.get("/")
async def get_all_suggestions(skip: int = 0, limit: int = 100, current_user=Depends(get_current_user)):
    return await manager.get_all_suggestions(skip, limit)