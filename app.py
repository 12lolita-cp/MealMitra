from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ============================================================
# NIErnaya Dashboard | SDG 2 - Zero Hunger
# Uses the cleaned, integrated district dataset exported from
# 01_Data_Understanding.ipynb and reports its executed findings.
# ============================================================
st.set_page_config(
    page_title="MealMitra | SDG 2",
    page_icon="🍽️",
    layout="wide"
)

DATA_PATH = Path(__file__).parent / "data" / "cleaned" / "NIErnaya_dashboard_data.csv"
st.title("MealMitra")
st.subheader("Bridging the Gap Between Agriculture and Nutrition")
st.markdown(
    "**SDG 2 – Zero Hunger**  \n"
    "District-level analysis of agricultural yield, child malnutrition and "
    "selected socioeconomic indicators."
)

if not DATA_PATH.exists():
    st.error(
        "Dashboard dataset not found. Save NIErnaya_dashboard_data.csv in "
        "the project's data/cleaned folder."
    )
    st.stop()

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    required = ["State_Name", "District_Name", "Stunting", "Wasting", "Underweight"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"Required columns are missing from the CSV: {missing}")
    return data

try:
    df = load_data(DATA_PATH)
except Exception as exc:
    st.error(f"Could not load the dashboard dataset: {exc}")
    st.stop()

# -------------------- Sidebar filters --------------------
st.sidebar.header("Dashboard Filters")
states = ["All States"] + sorted(df["State_Name"].dropna().astype(str).unique().tolist())
selected_state = st.sidebar.selectbox("Select state / UT", states)
filtered = df.copy()
if selected_state != "All States":
    filtered = filtered[filtered["State_Name"] == selected_state]

st.sidebar.caption(f"Showing {filtered['District_Name'].nunique()} districts")

# -------------------- Overview --------------------
st.header("1. District Overview")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Districts analysed", f"{filtered['District_Name'].nunique():,}")
k2.metric("Average stunting", f"{filtered['Stunting'].mean():.1f}%")
k3.metric("Average wasting", f"{filtered['Wasting'].mean():.1f}%")
k4.metric("Average underweight", f"{filtered['Underweight'].mean():.1f}%")
st.caption(
    "The integrated dataset contains 562 matched districts. Individual statistical "
    "analyses may have smaller sample sizes where crop-yield observations are unavailable."
)
st.divider()

# -------------------- Nutrition --------------------
st.header("2. Child Malnutrition Profile")
nutrition_cols = ["Stunting", "Wasting", "Underweight"]
avg_nutrition = filtered[nutrition_cols].mean()
fig, ax = plt.subplots(figsize=(8, 4))
avg_nutrition.plot(kind="bar", ax=ax)
ax.set_ylabel("Average prevalence (%)")
ax.set_xlabel("")
ax.set_title("Average child malnutrition indicators")
ax.tick_params(axis="x", rotation=0)
st.pyplot(fig, use_container_width=False)
plt.close(fig)

left, right = st.columns(2)
with left:
    st.subheader("Highest stunting prevalence")
    top_stunting = filtered.nlargest(10, "Stunting").sort_values("Stunting")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(top_stunting["District_Name"], top_stunting["Stunting"])
    ax.set_xlabel("Stunting (%)")
    ax.set_title("Top 10 districts")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
with right:
    st.subheader("Nutrition indicator data")
    st.dataframe(
        filtered[["State_Name", "District_Name"] + nutrition_cols]
        .sort_values("Stunting", ascending=False)
        .round(2),
        use_container_width=True,
        hide_index=True,
    )
st.divider()

# -------------------- Agriculture --------------------
st.header("3. Agricultural Productivity")
crop_cols = [c for c in ["Rice", "Wheat", "Maize"] if c in filtered.columns]
if crop_cols:
    crop_means = filtered[crop_cols].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    crop_means.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average yield (as recorded in source data)")
    ax.set_xlabel("")
    ax.set_title("Average district crop yield")
    ax.tick_params(axis="x", rotation=0)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
    st.caption(
        "Crop yields are agricultural productivity measures; they do not directly measure "
        "household food availability, affordability, dietary diversity or access."
    )
st.divider()

# -------------------- Correlation findings from notebook --------------------
st.header("4. Statistical Findings: Crop Yield and Nutrition")
st.markdown("**Pearson correlation coefficients reproduced in `01_Data_Understanding.ipynb`.**")
crop_corr = pd.DataFrame(
    {
        "Stunting": [-0.210404, -0.113418, -0.124833],
        "Wasting": [-0.108525, -0.136862, 0.007293],
        "Underweight": [-0.125618, -0.112453, 0.002193],
    },
    index=["Rice", "Wheat", "Maize"],
)
st.dataframe(crop_corr.round(3), use_container_width=True)
st.info(
    "Interpretation: crop-yield correlations with malnutrition are weak. "
    "These bivariate associations do not establish that higher crop yield causes "
    "lower malnutrition."
)

st.subheader("Socioeconomic indicators and stunting")
socio_corr = pd.DataFrame(
    {"Pearson correlation with stunting": [-0.5689, -0.5221, -0.4429, -0.4246]},
    index=["Women's education", "Improved sanitation", "Clean cooking fuel", "Electricity"],
)
st.dataframe(socio_corr.round(3), use_container_width=True)
st.markdown(
    "The notebook found moderate negative bivariate associations between these "
    "socioeconomic indicators and stunting. They should be interpreted as associations, "
    "not causal effects."
)
st.divider()

# -------------------- Regression --------------------
st.header("5. Multiple Linear Regression")
st.markdown("**OLS results from the notebook's five-predictor models.**")
regression = pd.DataFrame(
    [
        ["Stunting", "Rice", -0.1257, 0.7444, 0.4330],
        ["Stunting", "Women's education", -0.1973, 0.0001, 0.4330],
        ["Stunting", "Sanitation", -0.1435, 0.0001, 0.4330],
        ["Stunting", "Clean fuel", -0.0180, 0.2973, 0.4330],
        ["Stunting", "Electricity", -0.4084, 0.0001, 0.4330],
        ["Wasting", "Rice", -0.3549, 0.2836, 0.1578],
        ["Wasting", "Women's education", -0.1098, 0.0001, 0.1578],
        ["Wasting", "Sanitation", -0.1087, 0.0001, 0.1578],
        ["Wasting", "Clean fuel", 0.0368, 0.0131, 0.1578],
        ["Wasting", "Electricity", 0.0244, 0.6682, 0.1578],
        ["Underweight", "Rice", 0.5246, 0.2259, 0.4272],
        ["Underweight", "Women's education", -0.2105, 0.0001, 0.4272],
        ["Underweight", "Sanitation", -0.2783, 0.0001, 0.4272],
        ["Underweight", "Clean fuel", 0.0047, 0.8092, 0.4272],
        ["Underweight", "Electricity", -0.0985, 0.1865, 0.4272],
    ],
    columns=["Outcome", "Predictor", "Coefficient", "P-value (displayed)", "Model R²"],
)
st.dataframe(regression, use_container_width=True, hide_index=True)
st.caption(
    "P-values displayed as 0.0001 represent values reported as <0.0001 in the notebook; "
    "they are not exactly 0.0001. Coefficients are unstandardised."
)
st.markdown(
    "**Main interpretation:** women's education and sanitation had statistically "
    "significant negative conditional associations with all three outcomes. Electricity "
    "was significant for stunting in this model. Rice was not statistically significant "
    "for any outcome. These are observational models and do not establish causation."
)
st.divider()

# -------------------- VIF and PCA --------------------
st.header("6. Model Diagnostics and PCA")
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Variance Inflation Factor (VIF)")
    vif = pd.DataFrame(
        {"Predictor": ["Rice", "Women's education", "Sanitation", "Clean fuel", "Electricity"],
         "VIF": [1.341, 2.128, 1.646, 2.018, 1.205]}
    )
    st.dataframe(vif, hide_index=True, use_container_width=True)
    st.caption("All VIF values are below 5; no concerning multicollinearity was indicated by this check.")
with col_b:
    st.subheader("PCA explained variance")
    pca = pd.DataFrame(
        {"Component": ["PC1", "PC2", "PC3", "PC4"],
         "Explained variance (%)": [59.00, 18.87, 13.34, 8.79]}
    )
    st.dataframe(pca, hide_index=True, use_container_width=True)
    st.metric("Variance explained by first two components", "77.87%")
    st.caption("PC1 represents a broad shared socioeconomic pattern; PC2 is largely an electricity contrast.")
st.divider()

# -------------------- Random Forest --------------------
st.header("7. Random Forest Model Performance")
rf = pd.DataFrame(
    [
        ["Stunting", 5.045, 6.621, 0.461],
        ["Wasting", 4.452, 5.470, 0.173],
        ["Underweight", 6.023, 7.775, 0.468],
    ],
    columns=["Outcome", "MAE", "RMSE", "R²"],
)
st.dataframe(rf, use_container_width=True, hide_index=True)
st.markdown(
    "The test-set R² values indicate moderate predictive performance for stunting and "
    "underweight, and weaker performance for wasting. This evaluation used a single "
    "80/20 random split; cross-validation and external/state-level validation were not performed."
)
st.divider()

# -------------------- District prioritisation --------------------
st.header("8. District Prioritisation")
st.markdown(
    "The notebook classified districts using the 67th-percentile thresholds for rice "
    "yield and stunting. The high-rice / high-stunting group contains 44 districts."
)
priority = filtered.copy()
priority["Malnutrition_Priority_Score"] = priority[nutrition_cols].mean(axis=1)
if "Agriculture_Level" in priority.columns and "Malnutrition_Level" in priority.columns:
    paradox = priority[
        (priority["Agriculture_Level"].astype(str).str.lower().str.contains("high"))
        & (priority["Malnutrition_Level"].astype(str).str.lower().str.contains("high"))
    ].copy()
else:
    # Recreate the notebook's 67th-percentile classification within the displayed subset.
    rice_cut = df["Rice"].quantile(0.67)
    stunt_cut = df["Stunting"].quantile(0.67)
    paradox = priority[(priority["Rice"] >= rice_cut) & (priority["Stunting"] >= stunt_cut)]

if selected_state == "All States":
    st.metric("High-rice / high-stunting districts", "44 (notebook result)")
else:
    st.metric("High-rice / high-stunting districts in selected state", f"{len(paradox)}")

st.subheader("Highest malnutrition priority scores in the selected view")
st.caption("Score = unweighted mean of stunting, wasting and underweight percentages. It is a descriptive ranking, not a validated clinical index.")
top_priority = priority.nlargest(15, "Malnutrition_Priority_Score")
st.dataframe(
    top_priority[["State_Name", "District_Name", "Stunting", "Wasting", "Underweight", "Malnutrition_Priority_Score"]]
    .round(2),
    use_container_width=True,
    hide_index=True,
)

st.subheader("High agricultural yield and high stunting")
if not paradox.empty:
    st.dataframe(
        paradox[["State_Name", "District_Name", "Rice", "Stunting", "Wasting", "Underweight"]]
        .sort_values("Stunting", ascending=False)
        .round(2),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.write("No districts in this filtered view meet both high-yield and high-stunting criteria.")
st.divider()

# -------------------- Limitations --------------------
st.header("9. Research Limitations")
st.markdown(
    "- District-level crop yield is not a direct measure of household food access or diet quality.\n"
    "- The analysis is observational; correlation and regression do not establish causation.\n"
    "- The available analysis does not directly link district-level food-distribution delivery or household receipt to nutrition outcomes; therefore, it cannot establish PDS effectiveness.\n"
    "- District matching and missing crop observations lead to different sample sizes across analyses.\n"
    "- Random Forest performance was evaluated using one random train/test split.\n"
    "- The district boundary map was not included because the GeoJSON matching attempt was not fully validated."
)

# -------------------- Data explorer / download --------------------
st.header("10. Explore and Download District Data")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button(
    "Download filtered district dataset",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="NIErnaya_filtered_district_data.csv",
    mime="text/csv",
)
st.caption("NIErnaya | SDG 2 – Zero Hunger | Analysis source: 01_Data_Understanding.ipynb")
