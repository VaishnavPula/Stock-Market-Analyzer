from datetime import datetime, timezone
from flask_login import UserMixin
from . import db, login_manager
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(30), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id','stock_symbol'),)
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(30), nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    forecast_horizon = db.Column(db.Integer, nullable=False)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
