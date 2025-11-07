import pandas as pd
from app.shap_explain import pipeline


def test_model_prediction_value():
    """
    Ensure model returns a probability between 0 and 1.
    """
    sample = {
        "loan_amnt": 10000,
        "term": "36 months",
        "int_rate": 12.0,
        "installment": 330,
        "grade": "B",
        "sub_grade": "B2",
        "home_ownership": "RENT",
        "annual_inc": 60000,
        "purpose": "credit_card",
        "dti": 20,
        "open_acc": 5,
        "revol_bal": 4000,
        "revol_util": 45,
        "tot_cur_bal": 20000,
        "fico_score": 700,
    }

    df = pd.DataFrame([sample])
    proba = pipeline.predict_proba(df)[0][1]

    # Assert probability is valid
    assert 0 <= proba <= 1
