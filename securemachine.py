import subprocess
from pathlib import Path
import datetime as dt
import time
from collections import deque

from gpiozero import DigitalInputDevice


def capture():
    output_dir = Path("/home/epitech/Desktop/SecureMachine/Results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / (
        f"video_{dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    )

    cmd = [
        "rpicam-vid",
        "-t", "10000",
        "-o", str(output_file)
    ] # On change cette commande pour changer le temps de video

    try:
        print(f"Recording video to {output_file} ...")
        subprocess.run(cmd, check=True)
        print("Recording finished.")
    except subprocess.CalledProcessError as e:
        print(f"Recording error: {e}")


if __name__ == "__main__":
    tilt = DigitalInputDevice(17)

    SAMPLE_INTERVAL = 0.02
    WINDOW_SECONDS = 1.0
    SAMPLE_RATIO = 0.6

    window_size = int(WINDOW_SECONDS / SAMPLE_INTERVAL)

    history = deque(maxlen=window_size)

    recording = False
    cooldown = 15
    last_record_time = 0

    while True:
        history.append(1 if tilt.value else 0)

        if len(history) == window_size:
            activity_ratio = sum(history) / window_size

            if activity_ratio > SAMPLE_RATIO:
                now = time.time()

                if now - last_record_time > cooldown:

                    capture()

                    last_record_time = now

        time.sleep(SAMPLE_INTERVAL)
