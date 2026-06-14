from app.autocomplete import configure_autocomplete
from app.command_handler import handle_command, parse_commandlind

def main():
    configure_autocomplete()

    while True:
        user_input = parse_commandlind(input("$ "))
        if not user_input:
            continue

        command = user_input[0]
        args = user_input[1:]
        handle_command(command, args)
    
if __name__ == "__main__":
    main()
