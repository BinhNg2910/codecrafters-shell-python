import sys
import os

def handle_echo(args):
    print(" ".join(args))

def handle_exit():
    sys.exit()

def main():
    while True:
        sys.stdout.write("$ ")
        commands = input().split()

        path = os.environ.get("PATH")
        delimeter = os.pathsep

        if commands[0] == "exit":
            handle_exit()
        elif commands[0] == "echo":
            if len(commands) > 1:
                handle_echo(commands[1:])
        elif commands[0] == "type":
            joinedCommand = "".join(commands[1:])
            if "".join(commands[1:]) in ["echo", "exit", "type"]:
                print(f"{joinedCommand} is a shell builtin")
            else:
                isFound = False
                if path:
                    seperated_paths = path.split(delimeter)
                    for path in seperated_paths:
                        split_paths = path.split("/")
                        check_path = ""
                        for split_path in split_paths:
                            check_path += f"{split_path}/"
                            if os.access(check_path + joinedCommand, os.X_OK):
                                print(f"{joinedCommand} is {check_path + joinedCommand}")
                                isFound = True
                if not isFound:
                    print(f"{joinedCommand}: not found")
        else:
            print(f"{"".join(commands)}: command not found")
if __name__ == "__main__":
    main()
