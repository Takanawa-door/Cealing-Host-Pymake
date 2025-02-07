# The major one

import requests
import requester
import socket
import random
import base64
import ping3
import logger
import traceback

# -- MAJOR FUNCTIONS --

def base64Decode(encoded_msg: str):
    # 将编码的字符串转换为字节格式
    encoded_bytes = encoded_msg.encode('utf-8')
    # 执行Base64解码
    decoded_bytes = base64.b64decode(encoded_bytes)
    # 将解码的字节形式转换回字符串并返回
    return decoded_bytes.decode('utf-8')

def getInformationFromDomain(domain: str):
    res = requests.get(f"https://ns.net.kg/dns-query?name={domain}",
                       headers = requester.headers, proxies = random.choice(requester.ipGents))
    return res.json()

def averageDelay(ipAddress: str):
    summary = 0
    realTimes = 0
    for i in range(3):
        try:
            summary += ping3.ping(ipAddress)
            realTimes += 1
        except:
            pass
    return summary / realTimes if realTimes != 0 else None


def analizeResponseInformation(response: str, convertFromIPv6toIPv4: bool = True):
    if not response: raise AttributeError("Response is empty. 'Answer' no found.")
    majorRes = response["Answer"]
    requestUrl = response["Question"][0]["name"]
    applyIPAddresGet = None
    applyIPAddres = None

    # 优选 IP
    miniDelay = None
    for i in majorRes:
        ipAddress = i["data"]
        try:
            delay = averageDelay(ipAddress)
            logger.LogInfo(f"Average delay of {ipAddress}: {delay}.")
            if delay is None: continue
            if miniDelay is None or delay < miniDelay:
                miniDelay = delay
                applyIPAddresGet = ipAddress
        except:
            logger.LogInfo(f"Failed to test {ipAddress}...\n{traceback.format_exc()}")

    if applyIPAddresGet is None:
        logger.LogWarn("None of the IP addresses are available. Using the last one.")
        applyIPAddresGet = majorRes[-1]["data"]
    applyIPAddres = applyIPAddresGet

    logger.LogInfo(f"Selected {applyIPAddresGet}(Delay: {delay}).")

    # IPv6 -> IPv4 if necessary
    if convertFromIPv6toIPv4:
        try:
            ip6_net = socket.inet_pton(socket.AF_INET6, applyIPAddresGet)[-4:]
            applyIPAddres = socket.inet_ntoa(ip6_net)
        except:
            pass

    # SPECIAL FIX: 纠正多余的点
    requestUrl = requestUrl[:-1]

    return [[f"*{requestUrl}"], "", str(applyIPAddres)]

def getDomainAnalize(domain: str, convertFromIPv6toIPv4: bool = True):
    return analizeResponseInformation(getInformationFromDomain(domain), convertFromIPv6toIPv4)

def getFromWeb(url: str = "https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt", readFromLocal: bool = False):
    is_general_list = False
    last_list_domain = ""
    outputList = []
    majorText = None

    if not readFromLocal:
        print("Getting resources...")
        response = requests.get("https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt")

        majorText  = base64Decode(response.text)

        # 写入
        with open("gfwlist.txt", "w") as file:
            file.write(majorText)
        print("Written done.")

    else:
        with open("gfwlist.txt", "r") as file:
            majorText = file.read()
        print("Opened gfwlist.txt.")

    print(end="", flush=True)

    for list_rule in majorText.split("\n"):
        # print(f">>> {list_rule}", flush=True)

        if not is_general_list:
            if "General List Start" in list_rule:
                is_general_list = True
            continue
        elif "General List End" in list_rule:
            return

        if not list_rule.startswith("!@[/") and list_rule.strip():
            list_domain = list_rule.strip().replace("|.*", "").replace("https?://", "").rstrip("/")
            if len(list_domain) >= 1 and list_domain[0] == '.':
                list_domain = list_domain[1:]
            try_count = 3

            if list_domain == last_list_domain:
                continue
            else:
                last_list_domain = list_domain

            while True:
                try:
                    """
                    response = requests.get(f"https://ns.net.kg/dns-query?name={list_domain}")
                    host_ip_answer = response.json().get("Answer")

                    print(host_ip_answer)
                    if host_ip_answer:
                        with open(f"{host_path}/Cealing-Host-List.json", "a") as file:
                            file.write(f"\t[\"*{list_domain}\",\"\", \"{host_ip_answer[-1]['data']}\"],")
                    else:
                        print(f"{list_domain} 解析失败")
                    """

                    print(f"{list_domain}: ", end = "", flush=True)
                    # outputList.append(getDomainAnalize(list_domain))
                    print(f"Done!", flush=True)

                    break
                except:
                    if not try_count:
                        print(f"Failed.", flush=True)
                        try_count -= 1
                        break
    return outputList

if __name__ == "__main__":
    getFromWeb(readFromLocal = True)