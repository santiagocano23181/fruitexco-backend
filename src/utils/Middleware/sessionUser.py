from sys import flags

from flask import session

def session_middleware():
    if(session.get('user_session')):
        ""