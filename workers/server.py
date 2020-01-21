"""Запуск проекта"""

__author__ = 'alexander'
__maintainer__ = 'alexander'
__credits__ = ['alexander', ]
__copyright__ = "LGPL"
__status__ = 'Development'
__version__ = '20200121'

import os
import sys
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_PATH)
# ! --------------------------
from server.server import *
import argparse


if __name__ != "__main__":
    raise Exception("Run worker.server, don't import!")
else:
    parser = argparse.ArgumentParser(add_help=True, description='Стрегоанализ с использованием машинного обучения')
    parser.add_argument('--version', action='version', version='%(prog)s 0.95')
    args = parser.parse_args()
    try:
        app.run(host='185.219.41.226', port=8080, debug=True)
    except KeyboardInterrupt:
        sys.exit()
