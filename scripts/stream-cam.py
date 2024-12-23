from bambu_connect import BambuClient

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
    output_file = f"stream-cam/latest_frame_{counter}.jpg"
    print(f"Saving frame to {output_file}")
    with open(output_file, "wb") as f:
        f.write(img)

    if counter == N_PICS:
        raise KeyboardInterrupt("Stopping camera stream")


def main():
    bambu_client = BambuClient(hostname, access_code, serial)
    bambu_client.start_camera_stream(save_latest_frame)


if __name__ == "__main__":
    main()
