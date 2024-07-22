from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # Initialize the Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"  # Configure the SQLite database URI
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app

# Define the Todo model for the database
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Primary key column
    title = db.Column(db.String(200), nullable=False)  # Title column (string, cannot be null)
    desc = db.Column(db.String(500), nullable=False)  # Description column (string, cannot be null)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Date created column (defaults to current datetime)

    # Define the string representation of the Todo model
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # Get title and description from the form
        title = request.form['title']
        desc = request.form['desc']
        
        # Create a new Todo object
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)  # Add the new Todo to the database session
        db.session.commit()  # Commit the session to save the Todo to the database
    
    # Retrieve all Todo items from the database
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)  # Render the index.html template with the Todo items

# Route for the show page (not currently used in templates)
@app.route('/show')
def products():
    allTodo = Todo.query.all()  # Retrieve all Todo items from the database
    print(allTodo)  # Print the Todo items to the console
    return 'product ka page!'  # Return a placeholder response

# Route for updating a Todo item
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        # Get the updated title and description from the form
        title = request.form['title']
        desc = request.form['desc']
        
        # Retrieve the Todo item by its serial number (sno)
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title  # Update the title
        todo.desc = desc  # Update the description
        db.session.add(todo)  # Add the updated Todo to the session
        db.session.commit()  # Commit the session to save the changes
        return redirect("/")  # Redirect to the home page after updating

    # Retrieve the Todo item by its serial number (sno)
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)  # Render the update.html template with the Todo item

# Route for deleting a Todo item
@app.route('/delete/<int:sno>')
def delete(sno):
    # Retrieve the Todo item by its serial number (sno)
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)  # Delete the Todo item from the session
    db.session.commit()  # Commit the session to save the changes
    return redirect("/")  # Redirect to the home page after deleting

# Main entry point of the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they do not exist
    app.run(debug=True)  # Run the Flask application in debug mode

