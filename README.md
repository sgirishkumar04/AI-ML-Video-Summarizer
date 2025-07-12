# AI/ML Video Summarizer 🚀

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_Now-2ea44f?style=for-the-badge&logo=render)](https://video-summarizer-acsw.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

An intelligent web application that transforms video content into organized, easy-to-read text. This tool leverages state-of-the-art open-source AI models to provide accurate transcriptions, multilingual translation, and concise summaries, making video content more accessible and digestible.

---

## 🎬 Live Demo

**Check out the live application hosted on Render:**

### 👉 [https://video-summarizer-acsw.onrender.com](https://video-summarizer-acsw.onrender.com)

*(Note: The free tier may take a moment to "wake up" on the first visit.)*

---

## ✨ Key Features

-   **Seamless Video Upload:** A clean, user-friendly interface to upload video files (MP4, MOV, etc.).
-   **Accurate Speech-to-Text:** Utilizes an optimized Whisper model (**`faster-whisper`**) to generate a full transcript of the spoken dialogue.
-   **Multilingual Translation to English:** Automatically detects the source language (e.g., Tamil, Spanish, French) and translates the entire transcript into English text.
-   **One-Click AI Summarization:** Employs a **Hugging Face Inference API** to condense the full transcript into a short, coherent summary.
-   **Efficient & Resourceful:** Built to run on free-tier services by using optimized, open-source models instead of paid APIs.

---

## 🛠️ Technology Stack & Architecture

This project follows a simple client-server architecture:

-   **Frontend (Client):** Built with vanilla **HTML**, **CSS**, and **JavaScript** to capture user input and display results dynamically using `fetch` API calls.
-   **Backend (Server):** A **Python** server using the **Flask** web framework, orchestrated by a **Gunicorn** WSGI server for production.
-   **AI Processing:**
    -   **Transcription & Translation:** `faster-whisper` runs locally on the server to process audio, offering high performance on CPU.
    -   **Summarization:** Connects to the **Hugging Face Inference API** to leverage powerful summarization models without a local GPU requirement.
-   **Deployment:** The entire application is deployed on **Render**, with a build script to pre-load AI models and a custom start command optimized for long-running tasks.

---

## 🚀 How to Run Locally

To get a local copy up and running, follow these simple steps.

### Prerequisites

-   Python 3.11+
-   Git
-   A Hugging Face account and [API Token](https://huggingface.co/settings/tokens)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/video-summarizer-web.git
    cd video-summarizer-web
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the project root and add your Hugging Face API token:
    ```
    HUGGING_FACE_HUB_TOKEN="hf_YourSecretTokenHere"
    ```

5.  **Run the application:**
    ```sh
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

## 💡 Challenges & Learnings

Building and deploying this project involved overcoming several real-world challenges, which were fantastic learning opportunities:

-   **Migrating from Paid to Open-Source Models:** The initial prototype used the OpenAI API. When credits ran out, I successfully migrated the entire backend to use free, self-hosted alternatives (**`faster-whisper`**) and the **Hugging Face API**, learning how to adapt code to entirely new libraries and API structures.

-   **Mastering Git for Security:** I learned the critical importance of not committing sensitive data. This involved mastering the use of `.gitignore` and learning how to scrub secrets from the entire Git history using **`git-filter-repo`** after an accidental commit.

-   **Optimizing for a Production Environment:** I troubleshooted and solved complex deployment issues on **Render**, including:
    -   Resolving Python version conflicts between my local machine and the server.
    -   Overcoming strict memory limits (`Out of Memory` errors) by optimizing the AI model size (`"small"` -> `"tiny"`) and fine-tuning the **Gunicorn** worker configuration.
