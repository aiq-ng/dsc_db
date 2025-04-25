import json

from fastapi import HTTPException

from modules.shared.db import db
from modules.targets.utils import validate_target_data


class TargetManager:
    async def create_target(
        self,
        target_name: str,
        file_number: str,
        target_number: str | None,
        folder: str | None,
        offence_id: int,
        operator_id: int,
        type: str,
        origin: str | None,
        target_date: str,
        metadata: dict,
        flagged: bool = False,
        threat_level: str | None = None,
    ):
        validate_target_data(target_name, file_number, type, threat_level)
        # ... (validation for offence_id and operator_id unchanged)
        query = """
                INSERT INTO targets (target_name, file_number, target_number, folder, offence_id, operator_id, 
                                    type, origin, target_date, metadata, flagged, threat_level)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING *
            """
        result = await db.fetchrow(
            query,
            target_name,
            file_number,
            target_number,
            folder,
            offence_id,
            operator_id,
            type,
            origin,
            target_date,
            json.dumps(metadata),
            flagged,
            threat_level,
        )
        return self._format_target(result)

    async def get_target(self, target_id: int):
        query = """
            SELECT
                t.id, t.target_name, t.file_number, t.target_number, t.folder, 
                o.name as offence_name, op.operator_name, 
                t.type, t.origin, t.target_date, t.metadata, threat_level, t.flagged,
                t.created_at, t.updated_at
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
        # Query for paginated results
        query = """
            SELECT
                t.id, t.target_name, t.file_number, t.target_number, t.folder, 
                o.name as offence_name, op.operator_name, 
                t.type, t.origin, t.target_date, t.metadata, t.threat_level, t.flagged,
                t.created_at, t.updated_at
            FROM targets t
            LEFT JOIN offences o ON t.offence_id = o.id
            LEFT JOIN operators op ON t.operator_id = op.id
            ORDER BY t.created_at DESC
            OFFSET $1 LIMIT $2
            """
        results = await db.fetch(query, skip, limit)

        # Query for total count
        total_query = "SELECT COUNT(*) as total FROM targets"
        total_result = await db.fetchrow(total_query)
        total = total_result["total"]

        # Format results
        targets = [
            {
                "id": result["id"],
                "target_name": result["target_name"],
                "target_number": result["target_number"],
                "file_number": result["file_number"],
                "folder": result["folder"],
                "offence_name": result["offence_name"],
                "operator_name": result["operator_name"],
                "type": result["type"],
                "origin": result["origin"],
                "target_date": result["target_date"],
                "metadata": json.loads(result["metadata"]),
                "threat_level": result["threat_level"],
                "flagged": result["flagged"],
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat(),
            }
            for result in results
        ]

        return targets, total

    async def update_target(self, target_id: int, target_data: dict):
        update_data = {k: v for k, v in target_data.items() if v is not None}
        if not update_data:
            raise HTTPException(
                status_code=400, detail="No data provided for update"
            )
        if "metadata" in update_data:
            update_data["metadata"] = json.dumps(update_data["metadata"])
            validate_target_data(update_data["threat_level"])

        set_clause = ", ".join(
            f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())
        )
        values = list(update_data.values())
        values.insert(0, target_id)
        query = f"""
            UPDATE targets 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            RETURNING *
        """
        result = await db.fetchrow(query, *values)
        if not result:
            raise HTTPException(status_code=404, detail="Target not found")
        return self._format_target(result)

    async def delete_target(self, target_id: int):
        query = "DELETE FROM targets WHERE id = $1 RETURNING id"
        result = await db.fetchrow(query, target_id)
        if not result:
            raise HTTPException(status_code=404, detail="Target not found")
        return {"message": f"Target {target_id} deleted"}

    async def search_targets(
        self,
        target_name: str = None,
        target_number: str = None,
        skip: int = 0,
        limit: int = 10,
    ):
        conditions = []
        params = []
        param_count = 1

        if target_name:
            conditions.append(f"target_name ILIKE ${param_count}")
            params.append(f"%{target_name}%")
            param_count += 1
        if target_number:
            conditions.append(f"target_number ILIKE ${param_count}")
            params.append(f"%{target_number}%")
            param_count += 1

        where_clause = " AND ".join(conditions) if conditions else "TRUE"

        count_query = f"SELECT COUNT(*) FROM targets WHERE {where_clause}"

        total = await db.fetchval(count_query, *params[: param_count - 1])

        query = f"""
            SELECT
                t.id, t.target_name, t.file_number, t.target_number, t.folder, 
                o.name as offence_name, op.operator_name, 
                t.type, t.origin, t.target_date, t.metadata, t.threat_level, t.flagged,  
                t.created_at, t.updated_at
            FROM targets t
            LEFT JOIN offences o ON t.offence_id = o.id
            LEFT JOIN operators op ON t.operator_id = op.id
            WHERE {where_clause}
            ORDER BY t.created_at DESC
            OFFSET ${param_count} LIMIT ${param_count + 1}
        """

        params.extend([skip, limit])
        results = await db.fetch(query, *params)
        print("result", results)  # Debugging

        data = [
            {
                "id": result["id"],
                "target_name": result["target_name"],
                "target_number": result["target_number"],
                "file_number": result["file_number"],
                "folder": result["folder"],
                "offence_name": result["offence_name"],
                "operator_name": result["operator_name"],
                "type": result["type"],
                "origin": result["origin"],
                "target_date": result[
                    "target_date"
                ].isoformat(),  # Convert to string
                "metadata": json.loads(result["metadata"]),
                "threat_level": result["threat_level"],
                "flagged": result["flagged"],
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat(),
            }
            for result in results
        ]

        base_url = f"/targets/search/?target_name={target_name or ''}&number={target_number or ''}"
        next_page = (
            f"{base_url}&skip={skip + limit}&limit={limit}"
            if skip + limit < total
            else None
        )
        previous_page = (
            f"{base_url}&skip={max(0, skip - limit)}&limit={limit}"
            if skip > 0
            else None
        )

        return {
            "data": data,
            "total": total,
            "next_page": next_page,
            "previous_page": previous_page,
        }

    async def flag_target(self, target_id: int, flagged: bool):
        query = """
            UPDATE targets 
            SET flagged = $2, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            RETURNING *
        """
        result = await db.fetchrow(query, target_id, flagged)
        if not result:
            raise HTTPException(status_code=404, detail="Target not found")
        return self._format_target(result)

    def _format_target(self, result):
        return {
            "id": result["id"],
            "target_name": result["target_name"],
            "file_number": result["file_number"],
            "target_number": result["target_number"],
            "folder": result["folder"],
            "offence_id": result["offence_id"],
            "operator_id": result["operator_id"],
            "type": result["type"],
            "origin": result["origin"],
            "target_date": result["target_date"].isoformat(),
            "metadata": json.loads(result["metadata"]),
            "flagged": result["flagged"],
            "threat_level": result["threat_level"],  # New field
            "created_at": result["created_at"].isoformat(),
            "updated_at": result["updated_at"].isoformat(),
        }
