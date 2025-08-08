# 🧠 AI Image Detector

A full-stack web application for detecting AI-generated images using an ensemble of **ResNet-50** and **Vision Transformer (ViT)** models. Built with **FastAPI**, **PyTorch**, **Next.js**, and **Docker**.  

Live frontend deployed on **Vercel**, and backend designed for **GCP Cloud Run**.

## 🌐 Live Demo

👉 **Check out the live version here:**  [🔗 AI-Detector ](https://ai-detector-phi.vercel.app/)

---

## 🚀 Features

- 📤 Upload images via modern web interface
- 🧠 Dual-model ensemble (ResNet-50 + ViT)
- ⚡ Fast predictions (< 5 seconds)
- 📊 Confidence scores & per-model breakdown
- 🔌 REST API for easy integration
- 🐳 Dockerized backend for easy deployment

---

## 🛠️ Backend Setup (FastAPI + PyTorch)

1. **Add trained models** to `backend/models/`:
   ```
   backend/models/
   ├── resnet_model.pth
   └── vit_detector_model.pth
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run with Docker**:
   ```bash
   docker-compose up --build
   ```

> 📍 FastAPI server will be available at `http://localhost:8000`

---

## 💻 Frontend Setup (Next.js + React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend/
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

> 🌐 Web app runs at `http://localhost:3000`

---

## 🧪 How to Use

1. Open the frontend in your browser.
2. Upload an image (drag & drop or file picker).
3. Wait 2–5 seconds for processing.
4. Get results:
   - **Prediction:** AI-Generated or Real
   - **Confidence score**
   - **Per-model analysis**

---

## 🚀 Deployment Guide

### 🔧 Backend (Google Cloud Run)

1. **Build Docker image**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/ai-detector-api
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy ai-detector-api      --image gcr.io/YOUR_PROJECT/ai-detector-api      --platform managed      --region us-central1      --cpu 2      --memory 4Gi      --allow-unauthenticated
   ```

### 🌐 Frontend (Vercel)

1. Push `frontend/` to GitHub
2. Link repo to [Vercel](https://vercel.com/)
3. Set environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-cloud-run-url
   ```

---

## 📡 API Endpoints

- **POST** `/predict`  
  → Accepts: image file  
  → Returns: prediction, confidence, per-model analysis

- **GET** `/health`  
  → Returns server status

- **GET** `/models-info`  
  → Returns model architecture and training data info

---

## 🧰 Tech Stack

| Layer     | Tools / Frameworks                               |
|-----------|--------------------------------------------------|
| Backend   | Python, FastAPI, PyTorch, Docker                 |
| Frontend  | Next.js, React, TypeScript, Tailwind CSS         |
| Deployment| GCP Cloud Run (API), Vercel (Frontend)           |
| Models    | ResNet-50, Vision Transformer (ViT)              |

---

## 📈 Performance

- **Accuracy**:  
  - ViT: ~98.9%  
  - ResNet-50: ~93.5%  
  - Ensemble: Higher combined accuracy

- **Response time**:  
  - Cloud: 1–3 seconds  
  - Local: 3–7 seconds

- **Max image size**: 10MB

---

## 🛠️ Troubleshooting

- ❗ **Build issues**: Check `requirements.txt` and `package.json`
- ❗ **TypeScript errors**: Validate interface definitions
- ❗ **Prediction bias**: Retrain with more diverse real images and adjust confidence thresholds
- ❗ **Docker/GCP errors**: Verify `.pth` model paths and permissions

---

## 📬 Contact

- **Author**: Omkar 
- **Repo**: [GitHub – ai-detector-app](https://github.com/Omkar-Gavali/ai-detector)  
- **License**: [MIT License](LICENSE)

---

🧠 _Detect AI, one image at a time._