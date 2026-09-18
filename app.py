from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = "emirates-law-ai-exams-2026"

# =========================================================
# إعدادات الاختبار التجريبي
# =========================================================

EXAM_NAME = "قانون الأحوال الشخصية الاتحادي"
EXAM_TIME_MINUTES = 30

# بنك أسئلة تجريبي فقط
# =========================================================
# تحميل بنك الأسئلة من questions.json
# =========================================================

# =========================================================
# إعدادات الاختبارات وبنوك الأسئلة
# =========================================================

EXAMS = {
    "personal_status": {
        "name": "قانون الأحوال الشخصية الاتحادي",
        "file": "questions.json",
        "time": 30
    },

    "civil_personal_status": {
        "name": "قانون الأحوال الشخصية المدني",
        "file": "questions_civil_personal_status.json",
        "time": 30
    },

    "civil_procedure": {
        "name": "قانون الإجراءات المدنية",
        "file": "questions_civil_procedure.json",
        "time": 30
    },
        "civil_transactions": {
        "name": "قانون المعاملات المدنية",
        "file": "questions_civil_transactions.json",
        "time": 30
    },
        "criminal_law": {
        "name": "قانون الجرائم والعقوبات",
        "file": "questions_criminal_law.json",
        "time": 30
    },
    "criminal_procedure": {
    "name": "قانون الإجراءات الجزائية",
    "file": "questions_criminal_procedure.json",
    "time": 30
    }
}
COMPREHENSIVE_EXAM = {
    "name": "الاختبار الشامل للقوانين",
    "time": 30,
    "questions_count": 100
}


def load_questions(file_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
# =========================================================
# عداد الزيارات - تجريبي
# =========================================================

VISITS = 0
REVIEW_RESULTS = {}

# =========================================================
# الصفحة الرئيسية
# =========================================================

HOME_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>الاختبارات القانونية | Emirates Law AI</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, Tahoma, sans-serif;
            background: #f3f6f9;
            color: #1f2937;
        }

        .header {
            background: #17365d;
            color: white;
            text-align: center;
            padding: 45px 20px;
        }

        .header h1 {
            margin: 0;
            font-size: 36px;
        }

        .header h2 {
            margin: 10px 0;
            font-size: 24px;
        }

        .header p {
            color: #e5e7eb;
        }

        .container {
            max-width: 950px;
            margin: 35px auto;
            padding: 0 20px;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
            text-align: center;
        }

        .laws-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .law-card {
            padding: 25px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            background: #ffffff;
        }

        .law-card h3 {
            color: #17365d;
            min-height: 55px;
        }

        .button {
            display: inline-block;
            background: #17365d;
            color: white;
            text-decoration: none;
            padding: 14px 30px;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 15px;
        }

        .button:hover {
            background: #0f2948;
        }

        .visits {
            margin-top: 30px;
            color: #64748b;
        }

        .footer {
            text-align: center;
            padding: 30px 15px;
            color: #64748b;
            line-height: 1.8;
        }
    </style>
</head>

<body>

<div class="header">
    <h1>Emirates Law AI</h1>
    <h2>قوانين الإمارات الذكية</h2>
    <p>منصة الاختبارات القانونية الذكية</p>
</div>

<div class="container">

    <div class="card">

        <h2>اختر القانون</h2>

        <p>
            اختر القانون الذي ترغب في اختبار معلوماتك فيه
        </p>

<div class="laws-grid">

    <div class="law-card">

        <h3>
            ⚖️ قانون الأحوال الشخصية الاتحادي
        </h3>

        <p>
            اختبار في أحكام قانون الأحوال الشخصية.
        </p>

        <p>
            مدة الاختبار:
            <strong>30 دقيقة</strong>
        </p>

        <a href="/exam/personal_status" class="button">
            بدء الاختبار
        </a>

    </div>


    <div class="law-card">

        <h3>
            ⚖️ قانون الأحوال الشخصية المدني
        </h3>

        <p>
            اختبار في أحكام قانون الأحوال الشخصية المدني.
        </p>

        <p>
            مدة الاختبار:
            <strong>30 دقيقة</strong>
        </p>

        <a href="/exam/civil_personal_status" class="button">
            بدء الاختبار
        </a>

    </div>


    <div class="law-card">

        <h3>
            ⚖️ قانون الإجراءات المدنية
        </h3>

        <p>
            اختبار في أحكام قانون الإجراءات المدنية.
        </p>

        <p>
            مدة الاختبار:
            <strong>30 دقيقة</strong>
        </p>

        <a href="/exam/civil_procedure" class="button">
            بدء الاختبار
        </a>

    </div>
<div class="law-card">

    <h3>
        ⚖️ قانون المعاملات المدنية
    </h3>

    <p>
        اختبار في أحكام قانون المعاملات المدنية.
    </p>

    <p>
        مدة الاختبار:
        <strong>30 دقيقة</strong>
    </p>

    <a href="/exam/civil_transactions" class="button">
        بدء الاختبار
    </a>

</div>
<div class="law-card">

    <h3>
        ⚖️ قانون الجرائم والعقوبات
    </h3>

    <p>
        اختبار في الأحكام العامة لقانون الجرائم والعقوبات.
    </p>

    <p>
        مدة الاختبار:
        <strong>30 دقيقة</strong>
    </p>

    <a href="/exam/criminal_law" class="button">
        بدء الاختبار
    </a>

</div>
<div class="law-card">

    <h3>
        ⚖️ قانون الإجراءات الجزائية
    </h3>

    <p>
        اختبار في أحكام قانون الإجراءات الجزائية.
    </p>

    <p>
        مدة الاختبار:
        <strong>30 دقيقة</strong>
    </p>

    <a href="/exam/criminal_procedure" class="button">
        بدء الاختبار
    </a>

</div>
</div>

        <div class="visits">
            👁️ عدد زيارات المنصة: {{ visits }}
        </div>

    </div>

</div>

<div class="footer">
    جميع الحقوق محفوظة © 2026<br>
    <strong>Emirates Law AI | قوانين الإمارات الذكية</strong><br>
    إعداد وتطوير: علي الجسمي
</div>

</body>
</html>
"""


# =========================================================
# صفحة الاختبار
# =========================================================

EXAM_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{{ exam_name }}</title>

    <style>
        body {
            font-family: Arial, Tahoma, sans-serif;
            background: #f3f6f9;
            margin: 0;
            color: #1f2937;
        }

        .container {
            max-width: 850px;
            margin: 30px auto;
            padding: 20px;
        }

        .timer {
            position: sticky;
            top: 0;
            background: #17365d;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            z-index: 10;
        }

        .question {
            background: white;
            padding: 25px;
            margin: 20px 0;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }

        label {
            display: block;
            padding: 7px;
        }

        input[type="text"],
        textarea {
            width: 100%;
            padding: 12px;
            margin-top: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            font-family: inherit;
        }

        textarea {
            min-height: 120px;
        }

        button {
            width: 100%;
            background: #17365d;
            color: white;
            border: none;
            padding: 16px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>

<body>

<div class="container">

    <div class="timer">
        ⏱️ الوقت المتبقي:
        <span id="timer"></span>
    </div>

    <h1>{{ exam_name }}</h1>

    <form id="examForm" method="POST" action="/submit">

        {% for q in questions %}

        <div class="question">

            <h3>
                السؤال {{ loop.index }}
            </h3>

            <p>
                <strong>{{ q.question }}</strong>
            </p>

{% if q.type == "true_false" %}

    <label>
        <input
            type="radio"
            name="q{{ q.id }}"
            value="صح"
        >
        صح
    </label>

    <label>
        <input
            type="radio"
            name="q{{ q.id }}"
            value="خطأ"
        >
        خطأ
    </label>

{% elif q.type == "mcq" %}

    {% for option in q.options %}

    <label>
        <input
            type="radio"
            name="q{{ q.id }}"
            value="{{ option }}"
        >
        {{ option }}
    </label>

    {% endfor %}

            {% elif q.type == "complete" %}

                <input
                    type="text"
                    name="q{{ q.id }}"
                    placeholder="اكتب الإجابة"
                >

            {% elif q.type == "analysis" %}

                <textarea
                    name="q{{ q.id }}"
                    placeholder="اكتب إجابتك التحليلية هنا..."
                ></textarea>

            {% endif %}

        </div>

        {% endfor %}

        <button type="submit">
            إنهاء وتسليم الاختبار
        </button>

    </form>

</div>

<script>

let seconds = {{ exam_time * 60 }};

function updateTimer() {

    let minutes = Math.floor(seconds / 60);
    let remainingSeconds = seconds % 60;

    document.getElementById("timer").innerText =
        minutes + ":" +
        String(remainingSeconds).padStart(2, "0");

    if (seconds <= 0) {
        document.getElementById("examForm").submit();
        return;
    }

    seconds--;
}

updateTimer();
setInterval(updateTimer, 1000);

</script>

</body>
</html>
"""


# =========================================================
# صفحة النتيجة
# =========================================================

RESULT_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>نتيجة الاختبار</title>

    <style>
        body {
            font-family: Arial, Tahoma, sans-serif;
            background: #f3f6f9;
            text-align: center;
            padding: 30px;
            color: #1f2937;
        }

        .result {
            max-width: 650px;
            margin: auto;
            background: white;
            padding: 40px;
            border-radius: 14px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        }

        .score {
            font-size: 40px;
            color: #17365d;
            font-weight: bold;
        }

        .notice {
            background: #fff8e1;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
        }

        a {
            display: inline-block;
            margin-top: 25px;
            background: #17365d;
            color: white;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 7px;
        }
    </style>

</head>

<body>

<div class="result">

    <h1>نتيجة الاختبار</h1>

    <div class="score">
        {{ score }} / {{ auto_questions }}
    </div>

    <p>
        الإجابات الصحيحة:
        <strong>{{ score }}</strong>
    </p>

    <p>
        الأسئلة المصححة آليًا:
        <strong>{{ auto_questions }}</strong>
    </p>

    {% if analysis_questions > 0 %}

    <div class="notice">
        يوجد {{ analysis_questions }}
        سؤال تعليل أو تحليل لم يدخل في الدرجة الآلية الحالية.
    </div>

    {% endif %}
    <a href="/review" class="button">
    مراجعة الإجابات الخاطئة
    </a>
    <a href="/">
        العودة إلى الصفحة الرئيسية
    </a>

</div>

</body>
</html>
"""
REVIEW_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
    <meta charset="UTF-8">
    <title>مراجعة الإجابات</title>

    <style>

        body {
            font-family: Arial;
            background: #f5f7fa;
            padding: 30px;
        }

        .container {
            max-width: 900px;
            margin: auto;
        }

        h1 {
            text-align: center;
        }

        .question {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            border-right: 5px solid #d9534f;
        }

        .wrong {
            color: #d9534f;
            font-weight: bold;
        }

        .correct {
            color: #198754;
            font-weight: bold;
        }

        .article {
            color: #666;
        }

        .button {
            display: block;
            width: 220px;
            margin: 30px auto;
            padding: 14px;
            text-align: center;
            background: #1d3557;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }

    </style>
</head>

<body>

<div class="container">

    <h1>مراجعة الإجابات الخاطئة</h1>

    {% if wrong_answers %}

        <p>
            عدد الإجابات التي تحتاج إلى مراجعة:
            <strong>{{ wrong_answers|length }}</strong>
        </p>

        {% for item in wrong_answers %}

        <div class="question">

            <h3>
                السؤال {{ loop.index }}
            </h3>

            <p>
                {{ item.question }}
            </p>

            <p class="wrong">
                إجابتك:
                {{ item.user_answer }}
            </p>

            <p class="correct">
                الإجابة الصحيحة:
                {{ item.correct_answer }}
            </p>

            {% if item.article %}

            <p class="article">
                المادة: {{ item.article }}
            </p>

            {% endif %}

        </div>

        {% endfor %}

    {% else %}

        <h2 style="text-align:center;">
            ممتاز! لا توجد إجابات خاطئة.
        </h2>

    {% endif %}

    <a href="/" class="button">
        العودة للصفحة الرئيسية
    </a>

</div>

</body>
</html>
"""

# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():

    global VISITS
    VISITS += 1

    return render_template_string(
        HOME_PAGE,
        exam_name=EXAM_NAME,
        exam_time=EXAM_TIME_MINUTES,
        visits=VISITS
    )
@app.route("/comprehensive")
def comprehensive_exam():

    all_questions = []

    # تحميل أسئلة جميع القوانين
    for exam_key, exam_config in EXAMS.items():

        questions = load_questions(exam_config["file"])

    for q in questions:
    question = q.copy()

    # حفظ اسم القانون ومفتاحه مع السؤال
    question["exam_key"] = exam_key
    question["law"] = exam_config["name"]

    # معرف فريد للسؤال داخل الاختبار الشامل
    question["form_id"] = (
        str(exam_key) + "_" + str(q["id"])
    )

    all_questions.append(question)

    # تقسيم الأسئلة حسب القانون
    questions_by_law = {}

    for question in all_questions:
        key = question["exam_key"]

        if key not in questions_by_law:
            questions_by_law[key] = []

        questions_by_law[key].append(question)

    # اختيار متوازن من القوانين الستة
    selected_questions = []

    exam_keys = list(EXAMS.keys())

    # 16 سؤالاً من كل قانون = 96
    for key in exam_keys:
        law_questions = questions_by_law[key]

        selected_questions += random.sample(
            law_questions,
            min(16, len(law_questions))
        )

    # إضافة 4 أسئلة إضافية عشوائياً لإكمال 100 سؤال
    remaining_questions = [
        q for q in all_questions
        if q not in selected_questions
    ]

    selected_questions += random.sample(
        remaining_questions,
        min(4, len(remaining_questions))
    )

    random.shuffle(selected_questions)

    # حفظ الأسئلة نفسها لأن أرقام ID تتكرر بين القوانين
    session["comprehensive_questions"] = selected_questions
    session["exam_key"] = "comprehensive"

    return render_template_string(
        EXAM_PAGE,
        exam_name=COMPREHENSIVE_EXAM["name"],
        exam_time=COMPREHENSIVE_EXAM["time"],
        questions=selected_questions
    )

@app.route("/exam/<exam_key>")
def exam(exam_key):

    # التأكد من أن القانون موجود
    if exam_key not in EXAMS:
        return redirect(url_for("home"))

    # بيانات القانون المختار
    exam_config = EXAMS[exam_key]

    exam_name = exam_config["name"]
    exam_time = exam_config["time"]

    # تحميل بنك الأسئلة الخاص بالقانون
    questions = load_questions(
        exam_config["file"]
    )

    # حفظ القانون المختار للممتحن
    session["exam_key"] = exam_key

    # تقسيم بنك الأسئلة حسب النوع
    true_false = [
        q for q in questions
        if q["type"] == "true_false"
    ]

    mcq = [
        q for q in questions
        if q["type"] == "mcq"
    ]

    complete = [
        q for q in questions
        if q["type"] == "complete"
    ]

    analysis = [
        q for q in questions
        if q["type"] == "analysis"
    ]

    # اختيار الأسئلة
    selected_questions = []

    selected_questions += random.sample(
        true_false,
        min(55, len(true_false))
    )

    selected_questions += random.sample(
        mcq,
        min(38, len(mcq))
    )

    selected_questions += random.sample(
        complete,
        min(5, len(complete))
    )

    selected_questions += random.sample(
        analysis,
        min(2, len(analysis))
    )

    # خلط الأسئلة
    random.shuffle(selected_questions)

    # حفظ أرقام أسئلة هذا الاختبار
    session["exam_question_ids"] = [
        q["id"] for q in selected_questions
    ]

    return render_template_string(
        EXAM_PAGE,
        exam_name=exam_name,
        exam_time=exam_time,
        questions=selected_questions
    )


@app.route("/submit", methods=["POST"])
def submit():

    score = 0
    auto_questions = 0
    analysis_questions = 0
    wrong_answers = []

    exam_key = session.get("exam_key")

    if exam_key == "comprehensive":

        questions = session.get(
            "comprehensive_questions",
            []
        )

        exam_question_ids = [
            q["id"] for q in questions
        ]

    elif exam_key in EXAMS:

        exam_config = EXAMS[exam_key]

        questions = load_questions(
            exam_config["file"]
        )

        exam_question_ids = session.get(
            "exam_question_ids",
            []
        )

    else:

        return redirect(url_for("home"))

    for question_id in exam_question_ids:

        question = next(
            (
                q for q in questions
                if q["id"] == question_id
            ),
            None
        )

        if question is None:
            continue

        user_answer = request.form.get(
            "q" + str(question["id"]),
            ""
        ).strip()

        # أسئلة التحليل لا تدخل في التصحيح حاليا
        if question["type"] == "analysis":
            analysis_questions += 1
            continue

        auto_questions += 1

        correct_answer = str(
            question.get("answer", "")
        ).strip()

        if user_answer.lower() == correct_answer.lower():

            score += 1

        else:

            wrong_answers.append({
                "id": question["id"],
                "question": question["question"],
                "user_answer": (
                    user_answer
                    if user_answer
                    else "لم تتم الإجابة"
                ),
                "correct_answer": correct_answer,
                "article": question.get("article", ""),
                "law": question.get("law", "")
            })

    review_id = str(uuid.uuid4())

    REVIEW_RESULTS[review_id] = wrong_answers

    session["review_id"] = review_id

    return render_template_string(
        RESULT_PAGE,
        score=score,
        auto_questions=auto_questions,
        analysis_questions=analysis_questions
    )
@app.route("/review")
def review():

    review_id = session.get("review_id")

    wrong_answers = REVIEW_RESULTS.get(
        review_id,
        []
    )

    return render_template_string(
        REVIEW_PAGE,
        wrong_answers=wrong_answers
    )

# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
