# Job Titles & ATS Keywords: Rohit Ahire

Recruiter review of `Rohit_Ahire_CV.pdf` (Nov 2026). It covers the 20 job titles you are most qualified for, the keywords an ATS matches for each one, and the problems in the CV file that hide those keywords today.

**How to read the keyword lists.** An ATS such as Workday, Greenhouse, SAP SuccessFactors, Personio or Lever has no fixed keyword list. It scores your CV against the words in that specific job posting. The lists below are the terms that appear most often in postings for each title.
- **Have:** the term is already in your CV. Keep the exact spelling.
- **Add if true:** postings ask for it and your CV doesn't mention it. Add it only if you can defend it in an interview.

**Seniority.** You have two internships, a student research job and an MSc in progress. In Germany that means you should search for these levels: *Werkstudent*, *Intern/Praktikum*, *Master Thesis/Abschlussarbeit*, *Junior* and *Graduate/Entry-level*. Add one of them to each title below when you search.

---

## Fix these first (they affect every application)

1. **The PDF has two text layers, and an ATS reads both.** Someone added the HiWi role with a PDF editor on top of the LaTeX original. Because of that:
   - The full CV text is in the file **twice**. A parser sees every keyword doubled, and some systems flag that as keyword stuffing.
   - Layout-aware parsers mix the two layers into unreadable text (I tested this; the summary and the experience section come out mixed together).
   - The HiWi role sits at the **end** of the text stream, after Technical Skills. Parsers will either drop it or attach it to the wrong section. It is your newest and most relevant job.
   - It uses a different font (Times, not embedded) from the rest of the CV (Computer Modern).
   **Fix:** add the HiWi role to the LaTeX source and compile again. Don't edit the PDF.
2. **Reverse chronological order is broken.** The ML internship from 2023 is listed above the NLP internship from 2024–25. Use this order: HiWi (2026) → NLP Intern (2024–25) → ML Intern (2023).
3. **Your Skills section leaves out keywords you have already earned.** Hugging Face, LLMs, RAG, FAISS, XGBoost, LSTM/GRU, SHAP, Gradio, Raspberry Pi and time-series forecasting all appear in your bullets but not in Skills. Many ATS systems give the skills section more weight. Suggested version:
   - **Languages:** Python, SQL *(if true)*
   - **ML / DL:** PyTorch, TensorFlow, Keras, scikit-learn, XGBoost, LSTM, GRU, SHAP
   - **NLP / LLMs:** Hugging Face Transformers, BERT, RoBERTa, LLaMA, Sentence Transformers, spaCy, RAG, FAISS, NER, semantic search
   - **Computer Vision:** CNNs, U-Net, image segmentation, OpenCV *(if true)*, SCNN, LaneATT, CLRNet
   - **Deployment / Tools:** FastAPI, Gradio, Docker *(if true)*, Git, Linux *(if true)*, Raspberry Pi, OctoPrint, Jupyter
   - **Data:** pandas, NumPy *(almost certainly true, so add them)*, time-series analysis, feature engineering
4. **No location and no languages.** Recruiters in Germany filter on both. Add `Saarbrücken, Germany` to the header, plus a line like `Languages: English (C1), German (B1)` with your real levels. Write the phone number in international format (`+49 ...`).
5. **No expected graduation date.** Write `Oct 2024 – Expected <Mon YYYY>`. Werkstudent, thesis and graduate postings screen on it.
6. **The summary should name the job titles.** For example: *"MSc Data Science & AI student and Machine Learning Engineer with experience in NLP, LLMs/RAG and computer vision..."*. The title match is one of the strongest ATS signals.
7. Check the spelling of "Toward's Imagination". If the company is "Towards Imagination", the apostrophe is wrong.

---

## The 20 titles, ranked by fit

| # | Title | Fit |
|---|---|---|
| 1 | Machine Learning Engineer | Strong |
| 2 | NLP Engineer | Strong |
| 3 | AI Engineer | Strong |
| 4 | Generative AI / LLM Engineer | Strong |
| 5 | Data Scientist | Strong |
| 6 | Computer Vision Engineer | Strong |
| 7 | Working Student / Student Research Assistant (HiWi), ML & AI | Strong |
| 8 | Master Thesis Candidate, ML / NLP / CV | Strong |
| 9 | Applied Scientist (ML) | Good |
| 10 | Deep Learning Engineer | Good |
| 11 | Machine Learning Research Engineer | Good |
| 12 | Search / Information Retrieval Engineer | Good |
| 13 | Perception Engineer (ADAS / Autonomous Driving) | Good |
| 14 | Machine Vision / Visual Quality Inspection Engineer | Good |
| 15 | Conversational AI / Chatbot Engineer | Good |
| 16 | ML Software Engineer (Python Backend) | Good |
| 17 | Time-Series / Forecasting Data Scientist | Good |
| 18 | Junior Quantitative Researcher / Quant Analyst | Stretch |
| 19 | MLOps Engineer | Stretch |
| 20 | Edge AI / Embedded ML Engineer | Stretch |

Honorable mention: **Healthcare / Clinical Data Scientist**. Your heart-disease project with XGBoost, SHAP and ROC-AUC fits, but one project isn't enough to rank it higher.

---

### 1. Machine Learning Engineer (Strong)
**Search also as:** ML Engineer, Junior Machine Learning Engineer, Machine Learning Engineer Intern, Werkstudent Machine Learning (m/w/d)
**Why:** You have trained, evaluated *and* deployed models: FastAPI microservices with <120 ms latency, XGBoost/LSTM/GRU benchmarks, and an evaluation-driven focus.
- **Have:** Python, PyTorch, TensorFlow, Keras, scikit-learn, XGBoost, model training, model evaluation, feature engineering, model deployment, FastAPI, microservices, inference latency, benchmarking, Git, end-to-end pipeline
- **Add if true:** Docker, CI/CD, AWS / GCP / Azure, MLflow, SQL, pandas, NumPy, Linux, REST API, unit testing (pytest), model monitoring

### 2. NLP Engineer (Strong)
**Search also as:** Natural Language Processing Engineer, NLP Scientist, Computational Linguist (industry), Text Analytics Engineer
**Why:** Your NLP internship covers the whole core NLP skill set: fine-tuning, classification, NER and semantic similarity.
- **Have:** NLP, Natural Language Processing, Transformers, Hugging Face, BERT, RoBERTa, LLaMA, fine-tuning, text classification, sentiment analysis, NER, Named Entity Recognition, spaCy, Sentence Transformers, semantic similarity, embeddings, F1-score, unstructured data
- **Add if true:** LLMs, PEFT / LoRA, tokenization, information extraction, multilingual NLP, German NLP, topic modeling, NLTK, text preprocessing

### 3. AI Engineer (Strong)
**Search also as:** Junior AI Engineer, Applied AI Engineer, KI-Entwickler (m/w/d), AI Developer, AI Solutions Engineer
**Why:** This is the fastest-growing title of 2025–26. Postings ask for LLMs, RAG, APIs and deployment, and your RAG project plus FastAPI work match that.
- **Have:** Artificial Intelligence, RAG, Retrieval-Augmented Generation, LLaMA, FAISS, vector search, embeddings, FastAPI, Gradio, Python, PyTorch, Hugging Face, model evaluation, deployment
- **Add if true:** LLMs, LangChain, LlamaIndex, OpenAI API, prompt engineering, vector database (Chroma, Qdrant, Pinecone, Weaviate), AI agents, Docker, cloud (Azure OpenAI / AWS Bedrock), REST APIs

### 4. Generative AI / LLM Engineer (Strong)
**Search also as:** GenAI Engineer, LLM Engineer, RAG Engineer, Generative AI Developer
**Why:** The CompanyDocs RAG Assistant is exactly what these teams build: chunking, retrieval, citations, and *measured* evaluation (top-k accuracy, rejection of unsupported questions, a baseline comparison). Most candidates can't show that evaluation work.
- **Have:** Generative AI, RAG, retrieval, chunking, citations, Sentence-Transformers, all-MiniLM-L6-v2, FAISS, semantic retrieval, top-k accuracy, LLaMA, evaluation, hallucination / unsupported-question rejection, Gradio
- **Add if true:** LLMs, LLM evaluation, RAG evaluation (RAGAS), prompt engineering, LangChain, LlamaIndex, vector database, reranking, hybrid search (BM25), fine-tuning (LoRA / QLoRA / PEFT), guardrails, Ollama / vLLM, OpenAI API

### 5. Data Scientist (Strong)
**Search also as:** Junior Data Scientist, Data Scientist Intern, Werkstudent Data Science, Data Science Graduate
**Why:** You have classical ML (XGBoost, stratified CV, threshold calibration, SHAP), time-series work and a Data Science MSc.
- **Have:** Data Science, Machine Learning, Python, scikit-learn, XGBoost, feature engineering, cross-validation, stratified CV, hyperparameter tuning, ROC-AUC, recall, precision, F1-score, SHAP, interpretability, time-series, predictive modeling, Jupyter
- **Add if true:** SQL, pandas, NumPy, statistics, hypothesis testing, A/B testing, data visualization, Matplotlib, Seaborn, Tableau / Power BI, EDA (exploratory data analysis), stakeholder communication

### 6. Computer Vision Engineer (Strong)
**Search also as:** CV Engineer, Computer Vision Scientist, Image Processing Engineer, Werkstudent Computer Vision
**Why:** You built the lane-detection benchmark with 4 architectures and full metrics, and your HiWi role does camera-based visual inspection.
- **Have:** Computer Vision, CNNs, U-Net, semantic segmentation, image segmentation, PyTorch, IoU, F1-score, FPS, real-time inference, TuSimple, SCNN, LaneATT, CLRNet, visual inspection, defect detection, camera pipeline, dataset annotation
- **Add if true:** OpenCV, object detection, YOLO, image classification, data augmentation, ONNX, TensorRT, model optimization / quantization, C++, CUDA

### 7. Working Student / Student Research Assistant (HiWi), ML & AI (Strong)
**Search also as:** Werkstudent (m/w/d) Machine Learning / KI / Data Science, Studentische Hilfskraft, Wissenschaftliche Hilfskraft, Student Assistant AI
**Why:** This is your most realistic offer while you're enrolled. Saarbrücken has DFKI, the Max Planck Institutes for Informatics and Software Systems, CISPA, and htw saar. Automotive employers (ZF, Bosch Homburg) are nearby.
- **Have:** Student Research Assistant, HiWi, prototype, Raspberry Pi, OctoPrint, monitoring dashboard, G-code, 3D printing / FDM, defect detection, dataset evaluation, failure analysis, research, Python, PyTorch
- **Add if true:** enrolled student (immatrikuliert), 20 hours/week, German language level, start date / availability, Linux, documentation, scientific writing

### 8. Master Thesis Candidate, ML / NLP / CV (Strong)
**Search also as:** Masterarbeit / Abschlussarbeit Machine Learning, Master Thesis Computer Vision, Master Thesis LLM / RAG, Thesis Student AI
**Why:** Industry thesis roles at Bosch, Siemens, SAP, Continental, Fraunhofer and others want research ability plus engineering skill, and your projects show both.
- **Have:** MSc Data Science and Artificial Intelligence, research, benchmarking, evaluation, experimental design, ablation-style comparison, PyTorch, deep learning, NLP, computer vision, RAG
- **Add if true:** expected graduation date, thesis start date, literature review, publication, LaTeX, GPU cluster / SLURM

### 9. Applied Scientist (ML) (Good)
**Search also as:** Applied Scientist Intern, Applied ML Scientist, Applied Research Scientist
**Why:** Postings use the words *evaluation*, *baselines* and *metrics* constantly, and your CV is built on them: +20 pts over a keyword baseline, 3.2× lower latency, F1 up 8%.
- **Have:** applied research, machine learning, deep learning, NLP, computer vision, baseline, evaluation metrics, experimentation, PyTorch, Transformers, fine-tuning, benchmarking
- **Add if true:** statistics, probability, publications, experiment design, A/B testing, large-scale data, Spark

### 10. Deep Learning Engineer (Good)
**Search also as:** Deep Learning Scientist, Neural Network Engineer, DL Engineer
- **Have:** Deep Learning, neural networks, PyTorch, TensorFlow, Keras, CNNs, LSTM, GRU, U-Net, Transformers, BERT, RoBERTa, fine-tuning, model training, GPU inference, FPS, parameter count, model size
- **Add if true:** CUDA, distributed training, mixed precision, model compression, quantization, pruning, ONNX, TensorRT, PyTorch Lightning, Weights & Biases

### 11. Machine Learning Research Engineer (Good)
**Search also as:** Research Engineer AI, Research Engineer NLP / CV, AI Research Engineer
- **Have:** research, prototype, benchmarking, reproducible, evaluation, failure cases, limitations, generalization, PyTorch, Transformers, segmentation, RAG
- **Add if true:** paper implementation, reproducing papers, publications, arXiv, open source contributions, experiment tracking, Weights & Biases, Hydra

### 12. Search / Information Retrieval Engineer (Good)
**Search also as:** Semantic Search Engineer, Search Relevance Engineer, Information Retrieval Engineer, Recommender Systems Engineer (junior)
**Why:** FAISS, embeddings, top-k evaluation and a semantic similarity system at 95%+ top-1 accuracy are core IR skills.
- **Have:** information retrieval, semantic search, semantic similarity, vector search, embeddings, FAISS, Sentence Transformers, top-1 / top-k accuracy, retrieval latency, keyword baseline
- **Add if true:** BM25, Elasticsearch, OpenSearch, hybrid search, reranking, cross-encoder, MRR, nDCG, recall@k, approximate nearest neighbor (ANN), HNSW

### 13. Perception Engineer (ADAS / Autonomous Driving) (Good)
**Search also as:** ADAS Engineer, Perception Software Engineer, Autonomous Driving Computer Vision Engineer, Werkstudent ADAS
**Why:** Lane detection on TuSimple with SCNN, LaneATT and CLRNet is directly relevant, and Germany's automotive industry hires heavily for this.
- **Have:** lane detection, perception, ADAS-relevant datasets (TuSimple), semantic segmentation, real-time inference, FPS, U-Net, SCNN, LaneATT, CLRNet, PyTorch, IoU
- **Add if true:** ADAS, autonomous driving, object detection, sensor fusion, camera calibration, LiDAR, point clouds, ROS / ROS 2, C++, CARLA, KITTI, nuScenes, ISO 26262 (awareness)

### 14. Machine Vision / Visual Quality Inspection Engineer (Good)
**Search also as:** Industrial Computer Vision Engineer, Quality Inspection AI Engineer, Bildverarbeitung (m/w/d), Manufacturing AI Engineer
**Why:** Your HiWi role is camera-based monitoring of FDM 3D printing with defect detection. That is Industry 4.0 work, which mid-sized manufacturers in Saarland and southwest Germany hire for.
- **Have:** visual inspection, defect detection, camera-based monitoring, Raspberry Pi camera, 3D printing / FDM, G-code, monitoring dashboard, alerting, real and simulated data, failure cases, occlusion, model generalization
- **Add if true:** machine vision, industrial image processing, anomaly detection, OpenCV, Halcon, industrial cameras, Industry 4.0, predictive maintenance, additive manufacturing, quality control, edge deployment

### 15. Conversational AI / Chatbot Engineer (Good)
**Search also as:** Chatbot Developer, Conversational AI Developer, Virtual Assistant Engineer
- **Have:** chatbot, RAG chatbot, conversational assistant, citations, Gradio, NLP, intent / text classification, NER, LLaMA, semantic retrieval, unsupported-question rejection
- **Add if true:** dialogue systems, Rasa, LangChain, prompt engineering, LLM APIs, Microsoft Bot Framework, Dialogflow, conversation design, guardrails

### 16. ML Software Engineer (Python Backend) (Good)
**Search also as:** Python Developer (AI/ML), Backend Engineer – Machine Learning, Software Engineer ML Platform
- **Have:** Python, FastAPI, microservices, model serving, inference latency (<120 ms), integration into internal tools, API, Git, modular framework design
- **Add if true:** REST API design, Docker, PostgreSQL / SQL, unit testing / pytest, CI/CD, GitHub Actions, async Python, Pydantic, Linux, cloud deployment, code review

### 17. Time-Series / Forecasting Data Scientist (Good)
**Search also as:** Forecasting Analyst, Demand Forecasting Data Scientist, Time-Series ML Engineer
- **Have:** time-series, forecasting, trend prediction, LSTM, GRU, XGBoost, OHLCV, feature engineering, technical indicators, backtesting, 3M+ records, baseline comparison
- **Add if true:** ARIMA / SARIMA, Prophet, statsmodels, demand forecasting, anomaly detection, temporal cross-validation, pandas, SQL, MAPE / RMSE

### 18. Junior Quantitative Researcher / Quant Analyst (Stretch)
**Search also as:** Quantitative Analyst, Quant Researcher Intern, Quantitative Developer (junior), Algorithmic Trading Analyst
**Why it's a stretch:** You have one internship with real quant signals (OHLCV, RSI/MACD/EMA, backtesting framework). Quant postings usually also screen for strong math or statistics and C++.
- **Have:** quantitative, financial time-series, OHLCV, stock market data, technical indicators, RSI, MACD, EMA, backtesting, strategy robustness, XGBoost, LSTM, feature engineering
- **Add if true:** statistics, probability, stochastic processes, alpha research, risk management, Sharpe ratio, portfolio optimization, C++, pandas, NumPy, market microstructure

### 19. MLOps Engineer (Stretch)
**Search also as:** Junior MLOps Engineer, ML Platform Engineer, ML Infrastructure Engineer
**Why it's a stretch:** You have deployment (FastAPI, latency, monitoring dashboard) but none of the infrastructure tools these postings screen for.
- **Have:** model deployment, FastAPI, microservices, inference latency, monitoring, dashboard, pipeline, Git
- **Add if true:** Docker, Kubernetes, CI/CD, MLflow, Kubeflow, Airflow, DVC, Terraform, AWS SageMaker / Azure ML / Vertex AI, Prometheus / Grafana, model registry, model monitoring, data drift

### 20. Edge AI / Embedded ML Engineer (Stretch)
**Search also as:** Embedded AI Engineer, TinyML Engineer, Edge Computer Vision Engineer
**Why it's a stretch:** You have real-time inference at 91.5 FPS and a Raspberry Pi camera pipeline, but no optimization or embedded toolchain on the CV.
- **Have:** Raspberry Pi, edge device, real-time inference, FPS, lightweight model, model size, parameter count, camera capture, IoT-style monitoring
- **Add if true:** ONNX, TensorRT, TensorFlow Lite, OpenVINO, NVIDIA Jetson, quantization, C / C++, embedded Linux, ARM, model compression

---

## Keywords that show up in most of the 20 titles and are missing from your CV

If any of these are true for you, adding them raises your match score for many titles at once:

| Keyword | Appears in titles |
|---|---|
| **Docker** | 1, 3, 4, 16, 19 and most postings in general |
| **SQL** | 1, 5, 16, 17, almost every Data Scientist posting |
| **pandas / NumPy** | 1, 5, 17, 18 |
| **LLMs** (the literal word) | 2, 3, 4, 15: you only list "LLaMA", and many parsers won't link that to "LLMs" |
| **Cloud (AWS / GCP / Azure)** | 1, 3, 16, 19 |
| **OpenCV** | 6, 13, 14, 20 |
| **LangChain / LlamaIndex / vector database** | 3, 4, 15 |
| **German language level** | Required or preferred in most German postings, including many in English |
