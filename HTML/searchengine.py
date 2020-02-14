
import os
import webbrowser

global results
results=[]

try:
    from flask import Flask,url_for,redirect,render_template,request
except:
    os.system("@echo off")
    os.system("INSTALLING FLASK THE REQUIRED MOFDULE")
    os.system("RESTART AFTER THIS DOWNLOAD FINISHES")
    os.system("pip install flask")
    print("THE REQUIRED PPACKAGE IS BEING INSTALLED")

try:
    import bs4 as bs
except:
    os.system("@echo off")
    os.system("INSTALLING BEAUTIFUL SOUP THE REQUIRED MOFDULE")
    os.system("RESTART AFTER THIS DOWNLOAD FINISHES")
    os.system("pip install flask")
    print("THE REQUIRED PPACKAGE IS BEING INSTALLED")


try:
    import urllib
except:
    os.system("@echo off")
    os.system("INSTALLING BEAUTIFUL SOUP THE REQUIRED MOFDULE")
    os.system("RESTART AFTER THIS DOWNLOAD FINISHES")
    os.system("pip install flask")
    print("THE REQUIRED PPACKAGE IS BEING INSTALLED")



def getlink(query):
    try:
        result={}
        q=query
        headers={}
        q=q.replace(" ","+")
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Li5nux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        url="https://www.google.com.np/search?q="+q
        sauce = urllib.request.Request(url, headers = headers) 
        sauce1=urllib.request.urlopen(sauce)

        soup=bs.BeautifulSoup(sauce1,'lxml')
        
       
        links=soup.find_all('a')
        a=0
        for j in links:
            a+=1
            if a>20:
                link = (str(j.get('href')))
                if (link!=None and len(link)>20 and link.startswith("http")):
                    
                    result["query"]=query
                    result["link"]=link
                    break
        results.append(result)
    except Exception as e:
        print (e)


#flasking starts here
app=Flask(__name__)
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
    app.run(debug=True)
    