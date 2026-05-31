import app.command_handler

def main():
    while True:
        userInput = app.command_handler.parse_doublequote_commandline(input("$ "))
        command = userInput[0]
        args = userInput[1:]
        app.command_handler.handle_command(command, args)
    
if __name__ == "__main__":
    main()
