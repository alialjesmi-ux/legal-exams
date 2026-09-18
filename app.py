from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import json
import os

app = Flask(__name__)
app.secret_key = "emirates-law-ai-exams-2026"

# =========================================================
# إعدادات الاختبار التجريبي
# =========================================================

EXAM_NAME = "قانون الأحوال الشخصية الاتحادي"
EXAM_TIME_MINUTES = 10

# بنك أسئلة تجريبي فقط
# =========================================================
# تحميل بنك الأسئلة من questions.json
# =========================================================

def load_questions():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "questions.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


QUESTIONS = load_questions()
# =========================================================
# عداد الزيارات - تجريبي
# =========================================================

VISITS = 0


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
            max-width: 850px;
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

        .law-card {
            margin-top: 25px;
            padding: 25px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
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

        .visits {
            margin-top: 25px;
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

        <div class="law-card">

            <h3>⚖️ {{ exam_name }}</h3>

            <p>
                اختبار تجريبي يتضمن اختيار من متعدد،
                صح أو خطأ، أكمل الجملة، والتعليل أو التحليل.
            </p>

            <p>
                مدة الاختبار:
                <strong>{{ exam_time }} دقائق</strong>
            </p>

            <a href="/exam" class="button">
                بدء الاختبار
            </a>

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

            {% if q.type == "mcq" or q.type == "true_false" %}

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

    <a href="/">
        العودة إلى الصفحة الرئيسية
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


@app.route("/exam")
def exam():

    # تقسيم بنك الأسئلة حسب النوع
    true_false = [
        q for q in QUESTIONS
        if q["type"] == "true_false"
    ]

    mcq = [
        q for q in QUESTIONS
        if q["type"] == "mcq"
    ]

    complete = [
        q for q in QUESTIONS
        if q["type"] == "complete"
    ]

    analysis = [
        q for q in QUESTIONS
        if q["type"] == "analysis"
    ]

    # اختيار التوزيع المطلوب
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

    # خلط جميع الأسئلة بعد اختيارها
    random.shuffle(selected_questions)

    # حفظ أرقام الأسئلة الخاصة بهذا الممتحن
    session["exam_question_ids"] = [
        q["id"] for q in selected_questions
    ]

    return render_template_string(
        EXAM_PAGE,
        exam_name=EXAM_NAME,
        exam_time=EXAM_TIME_MINUTES,
        questions=selected_questions
    )


@app.route("/submit", methods=["POST"])
def submit():
    score = 0
    auto_questions = 0
    analysis_questions = 0

    # أرقام الأسئلة التي ظهرت للممتحن
    exam_question_ids = session.get("exam_question_ids", [])

    # اختيار الأسئلة التي ظهرت فقط
    exam_questions = [
        q for q in QUESTIONS
        if q["id"] in exam_question_ids
    ]

    for question in exam_questions:

        user_answer = request.form.get(
            "q" + str(question["id"]),
            ""
        ).strip()

        # أسئلة التحليل سنضيف تصحيحها الذكي في الخطوة التالية
        if question["type"] == "analysis":
            analysis_questions += 1
            continue

        auto_questions += 1

        correct_answer = str(
            question["answer"]
        ).strip()

        if user_answer.lower() == correct_answer.lower():
            score += 1

    return render_template_string(
        RESULT_PAGE,
        score=score,
        auto_questions=auto_questions,
        analysis_questions=analysis_questions
    )

# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
