import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Sidebar filters
st.sidebar.header("الفلاتر")
# from_date = st.sidebar.date_input("From", datetime.date(2025, 2, 1))
# to_date = st.sidebar.date_input("To", datetime.date(2025, 2, 28))  # Adjusted to a later date
promo = st.sidebar.radio('اختر الفترة' , ['كامل الشهر', 'قبل الخصومات', 'فترة الخصومات'])

if promo == 'كامل الشهر':
    # data = pd.read_csv("clothes_shop_data.csv", parse_dates=['Date'])
    from_date = '2025-2-1'
    to_date = '2025-2-28'
    deltas = ''
    deltap = ''
    deltam = ''

elif promo == 'قبل الخصومات':
    # data = pd.read_csv("clothes_shop_data_290.csv", parse_dates=['Date'])
    from_date = '2025-2-11'
    to_date = '2025-2-19'
    deltas = ''
    deltap = ''
    deltam = ''

elif promo == 'فترة الخصومات':
    # data = pd.read_csv("clothes_shop_data_290.csv", parse_dates=['Date'])
    from_date = '2025-2-20'
    to_date = '2025-2-28'
    deltas = ''
    deltap = ''
    deltam = ''

st.sidebar.subheader("من: ")
st.sidebar.text(from_date)
st.sidebar.subheader("الى: ")
st.sidebar.text(to_date)

category_filter = st.sidebar.multiselect("المنتجات", ['قميص', 'بنطلون', 'جاكيت'], default=['قميص', 'بنطلون', 'جاكيت'])
# Ensure from_date is not after to_date
# if from_date > to_date:
#     st.error("Error: 'From' date must be before 'To' date.")

# Load and process data
data = pd.read_csv("clothes_shop_data.csv", parse_dates=['Date'])
data['Product'] = data['Product'].map({'Shirt': 'قميص', 'Jeans': 'بنطلون', 'Jacket': 'جاكيت'})
data.loc[(data['Date'] >= '2025-2-20') & (data['Product'] == 'جاكيت'), 'Quantity'] = data['Quantity'] * 4
data.loc[(data['Date'] >= '2025-2-20') & (data['Product'] == 'جاكيت'), 'Price'] = data['Price'] * 0.3
data['المبيعات'] = data['Price'] * data['Quantity']
data['cost'] = data['COGS'] * data['Quantity']
data['الأرباح'] = data['المبيعات'] - data['cost']
data['الهامش'] = data['الأرباح'] / data['المبيعات']
data['هامش المنتج'] = data['الهامش'].apply(lambda x: str(round(x*100, 2)) + ' %')

# Apply filters
filtered_df = data[(data['Product'].isin(category_filter)) &
                   (data['Date'] >= pd.to_datetime(from_date)) & 
                   (data['Date'] <= pd.to_datetime(to_date))]

# st.markdown("# Cafe Dashboard")
st.html("""
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        .content {
            direction: rtl;
            text-align: right;
            الهامش: 20px;
        }

        .content ul {
            padding-right: 0;
            الهامش-right: 0;
            list-style-position: inside;
        }

        h1 {
            font-size: 36px; /* Increased font size */
            font-weight: bold;
        }

        .content li {
            الهامش-bottom: 10px;
        }

        .highlight {
            color: yellow;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>لوحة بيانات تحليل الهوامش: كيف تكشف المشاكل وتحسن الأداء؟</h1>
        <p>لدينا مثال عملي على كيفية استخدام لوحة البيانات لفهم أداء الهوامش واتخاذ قرارات مالية أكثر ذكاءً. من خلال تحليل الهوامش، يمكننا التعرف على المشكلات التي تؤثر على الربحية واتخاذ إجراءات تصحيحية في الوقت المناسب.</p>
        
        <h2>متجر بيع ملابس</h2>
        <p>قام المتجر بتقديم خصومات على بعض المنتجات في الفترة من 20 فبراير إلى 28 فبراير. نريد أن نرى كيف أثرت هذه الخصومات على الهوامش الإجمالية وأداء المتجر.</p>

        <h2>تحليل الفترات المختلفة باستخدام لوحة البيانات</h2>
        <p class="highlight">استخدم الفلاتر في الشريط الجانبي</p>

        <h3>🔹 شهر فبراير (كامل الشهر)</h3>
        <ul>
            <li>إذا نظرنا إلى الرسم البياني الذي يظهر المبيعات والأرباح، نلاحظ أنه قبل فترة التخفيضات كانت المبيعات ثابتة.</li>
            <li>خلال فترة التخفيضات كان هناك ارتفاع بسيط في المبيعات، وفي نفس الوقت هناك انخفاض في الأرباح.</li>
            <li>نلاحظ أيضًا انخفاضًا حادًا في رسم الهوامش من بداية فترة التخفيضات.</li>
        </ul>

        <h3>🔹 الأداء الطبيعي (قبل الخصومات)</h3>
        <ul>
            <li>متوسط هامش الربح كان 51.55% وكان الأداء المالي مستقرًا.</li>
        </ul>

        <h3>🔹 أداء الخصومات (فترة الخصومات)</h3>
        <ul>
            <li>انخفض الهامش بشكل حاد إلى 13.55%.</li>
            <li>انخفاض الهوامش طبيعي عند تقديم الخصومات، ولكن لاحظنا أن الانخفاض حاد جدًا وأيضًا هنالك انخفاض في إجمالي الأرباح، مما يستدعي استقصاء السبب.</li>
        </ul>

        <h3>🔹 سبب الانخفاض (فترة الخصومات)</h3>
        <ul>
            <li>بالنظر إلى جداول الأسعار والهوامش، نرى أنه تم تخفيض سعر الجاكيت بنسبة 70% مما أدى إلى انخفاض في الهوامش.</li>
            <li>استخدم فلتر المنتج  للاطلاع أكثر على أداء كل منتج على حده.</li>
        </ul>
    </div>
</body>
</html>

""")
st.header('')

a, b, c = st.columns(3)
a.metric("المبيعات", filtered_df['المبيعات'].sum(), deltas, border=True)
b.metric("الأرباح", filtered_df['الأرباح'].sum(), deltap, border=True)
c.metric("الهامش", str(round(filtered_df['الأرباح'].sum() / filtered_df['المبيعات'].sum() * 100, 2)) + " %", deltam, border=True)

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.subheader(filtered_df['المبيعات'].sum())
#     st.header("المبيعات")

# with col2:
#     st.subheader(filtered_df['الأرباح'].sum())
#     st.header("الأرباح")

# with col3:
#     st.subheader(str(round(filtered_df['الأرباح'].sum() / filtered_df['المبيعات'].sum() * 100, 2)) + " %")
#     st.header("الهامش")

# st.header('')


# Summary Statistics (Replaced Value1 and Value2 with meaningful columns)
# st.markdown("### Summary Statistics")
# st.write(f"**Number of data points:** {len(filtered_df)}")
# st.write(f"**Mean المبيعات:** {filtered_df['المبيعات'].mean():.2f}")
# st.write(f"**Mean الأرباح:** {filtered_df['الأرباح'].mean():.2f}")

# Place two plots side by side using columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("#### المبيعات")
#     المبيعات_data = filtered_df.groupby('Date')['المبيعات'].sum().reset_index()
#     st.line_chart(المبيعات_data.set_index('Date'))

# with col2:
#     st.markdown("#### الأرباح")
#     الأرباح_data = filtered_df.groupby('Date')['الأرباح'].sum().reset_index()
#     st.line_chart(الأرباح_data.set_index('Date'))

# st.header('')

# st.markdown("#### المبيعات per Product")
# المبيعات_line = filtered_df.groupby(['Date', 'Product'])['المبيعات'].sum().reset_index()
# st.line_chart(المبيعات_line, x='Date', y='المبيعات', color='Product')

# st.header('')

# st.markdown("#### الأرباح per Product")
# الأرباح_line = filtered_df.groupby(['Date', 'Product'])['الأرباح'].sum().reset_index()
# st.line_chart(الأرباح_line, x='Date', y='الأرباح', color='Product')

# st.header('')

st.markdown("#### المبيعات و الأرباح")
الهامش_line = filtered_df.groupby('Date')[['المبيعات', 'الأرباح']].sum().reset_index()
الهامش_line = الهامش_line.melt(id_vars=['Date'], value_vars=['المبيعات', 'الأرباح'])
st.line_chart(الهامش_line.rename(columns={'Date': 'التاريخ'}), x='التاريخ', y='value', color="variable")

# st.header('')

st.markdown("#### الهامش")
الهامش_line = filtered_df.groupby('Date')[['المبيعات', 'cost']].mean().reset_index()
الهامش_line['الهامش'] = (الهامش_line['المبيعات'] - الهامش_line['cost'])/ الهامش_line['المبيعات']
st.line_chart(الهامش_line.rename(columns={'Date': 'التاريخ'}), x='التاريخ', y='الهامش')


displaydf = filtered_df.rename(columns={'Product': 'المنتج', 'Price': 'السعر'})
col1, col2 = st.columns(2)
# Display the first few rows of the dataset
with col1:
    st.markdown("#### أسعار المنتجات")
    st.dataframe(displaydf[displaydf['Date'] == from_date][['المنتج', 'السعر']].set_index('المنتج').drop_duplicates())

with col2:
    st.markdown("#### هوامش المنتجات")
    st.dataframe(displaydf[displaydf['Date'] == from_date][['المنتج', 'هامش المنتج']].set_index('المنتج').drop_duplicates())

# with col3:
#     st.dataframe(filtered_df[['Product', 'COGS']].drop_duplicates())
