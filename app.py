from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///post.db'
db = SQLAlchemy(app)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='N')
    date_entered = db.Column(
        db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return 'list_tile ' + str(self.id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/master')
def master():
    val = {'title': "Master List", 'data': List.query.all()}
    print(val)
    return render_template("base_list.html", val=val)


@app.route('/monthly')
def monthly():
    val = {'title': "Monthly List", 'data': List.query.all()}
    return render_template("base_list.html", val=val)


@app.route('/weekly')
def weekly():
    val = {'title': "Weekly List", 'data': List.query.all()}
    return render_template("base_list.html", val=val)


@app.route('/daily')
def daily():
    val = {'title': "Daily List", 'data': List.query.all()}
    return render_template("base_list.html", val=val)


@app.route('/ch/delete')
def delete():
    type = request.args.get('type')
    id = int(request.args.get('id'))
    data = List.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    val = {'title': type, 'data': List.query.all()}
    return render_template("base_list.html", val=val)


@app.route('/ch/edit')
def edit():
    type = request.args.get('type')
    id = request.args.get('id')
    val = {'title': type, 'data': List.query.all()}
    print(val, id)
    return render_template("edit.html", val=val, id=id)


@app.route('/add', methods=['POST'])
def add():
    type = request.form['type']
    title = request.form['title']
    content = request.form['content']
    db.session.add(List(type=type, title=title, content=content))
    db.session.commit()
    val = {'title': type, 'data': List.query.all()}
    return render_template("base_list.html", val=val)


@app.route('/edit', methods=['GET', 'POST'])
def editi():
    type = request.args.get('type')
    id = int(request.form['id'])
    data = List.query.get_or_404(id)
    data.title = request.form['title']
    data.content = request.form['content']
    db.session.commit()
    val = {'title': type, 'data': List.query.all()}
    return render_template("base_list.html", val=val)


if __name__ == "__main__":
    app.run(debug=True)
