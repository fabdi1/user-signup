from flask import Flask, request, redirect
import sys
import html 
import os 
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),"templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def index():
    template=jinja_env.get_template("signup.html")
    return template.render()

def check_email(email):
    def restrict_char(symbol,string):
        counter=0
        for char in string:
            if char == symbol:
                counter=counter+1
            else:
                continue

        if counter>1:
            error = "Email input may only have one @ and a single period (.)"
            return error
        else:
            error=""
            return error

    error=restrict_char('@',email)
    error+=restrict_char('.',email)
    return error


def validate_input(form_input):
    if form_input == "":
        error="This field must be filled." 
        return error
    elif len(form_input)<3 or len(form_input)>20:
        error="Input must be between 3 and 20 characters long."
        return error
    elif " " in form_input:
        error="Input must not include any whitespace"
        return error
    else: 
        error=""
        return error 

@app.route('/add-user', methods=['POST'])
def add_user():
    uname=request.form['username']
    pwd=request.form['password']
    vpwd=request.form['vpwd']
    email=request.form['email']
  
    
    uname_error=validate_input(uname)
    pwd_error=validate_input(pwd)
    vpwd_error=validate_input(vpwd)
    match_err=""
    
    
    if vpwd != pwd:
        match_err="Passwords must match."
    else:
        match_err=""

    if email != "":
        email_error=validate_input(email)
        email_error+=check_email(email)
    else:
        email_error=""
    

    error_list=[uname_error,pwd_error,vpwd_error,email_error,match_err]

    for x in error_list:
        if (x != ""):
            error=True
            break;
        else:
            error=False


    if error==False:
        template=jinja_env.get_template("welcome.html")
        return template.render(user=uname)
    else: 
        template=jinja_env.get_template("signup.html")
        return template.render(
                username=uname,
                email=email,
                uname_error=uname_error,
                pwd_error=pwd_error,
                vpwd_error=vpwd_error,
                email_error=email_error,
                match_error=match_err
                )

app.run()