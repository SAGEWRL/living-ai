import os
os.environ['LIVING_AI_SKIP_INIT'] = '1'
print('env set')
import importlib
m = importlib.import_module('main')
print('imported main, system =', m.system)
