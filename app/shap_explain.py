import os
import sys
sys.path.append(os.path.abspath("./src"))
import joblib
import pandas as pd
import shap

from src.features.feature_engineering import feature_engineering_function


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "final_pipeline_LightGBM.pkl")

pipeline = joblib.load(MODEL_PATH)
model = pipeline.named_steps["model"]
explainer = shap.TreeExplainer(model)


def get_selected_feature_names():
    preprocess = pipeline.named_steps["preprocess"]
    try:
        names = preprocess.get_feature_names_out()
    except:
        names = []
        for _, _, cols in preprocess.transformers_:
            names.extend(cols)

    selector = pipeline.named_steps["feature_selection"]
    return [names[i] for i in selector.get_support(indices=True)]


def explain_prediction(input_json):

    df_raw = pd.DataFrame([input_json])

    # Apply Feature Engineering
    X_fe = feature_engineering_function(df_raw)

    # Preprocessing transform
    X_pp = pipeline.named_steps["preprocess"].transform(X_fe)

    # Feature selection
    X = pipeline.named_steps["feature_selection"].transform(X_pp)

    # Model prediction
    prob = pipeline.predict_proba(df_raw)[0][1]

    # SHAP Calculation
    shap_vals = explainer.shap_values(X)
    shap_values = shap_vals[1] if isinstance(shap_vals, list) else shap_vals

    features = get_selected_feature_names()
    df_shap = pd.DataFrame(
        {
            "feature": features,
            "shap_value": shap_values[0],
        }
    ).sort_values(by="shap_value", ascending=False)

    for i, row in df_shap.iterrows():
        feature_name = row["feature"]
        if feature_name in X_fe.columns:
            df_shap.at[i, "feature_value"] = X_fe[feature_name].iloc[0]
        else:
            df_shap.at[i, "feature_value"] = "—"

    explanation = create_human_explanation(df_shap, prob)

    return df_shap, prob, explanation


def create_human_explanation(shap_df, prob=None):

    increasing = shap_df[shap_df["shap_value"] > 0].head(5)
    decreasing = shap_df[shap_df["shap_value"] < 0].tail(5)

    feature_translations = {
        "tot_cur_bal_log": "مانده کل حساب‌ها",
        "dti": "نسبت بدهی به درآمد",
        "home_ownership_enc": "مالکیت خانه",
        "installment_to_fico": "نسبت قسط به امتیاز اعتباری",
        "term_int_rate": "نرخ بهره و مدت وام",
        "grade_rank": "رتبه اعتباری",
        "fico_dti_interaction": "نسبت بدهی به امتیاز اعتباری",
        "installment_to_income": "نسبت قسط به درآمد",
        "purpose_term_interaction": "نوع وام و مدت آن",
        "open_acc_group_num": "تعداد حساب‌های باز",
        "purpose_risk": "ریسک نوع وام",
        "tot_cur_bal_group_num": "گروه تراز حساب‌ها",
        "fico_income_interaction": "ترکیب درآمد و امتیاز اعتباری",
        "fico_bin_num": "بازه امتیاز اعتباری",
        "revol_util_to_fico": "نسبت استفاده از اعتبار به امتیاز اعتباری",
        "income_group": "گروه درآمدی",
        "fico_balance_interaction": "نسبت مانده حساب به امتیاز اعتباری",
        "installment_to_income_interaction": "تعامل نسبت قسط و درآمد",
    }

    if prob is None:
        prob = 0
    if prob < 0.4:
        risk_label = "🟢 مشتری توان بازپرداخت وام را دارد و ریسک نکول پایین است."
    elif prob < 0.65:
        risk_label = "🟡 مشتری ریسک متوسطی در بازپرداخت وام دارد."
    else:
        risk_label = "🔴 این وام برای مشتری ریسک بالایی از نظر عدم بازپرداخت دارد."

    explanation = f"📊 احتمال نکول: {prob * 100:.1f}%\n{risk_label}\n"
    explanation += " من شرایط رو بررسی کردم و بر اساس سوابق مشتری های قبلی، نتایج زیر به دست اومده 👇\n\n"

    explanation += "🚨 عواملی که بیشترین نقش را در افزایش ریسک نکول داشتند:\n"
    for _, row in increasing.iterrows():
        f = row["feature"]
        fa_name = feature_translations.get(f, f.replace("_", " "))
        explanation += f"• {fa_name} ({f}) \n"

    if len(decreasing) > 0:
        explanation += "\n عواملی  که باعث کاهش ریسک نکول میشن:\n"
        for _, row in decreasing.iterrows():
            f = row["feature"]
            fa_name = feature_translations.get(f, f.replace("_", " "))
            explanation += f"• {fa_name} ({f}) \n"

    high_risk_feats = [
        feature_translations.get(f, f.replace("_", " "))
        for f in increasing["feature"].tolist()[:3]
    ]
    low_risk_feats = [
        feature_translations.get(f, f.replace("_", " "))
        for f in decreasing["feature"].tolist()[:3]
    ]
    if prob > 0.65:

        explanation += "\n💡 برای کاهش ریسک، بهتر است روی موارد زیر تمرکز کنید:\n"
        explanation += "کاهش " + ", ".join(high_risk_feats)
    return explanation
