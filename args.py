"""
A module to handle command line arguments for lsb.py
"""

import sys

class Command:
    def __init__(self, name):
        self.name = name
        self.arguments = []

    def add_arg(self, short_name, long_name, default=None, description=""):
        """Add a possible argument"""
        self.arguments.append({
            "short": short_name,
            "long": long_name,
            "default": default,
            "description": description
        })

    def parse(self, args, usage_callback):
        """Parse an array of arguments based on the loaded possible arguments"""
        
        parsed_values = {}

        for argument in self.arguments:
            arg_idx = [idx for idx in range(len(args)) if args[idx] == argument["short"] or args[idx] == argument["long"]]

            value = None

            if len(arg_idx) > 1:
                usage_callback(f"Duplicate argument: {argument['short']}")
            elif len(arg_idx) == 0:
                if argument["default"] == None:
                    usage_callback(f"Expected argument: {argument['short']}")
                else:
                    value = argument["default"]
            else:
                try:
                    value = args[arg_idx[0] + 1]
                except IndexError:
                    usage_callback(f"Expected value for argument: {argument['short']}")

            parsed_values[argument["short"]] = value

        return parsed_values



class ArgumentsParser:
    """A class to handle command line argument processing"""

    def __init__(self):
        self.commands = []

    def usage(self, error_msg):
        """Print usage information and exit"""

        print(f"error: {error_msg}\n")
        print("Usage:")
        print("python lsb.py [command] <arguments>\n")

        print("Available commands:")

        for command in self.commands:
            print(command.name)
            for arg in command.arguments:
                print("\t{:<20} {:<}".format(f"{arg['short']}/{arg['long']}", arg["description"]))

        sys.exit()

    def add_command(self, command):
        """Add a new command object to the ArgumentsParser instance"""
        self.commands.append(command)

    def parse_args(self, argv):
        """Parse the arguments based on established rules"""

        if len(argv) == 1:
            self.usage("Missing arguments")

        parsed = False
        for cmd in self.commands:
            if argv[1] == cmd.name:
                name = cmd.name
                values = cmd.parse(argv[2:], self.usage)
                parsed = True
                break
        if not parsed:
            self.usage(f"Unknown command: {argv[1]}")

        return (name, values)