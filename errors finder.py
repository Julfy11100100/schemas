from jsonschema import validate
from jsonschema.exceptions import ValidationError
import os
import json


def validation(instance, result, file, schema):
    """
    Поиск ошибок в instance по schema.
    Запись в result[file]
    """
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as err:
        message = err.message
        if message.find("is a required property") != -1:
            message = "field " + message.split()[0] + " must be filled"
        elif message.find("is not of type") != -1:
            message = "field " + message.split()[0] + " must be filled"
        result[file].append(message)

result = {}
cmarker_created = {"type": "object", "$schema": "http://json-schema.org/schema#", "required": ["cmarkers", "datetime", "user_id"], "properties": {"user_id": {"type": "integer"}, "cmarkers": {"type": "array", "items": {"type": ["object", "string"], "required": ["date", "id", "slug"], "properties": {"id": {"type": "integer"}, "date": {"type": "string"}, "slug": {"type": "string"}}}}, "datetime": {"type": "string"}}}
label_selected = {"type": "object", "$schema": "http://json-schema.org/schema#", "required": ["id", "labels", "rr_id", "timestamp", "unique_id", "user", "user_id"], "properties": {"id": {"type": ["null", "integer"]}, "user": {"type": "object", "required": ["id"], "properties": {"id": {"type": "integer"}}}, "rr_id": {"type": ["null", "integer"]}, "labels": {"type": "array", "items": {"type": "object", "required": ["category", "color", "is_custom_tag", "name_en", "name_ru", "property_arousal", "property_pleasure", "property_stability", "property_vitality", "property_where", "slug", "type", "type_stress"], "properties": {"slug": {"type": "string"}, "type": {"type": "integer"}, "color": {"type": ["null", "object"]}, "name_en": {"type": "string"}, "name_ru": {"type": "string"}, "category": {"type": ["null", "string"]}, "type_stress": {"type": "integer"}, "is_custom_tag": {"type": "boolean"}, "property_where": {"type": ["string", "null"]}, "property_arousal": {"type": ["string", "null"]}, "property_pleasure": {"type": ["string", "null"]}, "property_vitality": {"type": ["string", "null"]}, "property_stability": {"type": ["string", "null"]}}}}, "user_id": {"type": "integer"}, "timestamp": {"type": "string"}, "unique_id": {"type": "string"}}}
sleep_created = {"type": "object", "$schema": "http://json-schema.org/schema#", "required": ["source", "timestamp", "finish_time", "activity_type", "time_start", "unique_id"], "properties": {"info": {"type": "array", "items": {"type": "object", "required": ["type", "value"], "properties": {"type": {"type": "string"}, "value": {"type": "number"}}}}, "points": {"type": "array", "items": {"type": "object", "required": ["x_date", "y_value"], "properties": {"x_date": {"type": "string"}, "y_value": {"type": "number"}}}}, "source": {"type": "string"}, "timestamp": {"type": "string"}, "unique_id": {"type": "string"}, "time_start": {"type": "string"}, "finish_time": {"type": "string"}, "phases_info": {"type": "array", "items": {"type": "object", "required": ["duration", "percent", "type"], "properties": {"type": {"type": "string"}, "percent": {"type": "number"}, "duration": {"type": "number"}}}}, "type_ranges": {"type": "array", "items": {"type": "object", "required": ["date", "type"], "properties": {"date": {"type": "string"}, "type": {"type": "string"}}}}, "activity_type": {"type": "string"}}}
workout_created = {"type": "object", "$schema": "http://json-schema.org/schema#", "required": ["activity_name", "activity_type", "source", "time_end", "time_start", "timestamp", "unique_id"], "properties": {"met": {"type": "number"}, "pulse": {"type": "integer"}, "steps": {"type": "integer"}, "source": {"type": "string"}, "calories": {"type": "integer"}, "distance": {"type": "integer"}, "duration": {"type": "number"}, "pace_avg": {"type": "number"}, "time_end": {"type": "string"}, "pulse_max": {"type": ["null", "integer"]}, "pulse_min": {"type": ["null", "integer"]}, "speed_avg": {"type": "number"}, "timestamp": {"type": "string"}, "unique_id": {"type": "string"}, "resting_hr": {"type": "integer"}, "time_start": {"type": "string"}, "type_ranges": {"type": "object", "required": ["cardio", "fat_burn", "hardcore", "warm_up"], "properties": {"cardio": {"type": "integer"}, "warm_up": {"type": "integer"}, "fat_burn": {"type": "integer"}, "hardcore": {"type": "integer"}}}, "activity_name": {"type": "string"}, "activity_type": {"type": "string"}, "exercise_time": {"type": "integer"}, "calories_basal": {"type": "number"}, "calories_active": {"type": "number"}, "steps_speed_avg": {"type": "number"}, "steps_speed_max": {"type": "number"}}}

event_dir = os.getcwd() + "\\" + "event\\"
files = os.listdir(event_dir)

for file in files:
    with open(event_dir + file, "r") as current_file:
        try:
            file_content = json.loads(current_file.read())
            data = file_content["data"]
            event = file_content["event"]
            result[file] = []
            if event == "cmarker_created":
                validation(data, result, file, cmarker_created)
            elif event == "label_selected":
                validation(data, result, file, label_selected)
            elif event == "sleep_created":
                validation(data, result, file, sleep_created)
            elif event == "workout_created":
                validation(data, result, file, workout_created)
            else:
                result[file].append("Incorrect event title \'" + event + "\' in schema")

        except (json.JSONDecodeError, AttributeError, KeyError, TypeError):
            pass

for res in result:
    print(result[res])

