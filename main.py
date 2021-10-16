import requests
import sys
import json
from itertools import combinations_with_replacement
from tqdm import tqdm
import concurrent.futures
import time
alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','q','u','v','w','x','y','z']
def getRoomCodes():
    roomCode=[]
    for subset in combinations_with_replacement(alphabet, 4):
        roomCode.append("https://ecast.jackboxgames.com/room/"+"".join(subset))
    return roomCode
out = []
CONNECTIONS = 1000
TIMEOUT = 5
choice=input("Do you want players, audience or both?: ")
choice=choice.lower()
if choice != "both" and choice != "players" and choice != "audience":
    print('invalid choice')
    sys.exit(1)

def load_url(url, timeout):
    ans = requests.get(url, timeout=timeout)
    rjson=json.loads(ans.text)
    try:
        if rjson['error']:
            return
    except:
        if rjson['roomid']:
            if rjson["requiresPassword"] == False:
                if rjson['audienceEnabled'] and rjson['joinAs'] == "audience" and (choice == "both" or choice == "audience"):
                    print(f"{rjson['roomid']} - {rjson['joinAs']} - {rjson['apptag']}")
                if rjson['joinAs'] == 'player' and (choice == "both" or choice == "players"):
                    print(f"{rjson['roomid']} - {rjson['joinAs']} - {rjson['apptag']}")
urls =getRoomCodes()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
    time1 = time.time()
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            out.append(data)
    time2=time.time()
print(f'Took {time2-time1:.2f} s')