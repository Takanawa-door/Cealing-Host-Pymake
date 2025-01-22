import app
import colorama
import traceback

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
                print(f"Successfully added {inputDomain} to the list.")
            except:
                print(f"{colorama.Fore.LIGHTRED_EX}{traceback.format_exc()}{colorama.Fore.RESET}")

        print(f"Successfully added {len(outputList)} items to the list.")
    elif LOGIC_LAUNCHER == "Web":
        pass

    outputPath = input("Input the output file path('|' for quit directly): ")
    if outputList == "|": 
        exit()

    try:
        outputStr = str(outputList).replace("'", '"')
        with open(outputPath, "w") as f:
            f.write(outputStr)
    except:
        print(f"{colorama.Fore.LIGHTRED_EX}{traceback.format_exc()}{colorama.Fore.RESET}")