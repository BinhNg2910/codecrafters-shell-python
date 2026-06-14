from app.command_handler import parse_commandlind, handle_command
import readline

BUILD_INS = ["echo", "exit"]

def completer(text, state):
    matches = []
    for command in BUILD_INS:
        if command.startswith(text):
            matches.append(command + " ")
    
    if state < len(matches):
        return matches[state]
    return None

def main():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        userInput = parse_commandlind(input("$ "))
        if not userInput:
            continue
        command = userInput[0]
        args = userInput[1:]
        handle_command(command, args)
    
if __name__ == "__main__":
    main()
