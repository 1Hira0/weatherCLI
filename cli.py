from handler import current
import requests


def commandHandler(inp):
    inp = inp.split()
    command = inp[0][1:]
    if command not in commands: return "Invalid command" 
    for i in commands:
        if command == i:
            if i in weCommands:
                if len(inp) < 2:
                    print("Getting IP")
                    loc = requests.get('https://api.ipify.org?format=json').json()['ip']
                else: loc = " ".join(j for j in inp[1:])
                weCommands[i](loc)
            else:
                localComands[i]()
            break


def _help(command=''): 
    if  command: ""
    print(f"""{".current":<10} {"[location=IP]":>10} Prints current weather of given location. If location is not given fetches from IP
{".forecast":<10} {"[location=IP]":>10} 
{".help":<10} {"":>10} Prints this message""")

weCommands = {"current":current}
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