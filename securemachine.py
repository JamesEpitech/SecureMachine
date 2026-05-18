import subprocess
from pathlib import Path
import datetime as dt
import time
from collections import deque
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

from gpiozero import DigitalInputDevice


load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SAMPLE_INTERVAL = 0.02
WINDOW_SECONDS = 1.0
SAMPLE_RATIO = 0.6
RECORD_TIME = "10000"

RECEIVER_EMAIL = "example@gmail.com"


def send_email(video_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = "SecureMachine - Motion Detected"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL

        msg.set_content(
            f"The machine has been shook!\n\nVideo attached:\n{video_path.name}"
        )

        with open(video_path, "rb") as f:
            file_data = f.read()
            file_name = video_path.name

        msg.add_attachment(
            file_data,
            maintype="video",
            subtype="mp4",
            filename=file_name
        )

        print("Sending email...")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email sent successfully.")

    except Exception as e:
        print(f"Email sending failed: {e}")


def capture():
    output_dir = Path("/home/epitech/Desktop/SecureMachine/Results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / (
        f"video_{dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    )

    cmd = [
        "rpicam-vid",
        "-t", RECORD_TIME,
        "-o", str(output_file)
    ]

    try:
        print(f"Recording video to {output_file} ...")
        subprocess.run(cmd, check=True)
        print("Recording finished.")

        send_email(output_file)

    except subprocess.CalledProcessError as e:
        print(f"Recording error: {e}")


if __name__ == "__main__":
    tilt = DigitalInputDevice(17)

    window_size = int(WINDOW_SECONDS / SAMPLE_INTERVAL)

    history = deque(maxlen=window_size)

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
