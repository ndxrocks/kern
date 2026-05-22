"""Kern prompt generation — replaces Kern's JSON Schema with flat templates.

The key difference: instead of dumping model_json_schema() (which produces
$defs, properties, anyOf, allOf chains that confuse small models), Kern
generates a simple fill-in-the-blanks template that any model can follow.
"""

import json
import types as _types
from typing import Literal, Type, Union, get_args, get_origin

from pydantic import BaseModel

from kern.utils.log import log_warning

# ── Template generation ───────────────────────────────────────────

_TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    type(None): "null",
}


def _resolve_union(args) -> str | dict | list:
    """Resolve a Union's args into a template-friendly representation."""
    model_args = [a for a in args if isinstance(a, type) and issubclass(a, BaseModel)]
    non_model_args = [a for a in args if a not in model_args]

    # Optional[Model] → just show the model template
    if len(model_args) == 1 and len(non_model_args) == 1 and non_model_args[0] is type(None):
        return _model_structure(model_args[0])

    # Union of models → list of alternative templates
    parts: list = []
    for a in model_args:
        parts.append(_model_structure(a))
    for a in non_model_args:
        parts.append(_TYPE_MAP.get(a, _resolve_type(a)))

    if len(parts) == 1:
        return parts[0]
    return parts


def _resolve_type(tp) -> str | dict | list:
    origin = get_origin(tp)

    # Literal — show allowed values
    if origin is Literal:
        vals = get_args(tp)
        return "|".join(repr(v) if isinstance(v, str) else str(v) for v in vals)

    # Union / Optional
    if origin is Union or origin is _types.UnionType or isinstance(tp, _types.UnionType):
        return _resolve_union(get_args(tp))

    # list[Something]
    if origin is list:
        inner = get_args(tp)[0]

        # list[Model] → [model_template]
        if isinstance(inner, type) and issubclass(inner, BaseModel):
            return [_model_structure(inner)]

        # list[Union[A, B]] → [template_A, template_B] — flat, not nested
        inner_origin = get_origin(inner)
        if inner_origin is Union or inner_origin is _types.UnionType or isinstance(inner, _types.UnionType):
            union_result = _resolve_union(get_args(inner))
            # If union resolved to a list of alternatives, spread them as list items
            if isinstance(union_result, list):
                return union_result
            return [union_result]

        return [_TYPE_MAP.get(inner, _resolve_type(inner))]

    # Nested model
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        return _model_structure(tp)

    return _TYPE_MAP.get(tp, str(tp))


def _model_structure(model: Type[BaseModel]) -> dict:
    return {name: _resolve_type(f.annotation) for name, f in model.model_fields.items()}


def _model_descriptions(model: Type[BaseModel]) -> dict:
    result = {}
    for name, field in model.model_fields.items():
        if field.description:
            result[name] = field.description
        tp = field.annotation
        origin = get_origin(tp)

        # Collect BaseModel types from any annotation (direct, Union, list, etc.)
        model_types = []
        if isinstance(tp, type) and issubclass(tp, BaseModel):
            model_types.append(tp)
        elif origin is list:
            inner = get_args(tp)[0]
            if isinstance(inner, type) and issubclass(inner, BaseModel):
                model_types.append(inner)
        elif origin is Union or origin is _types.UnionType or isinstance(tp, _types.UnionType):
            for a in get_args(tp):
                if isinstance(a, type) and issubclass(a, BaseModel):
                    model_types.append(a)

        for mt in model_types:
            nested = _model_descriptions(mt)
            if nested:
                existing = result.get(name, {})
                if isinstance(existing, str):
                    existing = {"_": existing}
                existing.update(nested)
                result[name] = existing
    return result


# ── Public API ────────────────────────────────────────────────────


def get_json_output_prompt(output_schema: Union[str, list, dict, Type[BaseModel], BaseModel]) -> str:
    """Return a small-model-friendly template prompt instead of JSON Schema.

    For Pydantic models, this generates a flat template like:
        {"title": "string", "questions": [{"question": "string", "options": ["string"]}]}
    Instead of the full $defs/properties/anyOf JSON Schema tree.
    """
    if output_schema is None:
        return "Provide the output as JSON.\nStart with `{` and end with `}`."

    # Plain string / list / dict — pass through
    if isinstance(output_schema, (str, list)):
        template = output_schema if isinstance(output_schema, str) else json.dumps(output_schema)
        return (
            f"Provide your output as JSON.\n\n"
            f"JSON structure:\n{template}\n\n"
            f"Start your response with `{{` and end it with `}}`.\n"
            f"Your output will be passed to json.loads(). Only valid JSON."
        )

    if isinstance(output_schema, dict):
        return (
            f"Provide your output as JSON.\n\n"
            f"JSON structure:\n{json.dumps(output_schema)}\n\n"
            f"Start your response with `{{` and end it with `}}`.\n"
            f"Your output will be passed to json.loads(). Only valid JSON."
        )

    # Pydantic model — use Kern template instead of JSON Schema
    if (isinstance(output_schema, type) and issubclass(output_schema, BaseModel)) or isinstance(
        output_schema, BaseModel
    ):
        schema_cls = output_schema if isinstance(output_schema, type) else type(output_schema)

        template = _model_structure(schema_cls)
        template_str = json.dumps(template, indent=2)

        descs = _model_descriptions(schema_cls)
        descs_str = json.dumps(descs, indent=2) if descs else ""

        prompt = (
            "CRITICAL: Respond with ONLY valid JSON. No markdown, no code blocks, no explanation.\n\n"
            f"JSON structure (replace type placeholders with actual values):\n{template_str}\n"
        )

        if descs_str:
            prompt += f"\nField descriptions:\n{descs_str}\n"

        prompt += (
            "\nStart with { and end with }.\n"
            "Your output will be passed to json.loads(). Only valid JSON."
        )
        return prompt

    log_warning(f"Could not build prompt for {output_schema}")
    return "Provide the output as JSON.\nStart with `{` and end with `}`."


def get_response_model_format_prompt(output_schema: Type[BaseModel]) -> str:
    """Return the format prompt for the response model."""
    message = "Make sure your response is a valid string (NOT JSON) that mentions the following topics:"

    for field_name, field_info in output_schema.model_fields.items():
        description = field_info.description or ""
        if description:
            message += f"\n- {field_name}: {description}"
        else:
            message += f"\n- {field_name}"

    return message
