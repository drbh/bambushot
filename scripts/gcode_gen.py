# | Command            | Description                                          | Example                                |
# |--------------------|------------------------------------------------------|----------------------------------------|
# | `G28`             | Home all axes.                                       | `G28`                                  |
# | `G1 Z10 F300`     | Move the plate to a Z height of 10 mm at 300 mm/min. | `G1 Z10 F300`                          |
# | `G1 X50 Y50 F5000`| Move the nozzle to X=50, Y=50 at 5000 mm/min.        | `G1 X50 Y50 F5000`                     |
# | `M106 S127`       | Turn on the cooling fan at 50% speed.                | `M106 S127`                            |
# | `M104 S200`       | Set the nozzle temperature to 200°C.                 | `M104 S200`                            |
# | `M140 S60`        | Set the bed temperature to 60°C.                     | `M140 S60`                             |
# | `G29`             | Trigger auto bed leveling.                           | `G29`                                  |


class GCodeGenerator:
    def __init__(self):
        self.commands = []

        # a 40 mm buffer
        self.min_z = 205
        self.max_z = 40

    def add_command(self, command):
        self.commands.append(command)

    def home_all_axes(self):
        self.add_command("G28")

    def move_plate(self, z_height, feedrate=300):
        if z_height < self.max_z or z_height > self.min_z:
            raise ValueError(f"Z height must be between {self.max_z} and {self.min_z}")

        self.add_command(f"G1 Z{z_height} F{feedrate}")

    def move_nozzle(self, x, y, feedrate=5000):
        self.add_command(f"G1 X{x} Y{y} F{feedrate}")

    def set_fan_speed(self, speed):
        if 0 <= speed <= 255:
            self.add_command(f"M106 S{speed}")

    def dwell(self, seconds):
        self.add_command(f"G4 S{seconds}")

    def turn_off_fan(self):
        self.add_command("M107")

    def set_nozzle_temperature(self, temperature, wait=False):
        self.add_command(f"M109 S{temperature}" if wait else f"M104 S{temperature}")

    def set_bed_temperature(self, temperature, wait=False):
        self.add_command(f"M190 S{temperature}" if wait else f"M140 S{temperature}")

    def auto_bed_level(self):
        self.add_command("G29")

    def reset_printer(self):
        self.add_command("M999")

    def disable_steppers(self):
        self.add_command("M84")

    def enable_steppers(self):
        self.add_command("M17")

    def set_position(self, x=None, y=None, z=None):
        position = " ".join(
            f"{axis}{value}"
            for axis, value in zip("XYZ", [x, y, z])
            if value is not None
        )
        self.add_command(f"G92 {position}")

    def get_commands(self):
        return self.commands

    def export_commands(self, file_path):
        with open(file_path, "w") as file:
            file.write("\n".join(self.commands))

    def clear_commands(self):
        self.commands = []
