import streamlit as st
import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()
LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL")

def clean_prompt(text):
    # Remove ALL punctuation/symbols (keep only letters, numbers, spaces)
    text = re.sub(r"[^\w\s]", '', text)
    # Collapse multiple spaces into one
    text = re.sub(r"\s+", ' ', text)
    text = text.strip()
    # Convert to title case (capitalize first letter of each word)
    return text.title()






st.set_page_config(page_title="AI Teacher Assistant", page_icon="🧠")
st.title("🧠 AI Teacher Assistant")

task = st.radio(
    "Choose a task:",
    [
        "Differentiate the Resource",
        "Plan & Print",
        "Generate Parent Message",
        "Convert Resource Format",
        "Emotion Check-in",
        "Simplified Instructions",
        "Functional Literacy Activities",
        "Behavior Reflection"

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
    cleaned_prompt = clean_prompt(user_prompt)
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": cleaned_prompt}
        ],
        "temperature": 0,
        "max_tokens": 1000
    }
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(LLAMA_SERVER_URL, json=payload, headers=headers)
        res.raise_for_status()
        response_content = res.json().get("choices", [{}])[0].get("message", {}).get("content", "⚠️ No content returned.")
        return response_content, cleaned_prompt
    except Exception as e:
        st.error(f"❌ Server Error: {e}")
        if 'res' in locals():
            st.code(res.text)
        return "⚠️ Failed to get a valid response.", cleaned_prompt



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

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)


# 🔹 Plan & Print
elif task == "Plan & Print":
    st.subheader("📘 Plan & Print a Lesson")

    input_method = st.radio(
        "Choose your input method:",
        ["📝 Topic – Age – Duration", "📄 Paste Chapter Notes"],
        horizontal=True
    )

    # Show only one input box based on selected method
    if input_method == "📝 Topic – Age – Duration":
        lesson_info = st.text_input("✍️ Enter Topic – Age – Duration (e.g., Photosynthesis – Age 8 – 50 mins):")
        uploaded_content = ""
    else:
        uploaded_content = st.text_area("📄 Paste chapter content or notes:")
        lesson_info = ""

    difficulty = st.selectbox("📘 Difficulty Level", ["Simplified", "Challenge Extension", "Scaffolded Support"])
    eal_support = st.checkbox("🌍 Include EAL Support")
    send_support = st.checkbox("👥 Include SEND Support")

    if st.button("📋 Generate Lesson Plan"):
        if not lesson_info.strip() and not uploaded_content.strip():
            st.error("⚠️ Please provide the required input.")
        else:
            support_notes = ""
            if eal_support:
                support_notes += "\n- Include support for EAL learners."
            if send_support:
                support_notes += "\n- Include accommodations for SEND learners."

            prompt_parts = []
            if lesson_info.strip():
                prompt_parts.append(f"Lesson Info: {lesson_info}")
            if uploaded_content.strip():
                prompt_parts.append(f"Content Reference:\n{uploaded_content}")
            prompt_parts.append(f"Difficulty: {difficulty}")
            prompt_parts.append(support_notes)

            prompt = "\n\n".join(prompt_parts)

            SYSTEM_PROMPT = """
            You are a world-class AI assistant that creates tailored lesson plans for teachers. 
            Use the provided topic/duration or content notes to generate a structured lesson plan with:
            - Learning Objectives
            - Slide Deck (titles only)
            - Differentiated Worksheets
            - AFL (Assessment for Learning) Questions

            Always adapt to the learner's needs (age, ability, support flags). 
            Do not introduce unrelated material.
            """

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)





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

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)


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

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)

# Emotion Check-in Templates
elif task == "Emotion Check-in":
    st.subheader("😊 Emotion Check-in")

    # Basic student info
    student_name = st.text_input("👤 Your Name")
    checkin_date = st.date_input("📅 Today's Date")

    # Emoji options
    st.markdown("### 💬 Today I am feeling (check all that apply):")
    emoji_options = {
        "😀 Happy": "😀",
        "😟 Worried": "😟",
        "😡 Angry": "😡",
        "😢 Sad": "😢",
        "😐 Okay": "😐",
        "🤩 Excited": "🤩",
        "😴 Tired": "😴",
        "🥳 Proud": "🥳",
        "🤔 Confused": "🤔",
        "😬 Nervous": "😬"
    }
    selected_emotions = st.multiselect(
        label="Select your emotions:",
        options=list(emoji_options.keys())
    )

    # Optional explanation
    other_feelings = st.text_area(
        "🗣️ Would you like to share why you feel this way? (Optional)",
        placeholder="I feel this way because..."
    )

    # Optional: Age group toggle (can still be useful for customizing language)
    use_age_group = st.checkbox("Include age group ?")
    age_group = None
    if use_age_group:
        age_group = st.selectbox("🎓 Select Age Group", ["5-7 (KS1)", "7-11 (KS2)", "11-14 (KS3)", "14-16 (KS4)"])

    if st.button("🧠 Generate Emotion Check-in Template"):
        prompt = "Create a short, age-appropriate emotion check-in summary, checkboxes and sentence stems for a student to fill.It should work like online dairy only to keep in check  "

        if student_name:
            prompt += f" Student Name: {student_name}."

        prompt += f" Date: {checkin_date}."

        if age_group:
            prompt += f" Age group: {age_group}."

        if selected_emotions:
            prompt += f" Emotions selected: {', '.join(selected_emotions)}."

        if other_feelings.strip():
            prompt += f" Additional note from student: '{other_feelings.strip()}'"

        SYSTEM_PROMPT = """
        You are a classroom wellbeing assistant. Generate a short, supportive and student-friendly emotion check-in summary.
        Do not overcomplicate the language – the user is a student. Keep it clear and use sentence stems based on input. 
        If the student has provided emotion checkboxes and a note, reflect both simply.
        """

        response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)


# 🔹 Simplified Instruction Scripts
elif task == "Simplified Instructions":
    st.subheader("🧾 Simplified Instruction Guide")

    complex_task = st.text_area(
        "🛠️ Describe the task you want to simplify:",
        placeholder="e.g., How to use the school printer, how to log into the computer..."
    )

   #include_steps = st.checkbox("🪜 Show steps as a numbered list?", value=True)

    if st.button("🧠 Simplify Instructions"):
        if not complex_task.strip():
            st.warning("Please describe the task or routine.")
        else:
            list_format = "Use short, clear sentences only." #"Format as a step-by-step numbered list." if include_steps else "Use short, clear sentences only."

            prompt = (
                f"Simplify the following task into plain, student-friendly language.\n"
                f"{list_format}\n\n"
                f"Task:\n{complex_task.strip()}"
            )

            SYSTEM_PROMPT = """
            You are a world class assistant that simplifies tasks for students with diverse learning needs. 
            Convert the input into short, clear, and repeatable steps. Avoid complex terms or technical jargon.
            Keep it focused and easy to understand. Use a numbered list if asked.
            """

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)



# 🔹 Functional Literacy Activities
elif task == "Functional Literacy Activities":
    st.subheader("🧺 Functional Literacy Builder")

    real_world_task = st.text_area(
        "📝 Describe a real-world reading or writing task:",
        placeholder="e.g., Write a list of things to buy for lunch, read a bus timetable, write directions to the school..."
    )

    literacy_type = st.selectbox(
        "📚 What type of literacy is this?",
        ["Reading", "Writing", "Both"]
    )


    if st.button("📄 Generate Literacy Activity"):
        if not real_world_task.strip():
            st.warning("Please describe the literacy activity.")
        else:
            prompt_parts = [
                f"Task: {real_world_task.strip()}",
                f"Literacy focus: {literacy_type}",
            ]

            prompt = "\n".join(prompt_parts)

            SYSTEM_PROMPT = """
            You are a classroom literacy assistant helping students build real-world reading and writing skills. 
            Based on the described task, generate a functional literacy activity that is scaffolded and age-appropriate. 
            Use sentence stems to support the task.
            The activity should focus on everyday life contexts (e.g., shopping, directions, signs).
            """

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)


# 🔹 Behavior Reflection Sheets
elif task == "Behavior Reflection":
    st.subheader("🧭 Behavior Reflection Sheet Generator")

    # Student input
    incident_description = st.text_area(
        "📖 Briefly describe the behavior incident or situation:",
        placeholder="e.g., Jamie shouted during group work, wouldn't follow instructions..."
    )

    use_age_group = st.checkbox("🎓 Include age group for tailoring?")
    if use_age_group:
        age_group = st.selectbox("Select Age Group:", ["5-7 (KS1)", "7-11 (KS2)", "11-14 (KS3)", "14-16 (KS4)"])
    else:
        age_group = None

    include_emotions = st.checkbox("😔 Include feelings/emotion reflection?")
    include_support_plan = st.checkbox("🙋 Add section for future support plan?")

    if st.button("📄 Generate Reflection Sheet"):
        if not incident_description.strip():
            st.warning("Please describe the incident.")
        else:
            prompt_parts = [
                f"Incident description: {incident_description.strip()}"
            ]
            if age_group:
                prompt_parts.append(f"Age group: {age_group}")
            if include_emotions:
                prompt_parts.append("Include emotional reflection questions.")
            if include_support_plan:
                prompt_parts.append("Include a support plan section to identify who can help next time.")

            prompt = "\n".join(prompt_parts)

            SYSTEM_PROMPT = """
            You are a school assistant helping generate a behavior reflection worksheet.
            Use the incident description and optional flags to create a printable set of reflection prompts for the student.
            Keep it short, clear, and accessible – aim for 4–6 open-ended questions with space to write.
            Tailor to the age group if provided. Focus on understanding, empathy, and accountability.
            """

            response, cleaned_prompt = get_llama_response(prompt, SYSTEM_PROMPT)




# 📝 Show result
if response:
    st.markdown("### 📝 Response")
    st.write(response)
## TO test the working of cleaned User prompt for accuracy
    st.markdown("---Testing Purpose---")
    st.markdown("### 🔍 Cleaned Prompt Sent to LLaMA")
    st.code(cleaned_prompt, language="markdown")
