import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from config import Config
from models import db, login_manager
from models.database import User, Watchlist, PredictionHistory
from services.stock_service import symbol_for, get_history, serialize
from services.analysis_service import insights
from services.prediction_service import predict_prices

app=Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.instance_path,exist_ok=True)
db.init_app(app);login_manager.init_app(app);CSRFProtect(app)
with app.app_context():db.create_all()

@app.get('/')
def index():return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username','').strip();email=request.form.get('email','').strip().lower();password=request.form.get('password','')
        if len(username)<3 or '@' not in email or len(password)<8:flash('Username must have 3+ characters, email must be valid, password must have 8+ characters.','error')
        else:
            try:
                user=User(username=username,email=email,password_hash=generate_password_hash(password));db.session.add(user);db.session.commit();login_user(user);return redirect(url_for('dashboard'))
            except IntegrityError:db.session.rollback();flash('Username or email already registered.','error')
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User.query.filter_by(email=request.form.get('email','').strip().lower()).first()
        if user and check_password_hash(user.password_hash,request.form.get('password','')):login_user(user);return redirect(url_for('dashboard'))
        flash('Invalid email or password.','error')
    return render_template('login.html')
@app.post('/logout')
@login_required
def logout():logout_user();return redirect(url_for('index'))
@app.get('/dashboard')
@login_required
def dashboard():return render_template('dashboard.html')
@app.get('/stock/<symbol>')
@login_required
def stock(symbol):return render_template('stock.html',symbol=symbol_for(symbol))
@app.get('/api/stock/<symbol>')
@login_required
def stock_api(symbol):
    try:
        symbol=symbol_for(symbol);df=get_history(symbol,request.args.get('period','1y'),request.args.get('start'),request.args.get('end'))
        rows=serialize(df);last=rows[-1];prev=rows[-2]['close'] if len(rows)>1 else last['close']
        return jsonify(symbol=symbol,rows=rows,latest=last['close'],change=round(last['close']-prev,2),change_pct=round((last['close']/prev-1)*100,2) if prev else 0,insights=insights(df))
    except (ValueError,KeyError) as e:return jsonify(error=str(e)),400
    except Exception:return jsonify(error='Stock data service unavailable. Please retry.'),503
@app.post('/api/predict')
@login_required
def prediction_api():
    try:
        data=request.get_json(silent=True) or {};symbol=symbol_for(data.get('symbol'));days=int(data.get('days',1))
        if days not in (1,5,7):raise ValueError('Forecast must be 1, 5 or 7 sessions.')
        df=get_history(symbol,'5y');result=predict_prices(df,days)
        db.session.add(PredictionHistory(user_id=current_user.id,stock_symbol=symbol,predicted_price=result['predictions'][-1],forecast_horizon=days));db.session.commit()
        return jsonify(symbol=symbol,**result)
    except (ValueError,TypeError) as e:return jsonify(error=str(e)),400
    except Exception:
        db.session.rollback();return jsonify(error='Prediction could not be completed. Check data availability.'),503
@app.get('/prediction')
@login_required
def prediction():return render_template('prediction.html')
@app.get('/predictions/history')
@login_required
def prediction_history():
    records=PredictionHistory.query.filter_by(user_id=current_user.id).order_by(PredictionHistory.id.desc()).limit(50).all()
    return render_template('prediction.html',records=records)
@app.get('/watchlist')
@login_required
def watchlist():return render_template('watchlist.html',items=Watchlist.query.filter_by(user_id=current_user.id).all())
@app.post('/watchlist/add')
@login_required
def watchlist_add():
    try:
        symbol=symbol_for(request.form.get('symbol'));db.session.add(Watchlist(user_id=current_user.id,stock_symbol=symbol));db.session.commit();flash('Stock added to watchlist.','success')
    except IntegrityError:db.session.rollback();flash('Already in your watchlist.','error')
    except ValueError as e:flash(str(e),'error')
    return redirect(url_for('watchlist'))
@app.post('/watchlist/remove')
@login_required
def watchlist_remove():
    item=Watchlist.query.filter_by(id=request.form.get('id',type=int),user_id=current_user.id).first_or_404();db.session.delete(item);db.session.commit();return redirect(url_for('watchlist'))
@app.get('/compare')
@login_required
def compare():return render_template('compare.html')
@app.get('/api/compare')
@login_required
def compare_api():
    try:
        s1=symbol_for(request.args.get('first'));s2=symbol_for(request.args.get('second'))
        a=get_history(s1,'1y')['Close'];b=get_history(s2,'1y')['Close'];joined=a.to_frame('a').join(b.to_frame('b'),how='inner').dropna()
        if len(joined)<2:raise ValueError('Not enough shared trading dates.')
        return jsonify(dates=[str(i.date()) for i in joined.index],first=s1,second=s2,a=(joined.a/joined.a.iloc[0]*100).round(2).tolist(),b=(joined.b/joined.b.iloc[0]*100).round(2).tolist(),return_a=round((joined.a.iloc[-1]/joined.a.iloc[0]-1)*100,2),return_b=round((joined.b.iloc[-1]/joined.b.iloc[0]-1)*100,2),volatility_a=round(joined.a.pct_change().std()*100,2),volatility_b=round(joined.b.pct_change().std()*100,2))
    except ValueError as e:return jsonify(error=str(e)),400
    except Exception:return jsonify(error='Comparison data unavailable.'),503
@app.errorhandler(404)
def not_found(error):return render_template('error.html',message='Page not found.'),404
if __name__=='__main__':app.run(debug=False)
