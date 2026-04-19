from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date
from sqlalchemy import case

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    due_date = db.Column(
        db.Date,
        nullable=True
    )

    priority = db.Column(
        db.String(10),
        default="Medium"
    )

    def __repr__(self):
        return f"<Task {self.id}>"

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        title = request.form.get("title")
        due_date_str = request.form.get("due_date")
        priority = request.form.get("priority")

        due_date = None

        if due_date_str:
            due_date = datetime.strptime(
                due_date_str,
                "%Y-%m-%d"
            ).date()

        new_task = Task(
            title=title,
            due_date=due_date,
            priority=priority
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect("/")

    search = request.args.get("search")
    sort = request.args.get("sort", "due")
    query = Task.query

    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    if sort == "priority":

        query = query.order_by(
            case(
                (Task.priority == "High", 1),
                (Task.priority == "Medium", 2),
                (Task.priority == "Low", 3),
                else_=4
            )
        )

    elif sort == "new":

        query = query.order_by(
            Task.id.desc()
        )

    elif sort == "old":

        query = query.order_by(
            Task.id.asc()
        )

    else:

        query = query.order_by(
            case(
                (Task.due_date == None, 1),
                else_=0
            ),
            Task.due_date.asc()
        )

    tasks = query.all()
    completed_count = Task.query.filter_by(
        completed=True
    ).count()

    uncompleted_count = Task.query.filter_by(
        completed=False
    ).count()

    total_count = Task.query.count()

    completed_count = Task.query.filter_by(
        completed=True
    ).count()

    uncompleted_count = Task.query.filter_by(
        completed=False
    ).count()

    overdue_count = Task.query.filter(
        Task.completed == False,
        Task.due_date < date.today()
    ).count()

    high_count = Task.query.filter_by(
        priority="High"
    ).count()

    medium_count = Task.query.filter_by(
        priority="Medium"
    ).count()

    low_count = Task.query.filter_by(
        priority="Low"
    ).count()

    return render_template(
        "index.html",
        tasks=tasks,
        completed_count=completed_count,
        uncompleted_count=uncompleted_count,
        total_count=total_count,
        overdue_count=overdue_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        date=date
    )

@app.route("/complete/<int:id>",methods=["POST"])
def complete(id):
    task = Task.query.get(id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>",methods=["GET", "POST"])
def edit(id):
    task = Task.query.get(id)
    if request.method == "POST":
        new_title = request.form.get("title")
        task.title = new_title
        db.session.commit()
        return redirect("/")
    
    return render_template("edit.html",task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)