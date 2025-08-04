from django import template
from django.utils import timezone
import math

register = template.Library()

@register.filter
def format_number(value):
    """
    Format number with spaces between groups of 3 digits.
    Example: 50000 -> 50 000
    """
    if value is None:
        return ''
    try:
        # Convert to string and remove any existing spaces
        num_str = str(int(value))
        # Reverse the string to process from right to left
        reversed_str = num_str[::-1]
        # Split into groups of 3 and join with spaces
        groups = [reversed_str[i:i+3] for i in range(0, len(reversed_str), 3)]
        # Join groups and reverse back
        formatted = '.'.join(groups)[::-1]
        return formatted
    except (ValueError, TypeError):
        return value

@register.filter

def split_by_newline(value):
    """
    Split the input string by newline character and return a list of strings.
    """
    if value is None:
        return []
    return [line.strip() for line in value.split('\n') if line.strip()]

@register.filter
def format_page_title(value):
    """
    Format page title by replacing underscores with spaces and capitalizing each word.
    Example: 'user_management' -> 'User Management'
    """
    if value is None:
        return ''
    else:
        value = value.replace('_', ' ')
        return value.title()

@register.filter
def days_left(expired_date):
    """
    Trả về số ngày còn lại tính từ thời điểm hiện tại đến ngày hết hạn.
    Nếu đã hết hạn, trả về 0.
    """
    if not expired_date:
        return 0
    now = timezone.now()
    delta = expired_date - now
    total_seconds = delta.total_seconds()
    if total_seconds <= 0:
        return 0
    return math.ceil(total_seconds / (24 * 60 * 60))