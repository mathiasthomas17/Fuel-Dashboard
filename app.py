# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# import plotly.express as px

# # ==========================
# # PAGE CONFIGURATION
# # ==========================
# st.set_page_config(page_title="Fuel Theft Dashboard", layout="wide")

# # --- THEME COLORS ---
# PRIMARY_GREEN = "#228B22"
# YELLOW = "#FFD700"

# st.markdown(f"""
#     <style>
#         [data-testid="stSidebar"] {{
#             background-color: #f7fff7;
#         }}
#         h1, h2, h3 {{
#             color: {PRIMARY_GREEN};
#         }}
#         .stMetric {{
#             background-color: #f0fff0;
#             border-radius: 12px;
#             padding: 10px;
#             border: 1px solid #d4edda;
#         }}
#     </style>
# """, unsafe_allow_html=True)

# # ==========================
# # GOOGLE SHEETS CONNECTION
# # ==========================
# SPREADSHEET_ID = "1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw"
# SHEET_NAME = "ALL"

# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]
# creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
# client = gspread.authorize(creds)

# try:
#     sheet = client.open_by_key(SPREADSHEET_ID)
#     worksheet = sheet.worksheet(SHEET_NAME)
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)
#     st.success("✅ Data loaded successfully from Google Sheets!")
# except Exception as e:
#     st.error(f"❌ Failed to load data: {e}")
#     st.stop()

# # ==========================
# # DATA CLEANING
# # ==========================
# df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# num_cols = [
#     "actual_theft",
#     "possible_return_pipe_theft",
#     "missed_fillings",
#     "amnt_consumed",
#     "consumption_rate",
#     "total_distance_covered",
# ]
# for c in num_cols:
#     if c in df.columns:
#         df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# # Extract week number from "duration" (assuming "Week 1", "Week 2", etc.)
# if "duration" in df.columns:
#     df["week"] = (
#         df["duration"]
#         .astype(str)
#         .str.extract(r"(\d+)")[0]
#         .fillna(0)
#         .astype(int)
#     )
# else:
#     df["week"] = 0

# # ==========================
# # SIDEBAR FILTER
# # ==========================
# st.sidebar.header("🔍 Filters")
# categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
# selected_category = st.sidebar.selectbox("Select Category", categories)

# if selected_category != "All":
#     df = df[df["category"] == selected_category]

# # ==========================
# # KPI METRICS
# # ==========================
# st.title("⛽ Fuel Theft Monitoring Dashboard")

# total_direct_thefts = df["actual_theft"].sum()
# total_return_pipe = df["possible_return_pipe_theft"].sum()
# total_missed_fillings = df["missed_fillings"].sum()

# col1, col2, col3 = st.columns(3)
# col1.metric("💧 Total Direct Thefts", f"{total_direct_thefts:,.0f} Ltrs")
# col2.metric("🧰 Total Return Pipe Thefts", f"{total_return_pipe:,.0f} Ltrs")
# col3.metric("⛔ Total Missed Fillings", f"{total_missed_fillings:,.0f}")

# st.markdown("---")

# # ==========================
# # WEEKLY TRENDS
# # ==========================
# if "week" in df.columns and df["week"].nunique() > 1:
#     theft_trend = (
#         df.groupby("week", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#         .sort_values("week")
#     )

#     col1, col2 = st.columns(2)

#     fig_direct = px.line(
#         theft_trend,
#         x="week",
#         y="actual_theft",
#         markers=True,
#         title="📈 Weekly Direct Theft Trend",
#         color_discrete_sequence=[PRIMARY_GREEN],
#     )
#     fig_direct.update_traces(line=dict(width=3))
#     col1.plotly_chart(fig_direct, use_container_width=True)

#     fig_return = px.line(
#         theft_trend,
#         x="week",
#         y="possible_return_pipe_theft",
#         markers=True,
#         title="📉 Weekly Return Pipe Theft Trend",
#         color_discrete_sequence=[YELLOW],
#     )
#     fig_return.update_traces(line=dict(width=3))
#     col2.plotly_chart(fig_return, use_container_width=True)
# else:
#     st.warning("⚠️ No week data found in 'duration' column.")

# st.markdown("---")

# # ==========================
# # TOP 10 ASSETS PER CATEGORY
# # ==========================
# st.subheader("🏆 Top 10 Assets by Theft Category")

# col1, col2 = st.columns(2)

# # --- Top 10 Direct Theft ---
# top_direct = (
#     df.groupby("reg", as_index=False)["actual_theft"]
#     .sum()
#     .sort_values("actual_theft", ascending=False)
#     .head(10)
# )
# fig_top_direct = px.bar(
#     top_direct,
#     x="reg",
#     y="actual_theft",
#     text="actual_theft",
#     color_discrete_sequence=[PRIMARY_GREEN],
#     title="Top 10 Assets - Direct Theft",
# )
# fig_top_direct.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col1.plotly_chart(fig_top_direct, use_container_width=True)

# # --- Top 10 Return Pipe Theft ---
# top_return = (
#     df.groupby("reg", as_index=False)["possible_return_pipe_theft"]
#     .sum()
#     .sort_values("possible_return_pipe_theft", ascending=False)
#     .head(10)
# )
# fig_top_return = px.bar(
#     top_return,
#     x="reg",
#     y="possible_return_pipe_theft",
#     text="possible_return_pipe_theft",
#     color_discrete_sequence=[YELLOW],
#     title="Top 10 Assets - Return Pipe Theft",
# )
# fig_top_return.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col2.plotly_chart(fig_top_return, use_container_width=True)

# # ==========================
# # RAW DATA PREVIEW
# # ==========================
# st.markdown("---")
# st.subheader("📋 Data Preview")
# st.dataframe(df)

# st.caption("Dashboard auto-updates when Google Sheet data changes.")



#VERSION 2

# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# import plotly.express as px

# # ==========================
# # PAGE CONFIGURATION
# # ==========================
# st.set_page_config(page_title="Fuel Theft Dashboard", layout="wide")

# # --- THEME COLORS ---
# PRIMARY_GREEN = "#228B22"
# YELLOW = "#FFD700"

# st.markdown(f"""
#     <style>
#         [data-testid="stSidebar"] {{
#             background-color: #f7fff7;
#         }}
#         h1, h2, h3 {{
#             color: {PRIMARY_GREEN};
#         }}
#         .stMetric {{
#             background-color: #f0fff0;
#             border-radius: 12px;
#             padding: 10px;
#             border: 1px solid #d4edda;
#         }}
#     </style>
# """, unsafe_allow_html=True)

# # ==========================
# # GOOGLE SHEETS CONNECTION
# # ==========================
# SPREADSHEET_ID = "1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw"
# SHEET_NAME = "ALL"

# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]
# creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
# client = gspread.authorize(creds)

# try:
#     sheet = client.open_by_key(SPREADSHEET_ID)
#     worksheet = sheet.worksheet(SHEET_NAME)
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)
#     st.success("✅ Data loaded successfully from Google Sheets!")
# except Exception as e:
#     st.error(f"❌ Failed to load data: {e}")
#     st.stop()

# # ==========================
# # DATA CLEANING
# # ==========================
# df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# num_cols = [
#     "actual_theft",
#     "possible_return_pipe_theft",
#     "missed_fillings",
#     "amnt_consumed",
#     "consumption_rate",
#     "total_distance_covered",
# ]
# for c in num_cols:
#     if c in df.columns:
#         df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# # Extract week number from "duration" (assuming "Week 1", "Week 2", etc.)
# if "duration" in df.columns:
#     df["week"] = (
#         df["duration"]
#         .astype(str)
#         .str.extract(r"(\d+)")[0]
#         .fillna(0)
#         .astype(int)
#     )
# else:
#     df["week"] = 0

# # ==========================
# # SIDEBAR FILTER
# # ==========================
# st.sidebar.header("🔍 Filters")
# categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
# selected_category = st.sidebar.selectbox("Select Category", categories)

# if selected_category != "All":
#     df = df[df["category"] == selected_category]

# # ==========================
# # KPI METRICS
# # ==========================
# st.title("⛽ Fuel Theft Monitoring Dashboard")

# total_direct_thefts = df["actual_theft"].sum()
# total_return_pipe = df["possible_return_pipe_theft"].sum()
# total_missed_fillings = df["missed_fillings"].sum()
# total_combined = total_direct_thefts + total_return_pipe

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("💧 Direct Thefts", f"{total_direct_thefts:,.0f} Ltrs")
# col2.metric("🧰 Return Pipe Thefts", f"{total_return_pipe:,.0f} Ltrs")
# col3.metric("⛔ Missed Fillings", f"{total_missed_fillings:,.0f}")
# col4.metric("🚛 Total Thefts (Combined)", f"{total_combined:,.0f} Ltrs")

# st.markdown("---")

# # ==========================
# # WEEKLY TRENDS
# # ==========================
# if "week" in df.columns and df["week"].nunique() > 1:
#     theft_trend = (
#         df.groupby("week", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#         .sort_values("week")
#     )
#     theft_trend["total_theft"] = theft_trend["actual_theft"] + theft_trend["possible_return_pipe_theft"]

#     col1, col2, col3 = st.columns(3)

#     # Direct Theft Trend
#     fig_direct = px.line(
#         theft_trend,
#         x="week",
#         y="actual_theft",
#         markers=True,
#         title="📈 Weekly Direct Theft Trend",
#         color_discrete_sequence=[PRIMARY_GREEN],
#     )
#     col1.plotly_chart(fig_direct, use_container_width=True)

#     # Return Pipe Theft Trend
#     fig_return = px.line(
#         theft_trend,
#         x="week",
#         y="possible_return_pipe_theft",
#         markers=True,
#         title="📉 Weekly Return Pipe Theft Trend",
#         color_discrete_sequence=[YELLOW],
#     )
#     col2.plotly_chart(fig_return, use_container_width=True)

#     # Combined Trend
#     fig_total = px.line(
#         theft_trend,
#         x="week",
#         y="total_theft",
#         markers=True,
#         title="💹 Combined Theft Trend (Direct + Return Pipe)",
#         color_discrete_sequence=["#006400"],
#     )
#     col3.plotly_chart(fig_total, use_container_width=True)

#     # Week with highest theft
#     max_week = theft_trend.loc[theft_trend["total_theft"].idxmax()]
#     st.success(
#         f"📅 **Week {int(max_week['week'])}** recorded the **highest total thefts** "
#         f"of **{max_week['total_theft']:,.0f} Ltrs** (Direct: {max_week['actual_theft']:,.0f}, Return: {max_week['possible_return_pipe_theft']:,.0f})."
#     )
# else:
#     st.warning("⚠️ No week data found in 'duration' column.")

# st.markdown("---")

# # ==========================
# # TOP 10 ASSETS PER CATEGORY
# # ==========================
# st.subheader("🏆 Top 10 Assets by Theft Category")

# col1, col2 = st.columns(2)

# # --- Top 10 Direct Theft ---
# top_direct = (
#     df.groupby("reg", as_index=False)["actual_theft"]
#     .sum()
#     .sort_values("actual_theft", ascending=False)
#     .head(10)
# )
# fig_top_direct = px.bar(
#     top_direct,
#     x="reg",
#     y="actual_theft",
#     text="actual_theft",
#     color_discrete_sequence=[PRIMARY_GREEN],
#     title="Top 10 Assets - Direct Theft",
# )
# fig_top_direct.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col1.plotly_chart(fig_top_direct, use_container_width=True)

# # --- Top 10 Return Pipe Theft ---
# top_return = (
#     df.groupby("reg", as_index=False)["possible_return_pipe_theft"]
#     .sum()
#     .sort_values("possible_return_pipe_theft", ascending=False)
#     .head(10)
# )
# fig_top_return = px.bar(
#     top_return,
#     x="reg",
#     y="possible_return_pipe_theft",
#     text="possible_return_pipe_theft",
#     color_discrete_sequence=[YELLOW],
#     title="Top 10 Assets - Return Pipe Theft",
# )
# fig_top_return.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col2.plotly_chart(fig_top_return, use_container_width=True)

# st.markdown("---")

# # ==========================
# # CATEGORY THEFT CONTRIBUTION
# # ==========================
# st.subheader("📦 Theft Contribution by Category")

# if "category" in df.columns:
#     cat_contrib = (
#         df.groupby("category", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#     )
#     cat_contrib["total_theft"] = cat_contrib["actual_theft"] + cat_contrib["possible_return_pipe_theft"]

#     fig_pie = px.pie(
#         cat_contrib,
#         names="category",
#         values="total_theft",
#         title="Category Contribution to Total Theft",
#         color_discrete_sequence=px.colors.sequential.Greens,
#     )
#     st.plotly_chart(fig_pie, use_container_width=True)
# else:
#     st.info("No category data found.")

# st.markdown("---")

# # ==========================
# # RAW DATA PREVIEW
# # ==========================
# st.subheader("📋 Data Preview")
# st.dataframe(df)

# st.caption("Dashboard updates automatically when Google Sheet data changes.")



#Version 3
# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# import plotly.express as px

# # ==========================
# # PAGE CONFIGURATION
# # ==========================
# st.set_page_config(page_title="Menengai Fuel Dashboard", layout="wide")

# # --- THEME COLORS ---
# PRIMARY_GREEN = "#228B22"
# YELLOW = "#FFD700"

# st.markdown(f"""
#     <style>
#         [data-testid="stSidebar"] {{
#             background-color: #f7fff7;
#         }}
#         h1, h2, h3 {{
#             color: {PRIMARY_GREEN};
#         }}
#         .stMetric {{
#             background-color: #f0fff0;
#             border-radius: 12px;
#             padding: 10px;
#             border: 1px solid #d4edda;
#         }}
#     </style>
# """, unsafe_allow_html=True)


# # ==========================
# # GOOGLE SHEETS CONNECTION
# # ==========================
# SPREADSHEET_ID = "1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw"
# SHEET_NAME = "ALL"

# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]
# creds = Credentials.from_service_account_file("service_account.json", scopes=scope)


# # NEW CREDS
# # import json
# # from google.oauth2.service_account import Credentials

# # creds_dict = st.secrets["google_service_account"]
# # creds = Credentials.from_service_account_info(dict(creds_dict), scopes=scope)



# client = gspread.authorize(creds)

# try:
#     sheet = client.open_by_key(SPREADSHEET_ID)
#     worksheet = sheet.worksheet(SHEET_NAME)
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)
#     st.success("✅ Data loaded successfully")
# except Exception as e:
#     st.error(f"❌ Failed to load data: {e}")
#     st.stop()

# # ==========================
# # DATA CLEANING
# # ==========================
# df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# num_cols = [
#     "actual_theft",
#     "possible_return_pipe_theft",
#     "missed_fillings",
#     "amnt_consumed",
#     "consumption_rate",
#     "total_distance_covered",
# ]
# for c in num_cols:
#     if c in df.columns:
#         df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# # Extract week number from "duration"
# if "duration" in df.columns:
#     df["week"] = (
#         df["duration"]
#         .astype(str)
#         .str.extract(r"(\d+)")[0]
#         .fillna(0)
#         .astype(int)
#     )
# else:
#     df["week"] = 0

# # ==========================
# # SIDEBAR FILTERS
# # ==========================
# st.sidebar.header("🔍 Filters")

# categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
# selected_category = st.sidebar.selectbox("Select Category", categories)

# if selected_category != "All":
#     df = df[df["category"] == selected_category]

# weeks = sorted(df["week"].dropna().unique())
# selected_weeks = st.sidebar.multiselect(
#     "Select Week(s)", options=weeks, default=weeks
# )

# if selected_weeks:
#     df = df[df["week"].isin(selected_weeks)]

# #  Button
# st.sidebar.markdown("---")  # adds a visual separator
# st.sidebar.link_button("📄 Open Actual Data", "https://docs.google.com/spreadsheets/d/1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw/edit?usp=sharing")


# # 













# # ==========================
# # KPI METRICS
# # ==========================
# st.title("⛽ Menengai Oil Fuel Monitoring Dashboard")

# total_direct_thefts = df["actual_theft"].sum()
# total_return_pipe = df["possible_return_pipe_theft"].sum()
# total_missed_fillings = df["missed_fillings"].sum()
# total_combined = total_direct_thefts + total_return_pipe

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("💧 Direct Thefts", f"{total_direct_thefts:,.0f} Ltrs")
# col2.metric("🧰 Return Pipe Thefts", f"{total_return_pipe:,.0f} Ltrs")
# col3.metric("⛔ Missed Fillings", f"{total_missed_fillings:,.0f}")
# col4.metric("🚛 Total Thefts (Combined)", f"{total_combined:,.0f} Ltrs")

# st.markdown("---")

# # ==========================
# # WEEKLY TRENDS
# # ==========================
# if "week" in df.columns and df["week"].nunique() > 1:
#     theft_trend = (
#         df.groupby("week", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#         .sort_values("week")
#     )
#     theft_trend["total_theft"] = (
#         theft_trend["actual_theft"] + theft_trend["possible_return_pipe_theft"]
#     )

#     col1, col2, col3 = st.columns(3)

#     fig_direct = px.line(
#         theft_trend,
#         x="week",
#         y="actual_theft",
#         markers=True,
#         title="📈 Weekly Direct Theft Trend",
#         color_discrete_sequence=[PRIMARY_GREEN],
#     )
#     col1.plotly_chart(fig_direct, use_container_width=True)

#     fig_return = px.line(
#         theft_trend,
#         x="week",
#         y="possible_return_pipe_theft",
#         markers=True,
#         title="📉 Weekly Return Pipe Theft Trend",
#         color_discrete_sequence=[YELLOW],
#     )
#     col2.plotly_chart(fig_return, use_container_width=True)

#     fig_total = px.line(
#         theft_trend,
#         x="week",
#         y="total_theft",
#         markers=True,
#         title="💹 Combined Theft Trend (Direct + Return Pipe)",
#         color_discrete_sequence=["#006400"],
#     )
#     col3.plotly_chart(fig_total, use_container_width=True)

#     max_week = theft_trend.loc[theft_trend["total_theft"].idxmax()]
#     st.success(
#         f"📅 **Week {int(max_week['week'])}** recorded the **highest total thefts** "
#         f"of **{max_week['total_theft']:,.0f} Ltrs** "
#         f"(Direct: {max_week['actual_theft']:,.0f}, Return: {max_week['possible_return_pipe_theft']:,.0f})."
#     )
# else:
#     st.warning("⚠️ No week data found in 'duration' column.")

# st.markdown("---")

# # ==========================
# # TOP 10 ASSETS PER CATEGORY
# # ==========================
# st.subheader("🏆 Top 10 Assets by Theft Category")

# col1, col2 = st.columns(2)

# top_direct = (
#     df.groupby("reg", as_index=False)["actual_theft"]
#     .sum()
#     .sort_values("actual_theft", ascending=False)
#     .head(10)
# )
# fig_top_direct = px.bar(
#     top_direct,
#     x="reg",
#     y="actual_theft",
#     text="actual_theft",
#     color_discrete_sequence=[PRIMARY_GREEN],
#     title="Top 10 Assets - Direct Theft",
# )
# fig_top_direct.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col1.plotly_chart(fig_top_direct, use_container_width=True)

# top_return = (
#     df.groupby("reg", as_index=False)["possible_return_pipe_theft"]
#     .sum()
#     .sort_values("possible_return_pipe_theft", ascending=False)
#     .head(10)
# )
# fig_top_return = px.bar(
#     top_return,
#     x="reg",
#     y="possible_return_pipe_theft",
#     text="possible_return_pipe_theft",
#     color_discrete_sequence=[YELLOW],
#     title="Top 10 Assets - Return Pipe Theft",
# )
# fig_top_return.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col2.plotly_chart(fig_top_return, use_container_width=True)

# st.markdown("---")

# # ==========================
# # CATEGORY THEFT CONTRIBUTION
# # ==========================
# st.subheader("📦 Theft Contribution by Category")

# if "category" in df.columns:
#     cat_contrib = (
#         df.groupby("category", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#     )
#     cat_contrib["total_theft"] = (
#         cat_contrib["actual_theft"] + cat_contrib["possible_return_pipe_theft"]
#     )

#     fig_pie = px.pie(
#         cat_contrib,
#         names="category",
#         values="total_theft",
#         title="Category Contribution to Total Theft",
#         color_discrete_sequence=px.colors.sequential.Greens,
#     )
#     st.plotly_chart(fig_pie, use_container_width=True)
# else:
#     st.info("No category data found.")



# START OF LOCAL HOSTED (FINAL VERSION 4)

# Version 4
# ============================================
# Version 4 – Menengai Fuel Dashboard
# ============================================

# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# import plotly.express as px
# import plotly.graph_objects as go

# # ==========================
# # PAGE CONFIGURATION
# # ==========================
# st.set_page_config(page_title="Menengai Fuel Dashboard", layout="wide")

# PRIMARY_GREEN = "#228B22"
# YELLOW = "#FFD700"

# st.markdown(f"""
#     <style>
#         [data-testid="stSidebar"] {{
#             background-color: #f7fff7;
#         }}
#         h1, h2, h3 {{
#             color: {PRIMARY_GREEN};
#         }}
#         .stMetric {{
#             background-color: #f0fff0;
#             border-radius: 12px;
#             padding: 10px;
#             border: 1px solid #d4edda;
#         }}
#     </style>
# """, unsafe_allow_html=True)


# # ==========================
# # GOOGLE SHEETS CONNECTION
# # ==========================
# SPREADSHEET_ID = "1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw"
# SHEET_NAME = "ALL"

# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]
# creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
# client = gspread.authorize(creds)

# try:
#     sheet = client.open_by_key(SPREADSHEET_ID)
#     worksheet = sheet.worksheet(SHEET_NAME)
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)
#     st.success("✅ Data loaded successfully")
# except Exception as e:
#     st.error(f"❌ Failed to load data: {e}")
#     st.stop()

# # ==========================
# # DATA CLEANING
# # ==========================
# df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# num_cols = [
#     "actual_theft",
#     "possible_return_pipe_theft",
#     "missed_fillings",
#     "amnt_consumed",
#     "consumption_rate",
#     "total_distance_covered",
# ]
# for c in num_cols:
#     if c in df.columns:
#         df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# if "duration" in df.columns:
#     df["week"] = (
#         df["duration"]
#         .astype(str)
#         .str.extract(r"(\d+)")[0]
#         .fillna(0)
#         .astype(int)
#     )
# else:
#     df["week"] = 0

# # ==========================
# # SIDEBAR FILTERS
# # ==========================
# st.sidebar.header("🔍 Filters")

# categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
# selected_category = st.sidebar.selectbox("Select Category", categories)

# if selected_category != "All":
#     df = df[df["category"] == selected_category]

# weeks = sorted(df["week"].dropna().unique())
# selected_weeks = st.sidebar.multiselect(
#     "Select Week(s)", options=weeks, default=weeks
# )

# if selected_weeks:
#     df = df[df["week"].isin(selected_weeks)]

# st.sidebar.markdown("---")
# st.sidebar.link_button(
#     "📄 Open Actual Data",
#     "https://docs.google.com/spreadsheets/d/1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw/edit?usp=sharing"
# )

# # ==========================
# # KPI METRICS
# # ==========================
# st.title("⛽ Menengai Oil Fuel Monitoring Dashboard")

# total_direct_thefts = df["actual_theft"].sum()
# total_return_pipe = df["possible_return_pipe_theft"].sum()
# total_missed_fillings = df["missed_fillings"].sum()
# total_combined = total_direct_thefts + total_return_pipe

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("💧 Direct Thefts", f"{total_direct_thefts:,.0f} Ltrs")
# col2.metric("🧰 Return Pipe Thefts", f"{total_return_pipe:,.0f} Ltrs")
# col3.metric("⛔ Missed Fillings", f"{total_missed_fillings:,.0f}")
# col4.metric("🚛 Total Thefts (Combined)", f"{total_combined:,.0f} Ltrs")

# st.markdown("---")

# # ==========================
# # WEEKLY TRENDS
# # ==========================
# if "week" in df.columns and df["week"].nunique() > 1:
#     theft_trend = (
#         df.groupby("week", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#         .sort_values("week")
#     )
#     theft_trend["total_theft"] = (
#         theft_trend["actual_theft"] + theft_trend["possible_return_pipe_theft"]
#     )

#     col1, col2, col3 = st.columns(3)

#     fig_direct = px.line(
#         theft_trend,
#         x="week",
#         y="actual_theft",
#         markers=True,
#         title="📈 Weekly Direct Theft Trend",
#         color_discrete_sequence=[PRIMARY_GREEN],
#     )
#     col1.plotly_chart(fig_direct, use_container_width=True)

#     fig_return = px.line(
#         theft_trend,
#         x="week",
#         y="possible_return_pipe_theft",
#         markers=True,
#         title="📉 Weekly Return Pipe Theft Trend",
#         color_discrete_sequence=[YELLOW],
#     )
#     col2.plotly_chart(fig_return, use_container_width=True)

#     fig_total = px.line(
#         theft_trend,
#         x="week",
#         y="total_theft",
#         markers=True,
#         title="💹 Combined Theft Trend (Direct + Return Pipe)",
#         color_discrete_sequence=["#006400"],
#     )
#     col3.plotly_chart(fig_total, use_container_width=True)

#     max_week = theft_trend.loc[theft_trend["total_theft"].idxmax()]
#     st.success(
#         f"📅 **Week {int(max_week['week'])}** recorded the **highest total thefts** "
#         f"of **{max_week['total_theft']:,.0f} Ltrs** "
#         f"(Direct: {max_week['actual_theft']:,.0f}, Return: {max_week['possible_return_pipe_theft']:,.0f})."
#     )
# else:
#     st.warning("⚠️ No week data found in 'duration' column.")

# st.markdown("---")

# # ==========================
# # TOP 10 ASSETS PER CATEGORY
# # ==========================
# st.subheader("🏆 Top 10 Assets by Theft Category")

# col1, col2 = st.columns(2)

# top_direct = (
#     df.groupby("reg", as_index=False)["actual_theft"]
#     .sum()
#     .sort_values("actual_theft", ascending=False)
#     .head(10)
# )
# fig_top_direct = px.bar(
#     top_direct,
#     x="reg",
#     y="actual_theft",
#     text="actual_theft",
#     color_discrete_sequence=[PRIMARY_GREEN],
#     title="Top 10 Assets - Direct Theft",
# )
# fig_top_direct.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col1.plotly_chart(fig_top_direct, use_container_width=True)

# top_return = (
#     df.groupby("reg", as_index=False)["possible_return_pipe_theft"]
#     .sum()
#     .sort_values("possible_return_pipe_theft", ascending=False)
#     .head(10)
# )
# fig_top_return = px.bar(
#     top_return,
#     x="reg",
#     y="possible_return_pipe_theft",
#     text="possible_return_pipe_theft",
#     color_discrete_sequence=[YELLOW],
#     title="Top 10 Assets - Return Pipe Theft",
# )
# fig_top_return.update_traces(texttemplate="%{text:.0f}", textposition="outside")
# col2.plotly_chart(fig_top_return, use_container_width=True)

# st.markdown("---")

# # ==========================
# # CATEGORY THEFT CONTRIBUTION
# # ==========================
# st.subheader("📦 Theft Contribution by Category")

# if "category" in df.columns:
#     cat_contrib = (
#         df.groupby("category", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
#         .sum()
#     )
#     cat_contrib["total_theft"] = (
#         cat_contrib["actual_theft"] + cat_contrib["possible_return_pipe_theft"]
#     )

#     fig_pie = px.pie(
#         cat_contrib,
#         names="category",
#         values="total_theft",
#         title="Category Contribution to Total Theft",
#         color_discrete_sequence=px.colors.sequential.Greens,
#     )
#     st.plotly_chart(fig_pie, use_container_width=True)
# else:
#     st.info("No category data found.")

# st.markdown("---")

# # =======================================================
# # NEW SECTION: WEEKLY COMPARISON (THEFT vs DISTANCE)
# # =======================================================
# st.subheader("🚚 Weekly Theft vs Distance Analysis by Category")

# df["total_theft"] = df["actual_theft"] + df["possible_return_pipe_theft"]

# weekly_summary = (
#     df.groupby(["week", "category"], as_index=False)
#     .agg({
#         "actual_theft": "sum",
#         "possible_return_pipe_theft": "sum",
#         "total_distance_covered": "sum"
#     })
# )
# weekly_summary["total_theft"] = (
#     weekly_summary["actual_theft"] + weekly_summary["possible_return_pipe_theft"]
# )
# weekly_summary["theft_per_km"] = (
#     weekly_summary["total_theft"] / weekly_summary["total_distance_covered"].replace(0, 1)
# )
# weekly_summary["pct_change_theft"] = (
#     weekly_summary.groupby("category")["total_theft"].pct_change() * 100
# )
# weekly_summary["pct_change_distance"] = (
#     weekly_summary.groupby("category")["total_distance_covered"].pct_change() * 100
# )

# # --- Category selector for trend chart ---
# selected_cat = st.selectbox("Select Category for Trend", sorted(df["category"].unique()))
# cat_df = weekly_summary[weekly_summary["category"] == selected_cat]

# fig = go.Figure()
# fig.add_trace(go.Bar(
#     x=cat_df["week"],
#     y=cat_df["total_theft"],
#     name="Total Theft (Ltrs)",
#     marker_color=PRIMARY_GREEN,
#     yaxis="y1"
# ))
# fig.add_trace(go.Line(
#     x=cat_df["week"],
#     y=cat_df["total_distance_covered"],
#     name="Distance Covered (Km)",
#     line=dict(color=YELLOW, width=3, dash="dot"),
#     yaxis="y2"
# ))
# fig.update_layout(
#     title=f"📊 Weekly Theft vs Distance Trend - {selected_cat}",
#     yaxis=dict(title="Total Theft (Ltrs)"),
#     yaxis2=dict(title="Distance Covered (Km)", overlaying="y", side="right"),
#     xaxis=dict(title="Week"),
#     legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0)"),
# )
# st.plotly_chart(fig, use_container_width=True)

# # --- Theft per km by category ---
# week_cat_pct = (
#     weekly_summary.groupby("category", as_index=False)[["total_theft", "total_distance_covered"]].sum()
# )
# week_cat_pct["theft_per_km"] = (
#     week_cat_pct["total_theft"] / week_cat_pct["total_distance_covered"].replace(0, 1)
# )

# fig_pct = px.bar(
#     week_cat_pct,
#     x="category",
#     y="theft_per_km",
#     title="⚖️ Theft per Km by Category (Overall)",
#     color="category",
#     text=week_cat_pct["theft_per_km"].round(2),
# )
# st.plotly_chart(fig_pct, use_container_width=True)

# # --- Heatmap: Weekly Theft Intensity per Category ---
# pivot_df = weekly_summary.pivot(index="category", columns="week", values="total_theft")
# fig_heatmap = px.imshow(
#     pivot_df,
#     text_auto=True,
#     aspect="auto",
#     title="🔥 Weekly Theft Intensity per Category",
#     color_continuous_scale="Greens"
# )
# st.plotly_chart(fig_heatmap, use_container_width=True)


# END OF LOCAL HOSTED
#Version 4
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

# ==========================
# PAGE CONFIGURATION
# ==========================
st.set_page_config(page_title="Menengai Fuel Dashboard", layout="wide")

# --- THEME COLORS ---
PRIMARY_GREEN = "#228B22"
YELLOW = "#FFD700"

st.markdown(f"""
    <style>
        [data-testid="stSidebar"] {{
            background-color: #f7fff7;
        }}
        h1, h2, h3 {{
            color: {PRIMARY_GREEN};
        }}
        .stMetric {{
            background-color: #f0fff0;
            border-radius: 12px;
            padding: 10px;
            border: 1px solid #d4edda;
        }}
    </style>
""", unsafe_allow_html=True)

# ==========================
# GOOGLE SHEETS CONNECTION
# ==========================
SPREADSHEET_ID = "1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw"
SHEET_NAME = "ALL"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import json
from google.oauth2.service_account import Credentials
creds_dict = st.secrets["google_service_account"]
creds = Credentials.from_service_account_info(dict(creds_dict), scopes=scope)
client = gspread.authorize(creds)

@st.cache_data(ttl=600)
def load_data():
    try:
        sheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.worksheet(SHEET_NAME)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        st.stop()

df = load_data()
st.success("✅ Data loaded successfully")

# ==========================
# DATA CLEANING
# ==========================
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

num_cols = [
    "actual_theft",
    "possible_return_pipe_theft",
    "missed_fillings",
    "amnt_consumed",
    "consumption_rate",
    "total_distance_covered",
]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# Extract week number from "duration"
if "duration" in df.columns:
    df["week"] = (
        df["duration"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
        .fillna(0)
        .astype(int)
    )
else:
    df["week"] = 0

# ==========================
# SIDEBAR FILTERS
# ==========================
st.sidebar.header("🔍 Filters")

categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)
if selected_category != "All":
    df = df[df["category"] == selected_category]

assets = ["All"] + sorted(df["reg"].dropna().unique().tolist())
selected_asset = st.sidebar.selectbox("Select Asset", assets)
if selected_asset != "All":
    df = df[df["reg"] == selected_asset]

weeks = sorted(df["week"].dropna().unique())
selected_weeks = st.sidebar.multiselect(
    "Select Week(s)", options=weeks, default=weeks
)
if selected_weeks:
    df = df[df["week"].isin(selected_weeks)]

#  Button
st.sidebar.markdown("---")
st.sidebar.link_button(
    "📄 Open Actual Data",
    "https://docs.google.com/spreadsheets/d/1IuzUrejc2uhNza1v_DexuwL1HOI8FxeYsuSVHj_HAHw/edit?usp=sharing"
)

# ==========================
# KPI METRICS
# ==========================
st.title("⛽ Menengai Oil Fuel Monitoring Dashboard")

total_direct_thefts = df["actual_theft"].sum()
total_return_pipe = df["possible_return_pipe_theft"].sum()
total_missed_fillings = df["missed_fillings"].sum()
total_combined = total_direct_thefts + total_return_pipe
total_consumed = df["amnt_consumed"].sum()
avg_rate = df["consumption_rate"].mean()

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("💧 Direct Thefts", f"{total_direct_thefts:,.0f} Ltrs")
col2.metric("🧰 Return Pipe Thefts", f"{total_return_pipe:,.0f} Ltrs")
col3.metric("⛔ Missed Fillings", f"{total_missed_fillings:,.0f}")
col4.metric("🚛 Total Thefts", f"{total_combined:,.0f} Ltrs")
col5.metric("⛽ Fuel Consumed", f"{total_consumed:,.0f} Ltrs")
col6.metric("⚙️ Avg Consumption Rate", f"{avg_rate:,.2f} L/Hr")

st.markdown("---")

# ==========================
# WEEKLY TRENDS
# ==========================
if "week" in df.columns and df["week"].nunique() > 1:
    theft_trend = (
        df.groupby("week", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
        .sum()
        .sort_values("week")
    )
    theft_trend["total_theft"] = (
        theft_trend["actual_theft"] + theft_trend["possible_return_pipe_theft"]
    )

    col1, col2, col3 = st.columns(3)

    fig_direct = px.line(
        theft_trend,
        x="week",
        y="actual_theft",
        markers=True,
        title="📈 Weekly Direct Theft Trend",
        color_discrete_sequence=[PRIMARY_GREEN],
    )
    col1.plotly_chart(fig_direct, use_container_width=True)

    fig_return = px.line(
        theft_trend,
        x="week",
        y="possible_return_pipe_theft",
        markers=True,
        title="📉 Weekly Return Pipe Theft Trend",
        color_discrete_sequence=[YELLOW],
    )
    col2.plotly_chart(fig_return, use_container_width=True)

    fig_total = px.line(
        theft_trend,
        x="week",
        y="total_theft",
        markers=True,
        title="💹 Combined Theft Trend (Direct + Return Pipe)",
        color_discrete_sequence=["#006400"],
    )
    col3.plotly_chart(fig_total, use_container_width=True)

    max_week = theft_trend.loc[theft_trend["total_theft"].idxmax()]
    st.success(
        f"📅 **Week {int(max_week['week'])}** recorded the **highest total thefts** "
        f"of **{max_week['total_theft']:,.0f} Ltrs** "
        f"(Direct: {max_week['actual_theft']:,.0f}, Return: {max_week['possible_return_pipe_theft']:,.0f})."
    )
else:
    st.warning("⚠️ No week data found in 'duration' column.")

st.markdown("---")

# ==========================
# TOP 10 ASSETS PER CATEGORY
# ==========================
st.subheader("🏆 Top 10 Assets by Theft Category")

col1, col2 = st.columns(2)

top_direct = (
    df.groupby("reg", as_index=False)["actual_theft"]
    .sum()
    .sort_values("actual_theft", ascending=False)
    .head(10)
)
fig_top_direct = px.bar(
    top_direct,
    x="reg",
    y="actual_theft",
    text="actual_theft",
    color_discrete_sequence=[PRIMARY_GREEN],
    title="Top 10 Assets - Direct Theft",
)
fig_top_direct.update_traces(texttemplate="%{text:.0f}", textposition="outside")
col1.plotly_chart(fig_top_direct, use_container_width=True)

top_return = (
    df.groupby("reg", as_index=False)["possible_return_pipe_theft"]
    .sum()
    .sort_values("possible_return_pipe_theft", ascending=False)
    .head(10)
)
fig_top_return = px.bar(
    top_return,
    x="reg",
    y="possible_return_pipe_theft",
    text="possible_return_pipe_theft",
    color_discrete_sequence=[YELLOW],
    title="Top 10 Assets - Return Pipe Theft",
)
fig_top_return.update_traces(texttemplate="%{text:.0f}", textposition="outside")
col2.plotly_chart(fig_top_return, use_container_width=True)

st.markdown("---")

# ==========================
# CATEGORY THEFT CONTRIBUTION
# ==========================
st.subheader("📦 Theft Contribution by Category")

if "category" in df.columns:
    cat_contrib = (
        df.groupby("category", as_index=False)[["actual_theft", "possible_return_pipe_theft"]]
        .sum()
    )
    cat_contrib["total_theft"] = (
        cat_contrib["actual_theft"] + cat_contrib["possible_return_pipe_theft"]
    )

    fig_pie = px.pie(
        cat_contrib,
        names="category",
        values="total_theft",
        title="Category Contribution to Total Theft",
        color_discrete_sequence=px.colors.sequential.Greens,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No category data found.")
