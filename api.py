from aiohttp import web
from addict import Dict
import re
import os
import aioredis
from datetime import datetime
from functools import reduce

HEX_COLOR_RE = re.compile(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')
REDIS_URL = os.getenv("REDIS_URL")


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
    redis = await aioredis.create_redis_pool(REDIS_URL)
    start_time = datetime.now()
    kwargs = await request.post()
    hex_color = dict(kwargs).get('hex')
    response_dict = Dict()
    try:
        rgb = await hex_to_rgb(hex_color)
    except ValueError:
        response_dict.status = 400
        await redis.hincrby('status_codes', response_dict.status, 1)
        response_dict.data = f"{hex_color} is not a valid hexadecimal color value"
        end_time = datetime.now()
        time_taken = end_time - start_time
        await redis.sadd('latencies', time_taken.total_seconds())
        return web.json_response(**response_dict)
    response_dict.status = 200
    response_dict.data = Dict(Input=f"#{hex_color}", RGB=rgb)
    end_time = datetime.now()
    time_taken = end_time - start_time
    await redis.sadd('latencies', time_taken.total_seconds())
    await redis.hincrby('status_codes', response_dict.status, 1)
    return web.json_response(**response_dict)


async def healthcheck(request):
    response_dict = Dict()
    response_dict.status = 200
    response_dict.data = "Pong"
    return web.json_response(**response_dict)


async def metrics(request):
    redis = await aioredis.create_redis_pool(REDIS_URL)
    status_codes = await redis.hgetall('status_codes')
    latencies = await redis.smembers('latencies')
    average_latency = reduce(lambda a, b: float(a) + float(b), latencies) / len(latencies)
    response_dict = Dict()
    response_dict.status = 200
    response_dict.data = Dict(status_codes=status_codes, average_latency=average_latency)
    return web.json_response(**response_dict)


async def main():
    app = web.Application()
    # Add routes here but you have to create custom handles before you add each route
    app.add_routes([web.post('/convert/', handle)])
    app.add_routes([web.get('/healthcheck/', healthcheck)])
    app.add_routes([web.get('/metrics/', metrics)])
    return app


if __name__ == "__main__":
    app = main()
    web.run_app(app)
