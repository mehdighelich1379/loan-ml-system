feature_texts = {
    "tot_cur_bal_log": {
        "fa": ("لگاریتم کل مانده حساب‌ها", "موجودی بالاتر → توان بازپرداخت بهتر"),
        "en": (
            "Total Balance (log)",
            "Higher total bank balance → higher repayment ability",
        ),
    },
    "fico_balance_interaction": {
        "fa": (
            "تعامل نمره اعتباری و موجودی",
            "نمره اعتباری بالا + موجودی خوب = ریسک کمتر",
        ),
        "en": ("FICO × Balance", "High FICO + strong balance = lower default risk"),
    },
    "balance_to_income": {
        "fa": ("نسبت موجودی به درآمد", "موجودی بیشتر نسبت به درآمد → ثبات مالی"),
        "en": ("Balance to Income", "Higher balance vs income → better stability"),
    },
    "installment_to_fico": {
        "fa": ("قسط به نسبت FICO", "قسط بالا + نمره پایین → ریسک بیشتر"),
        "en": ("Installment / FICO", "High installment vs FICO → higher risk"),
    },
    "purpose_risk": {
        "fa": ("ریسک هدف وام", "اهداف مصرفی مثل کارت اعتباری ریسک بیشتری دارند"),
        "en": ("Loan Purpose Risk", "Consumer credit loans have higher risk"),
    },
    "purpose_term_interaction": {
        "fa": ("تعامل هدف و مدت وام", "مدت طولانی + هدف پرریسک → ریسک بیشتر"),
        "en": ("Purpose × Term", "Long term and risky purpose → higher risk"),
    },
    "revol_util_to_fico": {
        "fa": ("نسبت مصرف اعتبار به FICO", "مصرف اعتبار بالا → فشار مالی"),
        "en": ("Revolving Util / FICO", "High utilization → higher pressure"),
    },
    "installment_to_income": {
        "fa": ("قسط به درآمد", "نسبت قسط بالا → احتمال نکول بیشتر"),
        "en": ("Installment / Income", "High installment vs income → default risk"),
    },
    "open_acc_group_num": {
        "fa": ("گروه تعداد حساب‌های باز", "تعداد زیاد/کم حساب → سیگنال رفتاری مالی"),
        "en": ("Open Accounts Group", "Too many/too few accounts matter"),
    },
    "fico_dti_interaction": {
        "fa": ("تعامل FICO با بدهی", "بدهی زیاد + FICO پایین = ریسک بالا"),
        "en": ("FICO × DTI", "High debt + low FICO → bad sign"),
    },
    "home_ownership_enc": {
        "fa": ("وضعیت مسکن", "مالک بودن = ثبات مالی بیشتر"),
        "en": ("Home Ownership", "Homeowners are lower risk"),
    },
    "fico_bin_num": {
        "fa": ("نمره اعتباری", "FICO بالاتر = عملکرد بهتر در بازپرداخت"),
        "en": ("FICO Score", "Higher FICO → safer borrower"),
    },
    "tot_cur_bal_group_num": {
        "fa": ("گروه‌بندی موجودی کل", "موجودی مناسب → احتمال نکول کمتر"),
        "en": ("Total Balance Group", "Higher grouped balance → lower risk"),
    },
    "term_int_rate": {
        "fa": ("مدت × بهره", "بهره بالا و مدت طولانی → ریسک بیشتر"),
        "en": ("Term × Interest", "High rate + long term → risky"),
    },
    "grade_rank": {
        "fa": ("رتبه اعتبار وام", "رتبه پایین‌تر (C,D...) → ریسک بالاتر"),
        "en": ("Loan Grade", "Lower grade = higher risk"),
    },
}
