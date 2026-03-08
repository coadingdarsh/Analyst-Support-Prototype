from __future__ import annotations

# Path helps us build a reliable file path to the CSV file
from pathlib import Path

# pandas is used to load and work with the case data
import pandas as pd

# streamlit is used to build the UI
import streamlit as st


# This points to: /data/mock_cases.csv
# It assumes your app.py file is in the main project folder
DATA_PATH = Path(__file__).parent / "data" / "mock_cases.csv"


# These are the basic rule weights for suspicious signals.
# Each key is a column in the CSV.
# Each value contains:
#   (risk points, human-readable reason)
WEIGHTS = {
    "vpn_detected": (25, "VPN detected"),
    "proxy_detected": (20, "Proxy detected"),
    "gps_spoof_flag": (30, "GPS spoofing signal"),
    "emulator_flag": (15, "Emulator environment"),
    "remote_desktop_flag": (15, "Remote desktop signal"),
    "device_mismatch": (15, "Device mismatch"),
    "previous_fraud_flag": (25, "Prior fraud history"),
}


def load_data() -> pd.DataFrame:
    """
    Load the mock case data from the CSV file.

    Returns:
        A pandas DataFrame containing all flagged cases.
    """
    return pd.read_csv(DATA_PATH)


def score_case(row: pd.Series) -> tuple[int, list[str]]:
    """
    Calculate the risk score for one case.

    How scoring works:
    - Every suspicious signal adds points
    - We also check for country mismatch, failed attempts,
      suspicious session volume, and high transaction value

    Args:
        row: One row from the DataFrame representing a single case

    Returns:
        score: total numeric risk score
        reasons: list of human-readable reasons explaining the score
    """
    score = 0
    reasons: list[str] = []

    # Check each binary signal from the WEIGHTS dictionary
    for col, (points, label) in WEIGHTS.items():
        if int(row[col]) == 1:
            score += points
            reasons.append(label)

    # If detected country and claimed country do not match,
    # we treat that as suspicious
    if row["detected_country"] != row["claimed_country"]:
        score += 20
        reasons.append("Claimed vs detected country mismatch")

    # Many failed attempts in a short time can indicate suspicious behavior
    if int(row["failed_attempts_24h"]) >= 5:
        score += 10
        reasons.append("High failed-attempt volume")

    # Repeated suspicious sessions across a week can also be a risk signal
    if int(row["suspicious_sessions_7d"]) >= 4:
        score += 10
        reasons.append("Elevated suspicious session count")

    # Higher transaction value may increase urgency / potential exposure
    if float(row["transaction_value"]) >= 500:
        score += 10
        reasons.append("High-value transaction")

    return score, reasons


def risk_level(score: int) -> str:
    """
    Convert a numeric score into a simple risk category.

    Args:
        score: total risk score

    Returns:
        "High", "Medium", or "Low"
    """
    if score >= 60:
        return "High"
    if score >= 30:
        return "Medium"
    return "Low"


def recommended_action(level: str) -> str:
    """
    Return a simple next-step recommendation based on the risk level.

    Args:
        level: risk level string

    Returns:
        A suggested analyst action
    """
    return {
        "High": "Escalate immediately for manual review and restrict high-risk actions until verification.",
        "Medium": "Route to analyst review queue and request additional verification if needed.",
        "Low": "Allow with monitoring and retain signals for future pattern analysis.",
    }[level]


def narrative(case_id: str, level: str, score: int, reasons: list[str]) -> str:
    """
    Build a short analyst-style summary for the selected case.

    We only show the top 3 reasons to keep the summary concise.

    Args:
        case_id: unique case id
        level: risk level
        score: total score
        reasons: list of reasons that contributed to the score

    Returns:
        A readable investigation summary paragraph
    """
    top = reasons[:3] if reasons else ["No material signals"]
    reason_text = ", ".join(top)

    return (
        f"Case {case_id} was automatically summarized as {level} risk with a score of {score}. "
        f"Top drivers: {reason_text}. "
        f"Recommended next step: {recommended_action(level)}"
    )


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add calculated fields to the raw case data.

    For every case, we create:
    - risk_score
    - risk_level
    - reason_summary
    - recommended_action
    - generated_summary

    Args:
        df: raw DataFrame

    Returns:
        Enriched DataFrame with extra columns
    """
    scores = []
    reasons = []
    levels = []
    actions = []
    summaries = []

    # Go row by row and calculate all outputs
    for _, row in df.iterrows():
        score, reason_list = score_case(row)
        level = risk_level(score)
        action = recommended_action(level)
        summary = narrative(row["case_id"], level, score, reason_list)

        scores.append(score)
        reasons.append("; ".join(reason_list) if reason_list else "None")
        levels.append(level)
        actions.append(action)
        summaries.append(summary)

    # Copy the original dataframe so we do not modify it directly
    out = df.copy()

    # Add all the new calculated columns
    out["risk_score"] = scores
    out["risk_level"] = levels
    out["reason_summary"] = reasons
    out["recommended_action"] = actions
    out["generated_summary"] = summaries

    return out


def show_risk_badge(level: str) -> None:
    """
    Show a colored badge depending on the risk level.

    High   -> red
    Medium -> yellow
    Low    -> green
    """
    if level == "High":
        st.error(f"Risk Level: {level}")
    elif level == "Medium":
        st.warning(f"Risk Level: {level}")
    else:
        st.success(f"Risk Level: {level}")


def format_binary_flag(value: int) -> str:
    """
    Convert 1/0 values into easy-to-read Yes/No text.

    Args:
        value: integer flag from the dataset

    Returns:
        "Yes" or "No"
    """
    return "Yes" if int(value) == 1 else "No"


def main() -> None:
    """
    Main Streamlit app.

    This function:
    1. sets up the page
    2. loads and enriches the data
    3. lets the user choose a case
    4. shows the investigation summary
    5. shows signals and operations dashboard
    """
    # Streamlit page settings
    st.set_page_config(
        page_title="Fraud Investigation Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Top title and subtitle
    st.title("Fraud Investigation Assistant (Prototype)")
    st.caption(
        "Internal workflow prototype exploring automation for case triage and investigation summaries."
    )

    # Load raw data, then enrich it with calculated outputs
    df = enrich(load_data())

    # Sidebar = where the user selects a case and filters the queue
    st.sidebar.header("Investigation Queue")
    st.sidebar.write(
        "Select a flagged case to review how risk signals are summarized into a consistent first-pass analyst report."
    )

    # Case selector in sidebar
    selected_case = st.sidebar.selectbox(
        "Choose a case",
        df["case_id"].tolist(),
    )

    # Optional filter so the user can filter queue by risk level
    selected_level = st.sidebar.multiselect(
        "Filter queue by risk level",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
    )

    # Apply the selected filter to the table shown in the dashboard
    filtered_df = df[df["risk_level"].isin(selected_level)]

    # Grab the single selected case from the full dataframe
    case = df[df["case_id"] == selected_case].iloc[0]

    st.markdown("---")

    # =========================
    # CASE OVERVIEW HEADER
    # =========================
    # Left side shows case details
    # Right side shows risk badge and status
    left_header, right_header = st.columns([2.2, 1])

    with left_header:
        st.subheader(f"Case {case['case_id']} – Investigation Overview")
        st.markdown(
            f"""
**Account ID:** {case['account_id']}  
**Detected Location:** {case['detected_country']}  
**Claimed Location:** {case['claimed_country']}  
**Risk Score:** {int(case['risk_score'])}  
**Failed Attempts (24h):** {int(case['failed_attempts_24h'])}
"""
        )

    with right_header:
        show_risk_badge(case["risk_level"])
        st.markdown("**Suggested Workflow Status:**")

        if case["risk_level"] == "High":
            st.markdown("Escalation recommended")
        elif case["risk_level"] == "Medium":
            st.markdown("Analyst review recommended")
        else:
            st.markdown("Monitoring recommended")

    st.markdown("---")

    # Tabs make the app feel more like a real internal tool
    tab1, tab2, tab3 = st.tabs(
        ["Investigation Summary", "Risk Signals", "Operations Dashboard"]
    )

    # =========================
    # TAB 1: INVESTIGATION SUMMARY
    # =========================
    with tab1:
        summary_col, action_col = st.columns([1.5, 1])

        with summary_col:
            st.subheader("Automated Case Summary")
            st.write(case["generated_summary"])

            st.subheader("Key Risk Drivers")
            for reason in case["reason_summary"].split("; "):
                st.write(f"• {reason}")

        with action_col:
            st.subheader("Recommended Action")

            # Color the action box based on risk level
            if case["risk_level"] == "High":
                st.error(case["recommended_action"])
            elif case["risk_level"] == "Medium":
                st.warning(case["recommended_action"])
            else:
                st.success(case["recommended_action"])

            # This simulates a simple analyst workflow step
            st.subheader("Analyst Decision")
            decision = st.selectbox(
                "Select disposition",
                ["Escalate", "Request Verification", "Monitor", "Close Case"],
                key="decision_select",
            )

            # Analyst can type a quick note
            analyst_note = st.text_area(
                "Analyst Notes",
                placeholder="Add a short note for the investigation log...",
                height=120,
            )

            # Prototype action button
            if st.button("Submit Decision"):
                st.success("Decision recorded in investigation log (prototype).")
                st.caption(f"Selected decision: {decision}")

                if analyst_note.strip():
                    st.caption(f"Latest note: {analyst_note}")

    # =========================
    # TAB 2: RISK SIGNALS
    # =========================
    with tab2:
        st.subheader("Signal Intelligence")

        # Split the signal view into two columns for readability
        signal_left, signal_right = st.columns(2)

        with signal_left:
            st.markdown("**Location & Access Signals**")
            st.write(f"Detected Country: {case['detected_country']}")
            st.write(f"Claimed Country: {case['claimed_country']}")
            st.write(f"VPN Detected: {format_binary_flag(case['vpn_detected'])}")
            st.write(f"Proxy Detected: {format_binary_flag(case['proxy_detected'])}")
            st.write(f"GPS Spoofing Flag: {format_binary_flag(case['gps_spoof_flag'])}")

            st.markdown("**Environment Signals**")
            st.write(f"Emulator Flag: {format_binary_flag(case['emulator_flag'])}")
            st.write(
                f"Remote Desktop Flag: {format_binary_flag(case['remote_desktop_flag'])}"
            )
            st.write(f"Device Mismatch: {format_binary_flag(case['device_mismatch'])}")

        with signal_right:
            st.markdown("**Behavioral & History Signals**")
            st.write(f"Failed Attempts (24h): {int(case['failed_attempts_24h'])}")
            st.write(
                f"Suspicious Sessions (7d): {int(case['suspicious_sessions_7d'])}"
            )
            st.write(
                f"Previous Fraud History: {format_binary_flag(case['previous_fraud_flag'])}"
            )
            st.write(f"Transaction Value: ${float(case['transaction_value']):,.2f}")

            st.markdown("**Interpretation**")
            st.write(
                "This section brings together the raw risk indicators an analyst would normally review manually before making a triage decision."
            )

    # =========================
    # TAB 3: OPERATIONS DASHBOARD
    # =========================
    with tab3:
        st.subheader("Operational Overview")

        # Small KPI row for the filtered queue
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Cases", len(filtered_df))
        c2.metric("High Risk", int((filtered_df["risk_level"] == "High").sum()))
        c3.metric("Medium Risk", int((filtered_df["risk_level"] == "Medium").sum()))
        c4.metric("Average Score", round(filtered_df["risk_score"].mean(), 1))

        st.markdown("### Case Queue")

        # Show a cleaner queue table
        st.dataframe(
            filtered_df[
                [
                    "case_id",
                    "account_id",
                    "risk_score",
                    "risk_level",
                    "reason_summary",
                    "recommended_action",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Export")

        # Convert filtered data to CSV so the user can download it
        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download enriched case file",
            csv,
            file_name="analyst_assist_enriched_cases.csv",
            mime="text/csv",
        )


# This makes sure the app runs only when this file is executed directly
if __name__ == "__main__":
    main()