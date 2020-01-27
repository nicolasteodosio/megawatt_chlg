report_schema = {
    "type": "object",
    "properties": {
        "plant_id": {"type": "string", "pattern": "^[0-9]*[1-9][0-9]*$"},
        "type": {"type": "string", "enum": ["Energy", "Irradiation"]},
        "date": {"type": "string", "pattern": "^\\d{4}\\-\\d{2}\\-\\d{2}$"}
    }
}