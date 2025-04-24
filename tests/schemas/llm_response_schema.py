pipeline_response_schema = {
    "type": "object",
    "properties": {
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "line_number", "segment_index", "original_text", "translated_text",
                    "segment_type", "speaker", "character_type", "gender", "emotion"
                ],
                "properties": {
                    "line_number": {"type": "integer"},
                    "segment_index": {"type": "integer"},
                    "original_text": {"type": "string"},
                    "translated_text": {"type": "string"},
                    "segment_type": {"enum": ["narration", "dialogue", "highlight"]},
                    "speaker": {"type": "string"},
                    "character_type": {"enum": [
                        "narrator", "protagonist", "supporting_male",
                        "supporting_female", "system", "unknown"
                    ]},
                    "gender": {"enum": ["male", "female", "unknown"]},
                    "emotion": {"enum": [
                        "neutral", "joy", "anger", "surprise", "hesitation", "shout"
                    ]}
                }
            }
        }
    },
    "required": ["segments"]
}


scenario_response_schema = {
    "type": "object",
    "properties": {
        "scenarios": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["index", "text"],
                "properties": {
                    "index": {"type": "integer"},
                    "text": {"type": "string"},
                    "location": {"type": ["string", "null"]},
                    "characters": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": []
                    }
                }
            }
        }
    },
    "required": ["scenarios"]
}
