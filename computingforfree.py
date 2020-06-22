from app import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
    """this is for flask shell to be able to assess objects on the commandline"""
    return {'db': db, 'User': User}
