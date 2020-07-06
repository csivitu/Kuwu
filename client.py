import subprocess
import requests

URL = 'http://xxxx:12345'

def monitor_docker():
    result = subprocess.run(['docker','stats','--no-stream'], stdout=subprocess.PIPE)
    data = str(result.stdout, 'utf-8').split()
    data = data[16:]
    data = list(filter(lambda x: x != '/', data))

    return data


while True:
 jdata={'server': ','.join(monitor_docker())}
 r = requests.post(URL, data=jdata)
 print(r.status_code, r.reason)
