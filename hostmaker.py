import app
import colorama
import traceback
import logger

# Two modes:
# - Input
# - Web
LOGIC_LAUNCHER = "Input"

if __name__ == '__main__':
    outputList = []

    if LOGIC_LAUNCHER == "Input":
        print("Type 'exit' to quit.")
        while True:
            inputDomain = input("Input the clean domain: ")
            if inputDomain == "exit":
                break
            try: 
                outputList.append(app.getDomainAnalize(inputDomain, False))
                logger.LogInfo(f"Successfully added {inputDomain} to the list.")
            except:
                logger.LogError(traceback.format_exc())

        print(f"Successfully added {len(outputList)} items to the list.")
    elif LOGIC_LAUNCHER == "Web":
        pass

    outputPath = input("Input the output file path('|' for quit directly; '>' for print here): ")
    if outputPath == "|": 
        exit()
    elif outputPath == ">":
        print(outputList)
        exit()

    try:
        outputStr = str(outputList).replace("'", '"')
        with open(outputPath, "w") as f:
            f.write(outputStr)
        logger.LogInfo("Finished writing.")
    except:
        logger.LogFatal(traceback.format_exc())