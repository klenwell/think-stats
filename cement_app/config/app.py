from os.path import dirname, realpath, join as path_join

PROJECT_ROOT = dirname(dirname(dirname(realpath(__file__))))
APP_ROOT = path_join(PROJECT_ROOT, 'cement_app')
DATA_ROOT = path_join(PROJECT_ROOT, 'data')
