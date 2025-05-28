import streamlit as st
import requests

# Backend server
LLAMA_SERVER_URL = "http://18.171.171.212:8080/v1/chat/completions"

st.set_page_config(page_title="AI Teacher Assistant", page_icon="🧠")
st.title("🧠 AI Teacher Assistant")

# Main task selection
task = st.radio(
    "Choose a task:",
    [
        "Differentiate the Resource",
        "Plan & Print",
        "Generate Parent Message",
        "Convert Resource Format"
    ],
    horizontal=True
)

# Show shared inputs only for relevant tasks
show_support_inputs = task == "Differentiate the Resource"

if show_support_inputs:
    age_group = st.selectbox("🎓 Age Group", ["5-7 (KS1)", "7-11 (KS2)", "11-14 (KS3)", "14-16 (KS4)", "16-18 (Post-16)"])
    difficulty = st.selectbox("📘 Difficulty Level", ["Simplified", "Challenge Extension", "Scaffolded Support"])
    eal_support = st.checkbox("🌍 Include EAL Support")
    send_support = st.checkbox("👥 Include SEND Support")

response = ""

def get_llama_response(user_prompt, system_prompt):
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(LLAMA_SERVER_URL, json=payload, headers=headers)
        res.raise_for_status()
        return res.json().get("choices", [{}])[0].get("message", {}).get("content", "⚠️ No content returned.")
    except Exception as e:
        st.error(f"❌ Server Error: {e}")
        if 'res' in locals():
            st.code(res.text)
        return "⚠️ Failed to get a valid response."

# 🔹 Differentiate the Resource
if task == "Differentiate the Resource":
    st.subheader("📄 Paste Lesson Content to Differentiate:")
    content = st.text_area("Enter your worksheet or lesson content here:")

    if st.button("✨ Generate Differentiated Version"):
        if not content.strip():
            st.warning("Please paste your content first.")
        else:
            support_notes = ""
            if eal_support:
                support_notes += "\n- Include support for EAL learners."
            if send_support:
                support_notes += "\n- Include accommodations for SEND learners."

            prompt = (
                f"Age group: {age_group}\n"
                f"Difficulty level: {difficulty}\n"
                f"{support_notes}\n\n"
                f"---\n\n"
                f"{content}"
            )

            SYSTEM_PROMPT = """
            You are an expert World class teaching assistant. Adapt the provided lesson content according to the age group, difficulty level, and learning needs. Do not invent unrelated topics.
            """

            response = get_llama_response(prompt, SYSTEM_PROMPT)

# 🔹 Plan & Print
elif task == "Plan & Print":
    st.subheader("📘 Enter Lesson Details (e.g., Photosynthesis – Year 8 – 50 mins):")
    lesson_info = st.text_input("Topic – Year – Duration:")
    uploaded_content = st.text_area("Optional: Paste chapter content or notes to help AI generate the lesson:")

    difficulty = st.selectbox("📘 Difficulty Level", ["Simplified", "Challenge Extension", "Scaffolded Support"])
    eal_support = st.checkbox("🌍 Include EAL Support")
    send_support = st.checkbox("👥 Include SEND Support")

    if st.button("📋 Generate Lesson Plan"):
        if not lesson_info.strip():
            st.warning("Please enter the lesson details.")
        else:
            support_notes = ""
            if eal_support:
                support_notes += "\n- Include support for EAL learners."
            if send_support:
                support_notes += "\n- Include accommodations for SEND learners."

            prompt = (
                f"Lesson Details: {lesson_info}\n"
                f"Difficulty: {difficulty}\n"
                f"{support_notes}\n\n"
                f"Content Reference (if any):\n{uploaded_content}"
            )

            SYSTEM_PROMPT = """
            You are an AI assistant for lesson planning. Based on the teacher's input (topic, year, duration, support needs), create a complete lesson plan including:
            - Learning Objectives
            - Slide Deck (titles only)
            - Differentiated Worksheets
            - AFL (Assessment for Learning) Questions
            Tailor the plan to the age group and needs. Avoid adding unrelated material.
            """

            response = get_llama_response(prompt, SYSTEM_PROMPT)

# 🔹 Generate Parent Message
elif task == "Generate Parent Message":
    st.subheader("✉️ Parent Comms Assistant")

    concern = st.text_area("📝 Describe the student situation (e.g., 'Jamie missed homework twice.'):")
    tone = st.selectbox("🎭 Select Tone", ["Professional", "Empathetic", "Constructive but Firm", "Encouraging"])
    student_name = st.text_input("👤 Student Name (optional):")

    if st.button("📨 Generate Message to Parents"):
        if not concern.strip():
            st.warning("Please enter a brief note or concern.")
        else:
            name_part = f"Student Name: {student_name}\n" if student_name else ""
            prompt = (
                f"{name_part}"
                f"Tone: {tone}\n"
                f"Situation: {concern}"
            )

            SYSTEM_PROMPT = """
            You are a school teacher assistant helping to communicate with parents. 
            Based on the input concern and tone, craft a respectful, clear, and professional message. 
            Avoid blame. Focus on support and partnership.
            """

            response = get_llama_response(prompt, SYSTEM_PROMPT)

# 🔹 Convert Resource Format
elif task == "Convert Resource Format":
    st.subheader("🔄 Reformat & Repurpose Resource")
    content = st.text_area("📄 Paste the resource you want to reformat (e.g., a worksheet or text):")

    format_type = st.radio("Select the output format:", ["Multiple Choice Quiz", "Flashcards", "Group Discussion Task"], horizontal=True)

    if st.button("🔧 Generate Reformatted Resource"):
        if not content.strip():
            st.warning("Please paste the resource content first.")
        else:
            if format_type == "Multiple Choice Quiz":
                format_prompt = "Reformat the content into a self-marking multiple-choice quiz. Give 10-20 Multiple choice questions only"
            elif format_type == "Flashcards":
                format_prompt = "Reformat the content into a set of flashcards for key terms."
            elif format_type == "Group Discussion Task":
                format_prompt = "Reformat the content into a group discussion task with guiding questions."
            else:
                format_prompt = "Reformat the content appropriately."

            prompt = f"{format_prompt}\n\nContent:\n{content}"

            SYSTEM_PROMPT = """
            You are an educational assistant. Transform the given resource into the selected format to suit varied teaching scenarios. Keep the content accurate and age-appropriate.
            """

            response = get_llama_response(prompt, SYSTEM_PROMPT)

# 📝 Show result
if response:
    st.markdown("### 📝 AI Output")
    st.write(response)
