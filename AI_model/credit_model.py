import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
try:
    from xgboost import XGBClassifier
    xgb_available = True
except ImportError:
    xgb_available = False


def train_credit_models(df):
    # Use 'loan_payment_defaulter' as target (Yes=1, No=0)
    df = df.copy()
    df['target'] = df['loan_payment_defaulter'].map({'Yes': 1, 'No': 0})
    features = [
        'age', 'gender', 'location', 'employment_status', 'job_type', 'years_employed',
        'smartphone_yes_or_no', 'android_or_ios', 'life_insurance', 'pre_existing_loans',
        'closed_loans', 'closed_on_time', 'loan_prepayment_made', 'calls_made', 'texts_sent',
        'data_used_gb', 'electricity_bill', 'electricity_bill_pay_defaulter', 'water_bill',
        'water_bill_pay_defaulter', 'internet_bill', 'internet_bill_pay_defaulter',
        'contacts_count', 'frequent_contacts', 'monthly_income', 'monthly_expense', 'transactions_count'
    ]
    # Encode categorical features
    encoder = {}
    for col in df[features].select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoder[col] = le
    X = df[features]
    y = df['target']
    models = {}
    models['random_forest'] = RandomForestClassifier(n_estimators=50, max_depth=8, random_state=42)
    models['random_forest'].fit(X, y)
    models['logistic_regression'] = LogisticRegression(max_iter=200)
    models['logistic_regression'].fit(X, y)
    if xgb_available:
        models['xgboost'] = XGBClassifier(n_estimators=50, max_depth=8, random_state=42, use_label_encoder=False, eval_metric='logloss')
        models['xgboost'].fit(X, y)
    return models, encoder

def predict_credit_score(models, encoder, user_data, model_name='best'):
    features = [
        'age', 'gender', 'location', 'employment_status', 'job_type', 'years_employed',
        'smartphone_yes_or_no', 'android_or_ios', 'life_insurance', 'pre_existing_loans',
        'closed_loans', 'closed_on_time', 'loan_prepayment_made', 'calls_made', 'texts_sent',
        'data_used_gb', 'electricity_bill', 'electricity_bill_pay_defaulter', 'water_bill',
        'water_bill_pay_defaulter', 'internet_bill', 'internet_bill_pay_defaulter',
        'contacts_count', 'frequent_contacts', 'monthly_income', 'monthly_expense', 'transactions_count'
    ]
    user_data = user_data.copy()
    for col in user_data[features].select_dtypes(include=['object', 'category']).columns:
        user_data[col] = encoder[col].transform(user_data[col].astype(str))
    X_user = user_data[features]
    results = {}
    for name, model in models.items():
        prob_default = model.predict_proba(X_user)[:, 1].mean()
        credit_score = int((1 - prob_default) * 900 + 300)
        print(f"credit_score: {credit_score}")
        if credit_score >= 800:
            credit_worthiness = 'Excellent'
        elif credit_score >= 750:
            credit_worthiness = 'Very Good'
        elif credit_score >= 625:
            credit_worthiness = 'Fair'
        else:
            credit_worthiness = 'Low'
        # Apply negative criteria for credit worthiness
        
        negative_flags = []
        if user_data['loan_payment_defaulter'].iloc[0] == 1:
            negative_flags.append('Has defaulted on loan payments')
        if user_data['closed_on_time'].iloc[0] == 0:
            negative_flags.append('No loans closed on time')
        if user_data['loan_prepayment_made'].iloc[0] == 0:
            negative_flags.append('No loan prepayments made')
        if user_data['pre_existing_loans'].iloc[0] == 1:
            negative_flags.append('Has pre-existing loans')
        if user_data['electricity_bill_pay_defaulter'].iloc[0] == 1 or user_data['water_bill_pay_defaulter'].iloc[0] == 1 or user_data['internet_bill_pay_defaulter'].iloc[0] == 1:
            negative_flags.append('Has bill payment defaults')
        if user_data['monthly_income'].iloc[0] <= 30000:
            negative_flags.append('Low monthly income')
        if user_data['monthly_expense'].iloc[0] >= user_data['monthly_income'].iloc[0] * 0.5:
            negative_flags.append('High monthly expenses relative to income')
        # Force Low worthiness if multiple negative flags
        # if len(negative_flags) >= 3:
        #     credit_worthiness = 'Low'
        #     # Penalize credit score for each negative flag (e.g., -50 per flag)
        #     penalty = 50 * len(negative_flags)
        #     credit_score = max(300, credit_score - penalty)
        print(f"credit_worthiness: {credit_worthiness}")
        # Build reasons from both positive and negative flags
        reasons = []
        remarks = []
        if credit_worthiness == 'Low':
            if negative_flags:
                reasons = negative_flags
            else:
                reasons = ['Limited positive financial indicators']
        else:
            if user_data['closed_on_time'].iloc[0] > 0:
                reasons.append('Has closed loans on time')
            if user_data['loan_prepayment_made'].iloc[0] > 0:
                reasons.append('Has made loan prepayments')
            if user_data['pre_existing_loans'].iloc[0] == 0:
                reasons.append('No pre-existing loans')
            if user_data['electricity_bill_pay_defaulter'].iloc[0] == 0 and user_data['water_bill_pay_defaulter'].iloc[0] == 0 and user_data['internet_bill_pay_defaulter'].iloc[0] == 0:
                reasons.append('No bill payment defaults')
            if user_data['monthly_income'].iloc[0] > 30000:
                reasons.append('High monthly income')
            if user_data['monthly_expense'].iloc[0] < user_data['monthly_income'].iloc[0] * 0.5:
                reasons.append('Low monthly expenses relative to income')
            if not reasons:
                reasons.append('Limited positive financial indicators')
            # if negative_flags:
            #     remarks.extend(negative_flags)
        credit_reason = '; '.join(reasons)
        # credit_remarks = '; '.join(remarks)
        results[name] = {
            'credit_score': int(credit_score),
            'credit_worthiness': credit_worthiness,
            'credit_reason': credit_reason,
        }
    # Return only the requested model if specified, else all
    # if model_name in results:
    #     return results[model_name]
    # return results
    if model_name == 'best':
        # Find the model with the highest credit_score
        best = max(results.values(), key=lambda x: x['credit_score'])
        return best
    elif model_name in results:
        return results[model_name]
    return results
