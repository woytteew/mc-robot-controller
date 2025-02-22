local component = require("component")
local internet = require("internet")
local event = require("event")
local robot = require("robot")

local server_ip = "YOUR_PC_IP"
local server_port = 12345

local function connect_to_server()
    print("Connecting to server...")

    local socket = internet.socket(server_ip, server_port)
    if not socket then
        print("Connection failed.")
        return nil
    end

    print("Connected to server!")
    return socket
end

local function process_commands(socket)
    while true do
        local response = ""
        local chunk = socket:read()

        if chunk and chunk ~= "" then
            response = chunk
            print("Received command: " .. response)

            -- Extract command
            local command = response:match("EXECUTE:(.*)")
            if command then
                -- Create a safe environment with access to robot API
                local env = {
                    robot = robot,
                    component = component,
                    print = print,
                    -- Add other APIs you need
                    os = os
                }

                -- Load the command with the environment
                local fn, err = load(command, "command", "t", env)

                if not fn then
                    socket:write("ERROR:Syntax error: " .. tostring(err))
                else
                    local success, result = pcall(fn)
                    if success then
                        socket:write("RESULT:OK" .. (result and (": " .. tostring(result)) or ""))
                    else
                        socket:write("ERROR:" .. tostring(result))
                    end
                end
            elseif response == "PONG" then
                print("Server is alive!")
            elseif response == "PING" then
                socket:write("PONG")  -- Respond to server ping
            elseif response == "EXIT" then
                print("Server requested exit.")
                return true
            else
                print("Unknown command received: '" .. response .. "'")
            end
        end

        os.sleep(0.5)  -- Prevent excessive CPU usage
    end
end

-- **Main loop to keep reconnecting**
while true do
    local socket = connect_to_server()
    if socket then
        socket:write("PING")  -- Notify server of connection
        local success = process_commands(socket)
        socket:close()
    end

    print("Reconnecting in 5 seconds...")
    os.sleep(5)
end