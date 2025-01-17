from flask import Flask, render_template, request, redirect, url_for  # Importing necessary modules from Flask
from datetime import datetime  # Importing datetime to handle timestamps
from config import Config  # Importing configuration settings from the Config object
from model import Todo, db  # Importing the Todo model and db instance for database interaction

app = Flask(__name__)  # Create a Flask application instance
app.config.from_object(Config)  # Load configuration from the Config class
db.init_app(app)  # Initialize the database with the app

# Create the necessary database tables if they don't already exist
with app.app_context():  # Ensures this happens within the Flask app context
    db.create_all()  # Create all tables defined by SQLAlchemy models (Todo)

@app.route("/", methods=["GET", "POST"])  # Defining the route for the home page
def index():
    if request.method == "POST":  # Check if the request is a POST request (form submission)
        title = request.form.get("title")  # Get the title from the form
        desc = request.form.get("desc")  # Get the description from the form
        if title and desc:  # Ensure both title and description are provided
            new_todo = Todo(title=title, desc=desc, date_created=datetime.now())  # Create a new Todo object
            db.session.add(new_todo)  # Add the new todo to the session
            db.session.commit()  # Commit the session to save the new todo to the database
            return redirect(url_for("index"))  # Redirect to the home page after adding the todo to avoid form resubmission

    # Fetch all todos from the database, ordered by the date created (most recent first)
    all_todos = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template("index.html", all_todos=all_todos)  # Render the home page with the todos

@app.route("/update/<int:sno>", methods=["GET", "POST"])  # Defining the route for updating a specific todo
def update(sno):
    todo = Todo.query.get_or_404(sno)  # Get the todo by its serial number (sno), or return a 404 if not found
    if request.method == "POST":  # Check if the request is a POST request (form submission)
        todo.title = request.form.get("title")  # Update the title with the new value from the form
        todo.desc = request.form.get("desc")  # Update the description with the new value from the form
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for("index"))  # Redirect to the home page after updating the todo

    return render_template("update.html", todo=todo)  # Render the update page with the current todo information

@app.route("/delete/<int:sno>")  # Defining the route for deleting a specific todo
def delete(sno):
    todo = Todo.query.get_or_404(sno)  # Get the todo by its serial number (sno), or return a 404 if not found
    db.session.delete(todo)  # Delete the todo from the session
    db.session.commit()  # Commit the deletion to the database
    return redirect(url_for("index"))  # Redirect to the home page after deletion

@app.route('/about')  # Defining the route for the About page
def about():
    return render_template('about.html')  # Render the about page

if __name__ == "__main__":  # Check if the script is run directly
    app.run(debug=True)  # Start the Flask application in debug mode (auto reload on code changes)