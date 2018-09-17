"""
Collect Host's proc metric
"""
import psutil
import time
import json
import copy
import logging
import win32serviceutil
import win32service

from rpc.transfer import send_data_to_transfer
from utils import g


def is_start(proc_name):
    '''
    Check whether the service is stopped
    '''
    flag = False
    try:
        ret = win32serviceutil.QueryServiceStatus(proc_name)
        flag = ret[1] != win32service.SERVICE_RUNNING
    except Exception, e:
        logging.error(e)
        flag = True
    return flag


def collect():
    """
    collect proc num
    """
    logging.debug('enter proc collect')
    push_interval = 60
    zh_decode = "gbk"

    time_now = int(time.time())
    payload = []
    tags = ""
    for k, v in g.TAGS.items():
        t = k + "=" + v
        tags = tags + t + ","

    data = {
        "endpoint": g.HOSTNAME,
        "metric": "",
        "timestamp": time_now,
        "step": push_interval,
        "value": "",
        "counterType": "GAUGE",
        "tags": tags.strip(",")
    }

    # agent proc num
    for metrics in g.PROC:
        data["metric"] = metrics["Metric"]
        data["tags"] = metrics["Tags"] + "," + tags.strip(",")
        proc_name = metrics["Tags"].split("=")[1]
        if is_start(proc_name):
            data["value"] = 0
        else:
            data["value"] = 1
        payload.append(copy.copy(data))
    logging.debug(payload)

    try:
        result = send_data_to_transfer(payload)
    except Exception as e:
        logging.error(e)
    else:
        logging.info(result)


def proc_collect(period):
    """
    deadloop to collect data periodically
    :params: `period` is the seconds of collecting circle
    """
    logging.debug('prepare collect proc data')
    while True:
        try:
            collect()
        except Exception as e:
            logging.error(e, exc_info=True)
        time.sleep(period)
