"""
This file contains the RobotController class which is responsible for controlling the robot

@Author: Vojtech Czakan
@Date: 2025-02-22
"""
import robot_commands

class RobotController:
    """
    Class to control the robot
    """
    def __init__(self, robot):
        self.robot = robot

    def dig(self, distance = 1, height = 1, orientation = "straight"):
        """
        Dig a hole at the specified distance, height, and orientation

        :param distance: The distance to dig
        :param height: The height to dig
        :param orientation: The orientation to dig (straight, up, down)
        :return:
        """

        for i in range(distance):
            match orientation:
                case "straight":
                    self.robot.send_command(robot_commands.get_lua_command("swing"))
                    self.robot.send_command(robot_commands.get_lua_command("forward"))
                    for j in range(height-1):
                        if j != 0:
                            self.robot.send_command(robot_commands.get_lua_command("up"))
                        self.robot.send_command(robot_commands.get_lua_command("swing_up"))
                    for j in range(height-1):
                        self.robot.send_command(robot_commands.get_lua_command("down"))

                case "up":
                    self.robot.send_command(robot_commands.get_lua_command("swing_up"))
                    self.robot.send_command(robot_commands.get_lua_command("up"))
                    for j in range(height-1):
                        if j != 0:
                            self.robot.send_command(robot_commands.get_lua_command("forward"))
                        self.robot.send_command(robot_commands.get_lua_command("swing"))
                    for j in range(height-1):
                        self.robot.send_command(robot_commands.get_lua_command("back"))
                case "down":
                    self.robot.send_command(robot_commands.get_lua_command("swing_down"))
                    self.robot.send_command(robot_commands.get_lua_command("down"))
                    for j in range(height-1):
                        if j != 0:
                            self.robot.send_command(robot_commands.get_lua_command("forward"))
                        self.robot.send_command(robot_commands.get_lua_command("swing"))
                    for j in range(height-1):
                        self.robot.send_command(robot_commands.get_lua_command("back"))

    def mine_zigzag(self, zigzag_count = 3, height = 2, length = 3):
        """
        Mine in a zigzag pattern

        :param zigzag_count: The number of zigzags to mine
        :param height: The height to mine
        :param length: The length of each zigzag
        :return:
        """

        for i in range(zigzag_count):
            self.dig(3, height, "straight")

            if i % 2 == 0:
                self.robot.send_command(robot_commands.get_lua_command("right"))
            else:
                self.robot.send_command(robot_commands.get_lua_command("left"))

            if i == 0:
                self.dig(int(length/2) , height, "straight")
            else:
                self.dig(length, height, "straight")

            if i % 2 == 0:
                self.robot.send_command(robot_commands.get_lua_command("left"))
            else:
                self.robot.send_command(robot_commands.get_lua_command("right"))




