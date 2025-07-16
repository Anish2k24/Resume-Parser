import streamlit as st
import PyPDF2
import re
import spacy
from io import StringIO
from datetime import datetime
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def extract_text_from_pdf(uploaded_file):
    text = ""

    try:
        file_bytes = uploaded_file.read()
        from io import BytesIO
        pdf_stream = BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_stream)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        if not text or not text.strip():
            st.warning("⚠️ No extractable text found. Trying OCR...")
            images = convert_from_bytes(file_bytes)
            for image in images:
                text += pytesseract.image_to_string(image, lang='eng')
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text if text else ""


def extract_email(text):
    return re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)

def extract_phone(text):
    return re.findall(r'(?:(?:\+?\d{1,3})?[\s-]?)?(?:\(?\d{3,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}', text)

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines[0] if lines else "Not Found"

def extract_skills(text):
    skills_list = [
        "Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS", "Machine Learning",
        "Deep Learning", "TensorFlow", "PyTorch", "Excel", "Power BI", "Tableau", "Data Analysis",
        "Data Science", "Communication", "Leadership", "Project Management", "Cloud", "AWS", "Docker", "Git"
    ]
    found_skills = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return list(set(found_skills))

def extract_education(text):
    keywords = [
        "Bachelor", "Master", "B.Tech", "M.Tech", "B.E", "MCA", "MBA", "PhD",
        "High School", "School", "University", "College", "BCA", "B.Sc", "M.Sc", "10th", "12th"
    ]
    lines = text.split('\n')  
    edu_section = []

    for i in range(len(lines)):
        line = lines[i].strip()
        lower_line = line.lower()
        if any(kw.lower() in lower_line for kw in keywords):
            entry = line
            if i + 1 < len(lines):
                entry += " | " + lines[i + 1].strip()
            if i + 2 < len(lines):
                entry += " | " + lines[i + 2].strip()
            edu_section.append(entry)
    return edu_section

def extract_experience(text):
    experience_keywords = ["experience", "internship", "worked at", "project", "responsibilities", "role", "designation"]
    lines = text.split('\n')
    experience_info = []
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in experience_keywords):
            experience_info.append(line.strip())
    return experience_info

def extract_projects(text):
    project_keywords = [
        "project", "projects", "worked on", "built", "developed", "designed",
        "created", "implemented", "led", "contributed", "deployed", "engineered"
    ]
    lines = text.split('\n')
    project_info = []

    for line in lines:
        if any(keyword in line.lower() for keyword in project_keywords):
            project_info.append(line.strip())

    return project_info 


# def extract_projects(text):
#     project_keywords = [
#         "projects", "worked on", "built", "developed", "designed", "created", 
#         "implemented", "led", "deployed"
#     ]
#     lines = text.split('\n')
#     project_info = []
#     collect = False

#     for line in lines:
#         line_lower = line.lower().strip()

#         if any(kw in line_lower for kw in project_keywords):
#             collect = True

#         if collect:
#             if line.strip():
#                 project_info.append(line.strip())
#             else:
#                 collect = False  # Stop when hitting a blank line

#     return project_info

        
def generate_report(name, emails, phones, skills, education, experience, projects):
    buffer = StringIO()
    buffer.write("==== AI Resume Parser Report ====\n")
    buffer.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    buffer.write(f"👤 Name: {name}\n")
    buffer.write(f"📧 Email(s): {', '.join(emails) if emails else 'Not Found'}\n")
    buffer.write(f"📱 Phone(s): {', '.join(phones) if phones else 'Not Found'}\n")
    buffer.write(f"\n🛠️ Skills:\n- " + "\n- ".join(skills if skills else ["Not Found"]))
    buffer.write(f"\n🎓Education:\n- " + "\n- ".join(education if education else ["Not Found"]))
    buffer.write(f"\n💼 Experience:\n- " + "\n- ".join(experience if experience else ["Not Found"]))
    buffer.write(f"\n📂 Projects:\n- " + "\n- ".join(projects if projects else ["Not Found"]))
    return buffer.getvalue()

st.set_page_config(page_title="Enhanced Resume Parser AI", layout="wide")

st.title("🧠 Enhanced AI Resume Parser")
st.markdown("Upload a PDF Resume and get a full AI-based extraction of key details.")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("🔍 Extracting data..."):
        text = extract_text_from_pdf(uploaded_file)
        st.write("DEBUG: Extracted text is:", text)
        st.write("DEBUG: Type of text:", type(text).__name__)

        if not text or not isinstance(text, str) or not text.strip():
            st.warning("⚠️ No extractable text found. The file might be image-based or encrypted.")
        else:
            name = extract_name(text)
            emails = extract_email(text)
            phones = extract_phone(text)
            skills = extract_skills(text)
            education = extract_education(text)
            experience = extract_experience(text)
            projects = extract_projects(text)


            st.success("✅ Extraction Completed!")

            st.subheader("📌 Extracted Information:")
            st.write(f"**👤 Name:** `{name}`")
            st.write(f"**📧 Emails:** `{emails if emails else 'Not Found'}`")
            st.write(f"**📱 Phones:** `{phones if phones else 'Not Found'}`")

            st.markdown("**🛠️ Skills:**")
            st.write(skills if skills else "Not Found")

            st.markdown("**🎓Education:**")
            st.write(education if education else "Not Found")

            st.markdown("**💼 Experience:**")
            st.write(experience if experience else "Not Found")

            st.markdown("**📂 Projects:**")
            st.write(projects if projects else "The resume does not contain any kind of projects in it.")


            report = generate_report(name, emails, phones, skills, education, experience, projects)

            st.download_button("⬇️ Download Extracted Report (.pdf)",
                               data=report,
                               file_name="resume_report.pdf",
                               mime="text/plain")

            with st.expander("📝 Full Resume Text"):
                st.text(text)

    st.caption("🔒 All data is processed locally and is not saved or shared.")
else:
    st.info("Please upload a PDF resume to begin.")
