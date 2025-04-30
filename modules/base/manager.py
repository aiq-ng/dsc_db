from datetime import datetime

from fastapi import HTTPException

from modules.shared.db import db


class BaseManager:

    async def get_all_resources(self):
        """
        Fetch all resources from the database.
        """
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """

        result = await db.fetch(query)

        return [table["table_name"] for table in result]

    async def create_data(self, table: str, data, returning: list = None):
        """
        Create new records in the database in bulk.
        """
        if not isinstance(data, list):
            data = [data]

        try:
            for record in data:
                record["created_at"] = datetime.now()

            allowed_fields = await self._get_table_columns(table)

            filtered_data = [
                await self.filter_valid_fields(record, allowed_fields)
                for record in data
            ]

            if not filtered_data:
                raise HTTPException(
                    status_code=400,
                    detail="No valid fields provided for insertion.",
                )

            columns = ", ".join(filtered_data[0].keys())

            placeholders = []
            for i in range(len(filtered_data)):
                offset = i * len(filtered_data[0])
                placeholder_values = [
                    f"${offset + j + 1}" for j in range(len(filtered_data[0]))
                ]
                placeholders.append(f"({', '.join(placeholder_values)})")

            values_placeholder = ", ".join(placeholders)

            values = [
                value for record in filtered_data for value in record.values()
            ]

            if returning is None:
                returning = ["id"]

            returning_clause = (
                f"RETURNING {', '.join(returning)}" if returning else ""
            )

            query = f"""
                INSERT INTO {table} ({columns})
                VALUES {values_placeholder}
                {returning_clause}
            """

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create data: {e}",
            )

        return await db.execute(query, *values)

    async def update_data(self, table, record_id, data):
        """
        Update a record in the database.
        """

        data["updated_at"] = datetime.now()

        try:
            data["updated_at"] = datetime.now()
            allowed_fields = await self._get_table_columns(table)
            filtered_data = await self.filter_valid_fields(
                data, allowed_fields
            )

            set_values = ", ".join(
                f"{key}=${i + 2}" for i, key in enumerate(filtered_data.keys())
            )
            query = f"""
                UPDATE {table}
                SET {set_values}
                WHERE id = $1
                RETURNING *
            """
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update data: {e}",
            )

        await db.fetchrow(query, [record_id] + list(filtered_data.values()))

    async def delete_data(self, table, record_ids: list):
        """
        Delete multiple records from the database.
        """

        try:
            if not record_ids:
                return False

            placeholders = ", ".join(
                f"${i + 1}" for i in range(len(record_ids))
            )
            query = f"""
                DELETE FROM {table} WHERE id IN ({placeholders}) RETURNING id
                """

            return await db.fetch(query, tuple(record_ids))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete data: {e}",
            )

    async def get_data(
        self, table, filters: dict = None, columns: list = None
    ):
        """
        Fetch records from the database with optional filtering, sorting,
        pagination, and column selection.
        """

        filters = filters or {}
        columns = columns or ["*"]
        id = filters.get("id")

        if id is not None:
            query = f"SELECT {', '.join(columns)} FROM {table} WHERE id = $1"
            result = await db.fetchrow(query, int(id))

            return result if result else None

        allowed_fields = await self._get_table_columns(table)
        page = int(filters.get("page", 1))
        page_size = int(filters.get("page_size", 10))

        sort_by = filters.get("sort_by") or "priority"
        order_by = filters.get("order_by") or "ASC"
        if sort_by == "priority" and sort_by not in allowed_fields:
            sort_by = "updated_at"
            order_by = "DESC"

        allowed_sort_columns = {
            "id",
            "name",
            "created_at",
            "priority",
            "updated_at",
        }
        sort_by = sort_by if sort_by in allowed_sort_columns else "updated_at"
        order_by = "DESC" if order_by.upper() == "DESC" else "ASC"

        conditions, params = [], []

        for idx, (key, value) in enumerate(filters.items()):
            if key in {"page", "page_size", "sort_by", "order_by"}:
                continue
            conditions.append(f"t.{key} = ${idx + 1}")
            params.append(value)

        query_conditions = " AND ".join(conditions) if conditions else "1=1"

        count_query = (
            f"SELECT COUNT(*) AS total FROM {table} t WHERE {query_conditions}"
        )
        total_count = await self._get_count(count_query, params)

        offset = (page - 1) * page_size
        query = f"""
            SELECT {", ".join(columns)}
            FROM {table} t
            WHERE {query_conditions}
            ORDER BY t.{sort_by} {order_by}, t.updated_at ASC
            LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        params.extend([page_size, offset])

        try:
            results = await db.fetch(query, *params)
            return await self._pagination_response(
                results, total_count, page, page_size
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch data: {e}",
            )

    async def _get_table_columns(self, table_name: str):
        """
        Fetch column names for a given table from the database.
        """
        try:
            query = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = $1
            """
            rows = await db.fetch(query, table_name)
            return {row["column_name"] for row in rows}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch table columns for '{table_name}'",
            ) from e

    async def _get_count(self, query, params):
        try:
            total_data = await db.fetchrow(query, *params)
            return total_data["total"] if total_data else 0
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch count: {e}",
            ) from e

    async def filter_valid_fields(self, data: dict, allowed_fields: set):
        """
        Filter incoming data to match allowed fields.
        """
        filtered_data = {
            k: v
            for k, v in data.items()
            if k in allowed_fields and v is not None
        }

        if not filtered_data:
            raise ValueError("No valid fields provided for insertion.")

        return filtered_data

    async def _pagination_response(self, data, total_count, page, page_size):
        try:
            total_pages = (total_count // page_size) + (
                1 if total_count % page_size > 0 else 0
            )
            total_pages = max(total_pages, 1) if total_count > 0 else 0

            return {
                "data": data,
                "meta": {
                    "page": page,
                    "page_size": page_size,
                    "total": total_count,
                    "total_pages": total_pages,
                },
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch pagination response: {e}",
            ) from e
