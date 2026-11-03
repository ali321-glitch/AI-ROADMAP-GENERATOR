import google.generativeai as genai
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Learning Roadmap Generator", page_icon="🚀", layout="wide"
)

# Initialize Gemini API using Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
  st.error(
      "🔑 GEMINI_API_KEY not found in Streamlit Secrets! Please add it in your"
      " app settings."
  )


def generate_roadmap(field, level, duration):
  """Generates a learning roadmap using Gemini Flash"""
  prompt = f"""
    Create a detailed, structured learning roadmap for someone who wants to master: {field}.
    Their current skill level is: {level}.
    The time available to learn is: {duration}.

    Please format the response cleanly using Markdown with:
    1. A brief encouraging introduction overview.
    2. Phase-by-phase breakdown (e.g., Phase 1, Phase 2, etc.) with estimated timelines.
    3. Core topics, concepts, and recommended skills to master in each phase.
    4. Suggested free resources, types of projects to build, and practical milestones.
    """

  try:
    # Using gemini-1.5-flash for fast and reliable text generation
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
  except Exception as e:
    st.error(f"⚠️ Error generating roadmap: {e}")
    return None


# --- UI LAYOUT ---
st.title("🚀 AI Learning Roadmap Generator")
st.markdown(
    "Generate a personalized, step-by-step learning path tailored to your"
    " goals, experience level, and timeline powered by Google Gemini."
)

# Sidebar for User Inputs
with st.sidebar:
  st.header("🎯 Roadmap Parameters")

  field_input = st.text_input(
      "What domain do you want to learn?",
      placeholder="e.g., Artificial Intelligence, React, Cybersecurity",
  )

  level_input = st.selectbox(
      "Select your skill level:", ["Beginner", "Intermediate", "Advanced"]
  )

  time_input = st.text_input(
      "Time available to learn:", placeholder="e.g., 3 months, 5 hours/week"
  )

  generate_btn = st.button("Generate Roadmap", type="primary")

# Main Content Area
if generate_btn:
  if not field_input or not time_input:
    st.warning("⚠️ Please fill in both the domain/field and your time commitment.")
  else:
    with st.spinner("🧠 Gemini is crafting your customized learning path..."):
      roadmap_text = generate_roadmap(field_input, level_input, time_input)

      if roadmap_text:
        st.success("🎉 Roadmap generated successfully!")
        st.markdown("---")

        # Display roadmap
        st.markdown(roadmap_text)

        # Download button
        st.download_button(
            label="📥 Download Roadmap as Markdown",
            data=roadmap_text,
            file_name=f"{field_input.lower().replace(' ', '_')}_roadmap.md",
            mime="text/markdown",
        )
else:
  st.info(
      "👈 Use the sidebar to enter your details and click **Generate"
      " Roadmap** to get started!"
  )
