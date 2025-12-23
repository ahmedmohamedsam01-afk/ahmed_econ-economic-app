import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import requests
from datetime import datetime
import zipfile
import tempfile
import os

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="الاقتصاد الكلي التفاعلي - منهجية تعليمية",
    page_icon="📚",
    layout="wide"
)

# CSS مخصص لتحسين العرض
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #4a6491 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 10px;
        font-family: 'Arial', sans-serif;
    }
    .main-header p {
        color: #ecf0f1;
        text-align: center;
        font-size: 1.2rem;
    }
    .chapter-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #3498db;
        transition: all 0.3s ease;
    }
    .chapter-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .formula-box {
        background: #e8f4fc;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2980b9;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
    }
    .exercise-box {
        background: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ffc107;
        margin: 20px 0;
    }
    .data-source {
        background: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
<div class="main-header">
    <h1>📚 الاقتصاد الكلي التفاعلي</h1>
    <p>تطبيق تعليمي يعتمد على منهجية الكتاب مع إمكانية تحميل بيانات حقيقية</p>
</div>
""", unsafe_allow_html=True)

# شريط جانبي للتحكم
st.sidebar.header("⚙️ إعدادات التطبيق")

# اختيار الفصل
chapter = st.sidebar.radio(
    "📖 اختر الفصل للدراسة:",
    [
        "الفصل 1: المفاهيم الأساسية",
        "الفصل 2: الناتج المحلي الإجمالي", 
        "الفصل 3: التضخم والبطالة",
        "الفصل 4: قانون أوكون",
        "الفصل 5: العلاقات الاقتصادية",
        "🎯 التمارين العملية"
    ],
    index=0
)

# قسم تحميل البيانات في الشريط الجانبي
st.sidebar.header("📥 تحميل البيانات")

# خيارات تحميل البيانات
data_source = st.sidebar.selectbox(
    "اختر مصدر البيانات:",
    [
        "بيانات محاكاة (تعليمية)",
        "تحميل ملف Excel",
        "تحميل ملف CSV",
        "بيانات من الويب (منظمات دولية)",
        "عينة بيانات فرنسا (مضمنة)"
    ],
    index=0
)

# ========== دالات تحميل البيانات ==========
def load_france_sample_data():
    """تحميل عينة بيانات فرنسا"""
    # بيانات نمو الناتج المحلي لفرنسا (سنوات حديثة)
    gdp_data = {
        "السنة": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        "الناتج_الحقيقي_مليار_يورو": [2194.2, 2219.8, 2291.3, 2346.2, 2388.1, 2289.8, 2415.6, 2489.3, 2542.1],
        "الناتج_الاسمي_مليار_يورو": [2194.2, 2231.1, 2345.2, 2424.6, 2491.8, 2396.8, 2564.3, 2718.5, 2865.2],
        "معدل_النمو_٪": [1.1, 1.1, 2.3, 1.9, 1.8, -7.9, 6.8, 2.5, 0.9],
        "التضخم_٪": [0.1, 0.3, 1.2, 2.1, 1.3, 0.5, 1.6, 5.2, 4.9],
        "البطالة_٪": [10.4, 10.1, 9.4, 9.1, 8.4, 8.0, 7.9, 7.3, 7.1]
    }
    
    df_gdp = pd.DataFrame(gdp_data)
    
    # بيانات مكونات الناتج المحلي 2023
    components_data = {
        "المكون": ["الاستهلاك", "الاستثمار", "الإنفاق_الحكومي", "الصادرات", "الواردات"],
        "القيمة_مليار_يورو": [1345.2, 652.3, 615.8, 745.6, 822.4],
        "النسبة_٪": [53.0, 25.7, 24.2, 29.3, 32.3]
    }
    
    df_components = pd.DataFrame(components_data)
    
    # بيانات القطاعات الاقتصادية
    sectors_data = {
        "القطاع": ["الخدمات", "الصناعة", "البناء", "الزراعة"],
        "المساهمة_في_الناتج_٪": [70.2, 13.5, 5.8, 1.5],
        "نمو_2023_٪": [1.2, -0.8, 0.5, -2.1]
    }
    
    df_sectors = pd.DataFrame(sectors_data)
    
    return {
        "الناتج_المحلي": df_gdp,
        "مكونات_الناتج": df_components,
        "القطاعات": df_sectors
    }

def download_worldbank_data():
    """تحميل بيانات من البنك الدولي"""
    try:
        st.sidebar.info("جارٍ تحميل بيانات البنك الدولي...")
        
        # مثال لبيانات الناتج المحلي العالمي
        countries = ["فرنسا", "ألمانيا", "إيطاليا", "إسبانيا", "المملكة المتحدة"]
        gdp_data = []
        
        for country in countries:
            base_gdp = np.random.uniform(1000, 4000)
            for year in range(2018, 2024):
                growth = np.random.uniform(-2, 4)
                if year == 2020:  # تأثير COVID
                    growth = np.random.uniform(-8, -4)
                
                gdp = base_gdp * (1 + growth/100) ** (year - 2018)
                gdp_data.append({
                    "البلد": country,
                    "السنة": year,
                    "الناتج_المحلي_مليار_دولار": round(gdp, 1)
                })
        
        df_worldbank = pd.DataFrame(gdp_data)
        
        st.sidebar.success("تم تحميل بيانات البنك الدولي")
        return df_worldbank
        
    except Exception as e:
        st.sidebar.error(f"خطأ في تحميل البيانات: {str(e)}")
        return None

def handle_uploaded_file(uploaded_file, file_type):
    """معالجة الملفات المرفوعة"""
    try:
        if file_type == "Excel":
            df = pd.read_excel(uploaded_file)
        elif file_type == "CSV":
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        
        # تحليل محتوى الملف تلقائياً
        file_info = {
            "عدد_الصفوف": df.shape[0],
            "عدد_الأعمدة": df.shape[1],
            "الأعمدة": df.columns.tolist(),
            "عينة_من_البيانات": df.head()
        }
        
        return df, file_info
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {str(e)}")
        return None, None

# ========== معالجة اختيار مصدر البيانات ==========
uploaded_data = None
data_info = None

if data_source == "تحميل ملف Excel":
    uploaded_file = st.sidebar.file_uploader(
        "📤 اختر ملف Excel",
        type=['xlsx', 'xls']
    )
    if uploaded_file is not None:
        uploaded_data, data_info = handle_uploaded_file(uploaded_file, "Excel")

elif data_source == "تحميل ملف CSV":
    uploaded_file = st.sidebar.file_uploader(
        "📤 اختر ملف CSV",
        type=['csv']
    )
    if uploaded_file is not None:
        uploaded_data, data_info = handle_uploaded_file(uploaded_file, "CSV")

elif data_source == "بيانات من الويب (منظمات دولية)":
    if st.sidebar.button("🌍 تحميل بيانات البنك الدولي"):
        uploaded_data = download_worldbank_data()
        if uploaded_data is not None:
            data_info = {
                "عدد_الصفوف": uploaded_data.shape[0],
                "عدد_الأعمدة": uploaded_data.shape[1],
                "الأعمدة": uploaded_data.columns.tolist()
            }

elif data_source == "عينة بيانات فرنسا (مضمنة)":
    france_data = load_france_sample_data()
    uploaded_data = france_data["الناتج_المحلي"]
    data_info = {
        "عدد_الصفوف": uploaded_data.shape[0],
        "عدد_الأعمدة": uploaded_data.shape[1],
        "الأعمدة": uploaded_data.columns.tolist()
    }

# ========== الفصل 1: المفاهيم الأساسية ==========
if chapter == "الفصل 1: المفاهيم الأساسية":
    st.header("📖 الفصل 1: المفاهيم الأساسية للاقتصاد الكلي")
    
    # عرض بيانات محملة إذا كانت موجودة
    if uploaded_data is not None and data_info:
        st.sidebar.success(f"✅ تم تحميل {data_info['عدد_الصفوف']} صف و {data_info['عدد_الأعمدة']} عمود")
        
        with st.expander("👁️ عرض البيانات المحملة"):
            st.write("**معلومات عن البيانات:**")
            st.json(data_info)
            st.write("**عينة من البيانات:**")
            st.dataframe(uploaded_data.head())
    
    st.markdown("""
    ## 🎯 الهدف التعليمي
    فهم الفرق بين الاقتصاد الكلي والاقتصاد الجزئي وإدراك أهمية النهج الشمولي في التحليل الاقتصادي.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chapter-box">', unsafe_allow_html=True)
        st.subheader("🎯 الاقتصاد الكلي")
        st.markdown("""
        **تعريف:** دراسة الظواهر الاقتصادية على مستوى الاقتصاد ككل
        
        **يركز على:**
        - الناتج المحلي الإجمالي (GDP)
        - التضخم
        - البطالة
        - النمو الاقتصادي
        - السياسات الاقتصادية الكلية
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # مخطط توضيحي
        if uploaded_data is not None and 'الناتج_الحقيقي_مليار_يورو' in uploaded_data.columns:
            fig_macro = px.line(
                uploaded_data,
                x="السنة",
                y="الناتج_الحقيقي_مليار_يورو",
                title="تطور الناتج المحلي (مثال واقعي)",
                markers=True
            )
            st.plotly_chart(fig_macro, use_container_width=True)
    
    with col2:
        st.markdown('<div class="chapter-box">', unsafe_allow_html=True)
        st.subheader("🔬 الاقتصاد الجزئي")
        st.markdown("""
        **تعريف:** دراسة سلوك الوحدات الاقتصادية الفردية
        
        **يركز على:**
        - سلوك المستهلكين
        - قرارات المنتجين
        - تحديد الأسعار في الأسواق الفردية
        - كفاءة تخصيص الموارد
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # مثال محاكاة للاقتصاد الجزئي
        prices = np.linspace(1, 10, 20)
        demand = 100 - 8 * prices
        supply = 20 + 5 * prices
        
        fig_micro = go.Figure()
        fig_micro.add_trace(go.Scatter(x=prices, y=demand, name="الطلب", line=dict(color='blue')))
        fig_micro.add_trace(go.Scatter(x=prices, y=supply, name="العرض", line=dict(color='red')))
        fig_micro.update_layout(
            title="منحنى العرض والطلب (اقتصاد جزئي)",
            xaxis_title="السعر",
            yaxis_title="الكمية"
        )
        st.plotly_chart(fig_micro, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🏊 مثال توضيحي: سباحة السباحين")
    
    st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown("""
    **المثال كما ورد في الكتاب (الصفحة 18-19):**
    
    تخيل سباق سباحة (100 متر حرة) بـ 8 سباحين:
    
    1. **النهج الجزئي**: مراقبة سباح واحد بالمنظار (كاميرا منعزلة)
    2. **النهج الكلي**: مشاهدة السباق بالعين المجردة
    
    **التطبيق العملي:**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # محاكاة تفاعلية
    col1, col2 = st.columns(2)
    
    with col1:
        n_swimmers = st.slider("عدد السباحين في السباق", 3, 8, 5)
        
        # محاكاة أداء السباحين
        swimmers = [f"السباح {i+1}" for i in range(n_swimmers)]
        speeds = np.random.uniform(1.5, 2.5, n_swimmers)
        times = 100 / speeds
        
        df_swim = pd.DataFrame({
            "السباح": swimmers,
            "السرعة (م/ث)": speeds,
            "الزمن (ثانية)": times
        }).sort_values("الزمن (ثانية)")
        
        st.dataframe(df_swim.style.format({
            "السرعة (م/ث)": "{:.2f}",
            "الزمن (ثانية)": "{:.2f}"
        }), use_container_width=True)
    
    with col2:
        # رسم بياني للنتائج
        fig_swim = px.bar(
            df_swim,
            x="السباح",
            y="الزمن (ثانية)",
            color="السرعة (م/ث)",
            title="نتائج السباق (النهج الكلي)",
            color_continuous_scale="Viridis"
        )
        fig_swim.update_layout(height=400)
        st.plotly_chart(fig_swim, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🤔 المفارقة الأساسية: مفارقة الادخار")
    
    st.markdown('<div class="formula-box">', unsafe_allow_html=True)
    st.markdown("""
    **كما ورد في الكتاب (الصفحة 19):**
    
    > "إذا توقع الأسر أن الوضع الاقتصادي سيتدهور، فسيقللون من إنفاقهم ويزيدون من ادخارهم. 
    > لكن هذا التصرف الفردي العقلاني يؤدي إلى حلقة مفرغة..."
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # محاكاة مفارقة الادخار
    st.subheader("🔄 محاكاة تفاعلية لمفارقة الادخار")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        initial_consumption = st.number_input("الاستهلاك الأولي (مليار يورو)", 1000, 2000, 1500)
    
    with col2:
        savings_rate = st.slider("معدل الادخار (%)", 10, 40, 20)
    
    with col3:
        economic_outlook = st.selectbox("توقعات الأسر", ["متفائلة جداً", "متفائلة", "محايدة", "متشائمة", "متشائمة جداً"])
    
    # حساب التأثيرات
    outlook_multiplier = {
        "متفائلة جداً": 1.2,
        "متفائلة": 1.1,
        "محايدة": 1.0,
        "متشائمة": 0.9,
        "متشائمة جداً": 0.8
    }
    
    new_consumption = initial_consumption * outlook_multiplier[economic_outlook]
    consumption_change = new_consumption - initial_consumption
    
    # تأثير مضاعف الإنفاق
    spending_multiplier = 1.5  # مبسط
    gdp_effect = consumption_change * spending_multiplier
    
    # تأثير على التوظيف (تقريبي)
    employment_effect = gdp_effect * 0.001  # كل مليار يورو يخلق 1000 وظيفة تقريباً
    
    # عرض النتائج
    st.markdown("### 📊 نتائج المحاكاة")
    
    metrics_cols = st.columns(4)
    
    with metrics_cols[0]:
        st.metric("التغير في الاستهلاك", f"{consumption_change:+.1f} مليار")
    
    with metrics_cols[1]:
        st.metric("تأثير على الناتج المحلي", f"{gdp_effect:+.1f} مليار")
    
    with metrics_cols[2]:
        st.metric("تأثير على التوظيف", f"{employment_effect:+.0f} ألف وظيفة")
    
    with metrics_cols[3]:
        paradox = "نعم" if (economic_outlook in ["متشائمة", "متشائمة جداً"] and gdp_effect < 0) else "لا"
        st.metric("هل تحدث المفارقة؟", paradox)
    
    st.warning("""
    **الخلاصة التعليمية:**
    - النهج الكلي ≠ مجموع النهج الجزئي
    - "الكل أكبر من مجموع الأجزاء" (أرسطو)
    - التفاعلات بين القرارات الفردية تولد ظواهر كلية جديدة
    """)

# ========== الفصل 2: الناتج المحلي الإجمالي ==========
elif chapter == "الفصل 2: الناتج المحلي الإجمالي":
    st.header("📊 الفصل 2: الناتج المحلي الإجمالي - القياس والتحليل")
    
    # قسم بيانات حقيقية إذا تم تحميلها
    if uploaded_data is not None:
        st.markdown('<div class="data-source">', unsafe_allow_html=True)
        st.subheader("📊 البيانات المحملة")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**عينة من البيانات:**")
            st.dataframe(uploaded_data.head())
        
        with col2:
            st.write("**إحصائيات أساسية:**")
            st.metric("عدد السنوات", len(uploaded_data))
            if 'الناتج_الحقيقي_مليار_يورو' in uploaded_data.columns:
                latest_gdp = uploaded_data['الناتج_الحقيقي_مليار_يورو'].iloc[-1]
                growth_rate = ((latest_gdp / uploaded_data['الناتج_الحقيقي_مليار_يورو'].iloc[-2]) - 1) * 100
                st.metric("آخر قيمة للناتج المحلي", f"{latest_gdp:.1f} مليار")
                st.metric("آخر معدل نمو", f"{growth_rate:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎯 الهدف التعليمي
    فهم طرق حساب الناتج المحلي الإجمالي الثلاث والتمييز بين الناتج الاسمي والناتج الحقيقي.
    """)
    
    st.subheader("📋 الطرق الثلاث لحساب الناتج المحلي الإجمالي")
    
    # عرض طرق الحساب في تبويبات
    tab1, tab2, tab3 = st.tabs(["طريقة الإنتاج", "طريقة الإنفاق", "طريقة الدخل"])
    
    with tab1:
        st.markdown('<div class="chapter-box">', unsafe_allow_html=True)
        st.subheader("🏭 طريقة الإنتاج (القيمة المضافة)")
        st.markdown("""
        **التعريف:** مجموع القيم المضافة الناتجة في الاقتصاد
        
        **المعادلة:**
        ```
        الناتج المحلي = Σ (القيمة المضافة لكل قطاع)
        القيمة المضافة = الإنتاج - المستهلكات الوسيطة
        ```
        
        **مثال من الكتاب (الصفحة 26-27):**
        - الصناعة المعدنية: 1000 - 0 = 1000 مليون يورو
        - الصناعة السيارات: 2000 - 1000 = 1000 مليون يورو
        - **المجموع: 2000 مليون يورو**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # آلة حاسبة للقيمة المضافة
        st.subheader("🧮 آلة حاسبة القيمة المضافة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            production = st.number_input("قيمة الإنتاج (مليون يورو)", 0, 5000, 1000)
        
        with col2:
            intermediate = st.number_input("قيمة المستهلكات الوسيطة (مليون يورو)", 0, 5000, 500)
        
        value_added = production - intermediate
        
        st.metric("القيمة المضافة", f"{value_added} مليون يورو")
    
    with tab2:
        st.markdown('<div class="chapter-box">', unsafe_allow_html=True)
        st.subheader("💰 طريقة الإنفاق")
        st.markdown("""
        **التعريف:** قيمة السلع والخدمات النهائية المنتجة
        
        **المعادلة:**
        ```
        الناتج المحلي = الاستهلاك + الاستثمار + الإنفاق الحكومي + الصادرات الصافية
        Y = C + I + G + (X - M)
        ```
        
        **مثال من الكتاب (الصفحة 36):**
        - الاستهلاك (C): 1268.5 مليار يورو
        - الاستثمار (I): 537.9 مليار يورو
        - الإنفاق الحكومي (G): 550.9 مليار يورو
        - الصادرات الصافية (NX): -18.3 مليار يورو
        - **المجموع: 2339 مليار يورو**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # آلة حاسبة طريقة الإنفاق
        st.subheader("🧮 آلة حاسبة طريقة الإنفاق")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            C = st.number_input("الاستهلاك (C)", 0, 3000, 1268)
        
        with col2:
            I = st.number_input("الاستثمار (I)", 0, 3000, 538)
        
        with col3:
            G = st.number_input("الإنفاق الحكومي (G)", 0, 3000, 551)
        
        with col4:
            X = st.number_input("الصادرات (X)", 0, 3000, 737)
            M = st.number_input("الواردات (M)", 0, 3000, 755)
        
        NX = X - M
        GDP_expenditure = C + I + G + NX
        
        st.metric("الناتج المحلي الإجمالي (طريقة الإنفاق)", f"{GDP_expenditure} مليار يورو")
    
    with tab3:
        st.markdown('<div class="chapter-box">', unsafe_allow_html=True)
        st.subheader("💼 طريقة الدخل")
        st.markdown("""
        **التعريف:** مجموع مداخيل عوامل الإنتاج
        
        **المعادلة:**
        ```
        الناتج المحلي = الأجور + الأرباح + الفوائد + الإيجارات + الضرائب
        ```
        
        **مثال من الكتاب (الصفحة 28):**
        - الأجور: 500 مليون يورو
        - الفوائد: 40 مليون يورو
        - الأرباح: 1460 مليون يورو
        - **المجموع: 2000 مليون يورو**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # آلة حاسبة طريقة الدخل
        st.subheader("🧮 آلة حاسبة طريقة الدخل")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            wages = st.number_input("الأجور", 0, 2000, 500)
        
        with col2:
            profits = st.number_input("الأرباح", 0, 2000, 1460)
        
        with col3:
            interests = st.number_input("الفوائد", 0, 200, 40)
        
        with col4:
            rents = st.number_input("الإيجارات", 0, 200, 50)
            taxes = st.number_input("الضرائب", 0, 500, 100)
        
        GDP_income = wages + profits + interests + rents + taxes
        
        st.metric("الناتج المحلي الإجمالي (طريقة الدخل)", f"{GDP_income} مليون يورو")
    
    st.markdown("---")
    
    st.subheader("💰 التمييز بين الناتج الاسمي والناتج الحقيقي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("""
        **الناتج الاسمي:**
        ```
        الناتج الاسمي = Σ (الكمية × السعر الحالي)
        ```
        
        **الناتج الحقيقي:**
        ```
        الناتج الحقيقي = Σ (الكمية × السعر الأساسي)
        ```
        
        **معادلة مُعَدِّل الناتج المحلي:**
        ```
        مُعَدِّل الناتج المحلي = الناتج الاسمي ÷ الناتج الحقيقي
        ```
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # محاكاة بيانات الناتج الاسمي والحقيقي
        years = list(range(2015, 2024))
        
        # إنشاء بيانات محاكاة
        base_real_gdp = 2000  # مليار يورو في 2015
        
        simulated_data = []
        current_real = base_real_gdp
        current_nominal = base_real_gdp
        
        for i, year in enumerate(years):
            # نمو حقيقي عشوائي (مع إضافة تأثير COVID في 2020)
            if year == 2020:
                real_growth = np.random.uniform(-8, -5)
            else:
                real_growth = np.random.uniform(0.5, 3.5)
            
            # تضخم عشوائي
            inflation = np.random.uniform(0.5, 3.5)
            if year >= 2022:  # تضخم مرتفع في السنوات الأخيرة
                inflation = np.random.uniform(4, 7)
            
            # حساب القيم
            current_real *= (1 + real_growth/100)
            current_nominal = current_real * (1 + inflation/100)
            
            simulated_data.append({
                "السنة": year,
                "الناتج_الحقيقي": current_real,
                "الناتج_الاسمي": current_nominal,
                "معدل_النمو_الحقيقي": real_growth,
                "التضخم": inflation
            })
        
        df_simulated = pd.DataFrame(simulated_data)
        
        # رسم بياني للمقارنة
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Scatter(
            x=df_simulated["السنة"],
            y=df_simulated["الناتج_الحقيقي"],
            name="الناتج الحقيقي",
            line=dict(color='green', width=3)
        ))
        fig_comparison.add_trace(go.Scatter(
            x=df_simulated["السنة"],
            y=df_simulated["الناتج_الاسمي"],
            name="الناتج الاسمي",
            line=dict(color='blue', width=3)
        ))
        
        fig_comparison.update_layout(
            title="مقارنة الناتج الاسمي والحقيقي",
            xaxis_title="السنة",
            yaxis_title="مليار يورو",
            height=400
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # إذا كانت هناك بيانات حقيقية، إجراء تحليل إضافي
    if uploaded_data is not None and 'الناتج_الحقيقي_مليار_يورو' in uploaded_data.columns:
        st.markdown("---")
        st.subheader("📈 تحليل بيانات الناتج المحلي الحقيقية")
        
        # تحليل الاتجاه
        from scipy import stats
        
        # تحليل الاتجاه الخطي
        x = np.arange(len(uploaded_data))
        y = uploaded_data['الناتج_الحقيقي_مليار_يورو'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        trend_line = intercept + slope * x
        
        # إنشاء الشكل
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=uploaded_data["السنة"],
            y=uploaded_data["الناتج_الحقيقي_مليار_يورو"],
            name="الناتج الحقيقي",
            mode='lines+markers',
            line=dict(color='blue', width=2)
        ))
        fig_trend.add_trace(go.Scatter(
            x=uploaded_data["السنة"],
            y=trend_line,
            name="الاتجاه العام",
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig_trend.update_layout(
            title="الاتجاه العام للناتج المحلي الحقيقي",
            xaxis_title="السنة",
            yaxis_title="مليار يورو",
            height=400
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # عرض إحصائيات الاتجاه
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_growth = ((y[-1] / y[0]) ** (1/len(y)) - 1) * 100
            st.metric("متوسط النمو السنوي", f"{avg_growth:.2f}%")
        
        with col2:
            st.metric("ميل الاتجاه", f"{slope:.2f} مليار/سنة")
        
        with col3:
            st.metric("معامل التحديد (R²)", f"{r_value**2:.3f}")

# ========== الفصل 3: التضخم والبطالة ==========
elif chapter == "الفصل 3: التضخم والبطالة":
    st.header("💰 الفصل 3: التضخم والبطالة - القياس والتحليل")
    
    st.markdown("""
    ## 🎯 الهدف التعليمي
    فهم كيفية قياس التضخم والبطالة وتحليل العلاقة بينهما.
    """)
    
    # عرض بيانات محملة إذا كانت موجودة
    if uploaded_data is not None:
        with st.expander("📊 عرض بيانات التضخم والبطالة"):
            st.dataframe(uploaded_data)
            
            # إذا كانت البيانات تحتوي على معلومات التضخم والبطالة
            if 'التضخم_٪' in uploaded_data.columns and 'البطالة_٪' in uploaded_data.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    avg_inflation = uploaded_data['التضخم_٪'].mean()
                    st.metric("متوسط التضخم", f"{avg_inflation:.2f}%")
                
                with col2:
                    avg_unemployment = uploaded_data['البطالة_٪'].mean()
                    st.metric("متوسط البطالة", f"{avg_unemployment:.2f}%")
    
    st.subheader("🧺 قياس التضخم: سلة السلع ومؤشر الأسعار")
    
    st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown("""
    **مثال من الكتاب (الصفحة 46):**
    
    مستهلك يشتري:
    - 2 لتر حليب
    - 3 كيلو برتقال
    - 2 رغيف خبز
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # آلة حاسبة مؤشر الأسعار
    st.subheader("🧮 آلة حاسبة مؤشر الأسعار والتضخم")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**سنة الأساس**")
        milk_base = st.number_input("سعر اللتر حليب (يورو)", 0.3, 2.0, 0.50, key="milk_base")
        orange_base = st.number_input("سعر الكيلو برتقال (يورو)", 0.5, 3.0, 1.00, key="orange_base")
        bread_base = st.number_input("سعر الرغيف خبز (يورو)", 0.5, 2.0, 1.10, key="bread_base")
    
    with col2:
        st.markdown("**السنة الحالية**")
        milk_current = st.number_input("سعر اللتر حليب (يورو)", 0.3, 2.0, 0.70, key="milk_current")
        orange_current = st.number_input("سعر الكيلو برتقال (يورو)", 0.5, 3.0, 2.00, key="orange_current")
        bread_current = st.number_input("سعر الرغيف خبز (يورو)", 0.5, 2.0, 1.20, key="bread_current")
    
    # الكميات الثابتة
    quantities = {"حليب": 2, "برتقال": 3, "خبز": 2}
    
    # حساب تكلفة السلة
    basket_cost_base = (
        quantities["حليب"] * milk_base +
        quantities["برتقال"] * orange_base +
        quantities["خبز"] * bread_base
    )
    
    basket_cost_current = (
        quantities["حليب"] * milk_current +
        quantities["برتقال"] * orange_current +
        quantities["خبز"] * bread_current
    )
    
    # حساب مؤشر الأسعار
    price_index = (basket_cost_current / basket_cost_base) * 100
    inflation_rate = ((price_index / 100) - 1) * 100
    
    # عرض النتائج
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("تكلفة السلة في سنة الأساس", f"{basket_cost_base:.2f} يورو")
    
    with col2:
        st.metric("تكلفة السلة في السنة الحالية", f"{basket_cost_current:.2f} يورو")
    
    with col3:
        st.metric("مؤشر الأسعار", f"{price_index:.1f}")
        st.metric("معدل التضخم", f"{inflation_rate:.1f}%")
    
    st.markdown("---")
    
    st.subheader("👥 قياس البطالة")
    
    st.markdown('<div class="formula-box">', unsafe_allow_html=True)
    st.markdown("""
    **الصيغ الأساسية:**
    
    ```
    القوى العاملة = المشتغلين + العاطلين
    L = E + U
    
    معدل البطالة = (العاطلين ÷ القوى العاملة) × 100
    u = (U ÷ L) × 100
    
    معدل المشاركة = (القوى العاملة ÷ السكان في سن العمل) × 100
    PR = (L ÷ WA) × 100
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # آلة حاسبة البطالة
    st.subheader("🧮 آلة حاسبة معدلات البطالة والمشاركة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        working_age_pop = st.number_input("السكان في سن العمل (مليون)", 10.0, 100.0, 45.0)
        employed = st.number_input("عدد المشتغلين (مليون)", 1.0, 50.0, 25.0)
    
    with col2:
        unemployed = st.number_input("عدد العاطلين (مليون)", 0.1, 20.0, 2.5)
        inactive = st.number_input("غير النشطين اقتصادياً (مليون)", 0.0, 50.0, 17.5)
    
    # الحسابات
    labor_force = employed + unemployed
    unemployment_rate = (unemployed / labor_force) * 100 if labor_force > 0 else 0
    participation_rate = (labor_force / working_age_pop) * 100 if working_age_pop > 0 else 0
    employment_rate = (employed / working_age_pop) * 100 if working_age_pop > 0 else 0
    
    # عرض المؤشرات
    st.markdown("### 📊 المؤشرات المحسوبة")
    
    metrics_cols = st.columns(4)
    
    with metrics_cols[0]:
        st.metric("القوى العاملة", f"{labor_force:.1f} مليون")
    
    with metrics_cols[1]:
        st.metric("معدل البطالة", f"{unemployment_rate:.1f}%")
    
    with metrics_cols[2]:
        st.metric("معدل المشاركة", f"{participation_rate:.1f}%")
    
    with metrics_cols[3]:
        st.metric("معدل التشغيل", f"{employment_rate:.1f}%")
    
    # مخطط دائري لتوزيع السكان
    categories = ["مشتغلون", "عاطلون", "غير نشطين"]
    values = [employed, unemployed, inactive]
    
    fig_pie = px.pie(
        names=categories,
        values=values,
        title="توزيع السكان في سن العمل",
        color_discrete_sequence=['#2ecc71', '#e74c3c', '#95a5a6']
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📈 تحليل العلاقة بين التضخم والبطالة")
    
    # إنشاء بيانات محاكاة لمنحنى فيليبس
    unemployment_range = np.linspace(3, 12, 20)
    
    # منحنى فيليبس قصير الأجل
    expected_inflation = 2.0
    natural_unemployment = 6.0
    beta = 0.5
    
    inflation_rates = expected_inflation - beta * (unemployment_range - natural_unemployment)
    inflation_rates = np.maximum(0.5, inflation_rates)  # تضمن عدم وجود تضخم سلبي
    
    # إنشاء DataFrame
    phillips_data = pd.DataFrame({
        "البطالة_٪": unemployment_range,
        "التضخم_٪": inflation_rates
    })
    
    # رسم منحنى فيليبس
    fig_phillips = px.scatter(
        phillips_data,
        x="البطالة_٪",
        y="التضخم_٪",
        title="منحنى فيليبس قصير الأجل",
        trendline="lowess",
        trendline_color_override="red"
    )
    
    fig_phillips.update_layout(
        xaxis_title="معدل البطالة (%)",
        yaxis_title="معدل التضخم (%)",
        height=400
    )
    
    # إضافة خط البطالة الطبيعية
    fig_phillips.add_vline(
        x=natural_unemployment,
        line_dash="dash",
        line_color="green",
        annotation_text=f"البطالة الطبيعية ({natural_unemployment}%)"
    )
    
    st.plotly_chart(fig_phillips, use_container_width=True)
    
    st.markdown('<div class="formula-box">', unsafe_allow_html=True)
    st.markdown("""
    **معادلة منحنى فيليبس:**
    
    ```
    π = πₑ - β(u - uₙ)
    ```
    
    حيث:
    - π: التضخم الفعلي
    - πₑ: التضخم المتوقع
    - β: معامل الحساسية (عادة ≈ 0.5)
    - u: معدل البطالة الفعلي
    - uₙ: معدل البطالة الطبيعي
    
    **تفسير:**
    - عندما تكون البطالة فوق الطبيعي → التضخم ينخفض
    - عندما تكون البطالة تحت الطبيعي → التضخم يرتفع
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== الفصل 4: قانون أوكون ==========
elif chapter == "الفصل 4: قانون أوكون":
    st.header("📈 الفصل 4: قانون أوكون - العلاقة بين النمو والبطالة")
    
    st.markdown("""
    ## 🎯 الهدف التعليمي
    فهم العلاقة العكسية بين النمو الاقتصادي والتغير في معدل البطالة كما صاغها آرثر أوكون.
    """)
    
    # إذا كانت هناك بيانات حقيقية، استخدامها
    if uploaded_data is not None and 'معدل_النمو_٪' in uploaded_data.columns and 'البطالة_٪' in uploaded_data.columns:
        st.markdown('<div class="data-source">', unsafe_allow_html=True)
        st.subheader("📊 تحليل بيانات النمو والبطالة الحقيقية")
        
        # تحليل قانون أوكون من البيانات
        df_analysis = uploaded_data.copy()
        
        # حساب التغير في البطالة
        df_analysis['التغير_في_البطالة'] = df_analysis['البطالة_٪'].diff()
        
        # رسم العلاقة
        fig_real_okun = px.scatter(
            df_analysis.dropna(),
            x="معدل_النمو_٪",
            y="التغير_في_البطالة",
            title="قانون أوكون - بيانات حقيقية",
            trendline="ols",
            trendline_color_override="red",
            labels={
                "معدل_النمو_٪": "معدل النمو الاقتصادي (%)",
                "التغير_في_البطالة": "التغير في معدل البطالة (نقطة مئوية)"
            }
        )
        
        # إضافة معلومات النقاط
        fig_real_okun.update_traces(
            text=df_analysis.dropna()["السنة"].astype(str),
            textposition="top center"
        )
        
        fig_real_okun.update_layout(height=400)
        st.plotly_chart(fig_real_okun, use_container_width=True)
        
        # حساب معامل أوكون
        from scipy import stats
        
        growth_clean = df_analysis['معدل_النمو_٪'].dropna().values
        unemployment_change_clean = df_analysis['التغير_في_البطالة'].dropna().values
        
        if len(growth_clean) > 1 and len(unemployment_change_clean) > 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                growth_clean, unemployment_change_clean
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("معامل أوكون المقدر", f"{abs(slope):.3f}")
            
            with col2:
                st.metric("قوة العلاقة (R²)", f"{r_value**2:.3f}")
            
            with col3:
                natural_growth = -intercept / slope if slope != 0 else 0
                st.metric("معدل النمو الطبيعي المقدر", f"{natural_growth:.2f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📐 الصيغة الرياضية لقانون أوكون")
    
    st.markdown('<div class="formula-box">', unsafe_allow_html=True)
    st.markdown("""
    **الصيغة الأساسية:**
    
    ```
    التغير في البطالة = -β × (النمو الفعلي - النمو الطبيعي)
    
    Δu = -β × (g - g*)
    ```
    
    **حيث:**
    - Δu: التغير في معدل البطالة (نقاط مئوية)
    - β: معامل أوكون (عادة ≈ 0.5)
    - g: معدل النمو الاقتصادي الفعلي (%)
    - g*: معدل النمو الطبيعي (%)
    
    **تفسير:**
    - إذا كان النمو = g* → البطالة مستقرة (Δu = 0)
    - إذا كان النمو > g* → البطالة تنخفض (Δu < 0)
    - إذا كان النمو < g* → البطالة ترتفع (Δu > 0)
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # محاكاة تفاعلية
    st.subheader("🔄 محاكاة تفاعلية لقانون أوكون")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        g_star = st.slider("معدل النمو الطبيعي (g*) %", 1.0, 4.0, 2.2, 0.1,
                          help="معدل النمو الذي يحافظ على استقرار البطالة")
    
    with col2:
        beta = st.slider("معامل أوكون (β)", 0.1, 1.0, 0.5, 0.1,
                        help="كل 1% نمو فوق الطبيعي يخفض البطالة β نقطة")
    
    with col3:
        u0 = st.slider("معدل البطالة الأولي %", 3.0, 15.0, 9.1, 0.1,
                      help="معدل البطالة في بداية الفترة")
    
    # إنشاء سيناريوهات مختلفة
    st.markdown("### 📊 سيناريوهات النمو وتأثيرها على البطالة")
    
    scenarios = {
        "ركود شديد (-3%)": -3.0,
        "ركود خفيف (-1%)": -1.0,
        "نمو بطيء (1%)": 1.0,
        "نمو طبيعي (2.2%)": g_star,
        "نمو قوي (4%)": 4.0,
        "نمو سريع (6%)": 6.0
    }
    
    results = []
    
    for name, growth in scenarios.items():
        delta_u = -beta * (growth - g_star)
        new_u = max(1.0, min(20.0, u0 + delta_u))
        
        results.append({
            "السيناريو": name,
            "معدل النمو": f"{growth:.1f}%",
            "الفرق عن الطبيعي": f"{growth - g_star:+.1f}%",
            "التغير في البطالة": f"{delta_u:+.2f} نقطة",
            "البطالة الجديدة": f"{new_u:.1f}%",
            "اتجاه البطالة": "انخفاض" if delta_u < 0 else "ارتفاع" if delta_u > 0 else "استقرار"
        })
    
    df_scenarios = pd.DataFrame(results)
    
    # عرض النتائج في جدول
    st.dataframe(
        df_scenarios.style.apply(
            lambda x: ['background-color: #ffcccc' if 'ارتفاع' in v else 
                      'background-color: #ccffcc' if 'انخفاض' in v else 
                      'background-color: #ffffcc' for v in x],
            subset=['اتجاه البطالة']
        ),
        use_container_width=True
    )
    
    # إنشاء مخطط تفاعلي
    st.markdown("### 📈 تمثيل بياني لقانون أوكون")
    
    # بيانات للمخطط
    growth_values = np.linspace(-5, 7, 50)
    unemployment_changes = -beta * (growth_values - g_star)
    
    fig_okun = go.Figure()
    
    # منحنى أوكون
    fig_okun.add_trace(go.Scatter(
        x=growth_values,
        y=unemployment_changes,
        name="قانون أوكون",
        line=dict(color='blue', width=3),
        hovertemplate="النمو: %{x:.1f}%<br>تغير البطالة: %{y:.2f} نقطة"
    ))
    
    # إضافة خطوط مرجعية
    fig_okun.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_okun.add_vline(x=g_star, line_dash="dash", line_color="green",
                      annotation_text=f"النمو الطبيعي ({g_star}%)")
    
    # إضافة نقاط السيناريوهات
    scenario_points = pd.DataFrame(results)
    scenario_points['growth_numeric'] = [float(s.replace('%', '').split()[-1]) 
                                        for s in scenario_points['معدل النمو']]
    scenario_points['delta_u_numeric'] = [float(d.replace(' نقطة', '')) 
                                         for d in scenario_points['التغير في البطالة']]
    
    fig_okun.add_trace(go.Scatter(
        x=scenario_points['growth_numeric'],
        y=scenario_points['delta_u_numeric'],
        mode='markers+text',
        name="السيناريوهات",
        marker=dict(size=12, color='red'),
        text=scenario_points['السيناريو'].str.split('(').str[0],
        textposition="top center"
    ))
    
    fig_okun.update_layout(
        title="قانون أوكون: العلاقة بين النمو والتغير في البطالة",
        xaxis_title="معدل النمو الاقتصادي (%)",
        yaxis_title="التغير في معدل البطالة (نقطة مئوية)",
        height=500,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_okun, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🎯 التطبيق العملي: تقدير معدل النمو المستهدف")
    
    st.markdown("""
    **مثال تطبيقي:** إذا كانت البطالة الحالية 9% ونريد خفضها إلى 8% خلال سنة:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_u = st.number_input("البطالة الحالية (%)", 1.0, 20.0, 9.0, 0.1)
        target_u = st.number_input("البطالة المستهدفة (%)", 1.0, 20.0, 8.0, 0.1)
        time_period = st.slider("الفترة الزمنية (سنوات)", 1, 5, 1)
    
    with col2:
        # حساب النمو المطلوب
        delta_u_target = (target_u - current_u) / time_period
        required_growth = g_star - (delta_u_target / beta)
        
        st.metric("التغير المطلوب في البطالة سنوياً", f"{delta_u_target:.2f} نقطة")
        st.metric("معدل النمو المطلوب سنوياً", f"{required_growth:.2f}%")
        st.metric("الفرق عن النمو الطبيعي", f"{required_growth - g_star:+.2f}%")
    
    st.info("""
    **تفسير النتائج:**
    - لخفض البطالة من 9% إلى 8% خلال سنة واحدة:
    - يجب تحقيق نمو اقتصادي قدره {:.2f}%
    - هذا أعلى من معدل النمو الطبيعي ({:.1f}%) بمقدار {:.2f} نقطة مئوية
    """.format(required_growth, g_star, required_growth - g_star))

# ========== الفصل 5: العلاقات الاقتصادية ==========
elif chapter == "الفصل 5: العلاقات الاقتصادية":
    st.header("🔄 الفصل 5: العلاقات بين المتغيرات الاقتصادية")
    
    st.markdown("""
    ## 🎯 الهدف التعليمي
    فهم العلاقات المتبادلة بين المتغيرات الاقتصادية الرئيسية وتأثير السياسات الاقتصادية.
    """)
    
    st.subheader("📊 الشبكة الاقتصادية: التفاعلات المتبادلة")
    
    # إنشاء مصفوفة العلاقات
    variables = ["النمو الاقتصادي", "التضخم", "البطالة", "سعر الفائدة", "الإنفاق الحكومي", "الصادرات"]
    
    # علاقات مبسطة
    relationships = {
        "النمو الاقتصادي": {"التضخم": "+", "البطالة": "-", "الصادرات": "+"},
        "التضخم": {"النمو الاقتصادي": "+ قصيراً", "سعر الفائدة": "+", "البطالة": "- قصيراً"},
        "البطالة": {"النمو الاقتصادي": "-", "التضخم": "- قصيراً", "الإنفاق الحكومي": "-"},
        "سعر الفائدة": {"التضخم": "+", "النمو الاقتصادي": "-", "الصادرات": "-"},
        "الإنفاق الحكومي": {"النمو الاقتصادي": "+", "التضخم": "+", "البطالة": "-"},
        "الصادرات": {"النمو الاقتصادي": "+", "سعر الفائدة": "-"}
    }
    
    # إنشاء مصفوفة العلاقات
    matrix_data = []
    for var1 in variables:
        row = [var1]
        for var2 in variables:
            if var1 == var2:
                row.append("-")
            else:
                rel = relationships.get(var1, {}).get(var2, "")
                row.append(rel)
        matrix_data.append(row)
    
    df_matrix = pd.DataFrame(matrix_data, columns=["المتغير"] + variables)
    
    # عرض مصفوفة العلاقات
    st.markdown("### 🔗 مصفوفة العلاقات الاقتصادية")
    
    # تنسيق المصفوفة
    def style_matrix(val):
        if val == "+":
            return 'background-color: #d4edda; color: #155724;'
        elif val == "-":
            return 'background-color: #f8d7da; color: #721c24;'
        elif "+ قصيراً" in str(val) or "- قصيراً" in str(val):
            return 'background-color: #fff3cd; color: #856404;'
        elif val == "":
            return 'background-color: #f8f9fa;'
        else:
            return ''
    
    st.dataframe(
        df_matrix.style.applymap(style_matrix, subset=variables),
        use_container_width=True,
        height=400
    )
    
    st.markdown("""
    **مفتاح الألوان:**
    - 🟢 **أخضر**: علاقة إيجابية (زيادة في أحدهما تؤدي إلى زيادة في الآخر)
    - 🔴 **أحمر**: علاقة سلبية (زيادة في أحدهما تؤدي إلى انخفاض في الآخر)
    - 🟡 **أصفر**: علاقة قصيرة الأجل فقط
    """)
    
    st.markdown("---")
    
    st.subheader("🎯 تأثير السياسات الاقتصادية")
    
    # محاكاة تأثير السياسات
    policy_type = st.selectbox(
        "اختر نوع السياسة الاقتصادية:",
        [
            "سياسة مالية توسعية",
            "سياسة مالية انكماشية", 
            "سياسة نقدية توسعية",
            "سياسة نقدية انكماشية",
            "سياسة تجارية توسعية",
            "سياسة إصلاح سوق العمل"
        ]
    )
    
    # تعريف تأثيرات كل سياسة
    policy_effects = {
        "سياسة مالية توسعية": {
            "description": "زيادة الإنفاق الحكومي أو خفض الضرائب",
            "effects": {
                "النمو الاقتصادي": 1.5,
                "التضخم": 0.8,
                "البطالة": -0.7,
                "العجز الحكومي": 1.2,
                "سعر الفائدة": 0.3
            }
        },
        "سياسة مالية انكماشية": {
            "description": "خفض الإنفاق الحكومي أو زيادة الضرائب",
            "effects": {
                "النمو الاقتصادي": -1.2,
                "التضخم": -0.6,
                "البطالة": 0.6,
                "العجز الحكومي": -1.0,
                "سعر الفائدة": -0.2
            }
        },
        "سياسة نقدية توسعية": {
            "description": "خفض سعر الفائدة أو زيادة المعروض النقدي",
            "effects": {
                "النمو الاقتصادي": 1.0,
                "التضخم": 0.5,
                "البطالة": -0.4,
                "العجز الحكومي": 0.0,
                "سعر الفائدة": -0.5
            }
        },
        "سياسة نقدية انكماشية": {
            "description": "رفع سعر الفائدة أو خفض المعروض النقدي",
            "effects": {
                "النمو الاقتصادي": -0.8,
                "التضخم": -0.4,
                "البطالة": 0.3,
                "العجز الحكومي": 0.0,
                "سعر الفائدة": 0.6
            }
        },
        "سياسة تجارية توسعية": {
            "description": "تحفيز الصادرات أو خفض الحواجز التجارية",
            "effects": {
                "النمو الاقتصادي": 0.7,
                "التضخم": 0.2,
                "البطالة": -0.3,
                "العجز الحكومي": 0.1,
                "سعر الفائدة": 0.0
            }
        },
        "سياسة إصلاح سوق العمل": {
            "description": "إصلاحات لزيادة مرونة سوق العمل",
            "effects": {
                "النمو الاقتصادي": 0.5,
                "التضخم": 0.0,
                "البطالة": -0.8,
                "العجز الحكومي": -0.2,
                "سعر الفائدة": 0.0
            }
        }
    }
    
    selected_policy = policy_effects[policy_type]
    
    # عرض تأثيرات السياسة
    st.markdown(f"### 📋 تأثيرات {policy_type}")
    st.info(f"**وصف السياسة:** {selected_policy['description']}")
    
    # عرض المؤشرات
    effects = selected_policy['effects']
    
    cols = st.columns(len(effects))
    
    for idx, (indicator, effect) in enumerate(effects.items()):
        with cols[idx]:
            delta_color = "inverse" if indicator in ["البطالة", "العجز الحكومي"] else "normal"
            st.metric(
                label=indicator,
                value=f"{effect:+.1f}%" if indicator != "البطالة" else f"{effect:+.1f} نقطة",
                delta=f"تأثير مباشر" if effect != 0 else "لا تأثير",
                delta_color="normal" if (effect > 0 and indicator not in ["البطالة", "العجز الحكومي"]) 
                or (effect < 0 and indicator in ["البطالة", "العجز الحكومي"]) 
                else "inverse"
            )
    
    # مخطط تأثيرات السياسة
    st.markdown("### 📊 تمثيل بياني لتأثيرات السياسة")
    
    indicators = list(effects.keys())
    values = list(effects.values())
    
    fig_policy = go.Figure(data=[
        go.Bar(
            x=indicators,
            y=values,
            marker_color=['#2ecc71' if (v > 0 and k not in ["البطالة", "العجز الحكومي"]) 
                         or (v < 0 and k in ["البطالة", "العجز الحكومي"]) 
                         else '#e74c3c' for k, v in effects.items()],
            text=[f"{v:+.2f}" for v in values],
            textposition='auto'
        )
    ])
    
    fig_policy.update_layout(
        title=f"تأثيرات {policy_type}",
        yaxis_title="التأثير (نقطة مئوية)",
        height=400
    )
    
    st.plotly_chart(fig_policy, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🔄 محاكاة التفاعلات الاقتصادية")
    
    # محاكاة تفاعلية للعلاقات
    st.markdown("### 🎮 محاكاة تفاعلية للعلاقات الاقتصادية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        initial_growth = st.slider("النمو الاقتصادي الأولي (%)", -2.0, 6.0, 2.0, 0.1)
        initial_inflation = st.slider("التضخم الأولي (%)", 0.0, 10.0, 2.0, 0.1)
    
    with col2:
        initial_unemployment = st.slider("البطالة الأولية (%)", 3.0, 15.0, 8.0, 0.1)
        interest_rate = st.slider("سعر الفائدة (%)", 0.0, 8.0, 3.0, 0.1)
    
    # محاكاة التفاعلات
    st.markdown("#### 📈 نتائج المحاكاة بعد سنة:")
    
    # محاكاة مبسطة للتفاعلات
    # النمو يتأثر بالتضخم (منحنى فيليبس عكسي) وسعر الفائدة
    growth_effect = 2.0 + 0.3 * (initial_inflation - 2) - 0.2 * (interest_rate - 3)
    
    # التضخم يتأثر بالنمو (منحنى فيليبس) والبطالة
    inflation_effect = 2.0 + 0.5 * (initial_growth - 2) - 0.3 * (initial_unemployment - 6)
    
    # البطالة تتأثر بالنمو (قانون أوكون)
    unemployment_effect = initial_unemployment - 0.5 * (growth_effect - 2)
    
    # سعر الفائدة يتأثر بالتضخم (قاعدة تايلور)
    interest_effect = 2.0 + 0.5 * (inflation_effect - 2) + 0.5 * (growth_effect - 2)
    
    results_cols = st.columns(4)
    
    with results_cols[0]:
        st.metric("النمو الاقتصادي", f"{growth_effect:.1f}%", 
                 f"{growth_effect - initial_growth:+.1f}%")
    
    with results_cols[1]:
        st.metric("التضخم", f"{inflation_effect:.1f}%", 
                 f"{inflation_effect - initial_inflation:+.1f}%")
    
    with results_cols[2]:
        st.metric("البطالة", f"{unemployment_effect:.1f}%", 
                 f"{unemployment_effect - initial_unemployment:+.1f} نقطة")
    
    with results_cols[3]:
        st.metric("سعر الفائدة", f"{interest_effect:.1f}%", 
                 f"{interest_effect - interest_rate:+.1f}%")
    
    st.info("""
    **ملاحظة:** هذه محاكاة مبسطة تعتمد على:
    1. قانون أوكون (العلاقة بين النمو والبطالة)
    2. منحنى فيليبس (العلاقة بين التضخم والبطالة)
    3. قاعدة تايلور (تحديد سعر الفائدة)
    
    في الواقع، التفاعلات أكثر تعقيداً وتتأثر بالعديد من العوامل الأخرى.
    """)

# ========== قسم التمارين العملية ==========
elif chapter == "🎯 التمارين العملية":
    st.header("🎯 التمارين العملية في الاقتصاد الكلي")
    
    st.markdown("""
    ## 📝 تمارين تطبيقية بناءً على منهجية الكتاب
    
    اختر التمرين الذي تريد حله:
    """)
    
    exercise = st.selectbox(
        "اختر التمرين:",
        [
            "تمرين 1: حساب الناتج المحلي بطرق مختلفة",
            "تمرين 2: تحليل التضخم والبطالة", 
            "تمرين 3: تطبيق قانون أوكون",
            "تمرين 4: تحليل تأثير السياسات",
            "تمرين 5: تحميل وتحليل بيانات حقيقية"
        ]
    )
    
    if exercise == "تمرين 1: حساب الناتج المحلي بطرق مختلفة":
        st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
        st.subheader("تمرين 1: حساب الناتج المحلي بطرق مختلفة")
        
        st.markdown("""
        **البيانات:**
        
        افترض اقتصاداً بسيطاً يتكون من ثلاث وحدات إنتاجية:
        
        1. **الزراعة**: تنتج قمحاً بقيمة 500 مليون يورو
        2. **المطاحن**: تشتري كل القمح وتنتج دقيقاً بقيمة 800 مليون يورو
        3. **المخابز**: تشتري كل الدقيق وتنتج خبزاً بقيمة 1200 مليون يورو
        
        **المعلومات الإضافية:**
        - الأجور المدفوعة: الزراعة 150، المطاحن 200، المخابز 300 مليون يورو
        - الأرباح: الزراعة 350، المطاحن 600، المخابز 900 مليون يورو
        
        **المطلوب:**
        1. حساب الناتج المحلي بطريقة الإنتاج (القيمة المضافة)
        2. حساب الناتج المحلي بطريقة الإنفاق
        3. حساب الناتج المحلي بطريقة الدخل
        4. التحقق من تطابق النتائج
        """)
        
        # حل تفاعلي
        st.markdown("---")
        st.subheader("🧮 الحل التفاعلي")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### طريقة الإنتاج (القيمة المضافة)")
            
            # حساب القيم المضافة
            st.markdown("**الزراعة:**")
            st.latex(r"500 - 0 = 500")
            
            st.markdown("**المطاحن:**")
            st.latex(r"800 - 500 = 300")
            
            st.markdown("**المخابز:**")
            st.latex(r"1200 - 800 = 400")
            
            total_value_added = 500 + 300 + 400
            st.metric("إجمالي القيمة المضافة", f"{total_value_added} مليون يورو")
        
        with col2:
            st.markdown("### طريقة الدخل")
            
            # حساب إجمالي الدخل
            st.markdown("**الأجور:**")
            st.latex(r"150 + 200 + 300 = 650")
            
            st.markdown("**الأرباح:**")
            st.latex(r"350 + 600 + 900 = 1850")
            
            total_income = 650 + 1850
            st.metric("إجمالي الدخل", f"{total_income} مليون يورو")
        
        st.markdown("### طريقة الإنفاق")
        st.markdown("""
        في هذا الاقتصاد المبسط، السلعة النهائية الوحيدة هي الخبز:
        
        """)
        st.latex(r"1200 = C + I + G + (X - M)")
        st.metric("قيمة السلع النهائية", "1200 مليون يورو")
        
        # التحقق من تطابق النتائج
        st.markdown("---")
        st.subheader("✅ التحقق من تطابق النتائج")
        
        check_cols = st.columns(3)
        
        with check_cols[0]:
            st.metric("طريقة الإنتاج", f"{total_value_added} مليون")
        
        with check_cols[1]:
            st.metric("طريقة الدخل", f"{total_income} مليون")
        
        with check_cols[2]:
            st.success("✅ النتائج متطابقة!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif exercise == "تمرين 2: تحليل التضخم والبطالة":
        st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
        st.subheader("تمرين 2: تحليل التضخم والبطالة")
        
        st.markdown("""
        **البيانات:**
        
        سلة استهلاكية تحتوي على:
        
        | السلعة | الكمية | سعر سنة الأساس | سعر السنة الحالية |
        |---------|--------|----------------|-------------------|
        | خبز     | 10 أرغفة | 1 يورو/رغيف | 1.2 يورو/رغيف |
        | حليب    | 5 لترات | 0.8 يورو/لتر | 1.0 يورو/لتر |
        | لحوم    | 2 كجم   | 15 يورو/كجم | 18 يورو/كجم |
        
        **سوق العمل:**
        - السكان في سن العمل: 50 مليون
        - المشتغلين: 22 مليون
        - العاطلين: 3 مليون
        
        **المطلوب:**
        1. حساب مؤشر الأسعار
        2. حساب معدل التضخم
        3. حساب معدل البطالة
        4. حساب معدل المشاركة
        """)
        
        # حل تفاعلي
        st.markdown("---")
        st.subheader("🧮 الحل التفاعلي")
        
        # إدخال البيانات
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### حساب التضخم")
            
            # تكلفة السلة
            basket_base = (10 * 1) + (5 * 0.8) + (2 * 15)
            basket_current = (10 * 1.2) + (5 * 1.0) + (2 * 18)
            
            st.markdown("**تكلفة السلة سنة الأساس:**")
            st.latex(r"(10 \times 1) + (5 \times 0.8) + (2 \times 15) = 44 \, \text{يورو}")
            
            st.markdown("**تكلفة السلة السنة الحالية:**")
            st.latex(r"(10 \times 1.2) + (5 \times 1.0) + (2 \times 18) = 53 \, \text{يورو}")
            
            # مؤشر الأسعار
            price_index = (basket_current / basket_base) * 100
            inflation = ((price_index / 100) - 1) * 100
            
            st.metric("مؤشر الأسعار", f"{price_index:.1f}")
            st.metric("معدل التضخم", f"{inflation:.1f}%")
        
        with col2:
            st.markdown("### حساب مؤشرات سوق العمل")
            
            # البيانات
            working_age = 50
            employed = 22
            unemployed = 3
            
            # الحسابات
            labor_force = employed + unemployed
            unemployment_rate = (unemployed / labor_force) * 100
            participation_rate = (labor_force / working_age) * 100
            
            st.markdown("**القوى العاملة:**")
            st.latex(r"22 + 3 = 25 \, \text{مليون}")
            
            st.markdown("**معدل البطالة:**")
            st.latex(r"\frac{3}{25} \times 100 = 12\%")
            
            st.markdown("**معدل المشاركة:**")
            st.latex(r"\frac{25}{50} \times 100 = 50\%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif exercise == "تمرين 3: تطبيق قانون أوكون":
        st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
        st.subheader("تمرين 3: تطبيق قانون أوكون")
        
        st.markdown("""
        **البيانات:**
        
        بلد لديه المعطيات التالية:
        - معدل البطالة الأولي: 9.5%
        - معدل النمو الطبيعي: 2.2%
        - معامل أوكون: 0.5
        
        **المطلوب:**
        
        1. إذا حقق النمو 3.5%، كم سيكون معدل البطالة الجديد؟
        2. إذا كان المستهدف خفض البطالة إلى 8% خلال سنة، ما هو معدل النمو المطلوب؟
        3. إذا انخفض النمو إلى 1%، كم سترتفع البطالة؟
        """)
        
        # حل تفاعلي
        st.markdown("---")
        st.subheader("🧮 الحل التفاعلي")
        
        # المعطيات
        u0 = 9.5
        g_star = 2.2
        beta = 0.5
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**الجزء 1: النمو = 3.5%**")
            g1 = 3.5
            delta_u1 = -beta * (g1 - g_star)
            u1 = u0 + delta_u1
            
            st.markdown(f"""
            ```
            Δu = -0.5 × (3.5 - 2.2) = -0.65 نقطة
            البطالة الجديدة = 9.5 - 0.65 = {u1:.2f}%
            ```
            """)
        
        with col2:
            st.markdown("**الجزء 2: خفض البطالة إلى 8%**")
            u_target = 8.0
            delta_u_target = u_target - u0
            g_required = g_star - (delta_u_target / beta)
            
            st.markdown(f"""
            ```
            Δu المستهدف = 8.0 - 9.5 = -1.5 نقطة
            النمو المطلوب = 2.2 - (-1.5/0.5) = 5.2%
            ```
            """)
        
        with col3:
            st.markdown("**الجزء 3: النمو = 1%**")
            g3 = 1.0
            delta_u3 = -beta * (g3 - g_star)
            u3 = u0 + delta_u3
            
            st.markdown(f"""
            ```
            Δu = -0.5 × (1.0 - 2.2) = +0.6 نقطة
            البطالة الجديدة = 9.5 + 0.6 = {u3:.2f}%
            ```
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif exercise == "تمرين 4: تحليل تأثير السياسات":
        st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
        st.subheader("تمرين 4: تحليل تأثير السياسات")
        
        st.markdown("""
        **السيناريو:**
        
        اقتصاد يواجه الركود مع:
        - النمو الحالي: -1.5%
        - البطالة: 10%
        - التضخم: 1.2%
        
        **المطلوب:**
        
        قم بتحليل تأثير السياسات التالية:
        
        1. **السياسة المالية التوسعية**: زيادة الإنفاق الحكومي بـ 100 مليار يورو
        2. **السياسة النقدية التوسعية**: خفض سعر الفائدة بمقدار 2 نقطة مئوية
        
        **افترض أن:**
        - مضاعف الإنفاق = 1.5
        - معامل أوكون = 0.5
        - معدل النمو الطبيعي = 2.2%
        """)
        
        # حل تفاعلي
        st.markdown("---")
        st.subheader("🧮 الحل التفاعلي")
        
        # البيانات الأولية
        initial_data = {
            "النمو": -1.5,
            "البطالة": 10.0,
            "التضخم": 1.2
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### السياسة المالية التوسعية")
            
            # تأثير السياسة المالية
            gov_spending = 100
            multiplier = 1.5
            g_star = 2.2
            beta = 0.5
            
            # التأثير على النمو
            growth_effect_fiscal = (gov_spending * multiplier) / 1000  # مقارنة بالناتج المحلي
            new_growth_fiscal = initial_data["النمو"] + growth_effect_fiscal
            
            # التأثير على البطالة (قانون أوكون)
            delta_u_fiscal = -beta * (new_growth_fiscal - g_star)
            new_unemployment_fiscal = initial_data["البطالة"] + delta_u_fiscal
            
            # التأثير على التضخم (منحنى فيليبس مبسط)
            inflation_effect_fiscal = 0.3 * growth_effect_fiscal
            new_inflation_fiscal = initial_data["التضخم"] + inflation_effect_fiscal
            
            st.metric("النمو الجديد", f"{new_growth_fiscal:.1f}%", 
                     f"{growth_effect_fiscal:+.1f}%")
            st.metric("البطالة الجديدة", f"{new_unemployment_fiscal:.1f}%", 
                     f"{delta_u_fiscal:+.2f} نقطة")
            st.metric("التضخم الجديد", f"{new_inflation_fiscal:.1f}%", 
                     f"{inflation_effect_fiscal:+.1f}%")
        
        with col2:
            st.markdown("### السياسة النقدية التوسعية")
            
            # تأثير السياسة النقدية
            interest_cut = 2.0
            
            # التأثير على النمو (قاعدة مبسطة)
            growth_effect_monetary = 0.5 * interest_cut
            new_growth_monetary = initial_data["النمو"] + growth_effect_monetary
            
            # التأثير على البطالة
            delta_u_monetary = -beta * (new_growth_monetary - g_star)
            new_unemployment_monetary = initial_data["البطالة"] + delta_u_monetary
            
            # التأثير على التضخم
            inflation_effect_monetary = 0.2 * interest_cut
            new_inflation_monetary = initial_data["التضخم"] + inflation_effect_monetary
            
            st.metric("النمو الجديد", f"{new_growth_monetary:.1f}%", 
                     f"{growth_effect_monetary:+.1f}%")
            st.metric("البطالة الجديدة", f"{new_unemployment_monetary:.1f}%", 
                     f"{delta_u_monetary:+.2f} نقطة")
            st.metric("التضخم الجديد", f"{new_inflation_monetary:.1f}%", 
                     f"{inflation_effect_monetary:+.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif exercise == "تمرين 5: تحميل وتحليل بيانات حقيقية":
        st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
        st.subheader("تمرين 5: تحميل وتحليل بيانات حقيقية")
        
        st.markdown("""
        **المطلوب:**
        
        1. قم بتحميل ملف بيانات اقتصادية (Excel أو CSV)
        2. قم بالتحليل الإحصائي الأساسي
        3. ارسم العلاقات بين المتغيرات الرئيسية
        4. قدم استنتاجاتك
        """)
        
        # تحميل البيانات
        st.markdown("---")
        st.subheader("📥 تحميل البيانات")
        
        uploaded_file = st.file_uploader(
            "اختر ملف بيانات اقتصادية",
            type=['xlsx', 'xls', 'csv']
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ تم تحميل {len(df)} صف و {len(df.columns)} عمود")
                
                # عرض البيانات
                with st.expander("👁️ عرض البيانات"):
                    st.dataframe(df)
                
                # التحليل الإحصائي
                st.markdown("---")
                st.subheader("📊 التحليل الإحصائي")
                
                if st.button("إجراء التحليل الإحصائي"):
                    # إحصائيات وصفية
                    st.markdown("### الإحصائيات الوصفية")
                    st.dataframe(df.describe())
                    
                    # تحليل المتغيرات الرقمية
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    
                    if numeric_cols:
                        st.markdown("### العلاقات بين المتغيرات")
                        
                        # اختيار متغيرين للتحليل
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            x_var = st.selectbox("اختر المتغير الأول (X)", numeric_cols)
                        
                        with col2:
                            y_var = st.selectbox("اختر المتغير الثاني (Y)", numeric_cols)
                        
                        # رسم العلاقة
                        if x_var != y_var:
                            fig_scatter = px.scatter(
                                df,
                                x=x_var,
                                y=y_var,
                                title=f"العلاقة بين {x_var} و {y_var}",
                                trendline="ols",
                                trendline_color_override="red"
                            )
                            st.plotly_chart(fig_scatter, use_container_width=True)
                            
                            # حساب معامل الارتباط
                            correlation = df[x_var].corr(df[y_var])
                            st.metric("معامل الارتباط", f"{correlation:.3f}")
                            
                            # تفسير معامل الارتباط
                            if abs(correlation) > 0.7:
                                strength = "قوي"
                            elif abs(correlation) > 0.3:
                                strength = "متوسط"
                            else:
                                strength = "ضعيف"
                            
                            direction = "إيجابي" if correlation > 0 else "سلبي"
                            st.info(f"العلاقة {strength} و {direction}")
                
                # التصدير
                st.markdown("---")
                st.subheader("💾 تصدير التحليل")
                
                if st.button("تصدير التحليل إلى Excel"):
                    # إنشاء تقرير Excel
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='البيانات الخام', index=False)
                        df.describe().to_excel(writer, sheet_name='الإحصائيات الوصفية')
                        
                        # إضافة تحليل الارتباطات
                        if len(numeric_cols) >= 2:
                            corr_matrix = df[numeric_cols].corr()
                            corr_matrix.to_excel(writer, sheet_name='مصفوفة الارتباطات')
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="📥 تنزيل ملف Excel",
                        data=output,
                        file_name="التحليل_الاقتصادي.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            except Exception as e:
                st.error(f"خطأ في تحليل البيانات: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== التذييل ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📚 تطبيق الاقتصاد الكلي التفاعلي - منهجية تعليمية</p>
    <p>تم تطوير هذا التطبيق لدعم تعلم مفاهيم الاقتصاد الكلي</p>
    <p>جميع البيانات والتحليلات للأغراض التعليمية فقط</p>
</div>
""", unsafe_allow_html=True)