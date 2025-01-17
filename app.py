from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from config import Config
from model import Todo, db

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from Config object
db.init_app(app)  # Initialize the database

# Create database tables if they don't already exist
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if title and desc:
            new_todo = Todo(title=title, desc=desc, date_created=datetime.now())
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("index"))  # Redirect to avoid form resubmission

    all_todos = Todo.query.order_by(Todo.date_created.desc()).all()  # Fetch all todos sorted by date
    return render_template("index.html", all_todos=all_todos)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == "POST":
        todo.title = request.form.get("title")
        todo.desc = request.form.get("desc")
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)