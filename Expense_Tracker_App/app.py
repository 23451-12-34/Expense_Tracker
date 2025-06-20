from flask import Flask,request,render_template,url_for,redirect
import pandas as pd
import calendar
import os
app=Flask(__name__)

@app.route('/')
def Home_page():
    df=pd.read_excel('Expense_tracker.xlsx')
    #formatting
    df['Amount']=pd.to_numeric(df['Amount'],errors='coerce') #errors='coerce if any invalid input goes it just write nan does not throw error ex='abc'==>NaN
    df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    df['Category']=df['Category'].astype(str)
    df['Description']=df['Description'].astype(str)
    total_expense=df['Amount'].sum()
    #category wise expense
    cat=df.groupby('Category')['Amount'].sum().reset_index()
    cat_dict=cat.to_dict('records')
    d1=df.to_dict('records')
    
    print(df.columns.to_list())
    return render_template("home.html",total=total_expense,categories=cat_dict,expenses=d1)



@app.route('/add')
def add_expense_form():
    return render_template("add_expense.html")

@app.route('/create',methods=['post'])
def create_expense():
    add_data={
        'Date':request.form['Date'],
        'Category':request.form["Category"],
        'Amount':request.form["Amount"],
        'Description':request.form["Description"],
    }
    df=pd.read_excel('Expense_tracker.xlsx')
    df=pd.concat([df,pd.DataFrame([add_data])],ignore_index=True)
    df.to_excel('Expense_tracker.xlsx',index=False)
    return redirect(url_for('Home_page')) #write_function name where you redirect at which route



@app.route('/expenses',methods=['GET','post']) 
def view_expenses():                                                                                                                     
                                    
    df=pd.read_excel('Expense_tracker.xlsx')

    #we already done this in home_page function but chatgpt suggest so add itwe can avoid because we already do
    df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    df['Amount']=pd.to_numeric(df['Amount'],errors='coerce').fillna(0)
    df['Category']=df['Category'].astype(str)

    start_date=request.form.get('start_date')
    end_date=request.form.get('end_date')
    category=request.form.get('category')

    if start_date:
        df=df[df['Date']>=pd.to_datetime(start_date)]
    if end_date:
        df=df[df['Date']<=pd.to_datetime(end_date)]
    if category and category!='All':
        df=df[df['Category']==category]
    
    categories = df['Category'].unique().tolist()
    df = df.sort_values(by='Date', ascending=False)
    return render_template('expense_list.html',expenses=df.to_dict('records'), categories=categories, selected_cat=category or 'All')



@app.route('/delete/<int:row_id>',methods=['post'])
def delete_expense(row_id):
    file = 'Expense_tracker.xlsx'
    if os.path.exists(file):
        df = pd.read_excel(file)
        if row_id < len(df):
            df = df.drop(index=row_id)              # Delete the row
            df.reset_index(drop=True, inplace=True) # Reset index after deletion
            df.to_excel(file, index=False)          # Save changes
    return redirect(url_for('Home_page'))       # Redirect to a page (you define this)



@app.route('/reports')
def report_page():
    df=pd.read_excel('Expense_tracker.xlsx')
    df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    df['Amount']=pd.to_numeric(df['Amount'],errors='coerce')
    df=df.dropna(subset=['Date']) #👉 subset specifies which column(s) to check for missing values. #here we not total date column just drop rowa where value is missing or invalid

    #monthly 
    df['year']=df['Date'].dt.year
    df['month']=df['Date'].dt.month #df['Date'].dt.month extracts the month number (1 to 12) from each date in the Date column.
    current_year = pd.Timestamp.now().year
    monthly_data = df[df['year'] == current_year].groupby('month')['Amount'].sum()
    months = [calendar.month_name[m] for m in monthly_data.index]
    monthly_totals = monthly_data.tolist()

    #Annually
    annual_data=df.groupby('year')['Amount'].sum()
    years = annual_data.index.tolist()
    annual_totals = annual_data.tolist()
    return render_template('report.html', months=months, years=years,monthly_totals=monthly_totals, annual_totals=annual_totals,current_year=current_year)
#what happens in def report_page and we render in report.html how it works
# Step	What Happens	                 Tool Used
# 1	Flask loads & cleans Excel data   	   pandas
# 2	Groups data month-wise, year-wise	   groupby
# 3	Converts to lists	                   .tolist()
# 4	Sends to report.html	               render_template()
# 5	Chart.js plots graphs in browser	   JavaScript

                              
app.run(debug=True)
