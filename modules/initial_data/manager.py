from fastapi import HTTPException
from modules.shared.db import db
import json

class InitialDataManager:
    # --- Operators CRUD ---
    async def create_operator(self, operator: dict):
        query = """
            INSERT INTO operators (operator_name, operator_code, contact_info, active)
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """
        try:
            result = await db.fetchrow(query, operator["operator_name"], operator["operator_code"],
                                     json.dumps(operator["contact_info"]), operator["active"])
            return {
                "id": result["id"],
                "operator_name": result["operator_name"],
                "operator_code": result["operator_code"],
                "contact_info": json.loads(result["contact_info"]),
                "active": result["active"],
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create operator: {str(e)}")

    async def get_operator(self, operator_id: int):
        query = "SELECT * FROM operators WHERE id = $1"
        result = await db.fetchrow(query, operator_id)
        if not result:
            raise HTTPException(status_code=404, detail="Operator not found")
        return {
            "id": result["id"],
            "operator_name": result["operator_name"],
            "operator_code": result["operator_code"],
            "contact_info": json.loads(result["contact_info"]),
            "active": result["active"],
            "created_at": result["created_at"].isoformat(),
            "updated_at": result["updated_at"].isoformat()
        }

    async def get_all_operators(self, skip: int = 0, limit: int = 100):
        count_query = "SELECT COUNT(*) FROM operators"
        total = await db.fetchval(count_query)
        query = "SELECT * FROM operators ORDER BY created_at DESC OFFSET $1 LIMIT $2"
        results = await db.fetch(query, skip, limit)
        data = [{
            "id": r["id"],
            "operator_name": r["operator_name"],
            "operator_code": r["operator_code"],
            "contact_info": json.loads(r["contact_info"]),
            "active": r["active"],
            "created_at": r["created_at"].isoformat(),
            "updated_at": r["updated_at"].isoformat()
        } for r in results]
        next_page = f"/initial-data/operators?skip={skip + limit}&limit={limit}" if skip + limit < total else None
        previous_page = f"/initial-data/operators?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None
        return {"data": data, "total": total, "next_page": next_page, "previous_page": previous_page}

    async def update_operator(self, operator_id: int, operator_data: dict):
        update_data = {k: v for k, v in operator_data.items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")
        if "contact_info" in update_data:
            update_data["contact_info"] = json.dumps(update_data["contact_info"])
        set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(update_data.keys()))
        values = list(update_data.values())
        values.insert(0, operator_id)
        query = f"UPDATE operators SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = $1 RETURNING *"
        result = await db.fetchrow(query, *values)
        if not result:
            raise HTTPException(status_code=404, detail="Operator not found")
        return {
            "id": result["id"],
            "operator_name": result["operator_name"],
            "operator_code": result["operator_code"],
            "contact_info": json.loads(result["contact_info"]),
            "active": result["active"],
            "created_at": result["created_at"].isoformat(),
            "updated_at": result["updated_at"].isoformat()
        }

    async def delete_operator(self, operator_id: int):
        query = "DELETE FROM operators WHERE id = $1 RETURNING id"
        result = await db.fetchrow(query, operator_id)
        if not result:
            raise HTTPException(status_code=404, detail="Operator not found")
        return {"message": f"Operator {operator_id} deleted"}

    # --- Offences CRUD ---
    async def create_offence(self, offence: dict):
        query = """
            INSERT INTO offences (name, description)
            VALUES ($1, $2)
            RETURNING *
        """
        try:
            result = await db.fetchrow(query, offence["name"], offence["description"])
            return {
                "id": result["id"],
                "name": result["name"],
                "description": result["description"],
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create offence: {str(e)}")

    async def get_offence(self, offence_id: int):
        query = "SELECT * FROM offences WHERE id = $1"
        result = await db.fetchrow(query, offence_id)
        if not result:
            raise HTTPException(status_code=404, detail="Offence not found")
        return {
            "id": result["id"],
            "name": result["name"],
            "description": result["description"],
            "created_at": result["created_at"].isoformat(),
            "updated_at": result["updated_at"].isoformat()
        }

    async def get_all_offences(self, skip: int = 0, limit: int = 100):
        count_query = "SELECT COUNT(*) FROM offences"
        total = await db.fetchval(count_query)
        query = "SELECT * FROM offences ORDER BY created_at DESC OFFSET $1 LIMIT $2"
        results = await db.fetch(query, skip, limit)
        data = [{
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "created_at": r["created_at"].isoformat(),
            "updated_at": r["updated_at"].isoformat()
        } for r in results]
        next_page = f"/initial-data/offences?skip={skip + limit}&limit={limit}" if skip + limit < total else None
        previous_page = f"/initial-data/offences?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None
        return {"data": data, "total": total, "next_page": next_page, "previous_page": previous_page}

    async def update_offence(self, offence_id: int, offence_data: dict):
        update_data = {k: v for k, v in offence_data.items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")
        set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(update_data.keys()))
        values = list(update_data.values())
        values.insert(0, offence_id)
        query = f"UPDATE offences SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = $1 RETURNING *"
        result = await db.fetchrow(query, *values)
        if not result:
            raise HTTPException(status_code=404, detail="Offence not found")
        return {
            "id": result["id"],
            "name": result["name"],
            "description": result["description"],
            "created_at": result["created_at"].isoformat(),
            "updated_at": result["updated_at"].isoformat()
        }

    async def delete_offence(self, offence_id: int):
        query = "DELETE FROM offences WHERE id = $1 RETURNING id"
        result = await db.fetchrow(query, offence_id)
        if not result:
            raise HTTPException(status_code=404, detail="Offence not found")
        return {"message": f"Offence {offence_id} deleted"}