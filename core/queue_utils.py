try:
    from rq.job import Job
    from rq import Queue
    import redis
except Exception:
    Job = None
    Queue = None
    redis = None


def get_redis_connection(url=None):
    if redis is None:
        raise ImportError("redis or rq package not available")
    from core.storage_config import create_storage_backend
    url = url or __import__('os').environ.get('LIVING_AI_REDIS_URL', 'redis://localhost:6379/0')
    return redis.from_url(url, decode_responses=True)


def fetch_job(job_id, connection_url=None):
    if Job is None:
        raise ImportError("rq is not installed")
    conn = get_redis_connection(connection_url)
    try:
        job = Job.fetch(job_id, connection=conn)
    except Exception:
        return None
    return {
        'id': job.id,
        'status': job.get_status(),
        'result': job.result,
        'exc_info': job.exc_info,
        'enqueued_at': job.enqueued_at,
        'started_at': job.started_at,
        'ended_at': job.ended_at
    }
