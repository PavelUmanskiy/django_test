from django import template


register = template.Library()


@register.filter
def string_split(string_: str, delimiter: str) -> list[str]:
    list_ = string_.split(delimiter)
    return list_