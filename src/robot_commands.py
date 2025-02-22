"""
This file contains the commands that the robot can execute.

@Author: Vojtech Czakan
@Date: 2025-02-22
"""

MOVEMENT_COMMANDS = {
    "forward": "robot.forward()",
    "back": "robot.back()",
    "left": "robot.turnLeft()",
    "right": "robot.turnRight()",
    "up": "robot.up()",
    "down": "robot.down()",
}

INTERACTION_COMMANDS = {
    "detect": "robot.detect()",
    "detect_up": "robot.detectUp()",
    "detect_down": "robot.detectDown()",
    "place": "robot.place()",
    "swing": "robot.swing()",
    "swing_up": "robot.swingUp()",
    "swing_down": "robot.swingDown()",
}

CUSTOM_COMMANDS = {
    "place": ""
}


def get_lua_command(command):
    """
    Convert a Python command to its Lua equivalent

    Args:
        command (str): The command name

    Returns:
        str: The Lua code to execute
    """
    # Check command in all command dictionaries
    for command_dict in [MOVEMENT_COMMANDS, INTERACTION_COMMANDS]:
        if command in command_dict:
            if callable(command_dict[command]):
                return command_dict[command]
            return command_dict[command]

    # If command not found, check if it's raw Lua
    if command.startswith("lua:"):
        return command[4:]

    # Command not found
    return None

def get_all_commands():
    """Return a list of all available commands with descriptions"""
    all_commands = []

    # Combine all command dictionaries
    categories = [
        ("Movement", MOVEMENT_COMMANDS),
        ("Interaction", INTERACTION_COMMANDS),
    ]

    for category, command_dict in categories:
        for cmd in command_dict:
            # Skip callables in this list since they need parameters
            if not callable(command_dict[cmd]):
                all_commands.append((category, cmd, command_dict[cmd]))

    return all_commands


def print_all_commands():
    """Print all available commands with descriptions"""
    all_commands = get_all_commands()
    for category, cmd, description in all_commands:
        print(f"{cmd}: {description}")