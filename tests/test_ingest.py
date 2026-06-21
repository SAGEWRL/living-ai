import json
import os
import sys

sys.path.insert(0, r'c:\Users\Administrator\Desktop\living-ai-core')

from core.system_engine import LivingAISystem
from core.alert_ingestor import ingest_alert
from fastapi.testclient import TestClient
import os
# prevent main from auto-initializing a heavy LivingAISystem at import-time
os.environ['LIVING_AI_SKIP_INIT'] = '1'
import main

AUTH_HEADERS = {
    'Authorization': 'Bearer demo-key'
}


def run_unit_checks():
    # 1) Direct ingest function
    s = LivingAISystem()
    # ensure a clean kernel state for deterministic testing
    s.kernel.load_goals([])
    before = len(s.kernel.goals)
    res = ingest_alert(s, 'Alert: test disk full', priority=6)
    assert res.get('status') == 'ok'
    assert len(s.kernel.goals) == before + 1
    assert s.kernel.goals[-1]['priority'] == 6

    # 2) Endpoint ingest
    # create a controlled system instance for the test
    main.system = LivingAISystem()
    client = TestClient(main.app)
    payload = {'alert': 'Add goal: endpoint-created-goal', 'priority': 4}
    r = client.post('/ingest_alert', json=payload, headers=AUTH_HEADERS)
    assert r.status_code == 200
    jr = r.json()
    assert jr.get('status') == 'ok'

    # 3) Structured alert ingestion
    structured_payload = {
        'source': 'prometheus',
        'payload': {
            'message': 'Disk usage above 90% on server X',
            'summary': 'High disk usage alert'
        },
        'priority': 8
    }
    r2 = client.post('/alerts/ingest', json=structured_payload, headers=AUTH_HEADERS)
    assert r2.status_code == 200
    jr2 = r2.json()
    assert jr2.get('status') == 'ok'
    assert 'Disk usage above 90% on server X' in jr2.get('goal', '')

    # 4) Duplicate goal ingestion should not create duplicates
    duplicate_payload = {'alert': 'Add goal: endpoint-created-goal', 'priority': 4}
    r3 = client.post('/ingest_alert', json=duplicate_payload, headers=AUTH_HEADERS)
    assert r3.status_code == 200
    assert r3.json().get('status') == 'ok'
    endpoint_goals = [g for g in main.system.kernel.goals if g['goal'] == 'endpoint-created-goal']
    assert len(endpoint_goals) == 1
    assert endpoint_goals[0].get('id') is not None

    # 5) Complete goal endpoint
    completion_payload = {'goal': 'endpoint-created-goal'}
    r4 = client.post('/goals/complete', json=completion_payload, headers=AUTH_HEADERS)
    assert r4.status_code == 200
    jr4 = r4.json()
    assert jr4.get('status') == 'completed'
    assert all(g['goal'] != 'endpoint-created-goal' for g in main.system.kernel.goals)

    # Confirm persistence file contains the kernel goal
    if os.path.exists('self_model.json'):
        with open('self_model.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        kernel_goals = data.get('kernel_goals', [])
        matches = [g for g in kernel_goals if isinstance(g, dict) and g.get('goal') == 'endpoint-created-goal']
        assert len(matches) == 0

    print('ALL_TESTS_PASSED')


def test_ingest_endpoints():
    run_unit_checks()


if __name__ == '__main__':
    try:
        run_unit_checks()
    except AssertionError as e:
        print('TEST_FAILED', e)
        raise
    except Exception as e:
        print('ERROR', e)
        raise
