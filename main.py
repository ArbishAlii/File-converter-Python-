# import streamlit as st
# import pandas as pd
# from io import BytesIO
# import os

# st.set_page_config(page_title="📂 File Converter & Cleaner", layout="wide")
# st.title("📂 File Converter & Cleaner")
# st.write("Upload your CSV and Excel Files to clean the data convert formats effortlessly ✨")

# files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

# for file in files:
#     ext = file.name.split(".")[-1]
#     df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

#     st.subheader(f"📄 {file.name} - Preview")
#     st.dataframe(df.head())

#     if st.checkbox(f"Fill Missing Values - {file.name}"):
#         df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
#         st.success("Missing values filled successfully!")
#         st.dataframe(df.head())

#     selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
#     df = df[selected_columns]
#     st.dataframe(df.head())

#     # ✅ Fixed typo "select_dtyp" to "select_dtypes"
#     if st.checkbox(f"📊 Show Chart - ({file.name})") and not df.select_dtypes(include="number").empty:
#         st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

#     format_choice = st.radio(f"Convert ({file.name}) to:", ["CSV", "Excel"], key=file.name)

#     if st.button(f"⬇️ Download ({file.name}) as {format_choice}", key=f"download_{file.name}"):
#         output = BytesIO()
#         base_name, file_ext = os.path.splitext(file.name)

#         if format_choice == "CSV":
#             df.to_csv(output, index=False)
#             mime = "text/csv"
#             new_name = base_name + ".csv"
#         else:
#             df.to_excel(output, index=False)
#             mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             new_name = base_name + ".xlsx"

#         st.download_button(label="📥 Click to Download",
#                            data=output.getvalue(),
#                            file_name=new_name,
#                            mime=mime)
# st.success("Operation Completed!⭐")













import streamlit as st
import pandas as pd
from io import BytesIO
import os

st.set_page_config(page_title="📂 File Converter & Cleaner", layout="wide")
st.title("📂 File Converter & Cleaner")
st.write("✨ Clean, preview, and convert your CSV/Excel files with ease!")

files = st.file_uploader("📤 Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.markdown(f"## 📄 {file.name}")

        # Tabs for UI separation
        tab1, tab2, tab3 = st.tabs(["🔍 Preview & Select Columns", "🧹 Clean Data", "📥 Convert & Download"])

        with tab1:
            st.subheader("🔍 Data Preview")
            st.dataframe(df.head())

            selected_columns = st.multiselect(f"Select Columns to Keep", df.columns, default=df.columns)
            df = df[selected_columns]
            st.dataframe(df.head())

            with st.expander("📊 Show Chart (Optional)"):
                if not df.select_dtypes(include="number").empty:
                    st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
                else:
                    st.info("No numeric columns available for chart.")

        with tab2:
            st.subheader("🧹 Clean Missing Values")
            if st.button(f"✨ Fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                st.success("Missing values filled successfully!")
                st.dataframe(df.head())

        with tab3:
            st.subheader("📥 Convert & Download")
            format_choice = st.radio("Choose format to convert", ["CSV", "Excel"], key=file.name)

            # Download trigger
            if st.button(f"⬇️ Download as {format_choice}", key=f"download_{file.name}"):
                output = BytesIO()
                base_name, file_ext = os.path.splitext(file.name)

                if format_choice == "CSV":
                    df.to_csv(output, index=False)
                    mime = "text/csv"
                    new_name = base_name + ".csv"
                    data = output.getvalue()

                else:
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Sheet1')
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = base_name + ".xlsx"
                    data = output.getvalue()

                st.download_button(label="📥 Click to Download",
                                   data=data,
                                   file_name=new_name,
                                   mime=mime)

    st.success("✅ All operations completed!")
else:
    st.info("Please upload files to get started.")
