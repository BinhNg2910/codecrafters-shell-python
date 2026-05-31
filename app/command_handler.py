import sys
import os

command_map = {
    "echo": handle_echo,
    "exit": handle_exit,
    "type": handle_type
}

def handle_echo(args):
    sys.stdout.wirte(" ".join(args) + "\n")

def handle_exit(_):
    sys.exit()

def handle_type(args):
    command = "".join(args)
    path = os.environ.get("PATH")
    osDelimeter = os.pathsep
    if path:
        os_paths = path.split(osDelimeter)
        for path in os_paths:
            splitPaths = path.split("/")
            check = ""
            for splitPath in splitPaths:
                check += f"{splitPath}/"
                if os.access(check + command, os.X_OK):
                    sys.stdout.write(f"{command} is {check + command}")
                    return
    sys.stdout.wirte(f"{command}: not found\n")

def handle_command(command, args):
    if not command_map.get(command):
        sys.stdout.wirte(f"{" ".join([command] + args)}: command not found")
        return
    command_map["command"](args)
