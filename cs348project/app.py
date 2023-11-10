from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)
app.secret_key='admin123'

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("ratings.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from log")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        parkName=request.form['parkName']
        state=request.form['state']
        yearVisited=request.form['yearVisited']
        rating=request.form['rating']
        comments=request.form['comments']
        con=sql.connect("ratings.db")
        cur=con.cursor()
        cur.execute("insert into log(parkName,state,yearVisited,rating,comments) values (?,?,?,?,?)",(parkName,state,yearVisited,rating,comments))
        con.commit()
        flash('Entry Added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:lid>",methods=['POST','GET'])
def edit_user(lid):
    if request.method=='POST':
        parkName=request.form['parkName']
        state=request.form['state']
        yearVisited=request.form['yearVisited']
        rating = request.form['rating']
        comments=request.form['comments']
        con=sql.connect("ratings.db")
        cur=con.cursor()
        cur.execute("update log set parkName=?,state=?,yearVisited=?,rating = ?,comments = ? where logId=?",(parkName,state,yearVisited,rating,comments,lid))
        con.commit()
        flash('Log Entry Updated!','success')
        return redirect(url_for("index"))
    con=sql.connect("ratings.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from log where logId=?",(lid,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)
    
@app.route("/delete_user/<string:lid>",methods=['GET'])
def delete_user(lid):
    con=sql.connect("ratings.db")
    cur=con.cursor()
    cur.execute("delete from log where logId=?",(lid,))
    con.commit()
    flash('Log Entry Deleted','warning')
    return redirect(url_for("index"))
    
if __name__=='__main__':
    app.run(debug=True)