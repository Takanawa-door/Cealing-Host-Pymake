# The major one

import requests
import requester
import socket
import random

# -- MAJOR FUNCTIONS --

def getInformationFromDomain(domain: str):
    res = requests.get(f"https://ns.net.kg/dns-query?name={domain}",
                       headers = requester.headers, proxies = random.choice(requester.ipGents))
    return res.json()

def analizeResponseInformation(response: str, convertFromIPv6toIPv4: bool = True):
    if not response: raise AttributeError("Response is empty. 'Answer' no found.")
    majorRes = response["Answer"]
    requestUrl = response["Question"][0]["name"]
    applyIPAddresGet = majorRes[-1]["data"]
    applyIPAddres = applyIPAddresGet

    # IPv6 -> IPv4 if necessary
    if convertFromIPv6toIPv4:
        ip6_net = socket.inet_pton(socket.AF_INET6, applyIPAddresGet)[-4:]
        applyIPAddres = socket.inet_ntoa(ip6_net)

    # SPECIAL FIX: 纠正多余的点
    requestUrl = requestUrl[:-1]

    return [[f"*{requestUrl}"], "", str(applyIPAddres)]

def getDomainAnalize(domain: str, convertFromIPv6toIPv4: bool = True):
    return analizeResponseInformation(getInformationFromDomain(domain), convertFromIPv6toIPv4)