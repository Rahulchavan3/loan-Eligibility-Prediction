# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
import numpy as np
from flask_pymongo import PyMongo
from gridfs import GridFS
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask import make_response
from bson import ObjectId



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://rahulchavan0010:rahulchavan0010@cluster0.6qbtf07.mongodb.net/loan_prediction?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

print("Connected to MongoDB successfully" if mongo.cx else "Failed to connect to MongoDB")

model = pickle.load(open('ensemble_model.pkl', 'rb'))

client = MongoClient(app.config['MONGO_URI'])
db = client.loan_prediction
fs = GridFS(db)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':

        # (ASAD)
        # if 'pdf_file' in request.files:
        #     aadhar = request.files['aadhar']
        #     pan = request.files['pan']
        #     salary = request.files['salary']
            # db = client['loan_model']
            # pdf_collection = db['aadhar']
            # pdf_collection.insert_one()
            # client.close()    

        #     print('PDF uploaded and stored in MongoDB.')
        # else:
        #     print("'No PDF file provided.'") 

           
        name = str(request.form['Name'])
        phone_no = str(request.form['Mobile_Number'])
        income = int(request.form['Income'])
        age = int(request.form['Age'])
        experience = int(request.form['Experience'])
        profession = request.form['profession']
        state = request.form['state']
        current_job_yrs = int(request.form['Current_Job_Year'])
        current_house_yrs = int(request.form['Current_House_Year'])
        gender = request.form['gender']
        married = request.form['married']
        dependents = int(request.form['dependents'])
        LoanAmount = int(request.form['LoanAmount'])
        Loan_Amount_Term = int(request.form['Loan_Amount_Term'])


        #age
        #experience
        #profession - condition
        #state- condition
        # CURRENT_JOB_YRS
        # CURRENT_HOUSE_YRS
        # Dependents	
        # LoanAmount	
        # Loan_Amount_Term	
        # Credit_History	
        # result


# gender
        if (gender == "Male"):
            gender=1
        else:
            gender=2
        
# married
        if(married=="Yes"):
            married = 1
        else:
            married=0

# dependents
        if(dependents== 0):
            dependents = 0

        elif(dependents == 1):
             dependents = 1

        elif(dependents==2):
             dependents = 2

        elif(dependents==3):
            dependents = 3
        

# profession
        if (profession =='Engineering'):
            profession =1 
        elif (profession =='IT Software'):
            profession =2
        elif (profession == 'Government'):
            profession =3
        elif (profession == 'Education'):
            profession =4
        elif (profession == 'Finance'):
            profession =5
        elif (profession =='Aviation'):
            profession =6
        elif (profession == 'Design'):
            profession =7
        elif (profession == 'Mediacal'):
            profession =8
        elif (profession == 'Art'):
            profession =9
        elif (profession == 'Others'):
            profession =10
        elif (profession =='Hospitality'):
            profession =11
        elif (profession == 'Entertainment'):
            profession =12
        elif (profession == 'Administration'):
            profession =13
        elif (profession =='Finance/Accounting'):
            profession =14
        elif (profession == 'Science/Research'):
            profession =15
    
        # if (profession=="Engineering"):
        #     not_graduate=1
        # else:
        #     not_graduate=0

#state

        if (state =='South/Central India'):
            state =1
        elif (state =='West India'):
            state = 2
        elif (state =='Telugu States'):
            state = 3
        elif (state =='North India'):
            state = 4
        elif (state== 'Unknown'):
            state = 5
        elif (state =='Northwest India'):
            state = 6
        elif (state =='Northeast India'):
            state = 7
        elif (state =='Central India'):
            state = 8
        elif (state =='Other'):
            state = 9

        # Extracting file uploads
        aadhar_file = request.files['aadhar']
        pan_file = request.files['pan']
        salary_file = request.files['salary']

        # Saving files to GridFS
        aadhar_id = fs.put(aadhar_file, filename=secure_filename(aadhar_file.filename))
        pan_id = fs.put(pan_file, filename=secure_filename(pan_file.filename))
        salary_id = fs.put(salary_file, filename=secure_filename(salary_file.filename))


        # # employed
        # if (employed == "Yes"):
        #     employed_yes=1
        # else:
        #     employed_yes=0

        # property area

        # if(area=="Semiurban"):
        #     semiurban=1
        #     urban=0
        # elif(area=="Urban"):
        #     semiurban=0
        #     urban=1
        # else:
        #     semiurban=0
        #     urban=0


        # ApplicantIncomelog = np.log(ApplicantIncome)
        # totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        # LoanAmountlog = np.log(LoanAmount)
        # Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[income,age,experience,profession,state,current_job_yrs,current_house_yrs,gender,married,dependents	,LoanAmount,Loan_Amount_Term]])

        # print(prediction)

        if(prediction==0):
                prediction="No"
        else:
                prediction="Yes"

        # user_data = {
        #     'income': income,
        #     'age': age,
        #     'experience': experience,

        #     # Add more fields as needed
        # }   
  

        mongo.db.inventory.insert_one({
            'name'  : name,
            'phone_no'  : phone_no,
            'income': income,
            'age': age,
            'experience': experience,
            'profession' : profession,
            'state' : state,
            'current_job_yrs' : current_job_yrs ,
            'current_house_yrs' : current_house_yrs ,
            'gender' : gender ,
            'married' : married,
            'dependents' : dependents ,
            'LoanAmount' : LoanAmount ,
            'Loan_Amount_Term' :Loan_Amount_Term ,
            'prediction' : prediction,
            'aadhar_id': str(aadhar_id),
            'pan_id': str(pan_id),
            'salary_id': str(salary_id)
            # 'aadhar': aadhar.filename, 'data': aadhar.read()
            # 'aadhar': "demoaadhar", 'data': aadhar.read()

            # Add more fields as needed
        } )

        


        return render_template("prediction.html", prediction_text="loan status is {}".format(prediction))

    else:
        return render_template("prediction.html")
    
@app.route('/admin')
def admin():   
    data =mongo.db.inventory.find({})
    return render_template("dashboard.html", data=data)

@app.route('/view_document/<file_id>')
def view_document(file_id):
    # Retrieve the file from GridFS
    file_data = fs.get(ObjectId(file_id))
    
    # Return the file data as a response
    response = make_response(file_data.read())
    response.mimetype = 'application/octet-stream'  # You might need to adjust the mimetype based on the file type
    response.headers.set('Content-Disposition', 'attachment', filename=file_data.filename)
    return response







if __name__ == "__main__":
    app.run(debug=True , port=8000)