from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from parse_dol import convert_dol_rub
from google_sheet import GoogleSheet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/task'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3894sdf382rerrredfj438udshf3hhdsHUAFR#&hsr3HUA)2jdsfsfds'

db = SQLAlchemy(app)


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_order = db.Column(db.Integer)
    cost_dol = db.Column(db.Float)
    date = db.Column(db.DateTime)
    cost_rub = db.Column(db.Float)


@app.route('/')
def index():
    gs = GoogleSheet()
    ranges = 'list1!A:E'
    res = gs.get_values(ranges)
    dol = convert_dol_rub()
    lst = []
    for i in res:
        if len(i) == 4:
            i.append(int(int(i[-2]) * dol))
            lst.append([i[-1]])
            info = Info(num_order=i[1], cost_dol=i[2], date=i[3], cost_rub=i[4])
            db.session.add(info)
            db.session.commit()
        else:
            info = Info.query.filter(Info.id == int(i[0])).all()
            i[-1] = int(int(i[-3])*dol)
            lst.append([i[-1]])
            info[0].cost_rub = i[-1]
    gs.updateRangeValues(f'list1!E2:E{len(lst)+1}', lst)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
