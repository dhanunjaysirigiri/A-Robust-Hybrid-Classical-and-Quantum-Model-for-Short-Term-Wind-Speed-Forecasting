from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,wind_speed_forecasting,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def index(request):
    return render(request, 'RUser/index.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city,address=address,gender=gender)

        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html',{'object':obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_wind_speed_forecasting(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Latitude= request.POST.get('Latitude')
            Langitude= request.POST.get('Langitude')
            Fdate= request.POST.get('Fdate')
            Wind_Speed= request.POST.get('Wind_Speed')
            First_Indicator= request.POST.get('First_Indicator')
            RAIN= request.POST.get('RAIN')
            Second_Indicator= request.POST.get('Second_Indicator')
            Max_Temp= request.POST.get('Max_Temp')
            Third_Indicator= request.POST.get('Third_Indicator')
            Min_temp= request.POST.get('Min_temp')
            Min_grass_temp= request.POST.get('Min_grass_temp')

        df = pd.read_csv('Datasets.csv')

        def apply_response(Label):
            if (float(Label) >= 10.0):
                return 0  # High
            else:
                return 1  # Low

        df['results'] = df['Wind_Speed'].apply(apply_response)

        cv = CountVectorizer()
        X = df['Fid']
        y = df['results']

        print("Fid")
        print(X)
        print("Results")
        print(y)

        cv = CountVectorizer()
        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print("ACCURACY")
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")
        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        print("Gradient Boosting Classifier")
        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(
            X_train,
            y_train)
        clfpredict = clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, clfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, clfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, clfpredict))
        models.append(('GradientBoostingClassifier', clf))

        print("Random Forest Classifier")
        from sklearn.ensemble import RandomForestClassifier
        rf_clf = RandomForestClassifier()
        rf_clf.fit(X_train, y_train)
        rfpredict = rf_clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, rfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, rfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, rfpredict))
        models.append(('RandomForestClassifier', rf_clf))

        # You can add if u want this model

        #print("Convolutional Neural Network---(CNN)")

        #from sklearn.neural_network import MLPClassifier
        #mlpc = MLPClassifier().fit(X_train, y_train)
        #y_pred = mlpc.predict(X_test)
        #print("ACCURACY")
        #print(accuracy_score(y_test, y_pred) * 100)
        #print("CLASSIFICATION REPORT")
        #print(classification_report(y_test, y_pred))
        #print("CONFUSION MATRIX")
        #print(confusion_matrix(y_test, y_pred))
        #models.append(('MLPClassifier', mlpc))
        #detection_accuracy.objects.create(names="Convolutional Neural Network---(CNN)",ratio=accuracy_score(y_test, y_pred) * 100)

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if (prediction == 0):
            val = 'High'
        elif (prediction == 1):
            val = 'Low'

        print(val)
        print(pred1)

        wind_speed_forecasting.objects.create(
        Fid=Fid,
        Latitude=Latitude,
        Langitude=Langitude,
        Fdate=Fdate,
        Wind_Speed=Wind_Speed,
        First_Indicator=First_Indicator,
        RAIN=RAIN,
        Second_Indicator=Second_Indicator,
        Max_Temp=Max_Temp,
        Third_Indicator=Third_Indicator,
        Min_temp=Min_temp,
        Min_grass_temp=Min_grass_temp,
        Prediction=val)

        return render(request, 'RUser/Predict_wind_speed_forecasting.html',{'objs': val})
    return render(request, 'RUser/Predict_wind_speed_forecasting.html')



