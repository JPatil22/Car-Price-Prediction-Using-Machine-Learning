#from curses import flash
from flask import Flask, render_template, request
#import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)


#here we are loading our trained model rfr
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
#render the basic template file
@app.route('/',methods=['GET'])
def Home():
    #return render_template('index.html')
    return render_template('new.html')

##read the data from the form
standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=1
        else:
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=0
        #this Year is for how many years the vehicle was used    
        Year=2022-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0 #next we are assing our accepted details to the model varible were we have loaded
        if not Year == "":
            if not Present_Price == "":
                if not Kms_Driven == "":
                    if not Owner == "":
                        if (not Fuel_Type_Diesel =="") and (not Fuel_Type_Petrol == ""):
                            if not Year=="":
                                if not Seller_Type_Individual=="":
                                    if not Transmission_Mannual=="":
                                        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
                                        output=round(prediction[0],2)
                                        if output<0:
                                            return render_template('new.html',prediction_texts="Sorry you cannot sell this car")
                                        else:
                                            return render_template('new1.html',prediction_text="You Can Sell The Car at {}".format(output))
            flash("Please Fill all the details")
    if request.method == 'POST':
        flash("Please fill out the form")

    else:
        return render_template('new.html')

if __name__=="__main__":
    app.run(debug=True)

