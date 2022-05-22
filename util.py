import http.client
import urllib.error
from urllib.request import build_opener, install_opener, ProxyHandler, urlopen
from random import randint
from sys import argv
from os import remove, startfile
from os.path import isfile

PROXY_ASCII = """  ____                         ____ _               _             
 |  _ \\ _ __ _____  ___   _   / ___| |__   ___  ___| | _____ _ __ 
 | |_) | '__/ _ \\ \\/ / | | | | |   | '_ \\ / _ \\/ __| |/ / _ \\ '__|
 |  __/| | | (_) >  <| |_| | | |___| | | |  __/ (__|   <  __/ |   
 |_|   |_|  \\___/_/\\_\\__, |  \\____|_| |_|\\___|\\___|_|\\_\\___|_|   
                      |___/\n"""

PROXIES = []
WORKING_PROXIES = []
DEAD_PROXY = "Proxy dead.. moving on"
RECHECK_PROXIES = True

UserAgents = ["Mozilla/5.0 (X11; CrOS x86_64 14588.98.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.59 Safari/537.36",
              "Mozilla/5.0 (X11; CrOS armv7l 14588.98.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.59 Safari/537.36",
              "Mozilla/5.0 (X11; CrOS aarch64 14588.98.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.59 Safari/537.36",
              "Mozilla/5.0 (X11; CrOS x86_64 14588.98.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.59 Safari/537.36",
              "Mozilla/5.0 (X11; CrOS armv7l 14588.98.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.59 Safari/537.36",
              "Mozilla/5.0 (X11; CrOS aarch64 14588.98.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.59 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 Edg/100.0.1185.39",
              "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"]


# Used to find and parse web source data
def parse_web(body, find_x, offset_x, find_y, offset_y):

    found = 0
    find_str = body.find(find_x)

    if find_str:
        found += 1
        find_x = find_str + offset_x

    find_str = body.find(find_y)

    if find_str:
        found += 1
        find_y = find_str + offset_y

    if found == 2:
        data = body[find_x:find_y]
        data = data.split("\n")

        for key, proxy in enumerate(data):
            PROXIES.append(proxy)

        return True
    else:
        print("Unable to find the data we were attempting to parse!")
        return False


# Used to get a random User Agent
def get_user_agent():
    num_user_agents = len(UserAgents)
    user_agent = randint(0, num_user_agents-1)

    return UserAgents[user_agent]


# Used to retrieve a build opener to construct proxy settings
def get_build_opener(web, search=True, proxy=False):

    user_agent = get_user_agent()
    opener = 0

    if proxy:
        proxy_support = ProxyHandler({"http": proxy})
        opener = build_opener(proxy_support)
        install_opener(opener)
    else:
        opener = build_opener()

    opener.addheaders = [("User-agent", user_agent)]

    if search:
        data = opener.open(web)
        data = data.read().decode()

    else:
        data = 0

    return data


# Used to write working proxies to file
def write_proxies_to_file(proxies, num_working, num_failed, exec_file=False):

    if num_working == 0:
        print("Found no working proxies..")
        return

    if isfile("proxies.txt"):
        remove("proxies.txt")

    proxies_handle = open("proxies.txt", 'a')

    for key, proxy in enumerate(proxies):

        if key+1 == len(proxies):
            proxy = proxy.rstrip()

        proxies_handle.write(proxy)

    proxies_handle.close()

    print(f"Retrieved {str(num_working)} working proxies out of {str(num_working + num_failed)} proxies\n"
          f"Saved working proxies to file")

    if exec_file:
        print("Executing file now..")
        startfile(exec_file)


# Used to check proxies
def check_proxies(recheck_proxies=True, num_needed=0, timeout=1.5, rechecked=False, exec_file=False):

    global WORKING_PROXIES
    global PROXIES

    num_working = 0
    num_failed = 0

    for key, proxy in enumerate(PROXIES):
        print(f"[{str(key+1)}]: Checking proxy {proxy}")

        try:
            opener = get_build_opener("http://google.com", False, proxy)
            data = urlopen("http://google.com", timeout=timeout).read()

            if recheck_proxies:
                if not rechecked:
                    WORKING_PROXIES.append(proxy)
                else:
                    WORKING_PROXIES.append(proxy + '\n')
            else:
                WORKING_PROXIES.append(proxy + '\n')

            num_working += 1

            print(f"[{str(key+1)}]: Proxy appears working, added")

            if not rechecked and num_needed > 0 and num_needed == num_working:
                print("Got enough proxies, stopping proxy check..\n")
                break

        except urllib.error.HTTPError:
            num_failed += 1
            print(f"[{str(key+1)}]: {DEAD_PROXY}")
        except urllib.error.URLError:
            num_failed += 1
            print(f"[{str(key+1)}]: {DEAD_PROXY}")
        except TimeoutError:
            num_failed += 1
            print(f"[{str(key+1)}]: {DEAD_PROXY}")
        except http.client.RemoteDisconnected:
            num_failed += 1
            print(f"[{str(key+1)}]: {DEAD_PROXY}")
        except ConnectionResetError:
            num_failed += 1
            print(f"[{str(key+1)}]: {DEAD_PROXY}")
        except http.client.BadStatusLine:
            print("Service stopped due to too many users. Saving current alive proxies.")
            write_proxies_to_file(WORKING_PROXIES)

        print(f"\t[{str(num_working)} working, {str(num_failed)} failed]\n")

    if recheck_proxies and not rechecked:
        print("Rechecking proxies..\n")
        PROXIES = WORKING_PROXIES.copy()
        WORKING_PROXIES = []
        check_proxies(recheck_proxies, num_needed, timeout, True, exec_file)
        return

    write_proxies_to_file(WORKING_PROXIES, num_working, num_failed, exec_file)
