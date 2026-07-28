from typing import Any, get_type_hints, get_origin, Annotated, get_args

from src.main.api.generators.creation_rule import CreationRule


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            else:
                value = RandomModelGenerator._generate_value(actual_type)

            init_data[field_name] = value

        return cls(**init_data)


    @staticmethod
    def _generate_from_regex(regex_str: str, actual_type: type) -> Any:
