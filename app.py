from flask_sqlalchemy import SQLAlchemy
from flask import Flask,url_for,redirect,render_template,request
import os
import webbrowser
import bs4 as bs
import requests

#os.system('database.py')


def log(x):
    filee=open("log.dat","w")
    filee.writeline(x)
    filee.close()

global results
results=[]

#flasking starts here
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./test.db'
app.config["secret_key"]="very_secret"
app.config['TESTING'] = True
db=SQLAlchemy(app)


class accessdb:
    def __init__(self):
        pass

    def writeindb(self,name,link):
            try:
                link=linkholder(name=name,link=link)
                db.session.add(link)
                db.session.commit()
                return True
            except:
                return False

    def readindb(self):
        try:
            link=linkholder(name=None,link=None)
            links=link.query.all()
            return links
        except:
            return False

class linkholder(db.Model):
    idd = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    link = db.Column(db.String(250), unique=True, nullable=False)
    
    def __repr__(self):
        return "User \n name "+self.name+" link "+self.link

access=accessdb()

def checkindb(query):

    if "--ignore-database" in query:
        
        return None
    
    try:
        links=access.readindb()
        query=query.lower()

        for linked in links:
            linkofsite=linked.link
            nameofsite=linked.name
            if (nameofsite.lower()==query):
                print(linkofsite)
                return linkofsite
            else:
                pass
    except:
        return None

def getlink(query):
    link_predict=checkindb(query)



    if link_predict:
        print("Using database")
        print(link_predict)
        result={}
        result["query"]=query
        result["link"]=link_predict
        results.insert(0,result)
    else:
    
        try:
            result={}
            q=query
            headers={}
            q=q.replace(" ","+")
            headers['User-Agent'] = 'Mozilla/5.0 (X11; Li5nux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
            url="https://www.google.com.np/search?q="+q
            sauce=requests.get(url,headers=headers)
            sauce=sauce.content
            soup=bs.BeautifulSoup(sauce,'html.parser')
            links=soup.find_all('a')
            a=0
            for j in links:
                a+=1
                if a>20:
                    link = (str(j.get('href')))
                    if (link!=None and len(link)>20 and link.startswith("http")):
                        
                        if "--ignore-database" in query:
                            query=query.replace("--ignore-database","")
                        else:
                            access.writeindb(query,link)
                        

                        result["query"]=query
                        result["link"]=link
                        break

            results.insert(0,result)
        except Exception as e:
            print (e)



@app.route("/database")
def database():
    links=access.readindb()
    return render_template("database.html",links=links)


@app.route("/",methods=["POST","GET"])
@app.route("/homepage",methods=["POST","GET"])
def home():
   
    if request.method=="GET":
        return render_template("home.html",results=results)
        
    else:
        if request.method=="POST":
            query=request.form["comm"]
            getlink(query)
            return redirect(url_for("home"))
            

if __name__=='__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True,port=5000)
    