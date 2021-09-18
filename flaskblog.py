from flask import Flask, render_template, url_for, flash, redirect,request
from forms import RegistrationForm, LoginForm
from scrapper import scrape
from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser
from sentiment_analyzer import sentiment_predictor

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    # {
    #     'author': 'Corey Schafer',
    #     'title': 'Blog Post 1',
    #     'content': 'First post content',
    #     'date_posted': 'April 20, 2018'
    # },
    # {
    #     'author': 'Jane Doe',
    #     'title': 'Blog Post 2',
    #     'content': 'Second post content',
    #     'date_posted': 'April 21, 2018'
    # }

    {'content': 'Product is 100 percent genuine as i have cross check with Nike Store. Quality is good. But The Advice that i would like to give Amazon, that They  should give some some Brand genuinity proof with there product, So Customer would Blindly Trust on product 😊',
   'date': 'Reviewed in India on 15 January 2018',
   'variant': 'Size: 10 UK (10.5 US) Color Name: Sequoia/DKStucco-DKStucco',
   'verified': 'Verified Purchase',
   'author': 'Rohit Haryan',
   'rating': '4.0 out of 5 stars',
    'sentiment':'positive sentiment'
   }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/output", methods=['POST','GET'])
def output():
    if request.method == "POST":
        url = request.form['projectFilePath']
        print("print the url")
        print(url)
    #call the model and give the predictions
    # url = "https://www.amazon.in/Adidas-Cotton-Polyster-Elastane-Grey_Medium/product-reviews/B098MG2C2C/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    url = request.form.get('projectFilePath')
    print("print the url")
    print(url)
    

    scrapped_content = scrape(url)
    print(scrapped_content)
    e = Extractor.from_yaml_file('selectors.yml')
    r = requests.get(url)
    print("scrapped the data")
    content = e.extract(r.text)
    print(content)

    reviews = content.get('reviews')
    Negative=0
    Positive=0
    for review in reviews:
        print(review.get('content'))
        ctn  = str(review.get('content'))
        author = str(review.get('author'))
        sentiment_res  = sentiment_predictor([ctn])

        sentiment_val = "dummy"
        if sentiment_res == 1:
            sentiment_val = "this is a positive review"
        else:
            sentiment_val = "this is a negative review"
        
        obj = {
            'content':ctn, 
            'author':author, 
            'sentiment':sentiment_val
           }

        posts.append(obj)

        if sentiment_res==0:
            print("this is negative {sentiment_res}")
            Negative+=1
        else:
            print("this is positive {sentiment_res}")
            Positive+=1

    print("printing negative and positive response")
    print(Positive,Negative)
    data = {'Negative_Reviews':str(Negative),'Positive_Reviews':str(Positive)}
            
    
    return render_template('output.html',posts = posts,data =data)




@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run()
