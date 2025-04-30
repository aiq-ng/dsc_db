from datetime import date, datetime, time
from decimal import Decimal

from asyncpg import Record
from fastapi.responses import JSONResponse


def serialize_data(obj):
    if isinstance(obj, dict):
        return {key: serialize_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_data(item) for item in obj]
    elif isinstance(obj, Record):
        return {key: serialize_data(value) for key, value in obj.items()}
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, time):
        return obj.strftime("%H:%M:%S")
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


def format_response(data, status_code=200, message="success"):
    content = {}

    if message is not None:
        content["message"] = message

    def filter_none(value):
        if isinstance(value, dict):
            return {
                k: filter_none(v) for k, v in value.items() if v is not None
            }
        elif isinstance(value, list):
            return [filter_none(item) for item in value if item is not None]
        else:
            return value

    if isinstance(data, dict):
        extracted_data = data.get("data", data)
        meta = data.get("meta")

        content["data"] = (
            serialize_data(filter_none(extracted_data))
            if extracted_data
            else []
        )

        if meta:
            content["meta"] = serialize_data(filter_none(meta))

    elif isinstance(data, list):
        content["data"] = serialize_data(filter_none(data)) if data else []

    else:
        content["data"] = (
            serialize_data(filter_none(data)) if data is not None else []
        )

    return JSONResponse(content=content, status_code=status_code)
