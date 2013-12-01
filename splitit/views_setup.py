from decorators import lookup_or_404
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from models.auction import Auction
from models.item import Item
from models.participant import Participant
from models.user import User
from models.shared import db


setup_views = Blueprint('setup', __name__, template_folder='templates')


@setup_views.route('/')
def homepage():
    session['auction_id'] = None
    auctions = Auction.query.all()
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('homepage.html', auctions=auctions, user=user)


@setup_views.route('/auction/create', methods=['POST'])
def create_auction():
    auction = Auction()
    db.session.add(auction)
    db.session.commit()
    return redirect(url_for('setup.step1', auction_id=auction.id))


@setup_views.route('/auction/<int:auction_id>/delete', methods=['POST'])
@lookup_or_404(Auction, 'auction_id', 'auction')
def delete_auction(auction_id, auction):
    db.session.delete(auction)
    db.session.commit()
    return redirect(url_for('setup.homepage'))


@setup_views.route('/auction/<int:auction_id>/actors', methods=['GET'])
@lookup_or_404(Auction, 'auction_id', 'auction_obj')
def step1(auction_id, auction_obj):
    users = auction_obj.users
    return render_template('step1.html',
                           users=users,
                           auction=auction_obj)


@setup_views.route('/auction/<int:auction_id>/actors', methods=['POST'])
@lookup_or_404(Auction, 'auction_id', 'auction_obj')
def step1_process(auction_id, auction_obj):
    auction_obj.participants.delete()

    for name in request.form.getlist('people[]'):
        if name:
            u = User(name)
            db.session.add(u)
            db.session.commit()
            db.session.add(Participant(u.id, auction_id))

    db.session.commit()
    return redirect(url_for('setup.step2', auction_id=auction_id))


@setup_views.route('/auction/<int:auction_id>/items', methods=['GET'])
@lookup_or_404(Auction, 'auction_id', 'auction_obj')
def step2(auction_id, auction_obj):
    items = auction_obj.items
    participants = auction_obj.participants
    return render_template('step2.html',
                           items=items,
                           participants=participants,
                           auction=auction_obj)


@setup_views.route('/auction/<int:auction_id>/items', methods=['POST'])
@lookup_or_404(Auction, 'auction_id', 'auction_obj')
def step2_process(auction_id, auction_obj):
    for item in db.session.query(Item).filter_by(auction_id=auction_id).all():
        db.session.delete(item)

    for item in request.form.getlist('items[]'):
        if item:
            db.session.add(Item(item, auction_id))

    db.session.commit()
    return redirect(url_for('setup.step3', auction_id=auction_id))


@setup_views.route('/auction/<int:auction_id>/finalize', methods=['GET'])
@lookup_or_404(Auction, 'auction_id', 'auction_obj')
def step3(auction_id, auction_obj):
    zipped_users_items = map(None, auction_obj.users, auction_obj.items)
    return render_template('step3.html',
                           auction=auction_obj,
                           zipped_users_items=zipped_users_items)


@setup_views.route('/auction/<int:auction_id>/finalize', methods=['POST'])
@lookup_or_404(Auction, 'auction_id', 'auction')
def step3_process(auction_id, auction):
    auction.total_bid = request.form['total_bid']
    auction.name = request.form['name']
    db.session.add(auction)
    db.session.commit()
    return redirect(url_for('auction.auction', auction_id=auction_id))
