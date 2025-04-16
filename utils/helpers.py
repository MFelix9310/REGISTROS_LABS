from datetime import datetime

def format_date(date):
    """Formatea una fecha a formato dd/mm/aaaa"""
    if not date:
        return ""
    return date.strftime("%d/%m/%Y")

def format_time(time):
    """Formatea una hora a formato hh:mm"""
    if not time:
        return ""
    return time.strftime("%H:%M")

def parse_date(date_str):
    """Convierte una cadena dd/mm/aaaa a objeto date"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        return None

def parse_time(time_str):
    """Convierte una cadena hh:mm a objeto time"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None 