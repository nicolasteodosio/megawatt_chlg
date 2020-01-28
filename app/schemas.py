report_schema = {
    "type": "object",
    "properties": {
        "plant_id": {"type": "string", "pattern": "^[0-9]*[1-9][0-9]*$"},
        "type": {"type": "string", "enum": ["Energy", "Irradiation"]},
        "date": {"type": "string", "pattern": "^\\d{4}\\-\\d{2}\\-\\d{2}$"}
    },
    "required": ["plant_id",  "type", "date"]
}

monitoring_schema = {
    "type": "object",
    "properties": {
        "plant": {"type": "string"},
        "date_end": {"type": "string", "pattern": "^\\d{4}\\-\\d{2}\\-\\d{2}$"},
        "date_start": {"type": "string", "pattern": "^\\d{4}\\-\\d{2}\\-\\d{2}$"}
    },
    "required": ["plant",  "date_end", "date_start"]
}