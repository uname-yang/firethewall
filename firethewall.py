import os
import json
import logging
import requests

TOKEN = "XXX"
FINGERPRINT = "XXX"

#EXAMPLE
#TOKEN = "6b360de366ab91d38e1dc153cb650f6297182998418cddca433f223af32497cf"
#FINGERPRINT = "6b:2c:c2:8b:84:c4:2d:19:d1:a1:c5:88:24:3f:11:c1"


def createServer():
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+TOKEN}

    url = "https://api.digitalocean.com/v2/droplets"
    
    payload = {"name": "sshtun", "region": "nyc3", "size": "s-1vcpu-1gb", "image": "ubuntu-17-10-x64",
               "ssh_keys": [FINGERPRINT], "tags": ["net"]}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        data = json.loads(r.text)
        return data['droplet']['id']
    except Exception:
        logging.error(Exception)
        raise


def deleteServer(sid):
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+TOKEN}

    url = "https://api.digitalocean.com/v2/droplets/"+str(sid)

    try:
        requests.delete(url, headers=headers)
    except Exception:
        logging.error(Exception)
        raise


def listServer():
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+TOKEN}

    url = "https://api.digitalocean.com/v2/droplets"

    try:
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        return data
    except Exception:
        logging.error(Exception)
        raise


def status(meta):
    return 0

def connect():
    return 0

def disconnect():
    return 0


if __name__ == '__main__':
    # sid = createServer()
    # print(sid)

    # print(listServer())

    # deleteServer(sid)

    print(listServer())
