from app.command_handler import parse_commandlind, handle_command

def main():
    while True:
        userInput = parse_commandlind(input("$ "))
        if not userInput:
            continue
        command = userInput[0]
        args = userInput[1:]
        handle_command(command, args)
    
if __name__ == "__main__":
    main()
