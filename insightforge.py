import streamlit as st
from pypdf import PdfReader
from collections import Counter
import re

st.set_page_config(page_title="InsightForge", layout="wide")

st.title("InsightForge")

st.markdown("""
### Turning Documents into Actionable Intelligence

Upload technical, commercial, investment or market reports and generate structured consulting analyses including:

- Executive Summaries
- Risk Assessments
- Due Diligence Reviews
- Investment Memos
- Market Intelligence Reports
""")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

risk_words = [
    "risk",
    "delay",
    "shortage",
    "inflation",
    "uncertainty",
    "challenge",
    "constraint",
    "bottleneck",
    "cost",
    "disruption"
]

opportunity_words = [
    "growth",
    "opportunity",
    "investment",
    "expansion",
    "innovation",
    "efficiency",
    "optimization",
    "demand",
    "market",
    "development"
]

stop_words = {
    "the", "and", "for", "that", "with", "this", "from",
    "are", "was", "were", "has", "have", "will", "not",
    "but", "can", "into", "than", "their", "there",
    "been", "also", "which", "they", "its", "our"
}


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text, len(reader.pages)


def get_top_keywords(text, top_n=15):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    return Counter(filtered_words).most_common(top_n)


def count_indicators(text, words):
    text_lower = text.lower()

    return {
        word: text_lower.count(word)
        for word in words
        if text_lower.count(word) > 0
    }


if uploaded_file:

    text, page_count = extract_text_from_pdf(uploaded_file)

    word_count = len(text.split())
    character_count = len(text)

    st.success("Document processed successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pages", page_count)

    with col2:
        st.metric("Words", word_count)

    with col3:
        st.metric("Characters", character_count)

    st.subheader("Document Preview")
    st.write(text[:3000])

    st.subheader("Top Keywords")

    keywords = get_top_keywords(text)

    for word, count in keywords:
        st.write(f"{word}: {count}")

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Risk Indicators")

        risks = count_indicators(text, risk_words)

        if risks:
            for word, count in risks.items():
                st.write(f"{word}: {count}")
        else:
            st.write("No major risk indicators found.")

    with col5:
        st.subheader("Opportunity Indicators")

        opportunities = count_indicators(text, opportunity_words)

        if opportunities:
            for word, count in opportunities.items():
                st.write(f"{word}: {count}")
        else:
            st.write("No major opportunity indicators found.")

    st.subheader("InsightForge Analysis Engine")

    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "Executive Summary",
            "Risk Assessment",
            "Investment Memo",
            "Due Diligence Review",
            "Market Intelligence"
        ]
    )

    prompts = {

        "Executive Summary": f"""
You are a senior strategy consultant.

Analyze the following document and provide:

1. Executive Summary
2. Key Findings
3. Strategic Implications
4. Recommended Actions

Document:

{text[:8000]}
""",

        "Risk Assessment": f"""
You are a senior risk consultant.

Analyze the document and identify:

1. Technical Risks
2. Commercial Risks
3. Supply Chain Risks
4. Financial Risks
5. Mitigation Actions

Document:

{text[:8000]}
""",

        "Investment Memo": f"""
You are an investment analyst.

Prepare an investment memo covering:

1. Investment Thesis
2. Market Opportunity
3. Key Risks
4. Growth Potential
5. Investment Recommendation

Document:

{text[:8000]}
""",

        "Due Diligence Review": f"""
You are conducting technical and commercial due diligence.

Provide:

1. Executive Summary
2. Strengths
3. Weaknesses
4. Key Risks
5. Missing Information
6. Recommendation

Document:

{text[:8000]}
""",

        "Market Intelligence": f"""
You are a market intelligence analyst.

Analyze the document and provide:

1. Market Trends
2. Competitive Landscape
3. Growth Drivers
4. Barriers
5. Strategic Opportunities

Document:

{text[:8000]}
"""
    }

    if st.button("Generate Analysis Prompt"):

        st.text_area(
            "Copy this prompt into ChatGPT Plus",
            prompts[analysis_type],
            height=350
        )