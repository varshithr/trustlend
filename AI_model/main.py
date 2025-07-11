import pandas as pd

from AI_model.credit_model import train_credit_models, predict_credit_score
# Load and preprocess data
DATA_PATH = 'AI_model/mockdata_10000_users.csv'
df = pd.read_csv(DATA_PATH)

# Train credit score model

def get_user_credit_report(user_id, df, model, encoder):
    """
    Returns credit report for a user by mobile or Aadhaar number.
    Args:
        user_id (str): Mobile number or Aadhaar number
        df (pd.DataFrame): DataFrame with user data
        model: trained model(s)
        encoder: encoder(s)
    Returns:
        dict: {'credit_score', 'credit_worthiness', 'credit_reason'} or None if not found
    """
    # user_data = df[(df['mobile_number'] == user_id) | (df['aadhaar_number'].astype(str) == user_id)]
    user_data = df[(df['mobile_number'] == int(user_id))]
    print(f"user_data: {user_data}")
    if user_data.empty:
        return None
    return predict_credit_score(model, encoder, user_data)

# CLI for user interaction
if __name__ == '__main__':
    print('TrustLend AI Microfinance Platform')
    user_id = input('Enter Mobile Number or Aadhaar Number: ')
    model, encoder = train_credit_models(df)
    result = get_user_credit_report(user_id, df, model, encoder)
    if result is None:
        print('User not found.')
    else:
        print(f"Predicted Credit Score: {result['credit_score']}")
        print(f"Credit Worthiness: {result['credit_worthiness']}")
        print(f"Credit Reason: {result['credit_reason']}")
