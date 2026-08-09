"""
helper/crud.py

Simple, easy-to-use helper functions to perform CRUD
(Create, Read, Update, Delete) operations on JSON files.

Each JSON file is expected to store a LIST of dictionaries (records),
where each record has a unique "id" field. Example structure:

[
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30}
]
"""

import json
import os
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Internal / low-level helpers
# ---------------------------------------------------------------------------

def _ensure_file_exists(file_path: str) -> None:
    """
    Make sure the JSON file (and its parent folder) exists.
    If it doesn't exist, create it with an empty list [] as content.
    """
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def read_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Read and return the full contents of a JSON file as a list of dicts.
    Returns an empty list if the file doesn't exist or is empty/corrupted.
    """
    _ensure_file_exists(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        # File exists but has invalid/corrupted JSON
        return []


def write_json(file_path: str, data: List[Dict[str, Any]]) -> None:
    """
    Overwrite the JSON file with the given list of dicts.
    """
    _ensure_file_exists(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def _generate_new_id(data: List[Dict[str, Any]]) -> int:
    """
    Generate a new unique integer id for a record.
    Takes the current max id in the list and adds 1.
    If the list is empty, starts at 1.
    """
    if not data:
        return 1
    existing_ids = [record.get("id", 0) for record in data]
    return max(existing_ids) + 1


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def create_record(file_path: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """
    CREATE: Add a new record to the JSON file.

    - If the record doesn't have an "id", one is auto-generated.
    - Returns the record that was actually inserted (with its id).
    """
    data = read_json(file_path)

    if "id" not in record:
        record["id"] = _generate_new_id(data)

    data.append(record)
    write_json(file_path, data)
    return record


def read_all_records(file_path: str) -> List[Dict[str, Any]]:
    """
    READ (all): Return every record stored in the JSON file.
    """
    return read_json(file_path)


def read_record(file_path: str, record_id: Any) -> Optional[Dict[str, Any]]:
    """
    READ (one): Return a single record matching the given id.
    Returns None if no record with that id is found.
    """
    data = read_json(file_path)
    for record in data:
        if record.get("id") == record_id:
            return record
    return None


def update_record(file_path: str, record_id: Any, updated_fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    UPDATE: Modify an existing record identified by record_id.

    - updated_fields is a dict of the fields you want to change,
      e.g. {"age": 26}. Only those fields are updated; everything
      else in the record stays the same.
    - Returns the updated record, or None if no record was found.
    """
    data = read_json(file_path)

    for record in data:
        if record.get("id") == record_id:
            record.update(updated_fields)
            write_json(file_path, data)
            return record

    return None  # record_id not found


def delete_record(file_path: str, record_id: Any) -> bool:
    """
    DELETE: Remove a record identified by record_id.

    Returns True if a record was deleted, False if no matching record was found.
    """
    data = read_json(file_path)
    new_data = [record for record in data if record.get("id") != record_id]

    if len(new_data) == len(data):
        return False  # nothing was deleted

    write_json(file_path, new_data)
    return True


def delete_all_records(file_path: str) -> None:
    """
    DELETE (all): Wipe the JSON file clean, leaving an empty list.
    """
    write_json(file_path, [])