from pydantic import BaseModel
class LoanRequest(BaseModel):
    loan_amnt: float
    term: str
    int_rate: float
    installment: float
    grade: str
    sub_grade: str
    home_ownership: str
    annual_inc: float
    purpose: str
    dti: float
    open_acc: float
    revol_bal: float
    revol_util: float
    tot_cur_bal: float
    fico_score: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "loan_amnt": 15000,
                "term": "36 months",
                "int_rate": 12.5,
                "installment": 350,
                "grade": "B",
                "sub_grade": "B4",
                "home_ownership": "MORTGAGE",
                "annual_inc": 75000,
                "purpose": "credit_card",
                "dti": 18.2,
                "open_acc": 6,
                "revol_bal": 4500,
                "revol_util": 42.3,
                "tot_cur_bal": 25000,
                "fico_score": 710,
            }
        }
    }
