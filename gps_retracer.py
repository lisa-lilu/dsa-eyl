class GPSRetracer:
    def __init__(self):
        # Stack to store logged actions
        self.stack = []

    def log(self, action):
        # Save the action in the stack
        self.stack.append(action)

    def invert_action(self, action):
        # Change the action to its opposite
        parts = action.split()

        if parts[0] == "LEFT":
            return "RIGHT"
        elif parts[0] == "RIGHT":
            return "LEFT"
        elif parts[0] == "FWD":
            return action
        else:
            raise ValueError("Unknown action")

    def calculate_return(self):
        # Print the return path
        step = 1
        temp_stack = self.stack.copy()

        while temp_stack:
            action = temp_stack.pop()
            inverted = self.invert_action(action)
            print(f"{step}. {inverted}")
            step += 1


# -------------------------
# CLI Input Section
# -------------------------
if __name__ == "__main__":
    gps = GPSRetracer()

    print("Enter commands (type EXIT to stop):")

    while True:
        command = input("> ").strip()

        if command == "EXIT":
            break

        elif command.startswith("LOG"):
            # Example: LOG FWD 100
            action = command.replace("LOG ", "")
            gps.log(action)

        elif command == "CALCULATE_RETURN":
            print("\nCALCULATE_RETURN")
            gps.calculate_return()

        else:
            print("Invalid command")
