import app
import colorama
import traceback

if __name__ == '__main__':
    outputList = []

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

    outputPath = input("Input the output file path('|' for quit directly): ")
    if outputList == "|": 
        exit()

    try:
        with open(outputPath, "w") as f:
            f.write(str(outputList))
    except:
        print(f"{colorama.Fore.LIGHTRED_EX}{traceback.format_exc()}{colorama.Fore.RESET}")