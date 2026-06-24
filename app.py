import streamlit as st
import pandas as pd

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="SmartRx NG",
    page_icon="💊",
    layout="wide"
)

# ======================
# CUSTOM STYLING
# ======================
st.markdown("""
<style>

.stApp {
    background: #FAFBFC;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.hero {
    background: linear-gradient(
    135deg,
    #14467C,
    #1E5A9B
    );
    color: white;
    padding: 35px;
    border-radius: 20px;
    border-left: 10px solid #F9CC48;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.20);
    backdrop-filter: blur(12px);
}

.card {
    background: #FFFFFF;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(20,70,124,0.10);
    box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
}

.safe {
    background-color: #D1FAE5;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid green;
}

.warning {
    background-color: #FEF3C7;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid orange;
}

.danger {
    background-color: #FEE2E2;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid red;
}

.footer {
    text-align: center;
    padding: 20px;
    color: #444;
    margin-top: 30px;
}

h1, h2, h3, h4 {
    color: black;
}

</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
try:
    df = pd.read_csv("medicines.csv")
except:
    st.error("medicines.csv not found.")
    st.stop()

medicine_list = sorted(df["Medicine"].tolist())

# ======================
# SIDEBAR
# ======================
st.sidebar.title("💊 SmartRx NG")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "ℹ️ About",
        "📘 How To Use",
        "🔍 Verify Your Medicines"
    ]
)

# ======================
# HOME PAGE
# ======================
if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
    <h1>💊 SmartRx NG</h1>
    <h3>Your Medication Safety Companion</h3>

    SmartRx NG helps users identify duplicate active ingredients,
    medicine conflicts, and important safety warnings before
    taking medications.

   </div>
""", unsafe_allow_html=True)

st.success(
    "📱 Add SmartRx NG to your Home Screen for faster access."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>🔍 Verify Medicines</h3>
    Check medicines for duplicate ingredients and safety concerns.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>⚠ Detect Risks</h3>
    Identify common medicine conflicts and overdose risks.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>📋 Get Guidance</h3>
    Receive practical medication recommendations.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="
background:#FFF8DC;
padding:25px;
border-radius:20px;
border-left:8px solid #F9CC48;
box-shadow:0 8px 20px rgba(0,0,0,0.08);
margin-top:20px;
">

<h3 style="color:#14467C;">💡 Why SmartRx NG?</h3>

<p style="color:#111111;">
Many medicines sold in Nigeria have different brand names but contain the same active ingredient.
</p>

<p style="color:#111111;">
Taking multiple medicines unknowingly may increase overdose risks and medication-related complications.
</p>

<p style="color:#111111;">
SmartRx NG helps users make safer decisions before use.
</p>

</div>
""", unsafe_allow_html=True)

# ======================
# VERIFY PAGE
# ======================
elif page == "🔍 Verify Your Medicines":

    st.title("🔍 Verify Your Medicines")

    st.write(
        "Select up to five medicines and check for possible issues."
    )

    med1 = st.selectbox(
       "Add Medicine 1",
        [""] + medicine_list
    )

    med2 = st.selectbox(
       "Add Medicine 2",
        [""] + medicine_list
    )

    med3 = st.selectbox(
        "Add Medicine 3",
        [""] + medicine_list
    )

    med4 = st.selectbox(
        "Add Medicine 4",
        [""] + medicine_list
    )

    med5 = st.selectbox(
        "Add Medicine 5",
        [""] + medicine_list
    )

    if st.button("CHECK SAFETY"):

        selected = [
            m for m in
            [med1, med2, med3, med4, med5]
            if m != ""
        ]

        if len(selected) == 0:

            st.warning(
                "Please select at least one medicine."
            )

        else:

            chosen = df[df["Medicine"].isin(selected)]

            st.subheader("Detected Medicines")

            st.dataframe(
                chosen[
                    [
                        "Medicine",
                        "Ingredient",
                        "Category"
                    ]
                ],
                use_container_width=True
            )

            ingredients = chosen["Ingredient"].tolist()

            ingredient_count = {}

            for item in ingredients:
                ingredient_count[item] = (
                    ingredient_count.get(item, 0) + 1
                )

            duplicates = [
                ingredient
                for ingredient, count
                in ingredient_count.items()
                if count > 1
            ]

            has_warning = False

            if duplicates:

                has_warning = True

                st.markdown(
                    """
                    <div class="danger">
                    <h3>🚨 Duplicate Ingredient Detected</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                for d in duplicates:
                    st.write(
                        f"Duplicate Active Ingredient: {d}"
                    )

            categories = chosen["Category"].tolist()

            if categories.count("NSAID") > 1:

                has_warning = True

                st.markdown(
                    """
                    <div class="warning">
                    <h3>⚠ NSAID Conflict Warning</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write(
                    "Multiple NSAID medicines detected."
                )

                st.write(
                    "Combining NSAIDs may increase the risk "
                    "of stomach irritation and bleeding."
                )

            if not has_warning:

                st.markdown(
                    """
                    <div class="safe">
                    <h3>✅ No Major Issues Detected</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

           st.info(
    "⚠ Disclaimer: This tool provides information only. "
    "Always consult a pharmacist or doctor before making medication decisions."
)

st.subheader("Recommendations")

st.write(
    "• Follow dosage instructions carefully."
)

st.write(
    "• Avoid medicines with duplicate active ingredients."
)

st.write(
    "• Consult a pharmacist when uncertain."
)

st.write(
    "• Complete prescribed antibiotic courses."
)

st.write(
    "• Read medicine labels before use."
)
# ======================
# HOW TO USE
# ======================
elif page == "📘 How To Use":

    st.title("📘 How To Use SmartRx NG")

    st.markdown("""
    ### Step 1
    Select the medicines you are currently taking.

    ### Step 2
    Click CHECK SAFETY.

    ### Step 3
    Review detected ingredients.

    ### Step 4
    Read warnings carefully.

    ### Step 5
    Follow recommendations provided.

    ### Step 6
    Consult a healthcare professional when necessary.
    """)

# ======================
# ABOUT
# ======================
elif page == "ℹ️ About":

    st.title("ℹ️ About SmartRx NG")

    st.write("""
    SmartRx NG is a medication safety support system
    developed to reduce medication errors caused by
    duplicate active ingredients and unsafe medicine
    combinations.

    The platform uses a structured pharmaceutical
    database and rule-based analysis to help users
    make safer medication decisions.

    This project was developed as a health-tech
    innovation showcase for Nigeria.
    """)

# ======================
# FOOTER
# ======================
st.markdown(
    "<div style='text-align:center; color:#555555; margin-top:30px;'>"
    "SmartRx NG © 2026 • Promoting safer medication decisions 🇳🇬"
    "</div>",
    unsafe_allow_html=True
)
