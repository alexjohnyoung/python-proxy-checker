# python-proxy-checker
HTTP Proxy Checker created in Python

<img src="https://i.imgur.com/KV7A9gr.png" width="700">
<img src="https://i.imgur.com/weOU5Xm.png" width="700">
<img src="https://i.imgur.com/8i828mo.png" width="700">

# Features
* Scanning for working proxies
* Rechecking working proxies
* Saving working proxies to file
* Executing specified file once complete

# Command Line Arguments
* First argument: amount of proxies to scan for (0 to not specify an amount)
* Second argument: amount of time to check individual proxy for (default 2 seconds)
* Third argument: should proxies be rechecked after initial check? (1/0 - added in the case of long scans)
* Fourth argument: file to execute after proxy checking is complete (not needed)

### Example
`main.py 5 2 1 file.exe`

Gather 5 working proxies, recheck them and run file.exe (2 second timeout on each connection attempt)

Also included in build/ directory is a 64-bit Python-compiled file for use on ARM64 machines (compiled using Nuitka library)
