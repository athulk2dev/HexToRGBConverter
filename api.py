from aiohttp import web
from addict import Dict
import re

HEX_COLOR_RE = re.compile(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')


async def normalize_hex(hex_value):
    try:
        hex_digits = HEX_COLOR_RE.match(hex_value).groups()[0]
    except AttributeError:
        raise ValueError("'%s' is not a valid hexadecimal color value." % hex_value)
    if len(hex_digits) == 3:
        hex_digits = ''.join(map(lambda s: 2 * s, hex_digits))
    return '#%s' % hex_digits.lower()


async def hex_to_rgb(hex_value):
    hex_digits = await normalize_hex(hex_value)
    return tuple(map(lambda s: int(s, 16),
                     (hex_digits[1:3], hex_digits[3:5], hex_digits[5:7])))


async def handle(request):
    kwargs = await request.post()
    hex_color = dict(kwargs).get('hex')
    response_dict = Dict()
    try:
        rgb = await hex_to_rgb(hex_color)
    except ValueError:
        response_dict.status = 200
        response_dict.data = f"{hex_color} is not a valid hexadecimal color value"
        return web.json_response(**response_dict)
    response_dict.status = 200
    response_dict.data = Dict(Input=f"#{hex_color}", RGB=rgb)
    return web.json_response(**response_dict)


async def convert_to_rgb(hex_code):
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


async def main():
    app = web.Application()
    # Add routes here but you have to create custom handles before you add each route
    app.add_routes([web.post('/convert/', handle)])
    return app


if __name__ == "__main__":
    app = main()
    web.run_app(app)
