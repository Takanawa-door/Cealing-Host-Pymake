import app
import re
import json
import traceback
import logger

SIGN_WRITE_TO_CONSOLE = ">"
SIGN_WRITE_TO_NUL = "|"

def readConfigFile():
    """
    读取配置文件。
    """

    config = None
    try: 
        with open("./config.jsonc", "r") as f:
            content = f.read()
            # 去除单行注释
            content = re.sub(re.compile(r'//.*?\n'), '', content)
            # 去除多行注释
            content = re.sub(re.compile(r'/\*.*?\*/', re.DOTALL), '', content)

            config = json.loads(content)
            logger.LogInfo("Successfully loaded the config file.")
        # 验证参数
        assert "OutputFile" in config.keys(), "OutputFile"
        assert config["ConvertIPv6ToIPv4"] in [True, False], "ConvertIPv6ToIPv4"
        assert config["SelectIP"] in [True, False], "SelectIP"
        assert type(config["PingMaxTryTimes"]) == int, "PingMaxTryTimes"
    except AssertionError as e:
        logger.LogFatal(f"The following configuration goes wrong: {e}.")
        exit(-1)
    except:
        logger.LogFatal("Cannot read the file `config.jsonc`.")
        traceback.print_exc()
        exit(-1)

    return config

def writeToFileAsHosts(outputList: str):
    """
    将结果以 hosts 格式写入文件。
    """

    pass

def convertToJson(source: list):
    """
    将列表转换为 Sheas-Cealer 的 Json 格式的规则。
    """
    result = "[\n"

    for item in source:
        # 缩进
        print(item)
        result += "    ["
        result += f"{str(item[0]).replace("'", '"')}, \"\", \"{item[2]}\""
        result += "],\n"

    result += "]"

    return result

def writeToFileAsJson(outputList: list):
    """
    将结果以 Json 格式写入文件。
    """

    # resultString = json.dumps(outputList, indent=4)
    resultString = convertToJson(outputList)
    if config["OutputFile"] == SIGN_WRITE_TO_CONSOLE:
        print(resultString)
        return 0
    elif config["OutputFile"] == SIGN_WRITE_TO_NUL:
        return 0

    try:
        with open(config["OutputFile"], "w") as f:
            f.write(resultString)
        logger.LogInfo("Finished writing.")
        return 0
    except:
        logger.LogFatal(traceback.format_exc())
        return -1

def readInputFile():
    """
    读取待处理网站列表文件。
    """

    try:
        with open(config["WebListFile"], "r") as f:
            inputList = f.readlines()
        logger.LogInfo("Successfully read the input file.")
        return inputList
    except:
        logger.LogFatal(traceback.format_exc())
        return []

if __name__ == '__main__':
    config = readConfigFile()
    outputList = []
    inputList = readInputFile()
    
    for line in inputList:
        if line[-1:] == "\n":
            line = line[:-1]
        try:
            logger.LogInfo(f"Processing {line}...")
            outputList.append(app.getDomainAnalize(line, config["ConvertIPv6ToIPv4"], config["SelectIP"],
                                                   config["PingMaxTryTimes"]))
        except:
            logger.LogError(traceback.format_exc())

    writeToFileAsJson(outputList)