from app.command_handler import parse_commandlind, handle_command
import readline, os

BUILT_INS = ["echo", "exit"]

def completer(text, state):
    matches = []

    # check current text with builtin command
    for command in BUILT_INS:
        if command.startswith(text):
            matches.append(command + " ")

    # check with all executable in path
    paths = os.environ.get("PATH", "")
    directories = paths.split(os.pathsep)
    for dir in directories:
        try:
            entries = os.listdir(dir)
            for entry in entries:
                if entry.startswith(text):
                    fullPath = os.path.join(dir, entry)
                    if os.path.isfile(fullPath) and os.access(fullPath, os.X_OK):
                        matches.append(entry + " ")
        except OSError:
            # sys.stdout.write(f'Error listing directory::{dir}')
            continue
    if state < len(matches):
        return matches[state]
    return None

def main():
    readline.set_completer(completer)
    # this condition to change the "tab" for macos local enviroment cmd
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
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
