"""
A simple server script to communicate with a robot over TCP/IP

@Author: Vojtech Czakan
@Date: 2025-02-22
"""
import socket
import time
import threading


class RobotServer:
    """
    A simple server class to communicate with a robot over TCP/IP

    Attributes:
        host (str): The host to bind the server to
        port (int): The port to listen on
        socket (socket): The server socket
        robot_connection (socket): The connection to the robot
        listener_thread (threading.Thread): The thread to listen for commands
        running (bool): Flag to indicate if the server is running
        processing (bool): Flag to indicate if a command is being processed
    """
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.robot_connection = None
        self.listener_thread = None
        self.running = True
        self.processing = False

    def start(self):
        """
        Start the server

        :return:
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)  # Only expect one connection

        print(f"Server started on {self.host}:{self.port}")
        print("Waiting for robot to connect...")

        # Accept one connection
        conn, addr = self.socket.accept()
        self.robot_connection = conn
        print(f"Robot connected from {addr}")

        # Start listening for commands in a separate thread
        self.listener_thread = threading.Thread(target=self._process_commands)
        self.listener_thread.daemon = True  # Thread will exit when main program exits
        self.listener_thread.start()

        print("Server ready to accept commands")

    def _process_commands(self):
        """
        Process commands from the connected robot

        :return:
        """
        try:
            self.robot_connection.settimeout(1.0)  # Set timeout to allow checking running flag
            while self.running and self.robot_connection:
                try:
                    # Wait for data
                    data = self.robot_connection.recv(1024)
                    if not data:
                        if not self.running:
                            break
                        time.sleep(0.1)
                        continue

                    self.processing = False

                    # Process command
                    command = data.decode().strip()

                    if command == "PING":
                        print("Send PONG")
                        self.robot_connection.sendall(b"PONG")
                    elif command.startswith("RESULT:"):
                        result = command[7:]
                        if not result:
                            result = "nil"
                        print(f"Command result: {result}")
                    elif command.startswith("ERROR:"):
                        error = command[6:]
                        print(f"Error from robot: {error}")
                    else:
                        print(f"Unknown command from robot: {command}")
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    if not self.running:
                        break
                    time.sleep(0.5)
        except Exception as e:
            print(f"Error processing commands: {e}")
        finally:
            if self.robot_connection and self.running:
                print("Robot disconnected")
                self.robot_connection = None

    def send_command(self, command):
        """
        Send a command to the robot

        :param command: The lua command to send
        :return:
        """
        if not self.robot_connection:
            print("Error: No robot connected")

        try:
            print(f"Send command: {command}")

            while self.processing:
                time.sleep(0.1)

            self.robot_connection.sendall(f"EXECUTE:{command}".encode())
            self.processing = True

        except Exception as e:
            print(f"Error: {e}")

    def stop(self):
        """
        Stop the server

        :return:
        """
        self.running = False
        time.sleep(1.5)  # Give time for the listener thread to exit

        # Send a final message to the robot
        if self.robot_connection:
            self.robot_connection.sendall(b"EXIT")

        if self.robot_connection:
            self.robot_connection.close()
            self.robot_connection = None

        if self.socket:
            self.socket.close()

        print("Server stopped")

# Create a global instance
server_instance = RobotServer()