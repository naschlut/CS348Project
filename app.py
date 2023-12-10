from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)
app.secret_key='admin123'

@app.route("/")
@app.route("/index")
def index():
    # Fetch data from the log table
    con_log = sql.connect("ratings.db")
    con_log.row_factory = sql.Row
    cur_log = con_log.cursor()
    cur_log.execute("SELECT * FROM log")
    data_log = cur_log.fetchall()

    # Fetch data from the new table (assuming the table name is 'average_ratings')
    con_avg = sql.connect("ratings.db")
    con_avg.row_factory = sql.Row
    cur_avg = con_avg.cursor()
    cur_avg.execute("SELECT * FROM avg_rating_year ORDER BY Average_Rating DESC")
    data_avg = cur_avg.fetchall()

    return render_template("index.html", datas=data_log, average_ratings=data_avg)

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

@app.route("/generate_report", methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        park_name = request.form['parkName']
        state = request.form['state']
        year_visited_start = request.form['yearVisitedStart']
        year_visited_end = request.form['yearVisitedEnd']
        rating_start = request.form['ratingStart']
        rating_end = request.form['ratingEnd']
        group_by = request.form['group_by']

        # Limit the grouping options
        valid_grouping_options = ['parkName', 'state', 'yearVisited', 'none']

        # Construct the dynamic query based on form input
        query = f"SELECT "
        if group_by != 'none':
            query += f"{group_by}, AVG(rating) as avg_rating FROM log WHERE 1=1"
        else:
            query +=" * FROM log WHERE 1=1"

        # Rating conditions in the main query block
        params = []
        if rating_start:
            query += " AND rating >= ?"
            params.append(float(rating_start))

        if rating_end:
            query += " AND rating <= ?"
            params.append(float(rating_end))

        if park_name:
            query += " AND parkName LIKE ?"
            params.append(f'%{park_name}%')

        if state:
            query += " AND state = ?"
            params.append(state)

        if year_visited_start:
            query += " AND yearVisited >= ?"
            params.append(int(year_visited_start))

        if year_visited_end:
            query += " AND yearVisited <= ?"
            params.append(int(year_visited_end))

        if group_by != 'none':
            query += f" GROUP BY {group_by}"

        # Execute the query
        con = sql.connect("ratings.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        result = cur.execute(query, params).fetchall()

        # Render the result in show_report.html
        if group_by == 'none':
            # If there's no grouping, return the entire table
            return render_template("show_report.html", result=result, group_by=group_by)
        else:
            # If there's grouping, return the grouped results with average rating
            return render_template("show_report.html", result=result, group_by=group_by)

    return render_template("generate_report.html")
    
if __name__=='__main__':
    app.run(debug=True)