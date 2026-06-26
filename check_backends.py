import os, json
out = {"redis": None, "postgres": None}

# Redis check
try:
    import redis
    redis_url = os.environ.get('LIVING_AI_REDIS_URL', 'redis://localhost:6379/0')
    client = redis.Redis.from_url(redis_url, decode_responses=True)
    ok = client.ping()
    test_key = 'health:redis_check'
    client.set(test_key, 'ok')
    val = client.get(test_key)
    client.delete(test_key)
    out['redis'] = {"reachable": True, "ping": ok, "test_get": val, "url": redis_url}
except Exception as e:
    out['redis'] = {"reachable": False, "error": str(e)}

# Postgres check
try:
    import psycopg2
    dsn = os.environ.get('LIVING_AI_POSTGRES_DSN', 'postgresql://postgres:postgres@localhost:5432/living_ai')
    # psycopg2 accepts dsn string
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    cur.close()
    conn.close()
    out['postgres'] = {"reachable": True, "version": ver[0], "dsn": dsn}
except Exception as e:
    out['postgres'] = {"reachable": False, "error": str(e)}

print(json.dumps(out, indent=2))
