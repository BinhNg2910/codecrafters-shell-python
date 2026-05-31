import app.command_handler

def main():
    while True:
        userInput = input("$ ")
        command = userInput.split(" ")[0]
        args = userInput.split(" ")[1:]
        app.command_handler.handle_command(command, args)
    
if __name__ == "__main__":
    main()
