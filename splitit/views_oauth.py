from oauth2client.client import verify_id_token

from flask import Blueprint
from flask import current_app
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_oauth import OAuth
from models.user import User
from models.shared import db

oauth_views = Blueprint('oauth', __name__, template_folder = 'templates')

oauth = OAuth()
google = oauth.remote_app('google',
    base_url=current_app.config['OAUTH_BASE_URL'],
    authorize_url=current_app.config['OAUTH_AUTHORIZE_URL'],
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                          'response_type': 'code'},
    access_token_method='POST',
    access_token_url=current_app.config['OAUTH_ACCESS_TOKEN_URL'],
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=current_app.config['OAUTH_CONSUMER_KEY'],
    consumer_secret=current_app.config['OAUTH_CONSUMER_SECRET']
    )

@google.tokengetter
def get_google_token(token=None):
    return session.get('google_token')

@oauth_views.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/')
    return google.authorize(callback=url_for('oauth.authorized', _external=True))

@oauth_views.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@oauth_views.route('/callback')
@google.authorized_handler
def authorized(resp):
    if resp is None:
        return redirect('/')
    token = resp['access_token']
    userinfo = verify_id_token(resp['id_token'],
                               current_app.config['OAUTH_CONSUMER_KEY'])
    email = userinfo['email']
    u = db.session.query(User).filter_by(email = email).first()
    if not u:
        u = User()
        u.email = email
        u.oauth_access_token = token
    else:
        u.oauth_access_token = token
    db.session.add(u)
    db.session.commit()
    session['user_id'] = u.id
    return redirect('/')
