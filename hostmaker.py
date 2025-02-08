import app
import re
import json
import traceback
import logger

def readConfigFile():
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
    except AssertionError as e:
        logger.LogFatal(f"The following configuration goes wrong: {e}.")
        exit(-1)
    except:
        logger.LogFatal("Cannot read the file `config.jsonc`.")
        traceback.print_exc()
        exit(-1)

    return config

def writeToFile(outputList: str):
    resultString = json.dumps(outputList, indent=4)
    if config["OutputFile"] == ">":
        print(resultString )
        return 0
    elif config["OutputFile"] == "|":
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
            outputList.append(app.getDomainAnalize(line, config["ConvertIPv6ToIPv4"], config["SelectIP"]))
        except:
            logger.LogError(traceback.format_exc())

    writeToFile(outputList)