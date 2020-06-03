from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
import datetime
from flask import  send_from_directory

from flask_sqlalchemy import SQLAlchemy


#loginform
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6,16)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class ModifyForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(2, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 16)])
    repeat_password = PasswordField('Again密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交修改')


class  dateForm(FlaskForm):
    submit = SubmitField("提交")


from flask import Flask
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sight:123456@192.168.190.147/open-vpn"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sight:123456@vpnsql/open-vpn"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class  Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(25), primary_key=True)
    admin_pass = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<User %r>' % self.admin_id


class  Log(db.Model):
    __tablename__ = 'log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(25))
    log_trusted_ip = db.Column(db.String(25))
    log_trusted_port = db.Column(db.String(25))
    log_remote_ip = db.Column(db.String(25))
    log_remote_port = db.Column(db.String(25))
    log_start_time = db.Column(db.DateTime)
    log_end_time = db.Column(db.DateTime)
    def __repr__(self):
        return '<User %r>' % self.user_id


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(25),primary_key=True)
    user_pass = db.Column(db.String(25), nullable=False, default='123456')
    user_online = db.Column(db.Boolean, default=False)
    user_enable = db.Column(db.Boolean, default=True)
    user_start_date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_end_date = db.Column(db.DateTime)
    def __init__(self, userid):
        self.user_id = userid
    def __repr__(self):
        return '<User %r>' % self.user_id


app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'
@app.route('/', methods=['GET', 'POST'])
def index():
   form = LoginForm()
   if 'username' not in session:
       if form.validate_on_submit():
           username = form.username.data
           passwd = form.password.data
           admin = Admin.query.first()
           if username == admin.admin_id and passwd == admin.admin_pass:
               session['username'] = username
               return redirect(url_for('admin', _external=True))
           else:
               flash('your usename or password is not correct, please check!')
               return render_template('index.html', form=form)
       return render_template('index.html', form=form)
   else:
       return redirect(url_for('admin', _external=True))


########
########开启普通用户可登录,可修改自己的密码
#####
# @app.route('/', methods=['GET', 'POST'])
# def index():
#         form = LoginForm()
#         if 'username' not in session:
#             if form.validate_on_submit():
#                 username = form.username.data
#                 passwd = form.password.data
#                 if username == "admin":
#                     admin = Admin.query.first()
#                     if passwd == admin.admin_pass:
#                         session['username'] = username
#                         return redirect(url_for('admin', _external=True))
#                     flash("检查你的账号密码")
#                     return render_template('index.html', form=form)
#                 else:
#                     login_user = User.query.filter_by(user_id=username).first()
#                     if login_user and passwd == login_user.user_pass:
#                         session['username'] = username
#                         return redirect(url_for('user', name=username))
#                     flash("检查你的账号密码")
#                     return render_template('index.html', form=form)
#             return render_template('index.html', form=form)

#         else:
#             session.pop('username', None)
#             return redirect(url_for('index', _external=True))
#             #return redirect(url_for('admin', _external=True))

# @app.route('/user/<name>', methods=['GET', 'POST'])
# def user(name):
#         form = ModifyForm()
#         form.username.data = session['username']
#         if 'username' in session:
#             if form.validate_on_submit():
#                 username = form.username.data
#                 passwd = form.password.data
#                 # count = User.query.filter_by(user_id='gf').update({'user_pass': 'hahahahahhah'})
#                 count = User.query.filter_by(user_id=username).update({'user_pass': passwd})  # 返回受影响行数
#                 db.session.commit()
#                 if count:
#                     flash("vpn 密码修改成功,请重新登录!!")
#                     session.pop('username', None)
#                     return redirect(url_for('index', _external=True))
#                 flash("vpn 密码修改失败!!")
#             return render_template('modify.html', form=form)
#         else:
#             flash("please login")
#             return redirect(url_for('index', _external=True))

######普通账号可修改自己的密码------结束#######################




@app.route('/admin',methods=['GET', 'POST'])
def admin():
    # users = User.query.all()
    form = dateForm()
    if request.method == 'GET':
        if 'username' not in session:
            flash('please  login!')
            return redirect(url_for('index', _external=True))
        if session['username'] == 'admin':
            users = User.query.filter_by(user_online=1).all()
            today = datetime.date.today().__format__('%Y-%m-%d')
            #users = User.query.all()
            logs = Log.query.filter(Log.log_start_time.startswith(today)).all()
            #logs = Log.query.all()
            return render_template('admin.html', users=users, logs=logs, form=form)
        else:
            flash("not allowed access!!")
            session.pop('username', None)
            return redirect(url_for('index', _external=True))
    else:
        if 'username' not in session:
            flash('please  login!')
            return redirect(url_for('index', _external=True))
        if session['username'] == 'admin':
            users = User.query.filter_by(user_online=1).all()
            today = date=request.form['getdate']
            #users = User.query.all()
            logs = Log.query.filter(Log.log_start_time.startswith(today)).all()
            #logs = Log.query.all()
            return render_template('admin.html', users=users, logs=logs, form=form)
        else:
            flash("not allowed access!!")
            session.pop('username', None)
            return redirect(url_for('index', _external=True))


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have logout!')
    return redirect(url_for('index', _external=True))

@app.route('/useradd', methods=['GET', 'POST'] )
def  useradd():
     if 'username' not in session:
        return redirect(url_for('index', _external=True))

     if request.method == 'POST':
          userstoadd = list(request.form.get('users').strip().split())
          for user in userstoadd:
              if User.query.filter_by(user_id=user).first():
                  flash('{} existed!'.format(user))
              else:
                  flash('{} created!'.format(user))
                  tmp = User(user)
                  db.session.add(tmp)
                  db.session.commit()
          return render_template('useradd.html')
                 
     return render_template('useradd.html')


@app.route('/help')
def  help():
     return render_template('openvpn-manual.html')


@app.route("/download/windows")
def windows():
    #改成容器内目录
    return send_from_directory(r"/app/download",filename="forwindows.zip",as_attachment=True)

@app.route("/download/ubuntu")
def ubuntu():
    return send_from_directory(r"/app/download",filename="forubuntu.zip",as_attachment=True)

@app.route("/download/mac")
def mac():
    return send_from_directory(r"/app/download",filename="formac.zip",as_attachment=True)
   

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = True)

