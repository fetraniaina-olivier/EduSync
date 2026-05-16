# app/mappers/school_to_ministry.py
"""
Traduit les payloads reçus de l'École vers le format attendu par le Ministère.
Gère les différences de nommage, les valeurs manquantes et la logique de fallback.
"""
from typing import Any, Callable, Dict

def map_student_payload(school_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Traduit le format École → format Ministère pour un étudiant."""
    # Fallback intelligent si l'école envoie un seul champ "name"
    full_name = school_payload.get("name", "")
    if " " in full_name:
        first_name, last_name = full_name.split(" ", 1)
    else:
        first_name, last_name = full_name, "Inconnu"

    return {
        "first_name": school_payload.get("first_name") or first_name,
        "last_name": school_payload.get("last_name") or last_name,
        "birth_date": school_payload.get("birth_date") or school_payload.get("dob"),
        "enrollment_date": school_payload.get("enrollment_date") or school_payload.get("start_date"),
    }

def map_teacher_payload(school_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Traduit le format École → format Ministère pour un enseignant."""
    full_name = school_payload.get("name", "")
    if " " in full_name:
        first_name, last_name = full_name.split(" ", 1)
    else:
        first_name, last_name = full_name, "Inconnu"

    return {
        "first_name": school_payload.get("first_name") or first_name,
        "last_name": school_payload.get("last_name") or last_name,
        "subject": school_payload.get("subject") or school_payload.get("discipline"),
        "hire_date": school_payload.get("hire_date") or school_payload.get("start_date"),
    }

# Registre centralisé des mappers
ENTITY_MAPPERS: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "student": map_student_payload,
    "teacher": map_teacher_payload,
}

def get_mapper(entity_type: str) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Retourne le mapper approprié ou lève une erreur si le type est inconnu."""
    mapper = ENTITY_MAPPERS.get(entity_type.lower())
    if not mapper:
        supported = ", ".join(ENTITY_MAPPERS.keys())
        raise ValueError(f"Type d'entité non supporté: '{entity_type}'. Types acceptés: {supported}")
    return mapper