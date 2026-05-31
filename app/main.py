import sys
import command_handler


def main():
    while True:
        user_input = input("$ ")
        command = user_input.split(" ")[0]
        args = user_input.split(" ")[1:]
        command_handler(command, args)
    
if __name__ == "__main__":
    main()
