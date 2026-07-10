import re

from django.core.exceptions import ValidationError


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def parse_datatables_params(request):
    params = request.POST
    draw = int(params.get('draw', 1))
    start = int(params.get('start', 0))
    length = int(params.get('length', 25))
    search_value = params.get('search[value]', '').strip()
    order_column_index = int(params.get('order[0][column]', 0))
    order_dir = params.get('order[0][dir]', 'asc')

    columns_data = []
    i = 0
    while f'columns[{i}][data]' in params:
        columns_data.append({
            'data': params.get(f'columns[{i}][data]'),
            'name': params.get(f'columns[{i}][name]'),
            'searchable': params.get(f'columns[{i}][searchable]') == 'true',
            'orderable': params.get(f'columns[{i}][orderable]') == 'true',
        })
        i += 1

    return {
        'draw': draw,
        'start': start,
        'length': length,
        'search_value': search_value,
        'order_column_index': order_column_index,
        'order_dir': order_dir,
        'columns_data': columns_data,
    }


def extract_validation_error(e):
    """Extrae un string legible de cualquier ValidationError (string, dict o lista)."""
    if not isinstance(e, ValidationError):
        return str(e)
    if isinstance(e.message, str):
        return e.message
    if isinstance(e.message, dict):
        for field_errors in e.message.values():
            for err in field_errors:
                return str(err)
    if isinstance(e.message, (list, tuple)):
        return str(e.message[0]) if e.message else 'Error de validación.'
    return str(e.message)


def normalizar_nombre(valor):
    """Convierte a Title Case preservando acrónimos técnicos comunes (HP, IP, USB...)."""
    if not valor or not isinstance(valor, str):
        return valor
    palabras = valor.strip().split()
    if not palabras:
        return ''
    ACRONIMOS = {
        'hp', 'ip', 'pc', 'pci', 'usb', 'hdmi', 'dvi', 'vga', 'lcd', 'led',
        'cpu', 'ram', 'ssd', 'hdd', 'dvd', 'lan', 'wan', 'vlan', 'vpn',
        'dns', 'dhcp', 'http', 'ftp', 'smtp', 'ssl', 'tls', 'ssh', 'snmp',
        'ntp', 'bios', 'uefi', 'raid', 'san', 'nas', 'poe', 'ups', 'pdu',
        'acl', 'nat', 'mac', 'poe', 'wifi', 'nfc', 'rfid', '3m',
    }
    resultado = []
    for p in palabras:
        if p.lower() in ACRONIMOS:
            resultado.append(p.upper())
        else:
            resultado.append(p.capitalize())
    return ' '.join(resultado)


def normalizar_codigo(valor):
    """Convierte a UPPERCASE, sin espacios y sin tildes."""
    if not valor or not isinstance(valor, str):
        return valor
    valor = valor.strip().upper()
    valor = re.sub(r'\s+', '', valor)
    return valor
