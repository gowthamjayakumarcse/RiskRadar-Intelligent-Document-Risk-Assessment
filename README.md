# 🧠 RiskRadar: Intelligent Document Risk Assessment

An **AI-powered legal document analyzer** that evaluates license agreements, privacy policies, and other contracts to identify **potential risks, data misuse, and compliance issues**.
Powered by **Google’s Gemini 1.5 Pro model**, RiskRadar provides actionable insights, a risk score, and interactive dashboards for better decision-making.

---

## 🚀 Key Features

* **⚙️ AI-Powered Document Analysis**
  Uses **Google Gemini 1.5 Pro** to extract, understand, and classify key clauses from complex legal documents.

* **📊 Dynamic Risk Scoring**
  Calculates an overall **Risk Score** using weighted metrics such as privacy concerns, major risks, and potential misuse.

* **🧩 Comprehensive Risk Categories**

  * 📝 **Key Points** – Major clauses and legal obligations
  * 🔒 **Privacy Issues** – Data collection, retention, and sharing policies
  * ⚠️ **Major Concerns** – Ambiguous or unfavorable terms
  * 🛡️ **Data Misuse Risks** – Possible exploitation or vulnerabilities
  * 💫 **Advantages** – User rights and protective clauses
  * ⚡ **Disadvantages** – Limitations and restrictions

* **📈 Interactive Dashboard (Streamlit)**

  * Real-time **gauge charts** showing overall risk score
  * Expandable sections with categorized insights
  * Clean, modern UI with dark/light mode friendly design

* **📑 PDF Document Support**
  Automatically extracts and analyzes text from uploaded PDF agreements.

---

## 🧠 Architecture Overview

1. **Text Extraction** → Reads PDF using `PyPDF2`
2. **Prompt Engineering** → Sends structured legal analysis prompt to **Gemini 1.5 Pro**
3. **AI Analysis** → Classifies findings into JSON-based categories
4. **Risk Scoring** → Applies weighted logic across privacy, data misuse, and concerns
5. **Dashboard Visualization** → Displays results via **Plotly** and **Streamlit**

---

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/RiskRadar.git
cd RiskRadar
```

### 2️⃣ Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add your Google API Key

Create a `.env` file in the root directory and add:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## 💡 Usage

### Run the application

```bash
streamlit run app.py
```

### Steps:

1. Upload a **PDF file** containing a license or agreement.
2. Wait for AI to analyze the content.
3. View the **interactive risk dashboard**:

   * Overall risk gauge
   * Issue breakdown
   * Expandable insights

---

## 🧩 Technologies Used

| Component                 | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| **Google Gemini 1.5 Pro** | AI-driven text understanding & classification |
| **Streamlit**             | Web-based interactive dashboard               |
| **PyPDF2**                | PDF text extraction                           |
| **Plotly**                | Risk score visualization                      |
| **dotenv**                | Secure API key management                     |
| **Python**                | Core logic & data processing                  |

---

## 🧱 Project Structure

```
RiskRadar/
├── app.py               # Main application logic
├── requirements.txt     # Dependencies list
├── .env                 # Environment variables
└── README.md            # Project documentation
```

---

## 📊 Risk Score Levels

| Risk Level           | Score Range | Meaning                           |
| -------------------- | ----------- | --------------------------------- |
| 🟢 **Low Risk**      | 0–30        | Safe and compliant                |
| 🟡 **Moderate Risk** | 31–70       | Contains moderate concerns        |
| 🔴 **High Risk**     | 71–100      | Potentially unsafe terms detected |

---

## 🧪 Example Output

**Uploaded Document:** `terms_and_conditions.pdf`
**AI Results:**

* Privacy Issues: 3
* Major Concerns: 2
* Data Misuse Risks: 1
  **Overall Risk Score:** 54 (⚠️ Medium Risk)

---

## 🔮 Future Enhancements

* 🧾 Multi-document comparison
* 🗂️ Support for Word (.docx) and text files
* 🧠 Integration with legal knowledge bases
* 🌐 Multi-language document support
* ☁️ Cloud deployment (Streamlit Cloud / Hugging Face Spaces)

---

## 👨‍💻 Author

**Gowtham J**
🎓 Post Graduate in AI & ML — *VIT Vellore*
📧 [gowtham.aidev@gmail.com](mailto:gowtham.aidev@gmail.com)

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

* **Google Generative AI** (Gemini 1.5 Pro)
* **Streamlit** team for the web framework
* **Plotly** for visualization components
* All contributors and testers of this project
