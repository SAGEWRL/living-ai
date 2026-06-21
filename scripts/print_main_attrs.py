import sys, os
sys.path.insert(0, r'c:\Users\Administrator\Desktop\living-ai-core')
os.environ['LIVING_AI_SKIP_INIT'] = '1'
import main
print('main.ingest_alert =', main.ingest_alert)
print('type:', type(main.ingest_alert))
print('main.system =', main.system)
