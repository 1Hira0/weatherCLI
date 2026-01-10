from handler import current, forecast
import requests


def commandHandler(inp):
    inp = inp.split()
    command = inp[0][1:]
    if command not in commands: print("Invalid command")
    for i in commands:
        if command == i:
            if i in weCommands:
                if len(inp) < 2 or (len(inp) >= 2 and not " ".join(j for j in inp[1:])):
                    print("Getting IP")
                    loc = requests.get('https://api.ipify.org?format=json').json()['ip']
                else: loc = " ".join(j for j in inp[1:])
                weCommands[i](loc)
            else:
                localComands[i]()
            break


def _help(command=''): 
    if command:
        return

    print(f"""{".current":<12} {"[location=IP]":>12} Prints current weather. If location not given, uses IP. Coordinates work too.
{".forecast":<12} {"[location=IP]":>12} Prints 2-day weather forecast (Today & Tomorrow). If location not given, uses IP. Coordinates work too.
{".help":<12} {"":>12} Prints this help message.
{".exit":<12} {"":>12} Exits the program.""")


weCommands = {"current":current , "forecast":forecast}
localComands = {"help":_help, "exit":exit}
commands = weCommands |localComands

if __name__ == "__main__":
    print('Welcome to Weather CLI.\nType ".help" for more information.\n".exit" to close')
    while True:
        inp = input(">")
        if not inp: continue
        if inp[0] != '.':
            print("Every command starts with .[command_name]. Try .help")
            continue
        commandHandler(inp)