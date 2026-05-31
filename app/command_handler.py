import sys
import os
import subprocess

def parse_commandlind(command):
    args = list()
    current = ""
    isSingleQuote = False
    isDoubleQuote = False
    isBackSlash = False
    for char in command:
        if char == '\\' and not isBackSlash:
            isBackSlash = not isBackSlash
        elif isBackSlash:
            current += char
            isBackSlash = not isBackSlash
        elif char == "'" and not isDoubleQuote: # the condition isDoubleQuote to marked if " appear in single quote, it will be treated as the normal character
            isSingleQuote = not isSingleQuote
        elif char == '"' and not isSingleQuote:
            isDoubleQuote = not isDoubleQuote
        elif char.isspace() and not isSingleQuote and not isDoubleQuote: # this condition check when the white space not in a pair of single or double quotes
            if current:
                args.append(current)
                current = ""
        else:
            current += char

    if current:
        args.append(current)

    return args

def parse_doublequote_commandline(command):
    args = list() 
    current = ""
    isDoubleQuote = False
    for c in command:
        if c == '"':
            isDoubleQuote = not isDoubleQuote
        elif c.isspace() and not isDoubleQuote:
            if current:
                args.append(current)
                current = ""
        else:
            current += c
    
    if current:
        args.append(current)
    return args

def handle_echo(args):
    sys.stdout.write(" ".join(args) + "\n")

def handle_exit(_):
    sys.exit()

def handle_type(args):
    command = "".join(args)

    if command_map.get(command):
        sys.stdout.write(f"{command} is a shell builtin\n")
        return
    
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
                    sys.stdout.write(f"{command} is {check + command}\n")
                    return
    sys.stdout.write(f"{command}: not found\n")

command_map = {
    "echo": handle_echo,
    "exit": handle_exit,
    "type": handle_type
}

def find_executable_file(command):
    path = os.environ.get("PATH")
    for dir in path.split(os.pathsep):
        executable_path = os.path.join(dir, command)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return True
    return False

def handle_execution(command, args):
    if find_executable_file(command):
        subprocess.run([command] + args)
        return True
        
    return False

    

def handle_command(command, args):
    if command_map.get(command):
        command_map[command](args)
        return
    if handle_execution(command, args):
        return
    sys.stdout.write(f"{" ".join([command] + args)}: command not found\n")
