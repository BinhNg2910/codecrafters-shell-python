import command_handler

def main():
    while True:
        userInput = command_handler.parse_commandlind(input("$ "))
        command = userInput[0]
        args = userInput[1:]
        command_handler.handle_command(command, args)
    
if __name__ == "__main__":
    main()
