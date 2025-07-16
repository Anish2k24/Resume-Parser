# AI Resume Parser

An intelligent resume parser built using **Streamlit**, **spaCy NLP**, **Tesseract OCR**, and **PyPDF2** that extracts structured data from both text-based and image-based resumes. This project was developed as **Task 2 for the Pinnacle Labs Internship**.

---

## Features

* Upload PDF resumes (text or scanned)
* Extracts:

  * Name (via spaCy)
  * Email and Phone (via Regex)
  * Education, Experience, Projects
  * Skills from a curated keyword list
* OCR-powered scanning for image-based resumes
* Downloadable AI-generated summary report
* Minimal UI powered by Streamlit

---

## Project Structure

```
.
├── app.py               # Main Streamlit app
├── requirements.txt     # All required Python packages
├── .gitignore           # Ignored files and folders
└── .venv/               # Virtual environment (ignored)
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-resume-parser.git
cd ai-resume-parser
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

* Download from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
* Add it to your system PATH

### 4. Run the App

```bash
streamlit run app.py
```

---

## Sample Output

```
Name: Anish Bhattacharjee
Email(s): anish@example.com
Phone(s): +91 9876543210

Skills:
- Python
- Streamlit
- spaCy
- OCR
- Git

Education:
- B.Tech in CSE | XYZ University | 2023

Experience:
- Internship at ABC Corp – Built an NLP-based chatbot

Projects:
- Developed this AI Resume Parser as part of Pinnacle Labs Internship
```

---

## Requirements

Install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Main packages used:

* `streamlit`
* `PyPDF2`
* `spacy`
* `pytesseract`
* `pdf2image`
* `Pillow`

Don’t forget to run:

```bash
python -m spacy download en_core_web_sm
```

---

## Internship Submission Note

Task 2 Completed and Submitted
Project Title: AI Resume Parser
Internship: Pinnacle Labs
Language Used: Python
IDE: VS Code
Description: Built a smart application to extract structured details from resumes using advanced text processing and OCR.

---

## Acknowledgements

* [Streamlit](https://streamlit.io/)
* [spaCy NLP](https://spacy.io/)
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* [pdf2image](https://github.com/Belval/pdf2image)
* [Pillow](https://python-pillow.org/)

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Let's Connect

Feel free to connect on [LinkedIn](https://www.linkedin.com/) and check out more projects!
