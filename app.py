from flask import Flask, request, jsonify
from datetime import datetime, time

app = Flask(__name__)

# store tasks here temporarily (no database)
tasks = []

@app.route("/")
def home():
    return "Energy-Efficient Task Scheduler Backend is running!"

# Add a task
@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json
    
    task = {
        "task_name": data["task_name"],
        "task_type": data["task_type"],
        "mode": data["mode"],                     # "normal" or "greenops"
        "run_time": data.get("run_time"),         # for normal mode
        "start_window": data.get("start_window"), # for greenops
        "end_window": data.get("end_window"),
        "status": "Scheduled"
    }
    
    tasks.append(task)
    return jsonify({"message": "Task added!", "task": task}), 201


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


# Simulate the scheduler (VERY SIMPLE)
@app.route("/run-scheduler", methods=["GET"])
def run_scheduler():
    now = datetime.now().time()
    
    for task in tasks:
        if task["status"] == "Completed":
            continue

        # NORMAL MODE LOGIC
        if task["mode"] == "normal":
            if task["run_time"] == now.strftime("%H:%M"):
                task["status"] = "Completed"

        # GREENOPS MODE LOGIC
        if task["mode"] == "greenops":
            start = datetime.strptime(task["start_window"], "%H:%M").time()
            end = datetime.strptime(task["end_window"], "%H:%M").time()

            # check if current time is inside window
            if start <= now <= end:
                task["status"] = "Completed"

    return jsonify({"message": "Scheduler checked tasks!", "tasks": tasks})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
