from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

goals = {}  # Dictionary: goal_id -> {title, description, steps}

@app.route("/")
def index():
    return render_template("index.html", goals=goals)

@app.route("/add_goal", methods=["POST"])
def add_goal():
    title = request.form["title"]
    description = request.form["description"]
    goal_id = str(len(goals) + 1)
    goals[goal_id] = {"title": title, "description": description, "steps": []}
    return redirect("/")

@app.route("/goal/<goal_id>")
def view_goal(goal_id):
    goal = goals.get(goal_id)
    return render_template("goal.html", goal=goal, goal_id=goal_id)

@app.route("/goal/<goal_id>/add_step", methods=["POST"])
def add_step(goal_id):
    step = request.form["step"]
    if goal_id in goals:
        goals[goal_id]["steps"].append({"text": step, "done": False})
    return redirect(url_for("view_goal", goal_id=goal_id))

@app.route("/goal/<goal_id>/complete_step/<int:step_index>")
def complete_step(goal_id, step_index):
    if goal_id in goals and 0 <= step_index < len(goals[goal_id]["steps"]):
        goals[goal_id]["steps"][step_index]["done"] = True
    return redirect(url_for("view_goal", goal_id=goal_id))

@app.route("/goal/<goal_id>/delete")
def delete_goal(goal_id):
    goals.pop(goal_id, None)
    return redirect("/")
