import os
from typing import Optional
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, select

# Create the app
app = Flask(__name__)

# Configure SQLite database path explicitly
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy extension
db = SQLAlchemy(app)

# Define Model inheriting from db.Model
class Rocket(db.Model):
    __tablename__ = "rocket"

    # Primary Key
    rocket_id: Mapped[int] = mapped_column(primary_key=True)

    # Rocket Name
    rocket_name: Mapped[str] = mapped_column(String(100))

    # Rocket Status
    rocket_status: Mapped[str] = mapped_column(String(50))

    # Image URL (Optional)
    imageurl: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)


@app.route('/')
def get_rockets():
    rockets = db.session.execute(select(Rocket)).scalars().all()
    return render_template('rockets.html', rockets=rockets)


if __name__ == "__main__":
    app.run(debug=True)
