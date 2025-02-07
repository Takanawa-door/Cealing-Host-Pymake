import colorama
import time

def Init():
    colorama.init()

def _Log(message, leader: str, foreground: str = "", background: str = ""):
    print(f"{foreground}{background}[{leader}]{colorama.Style.RESET_ALL}",
          f" {time.strftime('%H:%M:%S')} | {message}",
          sep = "")

def LogInfo(message):
    _Log(message, "INFO ")

def LogWarn(message):
    _Log(message, "WARN ", colorama.Fore.YELLOW)

def LogError(message):
    _Log(message, "ERROR", colorama.Fore.RED)

def LogFatal(message):
    _Log(message, "FATAL", colorama.Fore.LIGHTWHITE_EX, colorama.Back.RED)