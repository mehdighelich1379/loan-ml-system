import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Loan Risk Prediction", layout="wide")
API_PRED = "http://127.0.0.1:8000/predict"
API_EXPLAIN = "http://127.0.0.1:8000/explain"

lang = st.sidebar.radio("Language / زبان", ["English", "فارسی"])

# ---------------- SAMPLE DATA ----------------
sample_data = {
    "loan_amnt": 25000,
    "term": "60 months",
    "int_rate": 14.2,
    "installment": 550,
    "grade": "C",
    "sub_grade": "C3",
    "home_ownership": "RENT",
    "annual_inc": 48000,
    "purpose": "debt_consolidation",
    "dti": 39.5,
    "open_acc": 5,
    "revol_bal": 8700,
    "revol_util": 68.0,
    "tot_cur_bal": 18000,
    "fico_score": 655,
}


# ---------------- RTL HELPER ----------------
def rtl(md_text: str):
    st.markdown(
        f"<div style='direction:rtl; text-align:right; line-height:1.8;'>{md_text}</div>",
        unsafe_allow_html=True,
    )


# ---------------- NARRATIVES ----------------
def narrative_fa(label, prob, data):
    fico = data.get("fico_score", 0)
    dti = data.get("dti", 0)
    revol = data.get("revol_util", 0)
    inc = data.get("annual_inc", 0)
    text = ""

    if prob >= 0.7:
        text += f"⚠️ مدل نشان می‌دهد احتمال نکول بالا است ({prob:.0%}).\n\n"
        text += f"نسبت بدهی به درآمد {dti:.1f}% فشار مالی بالایی را نشان می‌دهد.\n"
        text += f"امتیاز اعتباری {fico} پایین‌تر از حد مطلوب است.\n"
        text += f"درصد استفاده از اعتبار {revol:.0f}% نیز نسبتاً زیاد است.\n\n"
        text += "🔻 عوامل ریسک: DTI بالا، FICO پایین، استفاده زیاد از اعتبار.\n\n"
    elif prob >= 0.3:
        text += f"⚖️ احتمال نکول متوسط است ({prob:.0%}).\n\n"
        text += f"DTI = {dti:.1f}% ، امتیاز FICO = {fico}.\n"
        text += "وضعیت مالی نسبتاً متعادل است ولی نیاز به مدیریت دارد.\n\n"
    else:
        text += f"✅ احتمال نکول پایین است ({prob:.0%}).\n\n"
        text += f"DTI {dti:.1f}% پایین است و امتیاز اعتباری {fico} قوی است.\n"
        text += f"درآمد سالانه ${inc:,.0f} نشانگر توان بازپرداخت مناسب است.\n\n"
        text += "🔹 نتیجه: مشتری از نظر مدل قابل اعتماد است."
    return text


def narrative_en(label, prob, data):
    fico = data.get("fico_score", 0)
    dti = data.get("dti", 0)
    revol = data.get("revol_util", 0)
    inc = data.get("annual_inc", 0)
    text = ""

    if prob >= 0.7:
        text += f"⚠️ The model predicts a high default risk ({prob:.0%}).\n\n"
        text += f"Debt-to-income ratio {dti:.1f}% shows heavy obligations.\n"
        text += f"FICO score {fico} indicates moderate creditworthiness.\n"
        text += f"Revolving utilization {revol:.0f}% is relatively high.\n\n"
        text += "🔻 Risk drivers: high DTI, low FICO, high utilization."
    elif prob >= 0.3:
        text += f"⚖️ The model predicts a moderate risk ({prob:.0%}).\n\n"
        text += f"DTI = {dti:.1f}%, FICO = {fico}.\n"
        text += "Manageable financial profile, but monitoring advised."
    else:
        text += f"✅ The model predicts a low risk ({prob:.0%}).\n\n"
        text += f"DTI {dti:.1f}% is low and FICO {fico} is strong.\n"
        text += f"Annual income ${inc:,.0f} supports repayment capacity.\n"
        text += "🔹 Conclusion: borrower shows healthy financial behavior."
    return text


# ---------------- MAIN APP ----------------
st.title("💰 Loan Risk Prediction" if lang == "English" else "💰 پیش‌بینی ریسک وام")

use_sample = st.checkbox(
    "Use sample data" if lang == "English" else "استفاده از داده‌ی نمونه", value=True
)

if use_sample:
    data = sample_data.copy()
else:
    st.subheader(
        "Enter borrower info" if lang == "English" else "اطلاعات وام‌گیرنده را وارد کنید"
    )
    col1, col2 = st.columns(2)
    with col1:
        data = {
            "loan_amnt": st.number_input("Loan Amount ($)", 1000, 100000, 25000),
            "term": st.selectbox("Term", ["36 months", "60 months"]),
            "int_rate": st.number_input("Interest Rate (%)", 5.0, 30.0, 14.2),
            "installment": st.number_input("Installment ($)", 100, 2000, 550),
            "grade": st.selectbox("Grade", ["A", "B", "C", "D", "E", "F", "G"]),
            "sub_grade": st.selectbox(
                "Sub-grade",
                [
                    "A1",
                    "A2",
                    "A3",
                    "A4",
                    "A5",
                    "B1",
                    "B2",
                    "B3",
                    "B4",
                    "B5",
                    "C1",
                    "C2",
                    "C3",
                    "C4",
                    "C5",
                    "D1",
                    "D2",
                    "D3",
                    "D4",
                    "D5",
                    "E1",
                    "E2",
                    "E3",
                    "E4",
                    "E5",
                ],
            ),
            "home_ownership": st.selectbox(
                "Home Ownership", ["RENT", "OWN", "MORTGAGE"]
            ),
            "annual_inc": st.number_input("Annual Income ($)", 10000, 300000, 48000),
        }
    with col2:
        data["purpose"] = st.selectbox(
            "Purpose",
            ["debt_consolidation", "credit_card", "car", "home_improvement", "medical"],
        )
        data["dti"] = st.number_input("DTI (%)", 0.0, 60.0, 39.5)
        data["open_acc"] = st.number_input("Open Accounts", 0, 20, 5)
        data["revol_bal"] = st.number_input("Revolving Balance ($)", 0, 100000, 8700)
        data["revol_util"] = st.number_input(
            "Revolving Utilization (%)", 0.0, 100.0, 68.0
        )
        data["tot_cur_bal"] = st.number_input(
            "Total Current Balance ($)", 0, 200000, 18000
        )
        data["fico_score"] = st.number_input("FICO Score", 300, 850, 655)
# ---------------- RUN PREDICTION ----------------
if st.button("Predict / پیش‌بینی"):
    try:
        with st.spinner("Contacting API..."):
            headers = {"Content-Type": "application/json"}

            # Send POST request to /predict endpoint
            resp_pred = requests.post(API_PRED, json=data, headers=headers)
            # st.write("🧩 API Predict Response:", resp_pred.status_code)
            # Comment out or remove the raw response line:
            # st.write(resp_pred.text)  # raw output for debug

            # Send POST request to /explain endpoint
            resp_exp = requests.post(API_EXPLAIN, json=data, headers=headers)
            # st.write("🧩 API Explain Response:", resp_exp.status_code)
            # Comment out or remove the raw response line:
            # st.write(resp_exp.text)

            if resp_pred.status_code != 200:
                st.error(f"Predict API Error: {resp_pred.text}")
            elif resp_exp.status_code != 200:
                st.error(f"Explain API Error: {resp_exp.text}")
            else:
                pred = resp_pred.json()
                shap_res = resp_exp.json()

                label = shap_res.get("prediction_label", "Unknown")
                prob = shap_res.get("default_probability", 0.0)
                df = pd.DataFrame(shap_res.get("shap_summary", []))

                # ------------- RESULT -------------
                st.subheader("📊 Result" if lang == "English" else "📊 نتیجه پیش‌بینی")
                if lang == "English":
                    st.markdown(narrative_en(label, prob, data))
                else:
                    rtl(narrative_fa(label, prob, data))

                # ------------- SHAP EXPLANATION -------------
                st.subheader(
                    "🔎 SHAP Explanation" if lang == "English" else "🔎 تحلیل SHAP"
                )

                if not df.empty and "feature" in df.columns:
                    st.dataframe(df)
                    st.bar_chart(df.set_index("feature")["shap_value"])
                else:
                    st.warning("No valid SHAP data received.")

    except Exception as e:
        st.error(f"❌ API request failed: {e}")
