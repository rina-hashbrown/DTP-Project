from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

#modern way includes
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, select
from typing import Optional
from sqlalchemy import Text
import os

# create the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

class Base(DeclarativeBase):
    pass

class Rocket(Base):
    __tablename__ = "rocket"

    # Primary Key
    rocket_id: Mapped[int] = mapped_column(primary_key=True)

    # Rocket Name (TEXT -> str)
    rocket_name: Mapped[str] = mapped_column(String(100))

    # Rocket Status (TEXT -> str)
    rocket_status: Mapped[str] = mapped_column(String(50))

    # Image URL (TEXT DEFAULT ->  str)
    image_url: Mapped[Optional[str]] = mapped_column("imageURL", Text(), nullable=True)

@app.route('/')
def get_rockets():  # Changed function name to avoid conflicts
    rockets = db.session.execute(select(Rocket)).scalars().all()  # Plural variable
    return render_template('rockets.html', rockets=rockets)

if __name__ == "__main__":
    app.run(debug=True) 

