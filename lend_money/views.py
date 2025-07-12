from django.shortcuts import render
from django.http import JsonResponse
from twilio.rest import Client
import random
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from AI_model import main
from AI_model.credit_model import train_credit_models, predict_credit_score

def send_otp(request,mobile):
    print(mobile)
    api_key = '401baeae-5e21-11f0-a562-0200cd936042'
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobile}/AUTOGEN"
    response = requests.get(url,verify=False)
    print(response)
    data = response.json()
    print(data)
    session_id = data.get('Details')
    request.session['session_id'] = session_id

def verify_otp(request, otp):
    api_key = '401baeae-5e21-11f0-a562-0200cd936042'
    session_id = request.session.get('session_id')
    url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp}"
    response = requests.get(url,verify=False)
    data = response.json()
    print(data)
    return data.get('Status')


@csrf_exempt
def index(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST.keys())
        ui_input = list(request.POST.keys())
        ui_input_dict = json.loads(ui_input[0])
        print(ui_input_dict)
        if 'send_otp' in ui_input_dict.keys():
            send_otp(request,ui_input_dict['mobile'])
            request.session['mobile'] =  ui_input_dict['mobile']
            return JsonResponse({"message": "OTP sent!"},status=200)
        elif 'verify_otp' in ui_input_dict.keys():
            response = verify_otp(request, ui_input_dict['otp'])
            # response = 'Success'
            return JsonResponse({"message": response},status = 200)
    return render(request, "user_form.html")

def user_info(request):

    genders = ['Male', 'Female']
    employment_status = ['Employed', 'Unemployed']
    job_types = ['Full-time', 'Part-time', 'Freelancer', 'Contract']
    mobile_brands = ['Android', 'iOS']
    life_insurance = ['Yes', 'No']
    loan_defaulter = ['Yes', 'No']
    closed_loans = ['Yes', 'No']
    loan_prepayment = ['Yes', 'No']
    months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai',
                'Hyderabad', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur']
    
    data = []
    mobile_number = str(random.randint(7000000000, 9999999999))
    aadhaar_number = random.randint(100000000000, 999999999999)
    age = random.randint(18, 60)
    gender = random.choice(genders)
    location = random.choice(locations)
    employment_status_val = random.choice(employment_status)
    job_type = random.choice(job_types)
    years_employed = random.randint(0, 30)
    smartphone = random.choice(['Yes', 'No'])
    android_or_ios = random.choice(mobile_brands) if smartphone == 'Yes' else None
    life_insurance_val = random.choice(life_insurance)
    pre_existing_loans = random.choice(['Yes', 'No'])
    # loan_payment_defaulter = random.choice(loan_defaulter)
    loan_payment_defaulters = ['Yes', 'No'] + [random.choice(loan_defaulter) for _ in range(len(months)-2)]
    random.shuffle(loan_payment_defaulters)
    closed_loans_val = random.choice(closed_loans)
    closed_on_time = random.choice(loan_defaulter)
    loan_prepayment_made = random.choice(loan_prepayment)
    
    for i, month in enumerate(months):
        record = {
            'mobile_number': request.session['mobile'],
            'aadhaar_number': aadhaar_number,
            'age': age,
            'gender': gender,
            'location': location,
            'employment_status': employment_status_val,
            'job_type': job_type,
            'years_employed': years_employed,
            'smartphone_yes_or_no': smartphone,
            'android_or_ios': android_or_ios,
            'life_insurance': life_insurance_val,
            'pre_existing_loans': pre_existing_loans,
            'loan_payment_defaulter': loan_payment_defaulters[i],
            'closed_loans': closed_loans_val,
            'closed_on_time': closed_on_time,
            'loan_prepayment_made': loan_prepayment_made,
            'month': month,
            'calls_made': random.randint(0, 100),
            'texts_sent': random.randint(0, 100),
            'data_used_gb': round(random.uniform(0.5, 20.0), 2),
            'electricity_bill': random.randint(500, 5000),
            'electricity_bill_pay_defaulter': random.choice(['Yes', 'No']),
            'water_bill': random.randint(100, 2000),
            'water_bill_pay_defaulter': random.choice(['Yes', 'No']),
            'internet_bill': random.randint(200, 4000),
            'internet_bill_pay_defaulter': random.choice(['Yes', 'No']),
            'contacts_count': random.randint(50, 300),
            'frequent_contacts': random.randint(5, 20),
            'monthly_income': random.randint(10000, 100000),
            'monthly_expense': random.randint(5000, 80000),
            'transactions_count': random.randint(50, 1000)
        }
        data.append(record)

# Create DataFrame
    df = pd.DataFrame(data)
    df = df.fillna('')
    
    request.session['df'] = df.to_json()
    mobile = request.session['mobile']
    ui_user_details = {}
    ui_user_details['Mobile'] = str(df['mobile_number'].values[0])
    ui_user_details['age'] = df['age'].values[0]
    ui_user_details['gender'] = df['gender'].values[0]
    ui_user_details['employment_status'] = df['employment_status'].values[0]
    ui_user_details['location'] = df['location'].values[0]
    ui_user_details['aadhaar_number'] = str(int(df['aadhaar_number'].values[0]))
    ui_user_details['monthly_income'] = round(df['monthly_income'].mean(),2)
    ui_user_details['monthly_expense'] = round(df['monthly_expense'].mean(),2)
    ui_user_details['transactions_count'] = int(df['transactions_count'].mean())
    ui_user_details['pre_existing_loans'] = random.randint(0, 5)
    ui_user_details['loan_payment_defaulter'] = 'Yes' if 'Yes' in df['loan_payment_defaulter'].to_list() else 'No'
    ui_user_details['closed_loans'] = random.randint(0, 3)
    ui_user_details['closed_on_time'] = 'Yes' if 'Yes' in df['closed_on_time'].to_list() else 'No'
    ui_user_details['loan_prepayment_made'] = 'Yes' if 'Yes' in df['loan_prepayment_made'].to_list() else 'No'
    ui_user_details['accounts'] = [
        {"name": "HDFC Bank", "account_number": "XXXX1654", "account_type": "Savings"},
        {"name": "ICICI Bank", "account_number": "XXXX5158", "account_type": "Current"},
        {"name": "SBI", "account_number": "XXXX9012", "account_type": "Savings"},
    ]
    ui_user_details['loans'] = [
        {"loan_id": "L001", "amount": 50000, "status": "Open", "interest_rate": 10.5, "due_date": "2025-12-31"},
        {"loan_id": "L002", "amount": 30000, "status": "Open", "interest_rate": 9.0, "due_date": "2026-03-15"},
        {"loan_id": "L003", "amount": 45000, "status": "Open", "interest_rate": 11.0, "due_date": "2026-08-20"},
        {"loan_id": "L004", "amount": 60000, "status": "Open", "interest_rate": 10.0, "due_date": "2025-11-10"},
        {"loan_id": "L005", "amount": 25000, "status": "Closed", "interest_rate": 8.5, "due_date": "2023-01-31"},
        {"loan_id": "L006", "amount": 35000, "status": "Closed", "interest_rate": 9.2, "due_date": "2022-09-15"},
    ]

    # request.session['user_details'] = ui_user_details
    context = {
        'user_details': ui_user_details
    }
    return render(request, "user_info.html", context)

def credit_score(request):
    mobile = request.session['mobile']
    model, encoder = train_credit_models(pd.read_json(request.session['df']))
    response = main.get_user_credit_report(mobile, pd.read_json(request.session['df']),model,encoder)
    print("response------"+str(response))
    credit_score = response['credit_score']  # Example credit score
    credit_worthiness = response['credit_worthiness']
    credit_reason = response['credit_reason']
    credit_score = max(300, min(credit_score, 900))
    interest_rate = round(9 + ((900 - credit_score) / (900 - 300)) * (20 - 9),2)
    banks_with_rates = {
        'kotak Mahendra Bank': round(interest_rate + random.uniform(0,1), 2),
        'State Bank Of India': round(interest_rate + random.uniform(0,1), 2),
        'HDFC Bank': round(interest_rate + random.uniform(0,1), 2),
        'ICICI Bank': round(interest_rate + random.uniform(0,1), 2),
        'CO-operative Bank': round(interest_rate + random.uniform(1,2), 2),
        'Anand CO-Operative Bank': round(interest_rate + random.uniform(1,2), 2),
        'Punjab National Bank': round(interest_rate + random.uniform(0,1), 2),
        'Grameena Bank': round(interest_rate + random.uniform(1,2), 2),
        'Canara Bank': round(interest_rate + random.uniform(0,1), 2)
    }
    registered_banks = dict(sorted(banks_with_rates.items(), key=lambda item: item[1]))
    if credit_worthiness == 'Excellent':
        referal_score = 9
    elif credit_worthiness == 'Very Good':
        referal_score = 7.5
    elif credit_worthiness == 'Fair':
        referal_score = 5
    elif credit_worthiness == 'Low':
        referal_score = 3
    context = {
        'credit_score': credit_score,
        'credit_worthiness': credit_worthiness,
        'credit_reason': credit_reason,
        'registered_banks': registered_banks,
        'referal_score': referal_score
    }
    return render(request,'credit_score.html',context=context)