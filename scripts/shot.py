from bambu_connect import BambuClient
import time
from gcode_gen import GCodeGenerator

from dotenv import load_dotenv
import os

load_dotenv()

hostname = os.getenv("HOSTNAME")
access_code = os.getenv("ACCESS_CODE")
serial = os.getenv("SERIAL")

counter = 0
N_PICS = 50


def save_latest_frame(img):
    global counter
    counter += 1
    output_file = f"frames/latest_frame_{counter}.jpg"
    print(f"Saving frame to {output_file}")
    with open(output_file, "wb") as f:
        f.write(img)

    if counter == N_PICS:
        raise KeyboardInterrupt("Stopping camera stream")


def main():
    bambu_client = BambuClient(hostname, access_code, serial)

    # place at bottom to initialize the shot process
    gcode = GCodeGenerator()
    gcode.move_plate(100, feedrate=1000)  # move fast
    gcode_command = "\n".join(gcode.get_commands())
    print(f"Sending G-code command: {gcode_command}")
    bambu_client.send_gcode(gcode_command)
    time.sleep(12)
    print("Finished moving to position")

    # move to position and take pictures
    gcode = GCodeGenerator()
    gcode.move_plate(40, feedrate=100)
    gcode_command = "\n".join(gcode.get_commands())
    print(f"Sending G-code command: {gcode_command}")
    bambu_client.send_gcode(gcode_command)
    time.sleep(1)

    bambu_client.start_camera_stream(save_latest_frame)


if __name__ == "__main__":
    main()
