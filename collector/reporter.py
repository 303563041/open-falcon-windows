from rpc.hbs import report_status_to_hbs
from rpc.hbs import get_hbs_builtinmetrics
from utils import g

import time
import logging


def report():
    """
    report status info to hbs
    """
    data = {
        "Hostname": g.HOSTNAME,
        "IP": g.IP,
        "AgentVersion": g.VERSION,
        "PluginVersion": "plugin not enabled"
    }
    logging.debug(data)

    try:
        res = report_status_to_hbs(data)
    except Exception as e:
        logging.error(e, exc_info=True)
    logging.info("report to hbs --> %s" % res)


def get_BuiltinMetrics():
    """
    get BuiltinMetrics
    """
    data = {
        "Hostname": g.HOSTNAME,
        "Checksum": ""
    }
    logging.debug(data)

    try:
        res = get_hbs_builtinmetrics(data)
        g.PROC = res["Metrics"]
    except Exception as e:
        logging.error(e, exc_info=True)
    logging.info("get metrics from hbs --> %s" % res)


def status_report(period):
    logging.debug('prepare collect basic data')
    while True:
        try:
            report()
            get_BuiltinMetrics()
        except Exception as e:
            logging.error(e, exc_info=True)
        time.sleep(period)
