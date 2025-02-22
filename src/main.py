"""
Main entry point for the robot controller. This script will start the server and
allow the user to send commands to the robot.

@Author: Vojtech Czakan
@Date: 2025-02-22
"""
import time

from robot_server import server_instance
import robot_commands
from robot_controller import RobotController
import robot_server

if __name__ == "__main__":
    try:
        test = robot_server.RobotServer()
        server_instance.start()
        robot_controller = RobotController(server_instance)

        # Keep the main thread running
        while True:
            time.sleep(1)
            cmd = input("Enter command ('help' for available commands): ")
            if cmd.lower() == 'help':
                robot_commands.print_all_commands()
                continue
            elif cmd.lower() == 'dig':
                distance = int(input("Enter distance to dig: "))
                height = int(input("Enter height to dig: "))
                orientation = input("Enter orientation to dig (straight, up, down): ")
                robot_controller.dig(distance, height, orientation)
                continue
            elif cmd.lower() == 'mine':
                zigzag_count = int(input("Enter number of zigzags: "))
                height = int(input("Enter height to mine: "))
                length = int(input("Enter length of each zigzag: "))
                robot_controller.mine_zigzag(zigzag_count, height, length)
                continue
            response = server_instance.send_command(robot_commands.get_lua_command(cmd))

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_instance.stop()