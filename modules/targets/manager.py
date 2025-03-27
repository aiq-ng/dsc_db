from fastapi import HTTPException
from modules.shared.db import db
from modules.targets.utils import validate_target_data
import json

class TargetManager:
    async def create_target(self, target_name: str, number: str, folder: str | None,
                        offence_id: int, operator_id: int, type: str, origin: str | None,
                        target_date: str, metadata: dict):
        validate_target_data(target_name, number, type)
        
        offence_check = await db.fetchrow("SELECT id FROM offences WHERE id = $1", offence_id)
        if not offence_check:
            raise HTTPException(status_code=400, detail="Invalid offence_id")
        operator_check = await db.fetchrow("SELECT id FROM operators WHERE id = $1", operator_id)
        if not operator_check:
            raise HTTPException(status_code=400, detail="Invalid operator_id")

        query = """
            INSERT INTO targets (target_name, number, folder, offence_id, operator_id, 
                            type, origin, target_date, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *
        """
        try:
            return await db.fetchrow(query, target_name, number, folder, offence_id,
                                operator_id, type, origin, target_date, json.dumps(metadata))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create target: {str(e)}")

    async def get_target(self, target_id: int):
        query = """
            SELECT t.*, o.name as offence_name, op.operator_name 
            FROM targets t
            LEFT JOIN offences o ON t.offence_id = o.id
            LEFT JOIN operators op ON t.operator_id = op.id
            WHERE t.id = $1
        """
        target = await db.fetchrow(query, target_id)
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")
        return target

    async def get_all_targets(self, skip: int = 0, limit: int = 100):
        query = """
            SELECT t.*, o.name as offence_name, op.operator_name 
            FROM targets t
            LEFT JOIN offences o ON t.offence_id = o.id
            LEFT JOIN operators op ON t.operator_id = op.id
            ORDER BY t.created_at DESC
            OFFSET $1 LIMIT $2
        """
        return await db.fetch(query, skip, limit)

    async def update_target(self, target_id: int, target_data: dict):
        # Remove None values from the update data
        update_data = {k: v for k, v in target_data.items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")

        # Validate only the fields being updated
        if "target_name" in update_data and not (0 < len(update_data["target_name"]) <= 255):
            raise HTTPException(status_code=400, detail="Target name must be between 1 and 255 characters")
        if "number" in update_data and not (0 < len(update_data["number"]) <= 100):
            raise HTTPException(status_code=400, detail="Target number must be between 1 and 100 characters")
        if "type" in update_data and update_data["type"] not in VALID_TYPES:
            raise HTTPException(status_code=400, detail=f"Type must be one of {VALID_TYPES}")

        # Convert metadata to JSON string if present
        if "metadata" in update_data:
            update_data["metadata"] = json.dumps(update_data["metadata"])

        # Build dynamic SET clause
        set_clause = ", ".join(f"{key} = ${i+2}" for i, key in enumerate(update_data.keys()))
        values = list(update_data.values())
        values.insert(0, target_id)  # Add target_id as first parameter

        query = f"""
            UPDATE targets 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            RETURNING *
        """
        try:
            result = await db.fetchrow(query, *values)
            if not result:
                raise HTTPException(status_code=404, detail="Target not found")
            return {
                "id": result["id"],
                "target_name": result["target_name"],
                "number": result["number"],
                "folder": result["folder"],
                "offence_id": result["offence_id"],
                "operator_id": result["operator_id"],
                "type": result["type"],
                "origin": result["origin"],
                "target_date": result["target_date"],
                "metadata": json.loads(result["metadata"]),
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to update target: {str(e)}")

    async def delete_target(self, target_id: int):
        query = "DELETE FROM targets WHERE id = $1 RETURNING id"
        result = await db.fetchrow(query, target_id)
        if not result:
            raise HTTPException(status_code=404, detail="Target not found")
        return {"message": f"Target {target_id} deleted"}
    


    async def search_targets(self, target_name: str = None, number: str = None):
            conditions = []
            params = []
            param_count = 1

            if target_name:
                conditions.append(f"target_name ILIKE ${param_count}")
                params.append(f"%{target_name}%")
                param_count += 1
            if number:
                conditions.append(f"number ILIKE ${param_count}")
                params.append(f"%{number}%")
                param_count += 1

            where_clause = " AND ".join(conditions) if conditions else "TRUE"
            query = f"""
                SELECT t.*, o.name as offence_name, op.operator_name 
                FROM targets t
                LEFT JOIN offences o ON t.offence_id = o.id
                LEFT JOIN operators op ON t.operator_id = op.id
                WHERE {where_clause}
                ORDER BY t.created_at DESC
            """
            results = await db.fetch(query, *params)
            return [{
                "id": result["id"],
                "target_name": result["target_name"],
                "number": result["number"],
                "folder": result["folder"],
                "offence_id": result["offence_id"],
                "operator_id": result["operator_id"],
                "type": result["type"],
                "origin": result["origin"],
                "target_date": result["target_date"],
                "metadata": json.loads(result["metadata"]),
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat()
            } for result in results]

