class GPSRetracer:
    def __init__(self):
        # Stack to store logged actions
        self.stack = []

    def log(self, action: str):
        """Push an action onto the stack."""
        self.stack.append(action)

    def invert_action(self, action: str) -> str:
        """Invert a single action according to the rules."""
        parts = action.split()

        if parts[0] == "LEFT":
            return "RIGHT"
        elif parts[0] == "RIGHT":
            return "LEFT"
        elif parts[0] == "FWD":
            # Forward distance remains the same
            return action
        else:
            raise ValueError(f"Unknown action: {action}")

    def calculate_return(self):
        """Read stack in reverse, invert actions, and print return path."""
        step = 1
        temp_stack = self.stack.copy()  # preserve original log

        while temp_stack:
            action = temp_stack.pop()  # LIFO
            inverted = self.invert_action(action)
            print(f"{step}. {inverted}")
            step += 1


# -------------------------
# Sample CLI-style usage
# -------------------------
if __name__ == "__main__":
    gps = GPSRetracer()

    gps.log("FWD 100")
    gps.log("LEFT")
    gps.log("FWD 50")

    print("\nCALCULATE_RETURN")
    gps.calculate_return()
