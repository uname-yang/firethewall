#!python3
import os
import json
import logging
import requests
import sys

TOKEN = "XXX"
FINGERPRINT = "XXX"

#EXAMPLE
#TOKEN = "6b360de366ab91d38e1dc153cb650f6297182998418cddca433f223af32497cf"
#FINGERPRINT = "6b:2c:c2:8b:84:c4:2d:19:d1:a1:c5:88:24:3f:11:c1"

IDENT = "sshtun66"

def createServer():
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+TOKEN}

    url = "https://api.digitalocean.com/v2/droplets"
    
    payload = {"name": IDENT, "region": "nyc3", "size": "s-1vcpu-1gb", "image": "ubuntu-17-10-x64",
               "ssh_keys": [FINGERPRINT], "tags": ["net-bridge"]}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        data = json.loads(r.text)
        # print(data)
        return data['droplet']['id']
    except Exception:
        logging.error(Exception)
        raise


def deleteServer(sid):
    # print(sid)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+TOKEN}

    url = "https://api.digitalocean.com/v2/droplets/"+str(sid)

    try:
        requests.delete(url, headers=headers)
        print("Drop server["+str(sid)+"]")
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

        drops={"droplets":[]}

        for droplet in data['droplets']:
            if droplet['name'] == IDENT:
                drops['droplets'].append(droplet)
        return drops

    except Exception:
        logging.error(Exception)
        raise


def status():
    # print(listServer())
    for droplet in listServer()['droplets']:
        # print(droplet)
        print("server["+str(droplet['id'])+"] with ip:"+droplet['networks']['v4'][0]['ip_address'])
        print("\t please run command `ssh root@" +
              droplet['networks']['v4'][0]['ip_address']+" -N -f -D 1088` in shell")
    return 0

def connect():
    if len(listServer()['droplets']) > 0:
        status()
    else:
        id = createServer()
        print("creating server ["+str(id)+"]")
        # status()
    return 0

def destroy():
    for droplet in listServer()['droplets']:
        deleteServer(droplet['id'])
    return 0

def help_text():
    print("available options:   connect|status|destroy")

if __name__ == '__main__':

    command = 'help'

    if len(sys.argv)>=2:
        command = sys.argv[1]

    if command == 'help':
        help_text()

    if command == 'status':
        status()

    if command == 'connect':
        connect()
    
    if command == 'destroy':
        destroy()
