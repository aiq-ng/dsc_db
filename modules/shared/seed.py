from modules.shared.db import db
import json

# Seed data for offences
OFFENCES_SEED_DATA = [
    {"name": "Espionage", "description": "Unauthorized acquisition of sensitive information"},
    {"name": "Terrorism", "description": "Acts intended to cause fear or harm for political purposes"},
    {"name": "Sabotage", "description": "Deliberate destruction of property or infrastructure"},
    {"name": "Cybercrime", "description": "Criminal activities carried out via digital means"},
]

# Seed data for operators
OPERATORS_SEED_DATA = [
    {
        "operator_name": "Agent Smith",
        "operator_code": "OP-001",
        "contact_info": {"email": "smith@agency.gov", "phone": "555-0101"},
        "active": True
    },
    {
        "operator_name": "Agent Jones",
        "operator_code": "OP-002",
        "contact_info": {"email": "jones@agency.gov", "phone": "555-0102"},
        "active": True
    },
    {
        "operator_name": "Agent Brown",
        "operator_code": "OP-003",
        "contact_info": {"email": "brown@agency.gov", "phone": "555-0103"},
        "active": False
    },
]

async def seed_table_if_empty(table_name: str, seed_data: list, query: str):
    """Seed a table with data if it exists and is empty."""
    # Check if table exists
    table_exists_query = """
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' AND tablename = $1
        )
    """
    table_exists = await db.fetchrow(table_exists_query, table_name)
    
    if table_exists and table_exists["exists"]:
        # Check row count
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        count_result = await db.fetchrow(count_query)
        
        if count_result and count_result["count"] == 0:
            # Seed the table
            for data in seed_data:
                if "contact_info" in data:
                    # Convert contact_info to JSON for operators
                    data["contact_info"] = json.dumps(data["contact_info"])
                values = tuple(data.values())
                await db.execute(query, *values)
            print(f"Seeded {table_name} with {len(seed_data)} rows")
        else:
            print(f"Skipping seeding {table_name}: table is not empty")
    else:
        print(f"Skipping seeding {table_name}: table does not exist")

async def seed_data():
    """Run seeding for all tables."""
    # Seed offences
    offences_query = """
        INSERT INTO offences (name, description) 
        VALUES ($1, $2)
    """
    await seed_table_if_empty("offences", OFFENCES_SEED_DATA, offences_query)

    # Seed operators
    operators_query = """
        INSERT INTO operators (operator_name, operator_code, contact_info, active) 
        VALUES ($1, $2, $3, $4)
    """
    await seed_table_if_empty("operators", OPERATORS_SEED_DATA, operators_query)