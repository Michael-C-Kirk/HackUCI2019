from flask import Flask, request, redirect, render_template, jsonify
import APIcalls as api
import decode as dcd
import decision_tree as dt
import data_update as du
import categories as c
from random import randrange
from helper import *
import restarauntURL as ru

KEY_WORD_LIST = ["sushi", "spaghetti", "taco", "ramen", "sandwich", "icecream", "kbbq", "fish", "soup", "pancake"]
CLF = None
app = Flask(__name__)
details = dict()
URL = []
Client_IP = {}

def get_ip():
    return str(request.remote_addr)

@app.route('/upbutton')
def upbutton():
    if(URL == []):
        return redirect("/")
    du.update_data_set("dataset3.txt", details, details["Result"])
    return redirect(URL[-1])

@app.route('/upbutton1')
def upbutton1():
    if(URL == []):
        return redirect("/")
    return redirect(URL[-1])

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    Client_IP = request.remote_addr
    return render_template('index.html')
@app.route('/surprise')
def surprise():
    foodDict = api.call(get_ip(), "14000", KEY_WORD_LIST[randrange(0, len(KEY_WORD_LIST))])
    binfo = dcd.ratingParser(foodDict, 4)[1]
    if len(binfo) == 0:
        return render_template('response.html', name = "All locations are closed at the moment", image = "We appologize for the inconvenience", rating = "", thumbsDownGoesTo='/surprise', thumbsUpGoesTo = '/surprise')
    placeNum = randrange(0, len(binfo))
    REST_ID = binfo[placeNum][3]
    URL.append(ru.getRestarauntURL(REST_ID))
    return render_template('response.html', name = binfo[placeNum][0], image = binfo[placeNum][2], rating = binfo[placeNum][1], URL = URL[-1], thumbsDownGoesTo='/surprise', thumbsUpGoesTo = '/upbutton1')
    
@app.route('/caffeine')
def coffee():
    foodDict = api.call(get_ip(), "10000", "cafe and coffee")
    binfo = dcd.ratingParser(foodDict, 3.5)[1]
    if len(binfo) == 0:
        return render_template('response.html', name = "All locations are closed at the moment", image = "We appologize for the inconvenience", rating = "", thumbsDownGoesTo='/caffeine', thumbsUpGoesTo = '/caffeine')
    placeNum = randrange(0, len(binfo))
    REST_ID = binfo[placeNum][3]
    URL.append(ru.getRestarauntURL(REST_ID))
    return render_template('response.html', name = binfo[placeNum][0], image = binfo[placeNum][2], rating = binfo[placeNum][1], URL = URL[-1], thumbsDownGoesTo='/caffeine', thumbsUpGoesTo = '/upbutton1')
    
@app.route('/quick')
def quick():
    foodDict = api.call(get_ip(), "10000", "fast food")
    binfo = dcd.ratingParser(foodDict, 3.5)[1]
    if len(binfo) == 0:
        return render_template('response.html', name = "All locations are closed at the moment", image = "We appologize for the inconvenience", rating = "", thumbsDownGoesTo='/quick', thumbsUpGoesTo = '/quick')
    placeNum = randrange(0, len(binfo))
    REST_ID = binfo[placeNum][3]
    URL.append(ru.getRestarauntURL(REST_ID))
    return render_template('response.html', name = binfo[placeNum][0], image = binfo[placeNum][2], rating = binfo[placeNum][1], URL = URL[-1], thumbsDownGoesTo='/quick', thumbsUpGoesTo = '/upbutton1')
    #return render_template('quick_response.html')

    
@app.route('/choose')
def choose():
    cat_num = int(dt.prediction(CLF, details))
    x = randrange(10)
    if (x < 2):
        cat_num -= 1
        if (cat_num == 0):
            cat_num = 2
    details["Result"] = cat_num
    cat = c.symbol_to_categories[cat_num]
    l = c.categories[cat]
    subcatnum = randrange(0, len(l))
    subcat = l[subcatnum]
    foodDict = api.call(get_ip(), "10000", subcat)
    binfo = dcd.ratingParser(foodDict, 3.8, details['Price'])[1]
    if len(binfo) == 0:
        return render_template('response.html', name = "All locations are closed at the moment", image = "We appologize for the inconvenience", rating = "", thumbsDownGoesTo='/choose', thumbsUpGoesTo = '/choose')
    placeNum = randrange(0, len(binfo))
    REST_ID = binfo[placeNum][3]
    URL.append(ru.getRestarauntURL(REST_ID))
    return render_template('response.html', name = binfo[placeNum][0], image = binfo[placeNum][2], rating = binfo[placeNum][1], URL = URL[-1], thumbsDownGoesTo='/choose', thumbsUpGoesTo = '/upbutton')

@app.route('/details_given', methods = ['POST'])
def detailed():
    if request.form['action'] == 'happy':
        details['Mood'] = 1
    elif request.form['action'] == 'sad':
        details['Mood'] = 0
    else:
        print("ERROR MOOD WAS NOT RIGHT")
        
    details['Price'] = int(request.form['price'])
    details['Time'] = time_parse()
    details['Age'] = age_paser(age_generator())
    cat_num = int(dt.prediction(CLF, details))
    details["Result"] = cat_num
    cat = c.symbol_to_categories[cat_num]
    l = c.categories[cat]
    subcatnum = randrange(0, len(l))
    subcat = l[subcatnum]
    foodDict = api.call(get_ip(), "10000", subcat)
    binfo = dcd.ratingParser(foodDict, 3.8, details['Price'])[1]
    if len(binfo) == 0:
        return render_template('response.html', name = "All locations are closed at the moment", image = "We appologize for the inconvenience", rating = "", thumbsDownGoesTo='/choose', thumbsUpGoesTo = '/choose')
    placeNum = randrange(0, len(binfo))
    REST_ID = binfo[placeNum][3]
    URL.append(ru.getRestarauntURL(REST_ID))
    return render_template('response.html', name = binfo[placeNum][0], image = binfo[placeNum][2], rating = binfo[placeNum][1], URL = URL[-1], thumbsDownGoesTo='/choose', thumbsUpGoesTo = '/upbutton')

if __name__ == '__main__':
    CLF = dt.train_initial_data("dataset3.txt")
    app.run(debug=True, host="0.0.0.0", port=80)
