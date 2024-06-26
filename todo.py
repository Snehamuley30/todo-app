from flask import Flask ,render_template ,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app)

class Todo(db.Model):
    sno =db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False)
    desc=db.Column(db.String,nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    
with app.app_context():
    db.create_all()


@app.route("/" , methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template("index1.html", allTodo=allTodo)
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
         title = request.form['title']
         desc = request.form['desc']
         todo=Todo.query.filter_by(sno=sno).first()
         todo.title=title
         todo.desc=desc
         db.session.add(todo)
         db.session.commit()
         return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    print(allTodo)
@app.route('/Delete/<int:sno>')
def Delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)