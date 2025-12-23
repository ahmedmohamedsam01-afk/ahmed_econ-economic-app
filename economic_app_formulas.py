import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import requests
from io import BytesIO
import openpyxl

# إعدادات الصفحة
st.set_page_config(
    page_title="قياس النشاط الاقتصادي - مع القوانين والأمثلة",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التنسيق العربي
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }

    .main-title {
        background: linear-gradient(120deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .formula-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        font-size: 18px;
    }

    .example-box {
        background: #d1ecf1;
        border: 2px solid #0c5460;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }

    .info-box {
        background: #f0f8ff;
        padding: 15px;
        border-radius: 8px;
        border-right: 3px solid #2E86AB;
        margin: 15px 0;
    }

    .law-box {
        background: #e8f5e9;
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }

    .calculation-step {
        background: #f5f5f5;
        border-left: 4px solid #2E86AB;
        padding: 15px;
        margin: 10px 0;
    }

    .stButton>button {
        background: linear-gradient(120deg, #2E86AB 0%, #1565C0 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
<div class="main-title">
    <h1>📊 قياس النشاط الاقتصادي - القوانين والأمثلة</h1>
    <p>تطبيق تفاعلي مع جميع الصيغ والأمثلة من الكتاب</p>
</div>
""", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.title("📌 القائمة الرئيسية")

    menu = st.radio(
        "اختر القسم:",
        ["🏠 نظرة عامة",
         "💰 الناتج المحلي الإجمالي (PIB)",
         "📐 مثال الصناعتين (من الكتاب)",
         "📊 PIB الاسمي والحقيقي",
         "📈 معدل النمو والدفلاتور",
         "💹 التضخم ومؤشر الأسعار",
         "👥 البطالة ومعدل المشاركة",
         "🔢 قاعدة 70",
         "📥 تحميل البيانات"]
    )

    st.markdown("---")
    st.info("📚 جميع الصيغ والأمثلة مستمدة من الكتاب")

# دالة لإنشاء بيانات تجريبية
@st.cache_data
def create_sample_data():
    years = list(range(2000, 2024))
    gdp = [100 * (1.025 ** i) * (1 + 0.05 * np.sin(i/3)) for i in range(len(years))]
    growth = [2.5 + 2 * np.sin(i/3) + np.random.normal(0, 0.5) for i in range(len(years))]
    inflation = [2.0 + 1.5 * np.sin(i/4) + np.random.normal(0, 0.3) for i in range(len(years))]
    unemployment = [8.0 + 2 * np.cos(i/3) + np.random.normal(0, 0.4) for i in range(len(years))]

    df = pd.DataFrame({
        'السنة': years,
        'الناتج_المحلي': gdp,
        'معدل_النمو': growth,
        'معدل_التضخم': inflation,
        'معدل_البطالة': unemployment
    })
    return df

if 'df' not in st.session_state:
    st.session_state.df = create_sample_data()

df = st.session_state.df

# ========== الصفحة الرئيسية ==========
if menu == "🏠 نظرة عامة":
    st.header("📚 المؤشرات الاقتصادية الكلية - القوانين والصيغ")

    st.markdown("""
    <div class="info-box">
        <h3>🎯 هذا التطبيق يعرض:</h3>
        <ul>
            <li>جميع الصيغ الرياضية لحساب المؤشرات الاقتصادية</li>
            <li>الأمثلة العددية الواردة في الكتاب</li>
            <li>شرح تفصيلي خطوة بخطوة للحسابات</li>
            <li>حاسبات تفاعلية لتطبيق القوانين</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📊 المؤشرات الرئيسية:

        **1. الناتج المحلي الإجمالي (PIB)**
        - طريقة الإنتاج (القيم المضافة)
        - طريقة الطلب (السلع النهائية)
        - طريقة الدخل (الأجور والأرباح)

        **2. معدل النمو الاقتصادي**
        - الصيغة الأساسية
        - التوسع والركود

        **3. الدفلاتور (Déflateur)**
        - PIB الاسمي / PIB الحقيقي
        - قياس التضخم
        """)

    with col2:
        st.markdown("""
        ### 📐 القوانين الأساسية:

        **4. مؤشر أسعار المستهلك (IPC)**
        - حساب التضخم
        - القوة الشرائية

        **5. البطالة**
        - معدل البطالة
        - معدل المشاركة
        - معدل التشغيل

        **6. قاعدة 70**
        - سنوات المضاعفة
        """)

# ========== صفحة PIB ==========
elif menu == "💰 الناتج المحلي الإجمالي (PIB)":
    st.header("💰 الناتج المحلي الإجمالي (PIB)")

    st.markdown("""
    <div class="info-box">
        <h3>📖 التعريف (من الكتاب)</h3>
        <p><b>الناتج المحلي الإجمالي (PIB)</b> يقيس الإنتاج الكلي للاقتصاد، أي مجموع الثروات المُنتَجة.</p>
        <p>يُحسب لمنطقة جغرافية معينة (عادة دولة) ولفترة زمنية محددة (عادة سنة أو فصل).</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 الطرق الثلاث لحساب PIB")

    tab1, tab2, tab3 = st.tabs(["1️⃣ طريقة الإنتاج", "2️⃣ طريقة الطلب", "3️⃣ طريقة الدخل"])

    with tab1:
        st.markdown("""
        ### 1️⃣ طريقة الإنتاج (Optique de la production)

        <div class="formula-box">
            <h4>📐 الصيغة الأساسية:</h4>
            <p style="font-size: 20px; text-align: center;">
                <b>PIB = مجموع القيم المضافة</b>
            </p>
            <p style="font-size: 18px; text-align: center;">
                <b>VA = Production - Consommations Intermédiaires</b>
            </p>
            <p style="text-align: center;">
                القيمة المضافة = الإنتاج - الاستهلاكات الوسيطة
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        #### 📚 من الكتاب:

        <div class="law-box">
            <p><b>لماذا نطرح الاستهلاكات الوسيطة؟</b></p>
            <p>لتجنب الحساب المزدوج (Double comptabilisation). إذا جمعنا إنتاج جميع الصناعات، 
            سنحسب إنتاج الفولاذ مرتين:</p>
            <ul>
                <li>المرة الأولى: عندما يُستخرج ويُباع كفولاذ</li>
                <li>المرة الثانية: عندما يُحوّل ويُباع كسيارة</li>
            </ul>
            <p><b>الحل:</b> نستخدم مفهوم القيمة المضافة!</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        ### 2️⃣ طريقة الطلب (Optique de la demande)

        <div class="formula-box">
            <h4>📐 الصيغة:</h4>
            <p style="font-size: 20px; text-align: center;">
                <b>PIB = C + I + G + (X - M)</b>
            </p>
            <p style="text-align: center;">حيث:</p>
            <ul>
                <li><b>C:</b> الاستهلاك (Consommation)</li>
                <li><b>I:</b> الاستثمار (Investissement - FBCF)</li>
                <li><b>G:</b> الإنفاق الحكومي (Dépenses publiques)</li>
                <li><b>X:</b> الصادرات (Exportations)</li>
                <li><b>M:</b> الواردات (Importations)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        #### 🧮 حاسبة PIB (طريقة الطلب)
        """)

        col1, col2 = st.columns(2)

        with col1:
            C = st.number_input("الاستهلاك (C) - بالمليار", value=1268.5, step=10.0, key="c_demand")
            I = st.number_input("الاستثمار (I) - بالمليار", value=537.9, step=10.0, key="i_demand")

        with col2:
            G = st.number_input("الإنفاق الحكومي (G) - بالمليار", value=550.9, step=10.0, key="g_demand")
            X = st.number_input("الصادرات (X) - بالمليار", value=737.4, step=10.0, key="x_demand")
            M = st.number_input("الواردات (M) - بالمليار", value=755.6, step=10.0, key="m_demand")

        NX = X - M
        PIB_calculated = C + I + G + NX

        st.markdown(f"""
        <div class="calculation-step">
            <h4>📊 الحساب خطوة بخطوة:</h4>
            <p><b>الخطوة 1:</b> حساب الصادرات الصافية (NX)</p>
            <p style="margin-right: 20px;">NX = X - M = {X:.2f} - {M:.2f} = <b>{NX:.2f}</b> مليار</p>

            <p><b>الخطوة 2:</b> حساب PIB</p>
            <p style="margin-right: 20px;">PIB = C + I + G + NX</p>
            <p style="margin-right: 20px;">PIB = {C:.2f} + {I:.2f} + {G:.2f} + ({NX:.2f})</p>
            <p style="margin-right: 20px;"><b style="font-size: 24px; color: #2E86AB;">PIB = {PIB_calculated:.2f} مليار</b></p>
        </div>
        """, unsafe_allow_html=True)

        # رسم بياني
        fig_pie = go.Figure(data=[go.Pie(
            labels=['الاستهلاك (C)', 'الاستثمار (I)', 'الإنفاق الحكومي (G)', 'الصادرات الصافية (NX)'],
            values=[C, I, G, NX if NX > 0 else 0],
            hole=.3,
            marker_colors=['#2E86AB', '#A23B72', '#F18F01', '#4CAF50']
        )])

        fig_pie.update_layout(title="توزيع مكونات PIB")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.markdown("""
        ### 3️⃣ طريقة الدخل (Optique des revenus)

        <div class="formula-box">
            <h4>📐 الصيغة:</h4>
            <p style="font-size: 18px; text-align: center;">
                <b>PIB = الأجور + الأرباح + الفوائد + الضرائب + ...</b>
            </p>
            <p style="text-align: center;">
                <b>PIB = Salaires + Profits + Intérêts + Taxes + ...</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        #### 📚 من الكتاب:

        حسب هذا المنهج، PIB هو مجموع دخول عوامل الإنتاج المُوزَّعة في الاقتصاد.

        **أشكال الدخول:**
        - **الأجور:** تعويض عامل الإنتاج "العمل"
        - **الأرباح:** تعويض عامل الإنتاج "رأس المال"
        - **الفوائد:** تعويض الادخار المُقرَض للشركة
        - **الضرائب:** الضرائب غير المباشرة
        """)

# ========== مثال الصناعتين ==========
elif menu == "📐 مثال الصناعتين (من الكتاب)":
    st.header("📐 مثال الصناعتين: الحديد والصلب والسيارات")

    st.markdown("""
    <div class="example-box">
        <h3>📖 المثال من الكتاب (صفحة 26-29)</h3>
        <p>لنفترض وجود صناعتين في الاقتصاد:</p>
        <ul>
            <li><b>الصناعة المعدنية (Métallurgique):</b> تنتج الفولاذ</li>
            <li><b>الصناعة السيارات (Automobile):</b> تنتج السيارات</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # البيانات من الكتاب
    st.subheader("📊 البيانات الأساسية (بملايين اليورو)")

    data_industries = {
        'البيان': ['الإنتاج (Production)', 'الاستهلاكات الوسيطة (CI)', 
                   'الأجور (Salaires)', 'الفوائد (Intérêts)', 
                   'التكاليف الكلية', 'الأرباح (Profit)'],
        'الصناعة المعدنية': [1000, 0, 100, 30, 130, 870],
        'صناعة السيارات': [2000, 1000, 400, 10, 1410, 590]
    }

    df_industries = pd.DataFrame(data_industries)
    st.table(df_industries)

    st.markdown("""
    <div class="info-box">
        <h4>📝 ملاحظات:</h4>
        <ul>
            <li>الصناعة المعدنية تستخرج الحديد بنفسها (CI = 0)</li>
            <li>الصناعة المعدنية تبيع الفولاذ لصناعة السيارات بـ 1000 مليون يورو</li>
            <li>صناعة السيارات تبيع السيارات بـ 2000 مليون يورو</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # الحسابات
    st.subheader("🔢 الحسابات التفصيلية")

    tab1, tab2, tab3 = st.tabs(["طريقة الإنتاج", "طريقة الطلب", "طريقة الدخل"])

    with tab1:
        st.markdown("""
        ### 1️⃣ حساب PIB بطريقة الإنتاج (القيم المضافة)
        """)

        st.markdown("""
        <div class="calculation-step">
            <h4>الخطوة 1: حساب القيمة المضافة للصناعة المعدنية</h4>
            <p style="font-size: 18px;">VA<sub>MET</sub> = P<sub>MET</sub> - CI<sub>MET</sub></p>
            <p style="font-size: 18px;">VA<sub>MET</sub> = 1000 - 0 = <b>1000 مليون يورو</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="calculation-step">
            <h4>الخطوة 2: حساب القيمة المضافة لصناعة السيارات</h4>
            <p style="font-size: 18px;">VA<sub>AUT</sub> = P<sub>AUT</sub> - CI<sub>AUT</sub></p>
            <p style="font-size: 18px;">VA<sub>AUT</sub> = 2000 - 1000 = <b>1000 مليون يورو</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="calculation-step">
            <h4>الخطوة 3: حساب PIB</h4>
            <p style="font-size: 18px;">PIB = VA<sub>MET</sub> + VA<sub>AUT</sub></p>
            <p style="font-size: 18px;">PIB = 1000 + 1000 = <b style="color: #2E86AB; font-size: 24px;">2000 مليون يورو</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.warning("""
        ⚠️ **ملاحظة مهمة من الكتاب:**

        مجموع المبيعات = 1000 + 2000 = 3000 مليون يورو

        لكن PIB ≠ 3000 !

        لماذا؟ لأن 3000 تتضمن حساباً مزدوجاً للفولاذ. لهذا نستخدم القيم المضافة.
        """)

        # جدول ملخص
        summary_production = pd.DataFrame({
            'الصناعة': ['المعدنية', 'السيارات', 'المجموع'],
            'الإنتاج': [1000, 2000, 3000],
            'الاستهلاكات الوسيطة': [0, 1000, 1000],
            'القيمة المضافة': [1000, 1000, 2000]
        })

        st.subheader("📊 جدول ملخص (Tableau 1.3 من الكتاب)")
        st.table(summary_production)

    with tab2:
        st.markdown("""
        ### 2️⃣ حساب PIB بطريقة الطلب (السلع النهائية)
        """)

        st.markdown("""
        <div class="calculation-step">
            <h4>التحليل:</h4>
            <p>لدينا عمليتا بيع:</p>
            <ol>
                <li>بيع الفولاذ من الصناعة المعدنية لصناعة السيارات (1000 مليون)</li>
                <li>بيع السيارات من صناعة السيارات للمستهلك (2000 مليون)</li>
            </ol>

            <p><b>السؤال:</b> أي عملية بيع نحسبها؟</p>

            <p><b>الجواب:</b> فقط بيع السلع النهائية (السيارات)!</p>

            <p style="font-size: 20px; margin-top: 20px;">
                <b>PIB = 2000 مليون يورو</b>
            </p>

            <p>الفولاذ هو <b>سلعة وسيطة</b> (bien intermédiaire) لا تُحسب في PIB بهذه الطريقة.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        ### 3️⃣ حساب PIB بطريقة الدخل
        """)

        st.markdown("""
        <div class="calculation-step">
            <h4>نجمع جميع الدخول المُوزَّعة:</h4>
        </div>
        """, unsafe_allow_html=True)

        # حساب كل صناعة
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **الصناعة المعدنية:**
            - الأجور: 100
            - الفوائد: 30
            - الأرباح: 870
            - **المجموع: 1000**
            """)

        with col2:
            st.markdown("""
            **صناعة السيارات:**
            - الأجور: 400
            - الفوائد: 10
            - الأرباح: 590
            - **المجموع: 1000**
            """)

        # جدول ملخص
        summary_income = pd.DataFrame({
            'نوع الدخل': ['الأجور', 'الفوائد', 'الأرباح', 'المجموع'],
            'الصناعة المعدنية': [100, 30, 870, 1000],
            'صناعة السيارات': [400, 10, 590, 1000],
            'المجموع': [500, 40, 1460, 2000]
        })

        st.subheader("📊 جدول الدخول (Tableau 1.4 من الكتاب)")
        st.table(summary_income)

        st.success("""
        ✅ **النتيجة النهائية:**

        PIB = 500 + 40 + 1460 = **2000 مليون يورو**

        **الطرق الثلاث تعطي نفس النتيجة!**
        """)

# ========== PIB الاسمي والحقيقي ==========
elif menu == "📊 PIB الاسمي والحقيقي":
    st.header("📊 PIB الاسمي والحقيقي")

    st.markdown("""
    <div class="info-box">
        <h3>📖 من الكتاب (صفحة 29-30)</h3>
        <p>في 2018، PIB الاسمي لفرنسا = 2353.1 مليار يورو</p>
        <p>في 1960، PIB الاسمي لفرنسا = 46.8 مليار يورو</p>
        <p><b>السؤال:</b> هل الإنتاج تضاعف 50.3 مرة؟</p>
        <p><b>الجواب:</b> لا! لأن PIB الاسمي يتأثر بارتفاع الأسعار.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📐 PIB الاسمي (PIB nominal)</h4>
            <p><b>PIB en valeur / en euros courants</b></p>
            <p style="font-size: 18px;">PIB<sub>nominal</sub> = Σ (Q<sub>t</sub> × P<sub>t</sub>)</p>
            <p>حيث:</p>
            <ul>
                <li>Q<sub>t</sub> = الكميات في السنة t</li>
                <li>P<sub>t</sub> = الأسعار الجارية في السنة t</li>
            </ul>
            <p><b>يتأثر بـ:</b></p>
            <ul>
                <li>✓ تغير الكميات</li>
                <li>✓ تغير الأسعار (التضخم)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="formula-box">
            <h4>📐 PIB الحقيقي (PIB réel)</h4>
            <p><b>PIB en volume / en euros constants</b></p>
            <p style="font-size: 18px;">PIB<sub>réel</sub> = Σ (Q<sub>t</sub> × P<sub>base</sub>)</p>
            <p>حيث:</p>
            <ul>
                <li>Q<sub>t</sub> = الكميات في السنة t</li>
                <li>P<sub>base</sub> = أسعار سنة الأساس (ثابتة)</li>
            </ul>
            <p><b>يتأثر بـ:</b></p>
            <ul>
                <li>✓ تغير الكميات فقط</li>
                <li>✗ لا يتأثر بالتضخم</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # مثال من الكتاب: اقتصاد بسلعة واحدة
    st.subheader("📚 مثال: اقتصاد ينتج الحواسيب فقط (Tableau 1.6 من الكتاب)")

    st.markdown("""
    <div class="example-box">
        <p>لنفترض أن الاقتصاد ينتج فقط الحواسيب، والبيانات كالتالي:</p>
    </div>
    """, unsafe_allow_html=True)

    # البيانات
    data_computers = {
        'السنة': ['السنة 1', 'السنة 2', 'السنة 3'],
        'الكمية (Q)': [50000, 55000, 58000],
        'السعر (P)': [100, 120, 150]
    }

    df_comp = pd.DataFrame(data_computers)
    st.table(df_comp)

    # الحسابات
    st.subheader("🔢 الحسابات خطوة بخطوة")

    tab1, tab2 = st.tabs(["PIB الاسمي", "PIB الحقيقي"])

    with tab1:
        st.markdown("""
        ### حساب PIB الاسمي (بالأسعار الجارية)
        """)

        st.markdown("""
        <div class="calculation-step">
            <h4>السنة 1:</h4>
            <p>PIB<sub>nominal</sub> = Q × P = 50,000 × 100 = <b>5,000,000</b></p>
        </div>

        <div class="calculation-step">
            <h4>السنة 2:</h4>
            <p>PIB<sub>nominal</sub> = Q × P = 55,000 × 120 = <b>6,600,000</b></p>
            <p>معدل النمو = [(6,600,000 - 5,000,000) / 5,000,000] × 100 = <b>32.0%</b></p>
        </div>

        <div class="calculation-step">
            <h4>السنة 3:</h4>
            <p>PIB<sub>nominal</sub> = Q × P = 58,000 × 150 = <b>8,700,000</b></p>
            <p>معدل النمو = [(8,700,000 - 6,600,000) / 6,600,000] × 100 = <b>31.8%</b></p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        ### حساب PIB الحقيقي (سنة الأساس: السنة 1)
        """)

        st.markdown("""
        <div class="calculation-step">
            <h4>السنة 1:</h4>
            <p>PIB<sub>réel</sub> = Q<sub>1</sub> × P<sub>1</sub> = 50,000 × 100 = <b>5,000,000</b></p>
            <p>ملاحظة: PIB الاسمي = PIB الحقيقي في سنة الأساس</p>
        </div>

        <div class="calculation-step">
            <h4>السنة 2:</h4>
            <p>PIB<sub>réel</sub> = Q<sub>2</sub> × P<sub>1</sub> = 55,000 × 100 = <b>5,500,000</b></p>
            <p>معدل النمو الحقيقي = [(5,500,000 - 5,000,000) / 5,000,000] × 100 = <b>10.0%</b></p>
        </div>

        <div class="calculation-step">
            <h4>السنة 3:</h4>
            <p>PIB<sub>réel</sub> = Q<sub>3</sub> × P<sub>1</sub> = 58,000 × 100 = <b>5,800,000</b></p>
            <p>معدل النمو الحقيقي = [(5,800,000 - 5,500,000) / 5,500,000] × 100 = <b>5.5%</b></p>
        </div>
        """, unsafe_allow_html=True)

    # جدول ملخص
    summary_pib = pd.DataFrame({
        'السنة': ['السنة 1', 'السنة 2', 'السنة 3'],
        'الكمية': [50000, 55000, 58000],
        'السعر': [100, 120, 150],
        'PIB الاسمي': [5000000, 6600000, 8700000],
        'PIB الحقيقي (أساس: سنة 1)': [5000000, 5500000, 5800000],
        'نمو اسمي (%)': ['-', 32.0, 31.8],
        'نمو حقيقي (%)': ['-', 10.0, 5.5]
    })

    st.subheader("📊 جدول ملخص (Tableau 1.7 من الكتاب)")
    st.table(summary_pib)

    st.success("""
    ✅ **الاستنتاج الرئيسي:**

    - النمو الاسمي (32%) > النمو الحقيقي (10%)
    - الفرق يعود إلى ارتفاع الأسعار (التضخم)
    - PIB الحقيقي يعكس النمو الفعلي للإنتاج
    """)

# ========== معدل النمو والدفلاتور ==========
elif menu == "📈 معدل النمو والدفلاتور":
    st.header("📈 معدل النمو والدفلاتور")

    st.subheader("1️⃣ معدل النمو (Taux de croissance)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة الأساسية (من الكتاب - صفحة 30-31):</h4>
        <p style="font-size: 22px; text-align: center;">
            <b>g<sub>t</sub> = [(Y<sub>t</sub> - Y<sub>t-1</sub>) / Y<sub>t-1</sub>] × 100</b>
        </p>
        <p style="text-align: center;">أو</p>
        <p style="font-size: 22px; text-align: center;">
            <b>g<sub>t</sub> = [(Y<sub>t</sub> / Y<sub>t-1</sub>) - 1] × 100</b>
        </p>
        <p style="text-align: center;">حيث Y = PIB</p>
    </div>
    """, unsafe_allow_html=True)

    # حاسبة معدل النمو
    st.subheader("🧮 حاسبة معدل النمو")

    col1, col2 = st.columns(2)

    with col1:
        pib_t1 = st.number_input("PIB السنة السابقة (t-1)", value=2247.2, step=10.0, key="pib_t1")
        pib_t = st.number_input("PIB السنة الحالية (t)", value=2285.9, step=10.0, key="pib_t")

    growth_rate = ((pib_t - pib_t1) / pib_t1) * 100

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>الحساب:</h4>
            <p>g = [(Y<sub>t</sub> - Y<sub>t-1</sub>) / Y<sub>t-1</sub>] × 100</p>
            <p>g = [({pib_t:.2f} - {pib_t1:.2f}) / {pib_t1:.2f}] × 100</p>
            <p>g = [{pib_t - pib_t1:.2f} / {pib_t1:.2f}] × 100</p>
            <p><b style="font-size: 24px; color: #2E86AB;">g = {growth_rate:.2f}%</b></p>
        </div>
        """, unsafe_allow_html=True)

    # التصنيف
    if growth_rate > 0:
        st.success(f"✅ **التوسع (Expansion):** معدل النمو إيجابي ({growth_rate:.2f}%)")
    elif growth_rate < 0:
        st.error(f"❌ **الركود (Récession):** معدل النمو سلبي ({growth_rate:.2f}%)")
    else:
        st.warning("⚠️ **ركود:** معدل النمو = صفر")

    st.markdown("---")

    # الدفلاتور
    st.subheader("2️⃣ دفلاتور PIB (Déflateur du PIB)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة (من الكتاب - صفحة 31):</h4>
        <p style="font-size: 22px; text-align: center;">
            <b>Déflateur = PIB<sub>nominal</sub> / PIB<sub>réel</sub></b>
        </p>
        <p style="text-align: center;">أو</p>
        <p style="font-size: 20px; text-align: center;">
            <b>P = Y<sub>n</sub> / Y<sub>r</sub></b>
        </p>
        <p style="text-align: center;">حيث:</p>
        <ul>
            <li>P = الدفلاتور</li>
            <li>Y<sub>n</sub> = PIB الاسمي</li>
            <li>Y<sub>r</sub> = PIB الحقيقي</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="law-box">
        <h4>📚 العلاقة الأساسية:</h4>
        <p style="font-size: 20px; text-align: center;">
            <b>PIB<sub>nominal</sub> = PIB<sub>réel</sub> × Déflateur</b>
        </p>
        <p style="font-size: 18px; text-align: center;">
            <b>Y<sub>n</sub> = Y<sub>r</sub> × P</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # حاسبة الدفلاتور
    st.subheader("🧮 حاسبة الدفلاتور")

    col1, col2 = st.columns(2)

    with col1:
        pib_nominal = st.number_input("PIB الاسمي", value=2353.1, step=10.0, key="pib_nom")
        pib_reel = st.number_input("PIB الحقيقي", value=2285.9, step=10.0, key="pib_reel")

    deflateur = pib_nominal / pib_reel

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>الحساب:</h4>
            <p>Déflateur = PIB<sub>nominal</sub> / PIB<sub>réel</sub></p>
            <p>Déflateur = {pib_nominal:.2f} / {pib_reel:.2f}</p>
            <p><b style="font-size: 24px; color: #2E86AB;">Déflateur = {deflateur:.4f}</b></p>
        </div>
        """, unsafe_allow_html=True)

    # معدل التضخم من الدفلاتور
    st.subheader("3️⃣ معدل التضخم من الدفلاتور")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة (من الكتاب - صفحة 31):</h4>
        <p style="font-size: 18px; text-align: center;">
            <b>π ≈ g<sub>nominal</sub> - g<sub>réel</sub></b>
        </p>
        <p style="text-align: center;">معدل التضخم ≈ معدل النمو الاسمي - معدل النمو الحقيقي</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="law-box">
        <h4>📚 الصيغة الدقيقة (من الكتاب):</h4>
        <p style="font-size: 18px; text-align: center;">
            <b>g<sub>nominal</sub> = (1 + g<sub>réel</sub>) × (1 + π) - 1</b>
        </p>
        <p style="font-size: 18px; text-align: center;">
            <b>g<sub>nominal</sub> ≈ g<sub>réel</sub> + π + (g<sub>réel</sub> × π)</b>
        </p>
        <p style="text-align: center;">
            عندما تكون قيم g و π صغيرة، يكون حاصل ضربهما قريباً من صفر،
        </p>
        <p style="text-align: center;">
            لذلك: <b>g<sub>nominal</sub> ≈ g<sub>réel</sub> + π</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # مثال من الكتاب
    st.subheader("📚 مثال من الكتاب (2017-2018)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **البيانات (من الكتاب):**
        - معدل نمو PIB الاسمي = 2.5%
        - معدل نمو PIB الحقيقي = 1.7%
        """)

    with col2:
        st.markdown("""
        **الحساب:**

        π ≈ 2.5% - 1.7% = **0.8%**

        معدل التضخم ≈ **0.8%**
        """)

# ========== التضخم ومؤشر الأسعار ==========
elif menu == "💹 التضخم ومؤشر الأسعار":
    st.header("💹 التضخم ومؤشر أسعار المستهلك (IPC)")

    st.markdown("""
    <div class="info-box">
        <h3>📖 التعريف</h3>
        <p><b>التضخم (Inflation):</b> الارتفاع المستمر والعام في مستوى الأسعار</p>
        <p><b>مؤشر أسعار المستهلك (IPC - Indice des Prix à la Consommation):</b> 
        يقيس التطور الزمني لمستوى أسعار سلة من السلع والخدمات المستهلكة</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("1️⃣ حساب مؤشر أسعار المستهلك (IPC)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 صيغة IPC:</h4>
        <p style="font-size: 20px; text-align: center;">
            <b>IPC<sub>t</sub> = [Σ(P<sub>t</sub> × Q<sub>base</sub>) / Σ(P<sub>base</sub> × Q<sub>base</sub>)] × 100</b>
        </p>
        <p style="text-align: center;">حيث:</p>
        <ul>
            <li>P<sub>t</sub> = أسعار السنة الحالية</li>
            <li>P<sub>base</sub> = أسعار سنة الأساس</li>
            <li>Q<sub>base</sub> = كميات سنة الأساس (السلة الثابتة)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🧮 حاسبة IPC - مثال تطبيقي")

    st.markdown("""
    <div class="example-box">
        <p>لنفترض سلة استهلاكية تحتوي على 3 منتجات:</p>
    </div>
    """, unsafe_allow_html=True)

    # البيانات
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**أسعار وكميات سنة الأساس (2020):**")
        q1_base = st.number_input("كمية الخبز", value=100.0, key="q1_base")
        p1_base = st.number_input("سعر الخبز", value=1.0, key="p1_base")

        q2_base = st.number_input("كمية الحليب", value=50.0, key="q2_base")
        p2_base = st.number_input("سعر الحليب", value=2.0, key="p2_base")

        q3_base = st.number_input("كمية اللحم", value=20.0, key="q3_base")
        p3_base = st.number_input("سعر اللحم", value=10.0, key="p3_base")

    with col2:
        st.markdown("**أسعار السنة الحالية (2023):**")
        st.write("")  # spacing
        st.write("")
        p1_current = st.number_input("سعر الخبز الحالي", value=1.2, key="p1_current")
        st.write("")
        st.write("")
        p2_current = st.number_input("سعر الحليب الحالي", value=2.5, key="p2_current")
        st.write("")
        st.write("")
        p3_current = st.number_input("سعر اللحم الحالي", value=12.0, key="p3_current")

    # الحسابات
    cost_base = (q1_base * p1_base) + (q2_base * p2_base) + (q3_base * p3_base)
    cost_current = (q1_base * p1_current) + (q2_base * p2_current) + (q3_base * p3_current)
    ipc = (cost_current / cost_base) * 100

    st.markdown(f"""
    <div class="calculation-step">
        <h4>الحساب خطوة بخطوة:</h4>

        <p><b>الخطوة 1: تكلفة السلة في سنة الأساس</b></p>
        <p>= ({q1_base} × {p1_base}) + ({q2_base} × {p2_base}) + ({q3_base} × {p3_base})</p>
        <p>= {q1_base * p1_base} + {q2_base * p2_base} + {q3_base * p3_base}</p>
        <p>= <b>{cost_base:.2f}</b></p>

        <p><b>الخطوة 2: تكلفة نفس السلة بالأسعار الحالية</b></p>
        <p>= ({q1_base} × {p1_current}) + ({q2_base} × {p2_current}) + ({q3_base} × {p3_current})</p>
        <p>= {q1_base * p1_current} + {q2_base * p2_current} + {q3_base * p3_current}</p>
        <p>= <b>{cost_current:.2f}</b></p>

        <p><b>الخطوة 3: حساب IPC</b></p>
        <p>IPC = ({cost_current:.2f} / {cost_base:.2f}) × 100</p>
        <p><b style="font-size: 24px; color: #2E86AB;">IPC = {ipc:.2f}</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("2️⃣ حساب معدل التضخم")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 صيغة معدل التضخم:</h4>
        <p style="font-size: 20px; text-align: center;">
            <b>π<sub>t</sub> = [(IPC<sub>t</sub> - IPC<sub>t-1</sub>) / IPC<sub>t-1</sub>] × 100</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        ipc_t1 = st.number_input("IPC السنة السابقة", value=100.0, key="ipc_t1")
        ipc_t = st.number_input("IPC السنة الحالية", value=ipc, key="ipc_t")

    inflation_rate = ((ipc_t - ipc_t1) / ipc_t1) * 100

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>حساب معدل التضخم:</h4>
            <p>π = [({ipc_t:.2f} - {ipc_t1:.2f}) / {ipc_t1:.2f}] × 100</p>
            <p><b style="font-size: 24px; color: #A23B72;">π = {inflation_rate:.2f}%</b></p>
        </div>
        """, unsafe_allow_html=True)

    # تصنيف التضخم
    if inflation_rate < 3:
        st.success(f"✅ **تضخم زاحف (معتدل):** {inflation_rate:.2f}% < 3%")
    elif 3 <= inflation_rate < 10:
        st.warning(f"⚠️ **تضخم معتدل:** 3% ≤ {inflation_rate:.2f}% < 10%")
    elif 10 <= inflation_rate < 50:
        st.error(f"❌ **تضخم جامح:** 10% ≤ {inflation_rate:.2f}% < 50%")
    else:
        st.error(f"🔥 **تضخم مفرط:** {inflation_rate:.2f}% ≥ 50%")

    st.markdown("---")

    st.subheader("3️⃣ القوة الشرائية (Pouvoir d'achat)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 صيغة القوة الشرائية:</h4>
        <p style="font-size: 20px; text-align: center;">
            <b>PA<sub>t</sub> = Revenu<sub>nominal</sub> / (1 + π)<sup>n</sup></b>
        </p>
        <p style="text-align: center;">حيث:</p>
        <ul>
            <li>PA = القوة الشرائية</li>
            <li>π = معدل التضخم السنوي</li>
            <li>n = عدد السنوات</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🧮 حاسبة القوة الشرائية")

    col1, col2 = st.columns(2)

    with col1:
        montant_initial = st.number_input("المبلغ الأولي", value=1000.0, step=100.0, key="montant_pa")
        taux_inflation = st.number_input("معدل التضخم السنوي (%)", value=3.0, step=0.5, key="taux_inf_pa")
        annees = st.slider("عدد السنوات", 1, 30, 10, key="annees_pa")

    pa_finale = montant_initial / ((1 + taux_inflation/100) ** annees)
    perte = ((montant_initial - pa_finale) / montant_initial) * 100

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>الحساب:</h4>
            <p>PA = {montant_initial:.2f} / (1 + {taux_inflation/100:.3f})<sup>{annees}</sup></p>
            <p>PA = {montant_initial:.2f} / {(1 + taux_inflation/100) ** annees:.4f}</p>
            <p><b style="font-size: 20px; color: #A23B72;">PA = {pa_finale:.2f}</b></p>
            <p style="margin-top: 15px;"><b>نسبة الفقدان:</b> {perte:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # رسم بياني
    years_list = list(range(annees + 1))
    values = [montant_initial / ((1 + taux_inflation/100) ** y) for y in years_list]

    fig_pa = go.Figure()
    fig_pa.add_trace(go.Scatter(
        x=years_list, y=values,
        mode='lines+markers',
        fill='tozeroy',
        name='القوة الشرائية',
        line=dict(color='#A23B72', width=3)
    ))

    fig_pa.update_layout(
        title=f"تآكل القوة الشرائية بمعدل تضخم {taux_inflation}%",
        xaxis_title="السنوات",
        yaxis_title="القوة الشرائية",
        height=400
    )

    st.plotly_chart(fig_pa, use_container_width=True)

# ========== البطالة ==========
elif menu == "👥 البطالة ومعدل المشاركة":
    st.header("👥 البطالة ومعدل المشاركة")

    st.markdown("""
    <div class="info-box">
        <h3>📖 التعريف حسب BIT (من الكتاب - صفحة 41-42)</h3>
        <p><b>العاطل عن العمل (Chômeur):</b> شخص في سن العمل (15 سنة فأكثر) يستوفي ثلاثة شروط:</p>
        <ol>
            <li>بدون عمل (لم يعمل حتى ساعة واحدة في الأسبوع المرجعي)</li>
            <li>متاح للعمل خلال 15 يوماً</li>
            <li>يبحث بنشاط عن عمل</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("1️⃣ معدل البطالة (Taux de chômage)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة (من الكتاب - صفحة 42):</h4>
        <p style="font-size: 22px; text-align: center;">
            <b>u = (Nombre de chômeurs / Population active totale) × 100</b>
        </p>
        <p style="font-size: 20px; text-align: center;">
            <b>معدل البطالة = (عدد العاطلين / القوى العاملة الكلية) × 100</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="law-box">
        <h4>📚 تعريف القوى العاملة:</h4>
        <p style="font-size: 18px; text-align: center;">
            <b>Population active = Nombre de chômeurs + Nombre d'employés</b>
        </p>
        <p style="font-size: 18px; text-align: center;">
            <b>القوى العاملة = عدد العاطلين + عدد العاملين</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🧮 حاسبة معدل البطالة")

    col1, col2 = st.columns(2)

    with col1:
        employes = st.number_input("عدد العاملين (بالمليون)", value=25.0, step=0.5, key="employes")
        chomeurs = st.number_input("عدد العاطلين (بالمليون)", value=2.5, step=0.1, key="chomeurs")
        population_totale = st.number_input("إجمالي السكان (بالمليون)", value=40.0, step=1.0, key="pop_totale")

    population_active = employes + chomeurs
    taux_chomage = (chomeurs / population_active) * 100

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>الحساب خطوة بخطوة:</h4>

            <p><b>الخطوة 1: القوى العاملة</b></p>
            <p>Population active = {employes:.2f} + {chomeurs:.2f}</p>
            <p>= <b>{population_active:.2f} مليون</b></p>

            <p><b>الخطوة 2: معدل البطالة</b></p>
            <p>u = ({chomeurs:.2f} / {population_active:.2f}) × 100</p>
            <p><b style="font-size: 24px; color: #F18F01;">u = {taux_chomage:.2f}%</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("2️⃣ معدل المشاركة / النشاط (Taux de participation)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة (من الكتاب - صفحة 42):</h4>
        <p style="font-size: 20px; text-align: center;">
            <b>Taux de participation = (Population active / Population en âge de travailler) × 100</b>
        </p>
        <p style="font-size: 18px; text-align: center;">
            <b>معدل المشاركة = (القوى العاملة / السكان في سن العمل) × 100</b>
        </p>
        <p style="text-align: center;">السكان في سن العمل = 15-64 سنة</p>
    </div>
    """, unsafe_allow_html=True)

    taux_participation = (population_active / population_totale) * 100

    st.markdown(f"""
    <div class="calculation-step">
        <h4>حساب معدل المشاركة:</h4>
        <p>Taux de participation = ({population_active:.2f} / {population_totale:.2f}) × 100</p>
        <p><b style="font-size: 24px; color: #2E86AB;">= {taux_participation:.2f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("3️⃣ معدل التشغيل (Taux d'emploi)")

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة:</h4>
        <p style="font-size: 20px; text-align: center;">
            <b>Taux d'emploi = (Nombre d'employés / Population en âge de travailler) × 100</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    taux_emploi = (employes / population_totale) * 100

    st.markdown(f"""
    <div class="calculation-step">
        <h4>حساب معدل التشغيل:</h4>
        <p>Taux d'emploi = ({employes:.2f} / {population_totale:.2f}) × 100</p>
        <p><b style="font-size: 24px; color: #4CAF50;">= {taux_emploi:.2f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

    # ملخص جميع المؤشرات
    st.subheader("📊 ملخص المؤشرات")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("معدل البطالة", f"{taux_chomage:.2f}%")
    with col2:
        st.metric("معدل المشاركة", f"{taux_participation:.2f}%")
    with col3:
        st.metric("معدل التشغيل", f"{taux_emploi:.2f}%")

    # رسم بياني توضيحي
    fig_emploi = go.Figure(data=[
        go.Bar(name='العاملون', x=['السكان'], y=[employes], marker_color='#4CAF50'),
        go.Bar(name='العاطلون', x=['السكان'], y=[chomeurs], marker_color='#F18F01'),
        go.Bar(name='خارج القوى العاملة', x=['السكان'], y=[population_totale - population_active], marker_color='#9E9E9E')
    ])

    fig_emploi.update_layout(
        barmode='stack',
        title='توزيع السكان حسب حالة التشغيل',
        yaxis_title='عدد السكان (مليون)',
        height=400
    )

    st.plotly_chart(fig_emploi, use_container_width=True)

# ========== قاعدة 70 ==========
elif menu == "🔢 قاعدة 70":
    st.header("🔢 قاعدة 70 - حساب سنوات المضاعفة")

    st.markdown("""
    <div class="info-box">
        <h3>📖 قاعدة 70 (Règle de 70)</h3>
        <p>قاعدة تقريبية لحساب عدد السنوات اللازمة لمضاعفة قيمة متغير ينمو بمعدل ثابت.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        <h4>📐 الصيغة:</h4>
        <p style="font-size: 24px; text-align: center;">
            <b>عدد سنوات المضاعفة ≈ 70 / معدل النمو السنوي</b>
        </p>
        <p style="font-size: 22px; text-align: center;">
            <b>n ≈ 70 / g</b>
        </p>
        <p style="text-align: center;">حيث:</p>
        <ul>
            <li>n = عدد السنوات للمضاعفة</li>
            <li>g = معدل النمو السنوي (%)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🧮 حاسبة قاعدة 70")

    col1, col2 = st.columns([1, 1])

    with col1:
        growth_rate_70 = st.slider(
            "معدل النمو السنوي (%)",
            min_value=0.5,
            max_value=10.0,
            value=3.0,
            step=0.5,
            key="growth_70"
        )

    years_to_double = 70 / growth_rate_70

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>الحساب:</h4>
            <p style="font-size: 20px;">n = 70 / {growth_rate_70}</p>
            <p><b style="font-size: 28px; color: #2E86AB;">n ≈ {years_to_double:.1f} سنة</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.info(f"""
    📊 **التفسير:**

    بمعدل نمو **{growth_rate_70}%** سنوياً، سيتضاعف PIB في حوالي **{years_to_double:.1f} سنة**.

    **مثال:** إذا كان PIB الحالي 100 مليار، سيصبح 200 مليار بعد {years_to_double:.1f} سنة.
    """)

    st.markdown("---")

    # أمثلة مقارنة
    st.subheader("📊 مقارنة معدلات النمو المختلفة")

    growth_rates = [1, 2, 3, 4, 5, 7, 10]
    doubling_times = [70/g for g in growth_rates]

    comparison_df = pd.DataFrame({
        'معدل النمو (%)': growth_rates,
        'سنوات المضاعفة': [f"{dt:.1f}" for dt in doubling_times]
    })

    st.table(comparison_df)

    # رسم بياني
    fig_70 = go.Figure()

    fig_70.add_trace(go.Scatter(
        x=growth_rates,
        y=doubling_times,
        mode='lines+markers',
        name='قاعدة 70',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=10)
    ))

    fig_70.update_layout(
        title="العلاقة بين معدل النمو وسنوات المضاعفة",
        xaxis_title="معدل النمو السنوي (%)",
        yaxis_title="عدد السنوات للمضاعفة",
        height=500,
        template='plotly_white'
    )

    st.plotly_chart(fig_70, use_container_width=True)

    st.markdown("""
    <div class="law-box">
        <h4>📚 ملاحظات مهمة:</h4>
        <ul>
            <li>قاعدة 70 هي قاعدة تقريبية، وليست دقيقة 100%</li>
            <li>تعمل بشكل جيد للمعدلات بين 1% و 10%</li>
            <li>يمكن استخدامها لأي متغير ينمو بمعدل ثابت (PIB، السكان، الاستثمار، ...)</li>
            <li>بدائل: قاعدة 69.3 (أكثر دقة) أو قاعدة 72 (أسهل للحساب)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # تطبيق عملي
    st.subheader("💡 تطبيق عملي: مضاعفة PIB")

    col1, col2 = st.columns(2)

    with col1:
        pib_initial_70 = st.number_input("PIB الأولي (مليار)", value=100.0, step=10.0, key="pib_init_70")
        growth_application = st.number_input("معدل النمو (%)", value=3.0, step=0.5, key="growth_app")

    years_double_app = 70 / growth_application
    pib_final_70 = pib_initial_70 * 2

    with col2:
        st.markdown(f"""
        <div class="calculation-step">
            <h4>النتيجة:</h4>
            <p>عدد السنوات = 70 / {growth_application} ≈ <b>{years_double_app:.1f} سنة</b></p>
            <p style="margin-top: 15px;">PIB سيتطور من:</p>
            <p><b>{pib_initial_70:.2f} مليار</b> → <b>{pib_final_70:.2f} مليار</b></p>
        </div>
        """, unsafe_allow_html=True)

    # محاكاة التطور
    years_simulation = int(years_double_app * 2)
    years_list = list(range(years_simulation + 1))
    pib_values = [pib_initial_70 * ((1 + growth_application/100) ** y) for y in years_list]

    fig_sim = go.Figure()

    fig_sim.add_trace(go.Scatter(
        x=years_list,
        y=pib_values,
        mode='lines+markers',
        name='PIB',
        line=dict(color='#2E86AB', width=3)
    ))

    # خط المضاعفة
    fig_sim.add_hline(
        y=pib_final_70,
        line_dash="dash",
        line_color="red",
        annotation_text=f"المضاعفة ({pib_final_70:.0f})"
    )

    # نقطة المضاعفة
    fig_sim.add_vline(
        x=years_double_app,
        line_dash="dash",
        line_color="green",
        annotation_text=f"{years_double_app:.1f} سنة"
    )

    fig_sim.update_layout(
        title=f"تطور PIB بمعدل نمو {growth_application}%",
        xaxis_title="السنوات",
        yaxis_title="PIB (مليار)",
        height=500
    )

    st.plotly_chart(fig_sim, use_container_width=True)

# ========== تحميل البيانات ==========
elif menu == "📥 تحميل البيانات":
    st.header("📥 تحميل البيانات")

    st.info("هذا القسم يسمح بتحميل بيانات حقيقية. راجع الكود السابق لتفاصيل التحميل.")

# تذييل
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><b>📚 جميع الصيغ والأمثلة مستمدة من كتاب الاقتصاد الكلي</b></p>
    <p>Macroéconomie - Licence | Dunod</p>
</div>
""", unsafe_allow_html=True)
