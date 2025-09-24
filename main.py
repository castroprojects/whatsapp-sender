from flask import Flask, request, jsonify
import pywhatkit as kit
import pyautogui
import time, datetime, os
from flask import send_from_directory

app = Flask(__name__)


@app.route("/")
def frontend():
    return send_from_directory("frontend", "index.html")


@app.route("/send", methods=["POST"])
def send_messages():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    message = request.form.get("message", "")

    # Save temporary file
    path = "numbers.txt"
    file.save(path)

    with open(path) as f:
        numbers = f.readlines()

    delay = 7
    for number in numbers:
        now = datetime.datetime.now()




        hour = now.hour
        minute = now.minute + 1
        if minute == 60:
            minute = 0
            hour = (hour + 1) % 24

        kit.sendwhatmsg(f"+91{number.strip()}", message, hour, minute, wait_time=20, tab_close=True, close_time=3)
        pyautogui.press("enter")
        time.sleep(15)
        time.sleep(delay)

    os.remove(path)
    return jsonify({"message": "Messages sent successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
