from util import PROXY_ASCII, parse_web, get_user_agent, get_build_opener, write_proxies_to_file, check_proxies
from sys import argv


# Entry point to our program
def main(args):

    recheck_proxies = True
    num_needed = 0
    timeout = 2
    exec_file = False

    print(PROXY_ASCII)

    try:
        num_needed = int(args[1])
    except IndexError:
        num_needed = int(input("Enter max amount of proxies (0 to not define): "))

    try:
        timeout = float(args[2])
    except IndexError:
        timeout = float(input("Enter timeout (2s default): "))

    try:
        if int(args[3]) == 1:
            recheck_proxies = True
        else:
            recheck_proxies = False
    except IndexError:
        recheck_proxies = int(input("Recheck proxies? (1/0): "))

        if recheck_proxies == 1:
            recheck_proxies = True
        else:
            recheck_proxies = False

    try:
        exec_file = args[4]

    except IndexError:
        pass

    print(f"Running with '{str(num_needed)}' needed proxies and '{str(timeout)}' seconds timeout")

    if exec_file:
        print(f"Will execute {exec_file} once complete\n")

    data = get_build_opener("https://free-proxy-list.net/")

    if parse_web(data, "UTC.", 6, "</textarea>", -1):
        check_proxies(recheck_proxies, num_needed, timeout, False, exec_file)


main(argv)
