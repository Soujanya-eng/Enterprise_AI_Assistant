# Enterprise Nexus: Secure Corporate AI Assistant(using prompt engineering)

**Enterprise Nexus** is a secure, full-stack web application designed to optimize corporate workflows and provide intelligent workspace assistance. Powered by **Python (Flask)** and **SQLite**, it integrates seamlessly with Google's advanced **Gemini AI** model via an asynchronous architecture to deliver instant, real-time responses without reloading pages.

---

## 🚀 Key Features

*   **Secure User Management:** Features robust user registration and login functionality protected by industry-standard password cryptographic hashing (`scrypt`).
*   **Real-Time Asynchronous Chat:** Leverages the native browser JavaScript `fetch` API to communicate instantly with the backend pipeline.
*   **Gemini AI Integration:** Fully integrated with Google AI Studio's **Gemini 3.5 Flash** free-tier API engine [NOT_FOUND].
*   **Persistent Chat Logging:** Automatically logs all conversations chronologically in a local SQLite database, ensuring data is preserved across sessions.
*   **Enterprise Interface:** Features a clean, responsive dark-mode dashboard tailored for professional corporate environments.

---

## 🛠️ Architecture & Tech Stack

*   **Frontend:** HTML5, CSS3 (Modern Dark Theme), JavaScript (Asynchronous ES6+ Fetch Engine)
*   **Backend Framework:** Python 3.13+ / Flask
*   **Database ORM:** SQLite / Flask-SQLAlchemy
*   **Security:** Werkzeug (Password Security Hashing)
*   **AI Engine:** Official Google GenAI SDK (`gemini-3.5-flash` model) [NOT_FOUND]

---

## 📁 Project Structure

```text
Enterprise-Nexus/
│
├── app.py                 # Core Python backend server, routes, and database models
└── templates/             # UI Presentation templates compiled by Flask
    ├── index.html         # Portal homepage with routing logic
    ├── login.html         # Secure credential validation screen
    ├── signup.html        # Enterprise user profile registration form
    └── dashboard.html     # Personalized real-time chat workspace
```

---

## ⚙️ Local Installation & Setup

### 1. Clone or Organize Your Files
Ensure your project files match the directory structure shown in the **Project Structure** section above.

### 2. Install Required Dependencies
Open your terminal inside the project directory and run the following command to download the required libraries:
```bash
pip install flask flask-sqlalchemy google-genai
```

### 3. Configure Your API Key
1. Obtain a free API key from [Google AI Studio](https://google.com).
2. Open `app.py` and paste your key string into the initialization client on line 16:
```python
ai_client = genai.Client(api_key="YOUR_ACTUAL_GEMINI_API_KEY_HERE")
```

### 4. Initialize Database & Run the Server
Launch the local development web server using the python command:
```bash
python app.py
```

### 5. Access the Web Application
Open your browser and navigate to the local address to test your portal:
```text
http://127.0.0
```

---

## 📝 License

This project is built for educational and enterprise portfolio development purposes under the MIT License.
 
