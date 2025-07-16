* Add your .pth file inside /model/.
* Create .env in next to requirement.txt and add your credentials 
eg: OPENAI_API_KEY=your-openai-api-key


---

## 🧠 Backend Workflow

The following explains the step-by-step processing pipeline of the backend system:

---

### 📤 1. Upload Image

The farmer captures an image of the affected tomato plant and sends it via the `/full-analysis` API endpoint.

---

### ⚙️ 2. Request Handling (FastAPI → `main.py`)

FastAPI receives the uploaded image and starts the processing pipeline.

---

### 📷 3. Disease Detection (`predict.py`)

- The image is passed to a pre-trained PyTorch model.
- It identifies the type of disease affecting the tomato crop.
- Example output: `"Tomato Yellow Leaf Curl Virus"`

---

### 🤖 4. Get Expert Advice (Gemini → `gemini.py`)

- The disease name is sent as a prompt to the Gemini model (via Vertex AI or OpenAI).
- Gemini responds with:
  - An explanation of the disease
  - Affordable treatment suggestions
  - Market price trends
  - Related government schemes

---

### 🈯 5. Translate to Kannada (`translate.py`)

- The Gemini-generated response (in English) is translated to **Kannada** using Google Cloud Translate API.

---

### 🔊 6. Convert Text to Speech (`tts.py`)

- The Kannada text is converted into an `.mp3` audio response using Google Cloud Text-to-Speech API.
- This helps overcome literacy barriers for farmers.

---

### 📦 7. Final Response (JSON)

The API responds with:

```json
{
  "disease": "Tomato Yellow Leaf Curl Virus",
  "summary": "ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ ವಿವರಣೆ...",
  "audio_url": "/audio"
}

```

Create `.env` in the root of your project with:

```
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
GCP_PROJECT_ID=your-google-cloud-project-id
GCP_REGION=us-central1
```
---
### NOTE: Make sure your .json file has access to:
Vertex AI
Translate API
Text-to-Speech API
---

Run the FastAPI App
From the root of your project, run:
`uvicorn api.main:app --reload`
FastAPI will start the backend at:
`http://127.0.0.1:8000`
You can now test the endpoint:

🧪 Endpoint to Test:
```POST /full-analysis
Form-data:
- file: <your-leaf-image.jpg>
```
The response will be like:
```
{
  "disease": "Tomato Leaf Mold",
  "summary": "ಈ ರೋಗವು...",
  "audio_url": "/audio/response_XXXX.mp3"
}
```
You can GET the audio at:
`GET /audio/response_XXXX.mp3`

---

```
Upload Photo
	|
Disease Dectection using pyTorch model
	|
Prompt Gemini (vertex AI)
	|
Translate to Kannada
	|
Covert Text to Speech
	|
Send api response
	|
Get summary

```
