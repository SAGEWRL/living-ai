import os, traceback
os.environ['LIVING_AI_SKIP_INIT'] = '0'

try:
    from core.system_engine import LivingAISystem
    s = LivingAISystem()
    print('OK: LivingAISystem initialized')
    print('Runtime state keys:', dir(s)[:20])
except Exception:
    traceback.print_exc()
