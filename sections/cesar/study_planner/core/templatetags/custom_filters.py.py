# Core application package


from django import template
   
register = template.Library()

@register.filter(name='abs')
def absolute_value(value):
    """
    Returns the absolute value of a number.
    """
    try:
        if value is None:
            return value
        return abs(int(value))
    except (ValueError, TypeError):
        return value