from django.shortcuts import render
from django.http import JsonResponse
from twilio.rest import Client
import random
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

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
            # send_otp(request,ui_input_dict['mobile'])
            request.session['mobile'] =  ui_input_dict['mobile']
            return JsonResponse({"message": "OTP sent!"},status=200)
        elif 'verify_otp' in ui_input_dict.keys():
            # response = verify_otp(request, ui_input_dict['otp'])
            response = 'Success'
            return JsonResponse({"message": response},status = 200)
    return render(request, "user_form.html")

def user_info(request):
    df = pd.read_csv("test_users.csv")
    user_details = (
        df.groupby('mobile_number')
        .apply(lambda x: x.to_dict(orient='records'))
        .to_dict()
    )
    print(request.session['mobile'])
    mobile = request.session['mobile']
    print(mobile)
    ui_user_details = {}
    if int(mobile) in user_details.keys():
        child_df = df[df['mobile_number'] == int(mobile)]
        print(child_df)
        ui_user_details['Name'] = child_df['Name'].values[0]
        ui_user_details['Mobile'] = str(child_df['mobile_number'].values[0])
        ui_user_details['age'] = child_df['age'].values[0]
        ui_user_details['gender'] = child_df['gender'].values[0]
        ui_user_details['employment_status'] = child_df['employment_status'].values[0]
        ui_user_details['location'] = child_df['location'].values[0]
        ui_user_details['aadhaar_number'] = str(int(child_df['aadhaar_number'].values[0]))
        ui_user_details['monthly_income'] = child_df['monthly_income'].mean()
        ui_user_details['monthly_expense'] = child_df['monthly_expense'].mean()
        ui_user_details['transactions_count'] = int(child_df['transactions_count'].mean())
        ui_user_details['pre_existing_loans'] = int(child_df['pre_existing_loans'].mean())
        ui_user_details['loan_payment_defaulter'] = 'Yes' if 'Yes' in child_df['loan_payment_defaulter'].to_list() else 'No'
        ui_user_details['closed_loans'] = int(child_df['closed_loans'].mean())
        ui_user_details['closed_on_time'] = 'Yes' if 'Yes' in child_df['closed_on_time'].to_list() else 'No'
        ui_user_details['loan_prepayment_made'] = 'Yes' if 'Yes' in child_df['loan_prepayment_made'].to_list() else 'No'
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
    
    print(ui_user_details)
    context = {
        'user_details': ui_user_details
    }
    return render(request, "user_info.html", context)

def credit_score(request):
    return render(request,'credit_score.html')