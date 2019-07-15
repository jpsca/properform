import re


__all__ = ("type_hex_color", )

rx_colors = re.compile(
    r'#?(?P<hex>[0-9a-f]{3,8})|'
    r'rgba?\((?P<r>[0-9]+)\s*,\s*(?P<g>[0-9]+)\s*,\s*(?P<b>[0-9]+)'
    r'(?:\s*,\s*(?P<a>[0-9\.]+))?\)',
    re.IGNORECASE
)


def type_hex_color(value):
    value = value.strip().replace(' ', '').lower()
    m = rx_colors.match(value)
    if not m:
        return None
    md = m.groupdict()
    if md['hex']:
        return normalize_hex(md['hex'])
    return normalize_rgb(md['r'], md['g'], md['b'], md.get('a'))


def normalize_hex(hex_color):
    """Transform a xxx hex color to xxxxxx.
    """
    hex_color = hex_color.replace('#', '').lower()
    length = len(hex_color)
    if length in (6, 8):
        return '#' + hex_color
    if length not in (3, 4):
        return None
    strhex = u'#%s%s%s' % (
        hex_color[0] * 2,
        hex_color[1] * 2,
        hex_color[2] * 2)
    if length == 4:
        strhex += hex_color[3] * 2
    return strhex


def normalize_rgb(r, g, b, a):
    """Transform a rgb[a] color to #hex[a].
    """
    r = int(r, 10)
    g = int(g, 10)
    b = int(b, 10)
    if a:
        a = float(a) * 256
    if r > 255 or g > 255 or b > 255 or (a and a > 255):
        return None
    color = '#%02x%02x%02x' % (r, g, b)
    if a:
        color += '%02x' % int(a)
    return color
