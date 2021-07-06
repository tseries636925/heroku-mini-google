from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///searchdata.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
search ='null'

class SearchData(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    websitetitle = db.Column(db.String(500), nullable=False)
    websitelink = db.Column(db.String(500), nullable=False)
    websitekeywords = db.Column(db.String(500), nullable=False)
    websitedescription = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.websitetitle} - {self.websitelink} - {self.websitekeywords} - {self.websitedescription}"



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        global search
        search = request.form['search']
        return redirect("/result")
    return render_template('index.html')

@app.route('/add_website', methods=['GET', 'POST'])
def add_website():
    if request.method=='POST':
        websitetitle = request.form['websitetitle']
        websitelink = request.form['websitelink']
        websitekeywords = request.form['websitekeywords']
        websitedescription = request.form['websitedescription']
        searchdata = SearchData(websitetitle=websitetitle, websitelink=websitelink,  websitekeywords= websitekeywords, websitedescription=websitedescription)
        db.session.add(searchdata)
        db.session.commit()
    return render_template('add_website.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method=='POST':
        global search
        search = request.form['searchfield']

    searchdata = SearchData.query.filter(SearchData.websitekeywords.like(search)).all()
    return render_template('result.html',searchdata=searchdata,searched=search)

@app.route('/table')
def table():
    searchdata = SearchData.query.all()
    return render_template('table.html', searchdata=searchdata)



@app.route('/delete/<int:sno>')
def delete(sno):
    searchdata = SearchData.query.filter_by(sno=sno).first()
    db.session.delete(searchdata)
    db.session.commit()
    return redirect("/table")

    

if __name__ == '__main__':
    app.run(debug='True', port='8000')