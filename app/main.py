import sys, os

sys.path.append(os.path.abspath("./src"))

from fastapi import FastAPI
from app.schemas import LoanRequest
from app.shap_explain import explain_prediction
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Loan Default Prediction API")

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Static
app.mount("/static", StaticFiles(directory="static"), name="static")


#  Health endpoint for CI
@app.get("/health")
def health():
    return {"status": "ok"}


#  Redirect / to /ui
@app.get("/")
def root():
    return RedirectResponse(url="/ui")


#  Serve UI page
@app.get("/ui")
def serve_ui():
    return FileResponse("static/index.html")


#  Explain
@app.post("/explain")
def explain(request: LoanRequest):
    df_shap, pred_prob, explanation = explain_prediction(request.model_dump())
    return {
        "prediction": "Default Risk" if pred_prob >= 0.5 else "Fully Paid",
        "default_probability": round(pred_prob, 4),
        "threshold": 0.5,
        "shap_summary": df_shap.to_dict(orient="records"),
        "explanation": explanation,
    }


#  Legacy /predict for tests
@app.post("/predict")
def predict(request: LoanRequest):
    result = explain(request)
    return {
        "prediction": result["prediction"],
        "default_probability": result["default_probability"],
    }
