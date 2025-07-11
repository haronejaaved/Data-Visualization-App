import streamlit as st
import pandas as pd
import altair as alt



# File uploader accepts csv or xlsx
uploaded_file = st.file_uploader("Upload a CSV or XLSX file to visualize data", type=["csv", "xlsx"])

if uploaded_file:
    # Load data based on file type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df)

    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if df.empty:
        st.warning("The uploaded file is empty.")
    else:
        chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot"])

        if chart_type == "Line Chart":
            if len(numeric_cols) < 1:
                st.warning("Need at least one numeric column for Y-axis.")
            else:
                y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols)
                x_axis = st.selectbox("Select X-axis (optional)", df.columns.tolist(), index=0)
                st.line_chart(df.set_index(x_axis)[y_axis])

        elif chart_type == "Bar Chart":
            if len(categorical_cols) < 1 or len(numeric_cols) < 1:
                st.warning("Need at least one categorical and one numeric column.")
            else:
                x_axis = st.selectbox("Select X-axis (categorical)", categorical_cols)
                y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols)
                st.bar_chart(df.groupby(x_axis)[y_axis].mean())

        elif chart_type == "Scatter Plot":
            if len(numeric_cols) < 2:
                st.warning("Need at least two numeric columns for scatter plot.")
            else:
                x_axis = st.selectbox("Select X-axis (numeric)", numeric_cols, index=0)
                y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                st.write("### Scatter Plot")
                scatter = alt.Chart(df).mark_circle(size=60).encode(
                    x=x_axis,
                    y=y_axis,
                    tooltip=df.columns.tolist()
                ).interactive()
                st.altair_chart(scatter, use_container_width=True)

        elif chart_type == "Histogram":
            if len(numeric_cols) < 1:
                st.warning("Need at least one numeric column for histogram.")
            else:
                column = st.selectbox("Select column (numeric)", numeric_cols)
                bins = st.slider("Number of bins", 5, 100, 30)
                hist = alt.Chart(df).mark_bar().encode(
                    alt.X(column, bin=alt.Bin(maxbins=bins)),
                    y='count()',
                    tooltip=['count()']
                ).interactive()
                st.altair_chart(hist, use_container_width=True)

        elif chart_type == "Box Plot":
            if len(numeric_cols) < 1:
                st.warning("Need at least one numeric column for box plot.")
            else:
                y_axis = st.selectbox("Select numeric column", numeric_cols)
                x_axis = None
                if categorical_cols:
                    x_axis = st.selectbox("Select categorical column (optional)", [None] + categorical_cols)
                box = alt.Chart(df).mark_boxplot().encode(
                    x=x_axis if x_axis else alt.value(""),
                    y=y_axis
                )
                st.altair_chart(box, use_container_width=True)

else:
    st.info("Please upload a CSV or XLSX file to get started. Included a kaggle file from my github Repository. Click the link below")
 

 
github = "https://github.com/haronejaaved"
myprojects = "https://haronejaaved.github.io"
csvfile = "https://codewithharone.com/wp-content/uploads/2025/05/cereal.csv.zip"


st.markdown(f'<a href="{github}" target="_blank">Visit My Github Page</a>', unsafe_allow_html=True)
st.markdown(f'<a href="{myprojects}" target="_blank">See some of my projects</a>', unsafe_allow_html=True)
st.markdown(f'<a href="{csvfile}" target="_blank">Csv file from Kaggle dataset</a>', unsafe_allow_html=True)

