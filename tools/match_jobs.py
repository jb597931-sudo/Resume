#!/usr/bin/env python3
"""Score job postings against the CV, build a tailored CV for each, write a tracker.

Usage (from the repo root):
    python3 tools/match_jobs.py              # all postings in jobs/postings/ and jobs/postings.csv
    python3 tools/match_jobs.py --no-build   # score only, skip PDF builds

Input: one .txt/.md file per posting in jobs/postings/ (header lines, then ---,
then the full job description), and/or rows in jobs/postings.csv
(title,company,location,url,source,posted,description). See jobs/README.md.

Output:
    output/job-matches.xlsx                  tracker, sorted by match score
    applications/auto/<slug>.tex             tailored application file per posting
    output/<Name>_CV_<slug>.pdf              tailored one-page CV per posting

What "tailored" means here (all of it truthful):
  * the CV profile (ml/genai/nlp/cv/ds/research/quant) closest to the posting
  * the posting's own job title as the CV headline
  * projects reordered so the most relevant one comes first
  * skills you already have, re-spelled the way the posting spells them,
    in an "Additional" row (e.g. the posting says "Large Language Models",
    the CV says "LLMs"), so an exact-match ATS finds them.
Skills the posting wants and the CV lacks are NEVER added. They're listed in
the "Missing" column for you to add to personal.tex only if true.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTINGS_DIR = ROOT / "jobs" / "postings"
POSTINGS_CSV = ROOT / "jobs" / "postings.csv"
AUTO_DIR = ROOT / "applications" / "auto"
OUTPUT = ROOT / "output"

# ---------------------------------------------------------------------------
# Skill taxonomy: canonical name -> regex of the spellings postings use.
# Matching is case-insensitive with word boundaries. Extend freely.
# ---------------------------------------------------------------------------
SKILLS: dict[str, str] = {
    # languages & libraries
    "Python": r"python",
    "SQL": r"sql|postgres(?:ql)?|mysql",
    "C++": r"c\+\+",
    "Java": r"java(?!script)",
    "Scala": r"scala",
    "JavaScript/TypeScript": r"javascript|typescript",
    "Bash": r"bash|shell scripting",
    "PyTorch": r"pytorch|torch",
    "TensorFlow": r"tensorflow",
    "Keras": r"keras",
    "scikit-learn": r"scikit[- ]?learn|sklearn",
    "XGBoost": r"xgboost",
    "LightGBM/CatBoost": r"lightgbm|catboost",
    "JAX": r"jax",
    "Hugging Face": r"hugging ?face|transformers library",
    "pandas": r"pandas",
    "NumPy": r"numpy",
    "Spark": r"py?spark|apache spark",
    "OpenCV": r"opencv",
    "spaCy": r"spacy",
    "NLTK": r"nltk",
    "LangChain": r"langchain",
    "LlamaIndex": r"llama ?index",
    "FastAPI": r"fastapi",
    "Flask/Django": r"flask|django",
    "Gradio/Streamlit": r"gradio|streamlit",
    "Sentence Transformers": r"sentence[- ]transformers?|sbert",
    # ML concepts
    "Machine Learning": r"machine learning|maschinelle[sn]? lernen|ml(?=[\s,/)])",
    "Deep Learning": r"deep learning|neural networks?|neuronale netze",
    "NLP": r"nlp|natural language processing|computerlinguistik|sprachverarbeitung",
    "Computer Vision": r"computer vision|bildverarbeitung|image processing|machine vision",
    "LLMs": r"llms?|large language models?|sprachmodelle?|foundation models?",
    "Generative AI": r"generative ai|genai|gen ai|generative ki",
    "RAG": r"rag|retrieval[- ]augmented(?: generation)?",
    "Embeddings": r"embeddings?",
    "Vector database": r"vector (?:db|database|store|search)|pinecone|weaviate|qdrant|chroma(?:db)?|milvus|pgvector",
    "FAISS": r"faiss",
    "Semantic search": r"semantic (?:search|similarity)",
    "Information retrieval": r"information retrieval|search relevance|ranking",
    "Prompt engineering": r"prompt(?:ing| engineering)",
    "AI agents": r"ai agents?|agentic|multi-agent",
    "Fine-tuning": r"fine[- ]?tun(?:e|ing|ed)",
    "LoRA / PEFT": r"lora|qlora|peft",
    "Transformers": r"transformers?(?: models?| architectures?)?",
    "BERT": r"bert|roberta",
    "LLaMA": r"llama(?! ?index)",
    "NER": r"ner|named entity recognition",
    "Text classification": r"text classification|textklassifikation",
    "Sentiment analysis": r"sentiment analysis",
    "CNNs": r"cnns?|convolutional",
    "LSTM/RNN": r"lstm|rnns?|recurrent neural",
    "GRU": r"gru",
    "Segmentation": r"segmentation|segmentierung|u-?net",
    "Object detection": r"object detection|objekterkennung|yolo",
    "Image classification": r"image classification|bildklassifikation",
    "Time series": r"time[- ]series|zeitreihen",
    "Forecasting": r"forecasting|prognose|vorhersage",
    "Anomaly detection": r"anomaly detection|anomalieerkennung",
    "Defect detection / visual inspection": r"defect detection|visual inspection|quality inspection|fehlererkennung|qualitätsprüfung",
    "Recommender systems": r"recommender|recommendation systems?",
    "Reinforcement learning": r"reinforcement learning",
    "Statistics": r"statistics|statistik|statistical",
    "A/B testing": r"a/b[- ]test(?:ing)?|experimentation",
    "Data visualization": r"data visuali[sz]ation|matplotlib|seaborn|plotly",
    "Feature engineering": r"feature engineering",
    "Model evaluation": r"model evaluation|evaluation metrics|benchmarking",
    "Cross-validation": r"cross[- ]validation",
    "Hyperparameter tuning": r"hyperparameter",
    "Explainability (SHAP)": r"shap|explainab\w*|interpretab\w*|xai",
    "Backtesting": r"backtest(?:ing)?",
    "Quant finance": r"quantitative finance|technical indicators|ohlcv",
    "Trading": r"trading|algorithmic trading",
    # engineering & deployment
    "Model deployment": r"model deployment|deploy(?:ing|ment)? (?:ml |machine learning )?models?|model serving|inference",
    "REST APIs": r"rest(?:ful)? apis?|apis?",
    "Microservices": r"microservices?",
    "Docker": r"docker|container(?:s|isation|ization)?",
    "Kubernetes": r"kubernetes|k8s",
    "CI/CD": r"ci/cd|continuous integration|github actions|gitlab ci",
    "MLOps": r"mlops",
    "MLflow": r"mlflow",
    "Airflow": r"airflow",
    "Git": r"git(?!hub actions|lab ci)",
    "Linux": r"linux|unix",
    "AWS": r"aws|amazon web services|sagemaker",
    "Azure": r"azure",
    "GCP": r"gcp|google cloud|vertex ai",
    "Databricks": r"databricks",
    "Tableau/Power BI": r"tableau|power ?bi",
    "ONNX/TensorRT": r"onnx|tensorrt|openvino|tflite|tensorflow lite",
    "Edge AI": r"edge (?:ai|devices?|computing|systems?)|jetson|raspberry pi",
    "Embedded systems": r"embedded(?: systems?| systeme| software)?|microcontrollers?|stm32|firmware",
    "ROS": r"ros2?",
    "LiDAR / sensor fusion": r"lidar|sensor fusion|radar",
    "ADAS / autonomous driving": r"adas|autonomous driving|autonomes fahren|self-driving",
    "Research / publications": r"publications?|research experience|peer-reviewed",
}
COMPILED = {k: re.compile(rf"(?<![\w+#])(?:{v})(?![\w+#])", re.I) for k, v in SKILLS.items()}

# Which projects to put first, by overlap with the posting's skills.
PROJECT_SKILLS = {
    r"\projRAG": {"RAG", "Embeddings", "FAISS", "Semantic search", "Information retrieval", "LLMs",
                   "Generative AI", "NLP", "Sentence Transformers", "Vector database", "Gradio/Streamlit",
                   "Prompt engineering", "AI agents"},
    r"\projLane": {"Computer Vision", "Segmentation", "CNNs", "Object detection", "ADAS / autonomous driving",
                    "PyTorch", "Deep Learning", "Image classification", "OpenCV", "Edge AI"},
    r"\projHeart": {"XGBoost", "scikit-learn", "Explainability (SHAP)", "Cross-validation",
                     "Hyperparameter tuning", "Statistics", "Feature engineering", "Machine Learning"},
}
# Projects each profile shows (order is decided per posting). Mirrors profiles.tex.
PROFILE_PROJECTS = {
    "ml": [r"\projRAG", r"\projLane", r"\projHeart"],
    "genai": [r"\projRAG", r"\projLane", r"\projHeart"],
    "nlp": [r"\projRAG", r"\projHeart", r"\projLane"],
    "cv": [r"\projLane", r"\projRAG", r"\projHeart"],
    "ds": [r"\projHeart", r"\projRAG", r"\projLane"],
    "research": [r"\projLane", r"\projRAG", r"\projHeart"],
    "quant": [r"\projHeart", r"\projRAG"],
}

# Skills the CV implies even when the exact word isn't there.
IMPLIED = {
    "Generative AI": {"RAG", "LLMs"},
    "Information retrieval": {"Semantic search", "FAISS"},
    "Deep Learning": {"PyTorch", "CNNs", "Transformers"},
    "Machine Learning": {"scikit-learn", "XGBoost", "PyTorch"},
}

# How well each job family fits the CV overall (Strong/Good/Stretch ratings in
# job-titles-ats-keywords.md). Used as a prior so that a posting with only a
# few recognisable skills isn't scored 0% or 100% on thin evidence.
FAMILY_PRIOR = {"genai": 0.8, "nlp": 0.8, "cv": 0.8, "ml": 0.75, "research": 0.75, "ds": 0.7, "quant": 0.5}
PRIOR_STRENGTH = 3.0  # acts like 3 extra skill mentions at the family's fit rate

# Title -> profile, checked in order. Covers the 20 titles in job-titles-ats-keywords.md.
TITLE_RULES = [
    ("quant", r"quant|trading|algorithmic"),
    ("cv", r"computer vision|vision|visual|perception|adas|autonom|image|bildverarbeitung|inspection|inspektion|prüf|"
           r"robot|edge ai|embedded"),
    ("nlp", r"\bnlp\b|natural language|computational ling|text analytics|sprach"),
    ("research", r"research|thesis|abschlussarbeit|masterarbeit|hiwi|hilfskraft|applied scientist|wissenschaftlich"),
    ("genai", r"gen ?ai|generative|\bllm|\brag\b|chatbot|conversational|\bsearch\b|retrieval|\bagent|\bai engineer|"
              r"\bki[- ]|artificial intelligence|künstliche intelligenz"),
    ("ds", r"data scien|forecast|analytics|data analyst"),
    ("ml", r"machine learning|\bml\b|mlops|deep learning|\bai\b|\bki\b"),
]
JUNIOR = re.compile(r"werkstudent|working student|student|intern(?:ship)?\b|praktik|thesis|abschlussarbeit|masterarbeit|"
                    r"junior|entry[- ]level|graduate|absolvent|berufseinst|hiwi|hilfskraft|trainee", re.I)
SENIOR = re.compile(r"\b(?:senior|sr\.?|lead|principal|staff|head of|director|manager|architect)\b", re.I)
YEARS = re.compile(r"(\d{1,2})\s*\+?\s*(?:-\s*\d+\s*)?(?:years?|yrs|jahre)", re.I)
GERMAN_REQ = re.compile(
    r"fließend(?:e|es)? deutsch|sehr gute(?:n)? deutsch|verhandlungssicher(?:e|es)? deutsch|deutsch\w* (?:auf )?(?:c1|c2|muttersprach)|"
    r"(?:fluent|business[- ]fluent|excellent|very good|native)\w*(?: command of| in)? german|german \(?(?:c1|c2|native|fluent)|"
    r"english and german (?:are |is )?required|german (?:is |are )?required|deutsch und englisch|deutschkenntnisse erforderlich",
    re.I)
GERMAN_WORDS = re.compile(r"\b(?:und|wir|sie|für|mit|ihre?|der|die|das|bei|unser(?:e|em)?|kenntnisse)\b", re.I)
NICE_TO_HAVE = re.compile(r"nice[- ]to[- ]have|bonus|plus\b|von vorteil|wünschenswert|optional|preferred|ideally|idealerweise", re.I)
GENDER_TAG = re.compile(r"\s*\((?:[mwfdxi]\s*/\s*){1,3}[mwfdxi]\)|\s*\(all genders?\)|\s*\(gn\)|\s*\*in\b", re.I)


@dataclass
class Posting:
    title: str
    company: str = ""
    location: str = ""
    url: str = ""
    source: str = ""
    posted: str = ""
    description: str = ""
    file: str = ""
    notes: str = ""
    # results
    profile: str = ""
    skills_pct: float = 0.0
    title_fit: float = 0.0
    level_fit: float = 0.0
    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    german: str = ""
    confidence: str = ""
    slug: str = ""
    cv_pdf: str = ""
    cv_note: str = ""

    @property
    def score(self) -> float:  # mirrors the spreadsheet formula with default weights
        return round(100 * (0.6 * self.skills_pct + 0.2 * self.title_fit + 0.2 * self.level_fit))


# ---------------------------------------------------------------------------
def strip_tex(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)            # comments
    text = re.sub(r"\\(?:onlyfor|skipfor)\{[^}]*\}", " ", text)  # profile tags, not content
    text = re.sub(r"profile@\w+|\\def\\role\{\w+\}", " ", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?", " ", text)       # commands
    return re.sub(r"[{}$\\]", " ", text)


def cv_text() -> str:
    # Only CV content: the project bank + document body of cv-master, and the
    # summaries/skill rows in profiles. Skips preamble code and comments.
    master = (ROOT / "cv-master.tex").read_text(encoding="utf-8")
    master = master[master.index("PROJECT BANK"):]
    parts = [master, (ROOT / "profiles.tex").read_text(encoding="utf-8")]
    personal = ROOT / "personal.tex"
    if personal.exists():
        m = re.search(r"\\def\\cvextraskills\{(.*)\}", personal.read_text(encoding="utf-8"))
        if m:
            parts.append(m.group(1))
    return strip_tex("\n".join(parts))


def german_level() -> str:
    """Your German level (e.g. 'B1') from \\cvlanguages in personal.tex, or ''."""
    personal = ROOT / "personal.tex"
    if personal.exists():
        m = re.search(r"\\def\\cvlanguages\{(.*)\}", personal.read_text(encoding="utf-8"))
        if m:
            lvl = re.search(r"(?:german|deutsch)\W*\(?\s*(A1|A2|B1|B2|C1|C2|native|muttersprach\w*)", m.group(1), re.I)
            if lvl:
                return lvl.group(1).upper() if len(lvl.group(1)) == 2 else "native"
    return ""


def find_skills(text: str) -> dict[str, str]:
    """canonical skill -> first surface form found in text"""
    out = {}
    for name, rx in COMPILED.items():
        m = rx.search(text)
        if m:
            out[name] = m.group(0)
    return out


def weighted_skills(desc: str) -> dict[str, float]:
    """Skill -> weight; 0.5 for skills only mentioned under a nice-to-have heading/line."""
    weights: dict[str, float] = {}
    in_nice = False
    for line in desc.splitlines():
        stripped = line.strip()
        is_heading = bool(stripped) and (len(stripped) < 60 and not stripped.startswith(("-", "•", "*")))
        if NICE_TO_HAVE.search(line):
            in_nice = True
        elif is_heading:
            in_nice = False
        for name, rx in COMPILED.items():
            if rx.search(line):
                w = 0.5 if (in_nice or NICE_TO_HAVE.search(line)) else 1.0
                weights[name] = max(weights.get(name, 0), w)
    return weights


def pick_profile(title: str, jd_skills: dict[str, float]) -> tuple[str, float]:
    for prof, rx in TITLE_RULES:
        if re.search(rx, title, re.I):
            return prof, 1.0
    # Title gave no signal: fall back to the posting's skills.
    votes = {
        "genai": {"LLMs", "Generative AI", "RAG", "Prompt engineering", "AI agents", "Vector database"},
        "nlp": {"NLP", "NER", "Text classification", "BERT", "spaCy"},
        "cv": {"Computer Vision", "Segmentation", "Object detection", "OpenCV", "CNNs"},
        "ds": {"Statistics", "SQL", "A/B testing", "Data visualization", "Forecasting"},
        "ml": {"Machine Learning", "Deep Learning", "Model deployment", "MLOps", "PyTorch"},
    }
    best = max(votes, key=lambda p: len(votes[p] & jd_skills.keys()))
    hits = len(votes[best] & jd_skills.keys())
    return (best if hits else "ml"), (0.5 if hits >= 2 else 0.0)


def level_fit(title: str, desc: str) -> float:
    if JUNIOR.search(title):
        return 1.0
    if SENIOR.search(title):
        return 0.1
    years = [int(y) for y in YEARS.findall(desc) if int(y) < 20]
    if years and min(years) >= 3:
        return 0.3
    if years and min(years) == 2:
        return 0.7
    if JUNIOR.search(desc):
        return 1.0
    return 0.7


def slugify(*parts: str) -> str:
    s = "-".join(p for p in parts if p)
    s = unicodedata.normalize("NFKD", GENDER_TAG.sub("", s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:70].rstrip("-")


def tex_escape(s: str) -> str:
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
           "–": r"\textendash{}", "—": r"\textemdash{}"}
    s = "".join(rep.get(c, c) for c in s)
    return re.sub(r"(?<=\s)-(?=\s)", r"\\textendash{}", s)


# ---------------------------------------------------------------------------
def load_postings(postings_dir: Path = POSTINGS_DIR, postings_csv: Path = POSTINGS_CSV) -> list[Posting]:
    postings = []
    if postings_dir.exists():
        for f in sorted(postings_dir.glob("*")):
            if f.suffix.lower() not in (".txt", ".md") or f.name.startswith(("_", ".")):
                continue
            raw = f.read_text(encoding="utf-8")
            head, sep, body = raw.partition("\n---")
            if not sep:
                print(f"skip {f.name}: no '---' line between header and description", file=sys.stderr)
                continue
            meta = {}
            for line in head.splitlines():
                k, _, v = line.partition(":")
                if v:
                    meta[k.strip().lower()] = v.strip()
            if not meta.get("title"):
                print(f"skip {f.name}: header needs a 'title:' line", file=sys.stderr)
                continue
            postings.append(Posting(title=meta["title"], company=meta.get("company", ""),
                                    location=meta.get("location", ""), url=meta.get("url", ""),
                                    source=meta.get("source", ""), posted=meta.get("posted", ""),
                                    description=body.lstrip("-\n"), file=f.name))
    if postings_csv.exists():
        with postings_csv.open(encoding="utf-8-sig", newline="") as fh:
            for i, row in enumerate(csv.DictReader(fh), start=2):
                row = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
                if not row.get("title"):
                    continue
                postings.append(Posting(title=row["title"], company=row.get("company", ""),
                                        location=row.get("location", ""), url=row.get("url", ""),
                                        source=row.get("source", ""), posted=row.get("posted", ""),
                                        description=row.get("description", ""), notes=row.get("notes", ""),
                                        file=f"{postings_csv.name}:{i}"))
    # de-duplicate on url, else on title+company
    seen, unique = set(), []
    for p in postings:
        key = p.url or (p.title.lower(), p.company.lower())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def score(p: Posting, cv: str, cv_skills: dict[str, str]) -> None:
    jd = f"{p.title}\n{p.description}"
    weights = weighted_skills(jd)
    total = sum(weights.values())
    have = {k: w for k, w in weights.items() if k in cv_skills}
    p.profile, p.title_fit = pick_profile(p.title, weights)
    prior = FAMILY_PRIOR[p.profile]
    p.skills_pct = round((sum(have.values()) + PRIOR_STRENGTH * prior) / (total + PRIOR_STRENGTH), 3)
    p.matched = sorted(have, key=lambda k: -weights[k])
    p.missing = sorted((k for k in weights if k not in cv_skills), key=lambda k: -weights[k])
    p.level_fit = level_fit(p.title, p.description)
    level = german_level()
    gap = f" (you: {level})" if level in ("A1", "A2", "B1", "B2") else ""
    if GERMAN_REQ.search(jd):
        p.german = "Required" + gap
    elif len(GERMAN_WORDS.findall(p.description)) > 25:
        p.german = "Likely (ad is in German)" + gap
    else:
        p.german = "Not stated"
    n = len(weights)
    p.confidence = "Low: paste the full description" if n < 5 or len(p.description) < 400 else "OK"
    p.slug = slugify(p.company, p.title) or slugify(Path(p.file).stem)


def write_application(p: Posting, cv: str, include_jobskills: bool = True) -> Path:
    jd_found = find_skills(f"{p.title}\n{p.description}")
    # Same skill, posting's spelling: add it if that exact spelling isn't in the CV.
    respell = []
    for k in p.matched:
        surface = jd_found.get(k)
        if surface and surface.lower() not in cv.lower():
            respell.append(surface.upper() if surface.islower() and len(surface) <= 4 else surface[0].upper() + surface[1:])
    respell = list(dict.fromkeys(respell))[:8]
    projects = sorted(PROFILE_PROJECTS[p.profile],
                      key=lambda pr: -len(PROJECT_SKILLS[pr] & set(p.matched)))
    title = GENDER_TAG.sub("", p.title).strip()
    lines = [
        f"% AUTO-GENERATED by tools/match_jobs.py from {p.file}. Edits are overwritten on the next run;",
        "% to customise, copy this file to applications/ and edit the copy.",
        f"% {p.company} | {p.location} | {p.url}",
        f"% Match {p.score}/100 | missing (add to personal.tex only if true): {', '.join(p.missing) or '-'}",
        rf"\def\role{{{p.profile}}}",
        rf"\def\targettitle{{{tex_escape(title)}}}",
        rf"\def\projectorder{{{''.join(projects)}}}",
    ]
    if include_jobskills and respell:
        lines.append(rf"\def\jobskills{{{tex_escape(', '.join(respell))}}}")
    lines.append(r"\input{cv-master}")
    AUTO_DIR.mkdir(parents=True, exist_ok=True)
    path = AUTO_DIR / f"{p.slug}.tex"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build(p: Posting, cv: str) -> None:
    for include in (True, False):
        app = write_application(p, cv, include_jobskills=include)
        res = subprocess.run([str(ROOT / "build.sh"), str(app.relative_to(ROOT))],
                             cwd=ROOT, capture_output=True, text=True)
        line = next((l for l in res.stdout.splitlines() if l.startswith("output/")), "")
        if res.returncode != 0 or not line:
            p.cv_note = "Build failed: see output/*.log"
            return
        p.cv_pdf = line.split()[0]
        if "WARNING" not in line:
            p.cv_note = "1 page" + ("" if include else " (posting-spelling row dropped to fit)")
            return
    p.cv_note = "Over 1 page: trim manually"


# ---------------------------------------------------------------------------
def write_workbook(postings: list[Posting], path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.comments import Comment
    from openpyxl.formatting.rule import ColorScaleRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    font = "Arial"
    hdr_fill = PatternFill("solid", start_color="1F3864")
    input_fill = PatternFill("solid", start_color="FFFF00")
    thin = Side(style="thin", color="BFBFBF")

    wb = Workbook()
    ws = wb.active
    ws.title = "Jobs"
    st = wb.create_sheet("Settings")

    # --- Settings ----------------------------------------------------------
    st["A1"] = "Match score weights (edit the yellow cells; Jobs!Score recalculates)"
    st["A1"].font = Font(name=font, bold=True, size=12)
    rows = [("Skills match weight", 0.6, "Share of the posting's recognised skills found in your CV (nice-to-haves count half), blended with the job family's overall fit when the text names only a few skills."),
            ("Title fit weight", 0.2, "1 = title matches one of your 20 target titles; 0.5 = matched via skills; 0 = no match."),
            ("Level fit weight", 0.2, "1 = Werkstudent/intern/thesis/junior; 0.7 = unstated; 0.3 = 3+ years required; 0.1 = senior/lead.")]
    for i, (label, val, note) in enumerate(rows, start=3):
        st.cell(i, 1, label).font = Font(name=font)
        c = st.cell(i, 2, val)
        c.font = Font(name=font, color="0000FF")
        c.fill = input_fill
        c.number_format = "0.00"
        st.cell(i, 3, note).font = Font(name=font, italic=True, color="595959")
    st["A7"] = "Legend"
    st["A7"].font = Font(name=font, bold=True)
    legend = ["Yellow cells with blue text are inputs you can change.",
              "Jobs: fill in Status, Applied on and Notes as you go. Every other column comes from tools/match_jobs.py.",
              "Re-running the script rebuilds this file, so keep your Status and Notes in a copy if you've edited them.",
              "Missing = skills the posting asks for that your CV doesn't show. Add one to personal.tex "
              "(\\cvextraskills) only if you can defend it in an interview, then re-run."]
    for i, t in enumerate(legend, start=8):
        st.cell(i, 1, t).font = Font(name=font)
    st.column_dimensions["A"].width = 26
    st.column_dimensions["B"].width = 8
    st.column_dimensions["C"].width = 95

    # --- Jobs ----------------------------------------------------------------
    headers = ["Rank", "Match Score", "Skills Match", "Title Fit", "Level Fit", "Job Title", "Company", "Location",
               "Source", "Posted", "Link", "CV Profile", "Matched Keywords", "Missing Keywords (add only if true)",
               "German", "Data Quality", "Tailored CV", "CV Check", "Status", "Applied On", "Notes", "Posting File"]
    widths = [6, 8, 9, 8, 8, 38, 22, 18, 10, 11, 10, 10, 45, 40, 16, 22, 34, 18, 13, 11, 30, 30]
    for col, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(1, col, h)
        c.font = Font(name=font, bold=True, color="FFFFFF")
        c.fill = hdr_fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[1].height = 32
    ws["B1"].comment = Comment("= 100 x weighted average of Skills/Title/Level fit, weights on the Settings sheet.", "match_jobs")

    n = len(postings)
    last = n + 1
    for r, p in enumerate(postings, start=2):
        vals = {
            1: f"=RANK(B{r},$B$2:$B${last})",
            2: (f"=ROUND(100*(Settings!$B$3*C{r}+Settings!$B$4*D{r}+Settings!$B$5*E{r})"
                f"/SUM(Settings!$B$3:$B$5),0)"),
            3: p.skills_pct, 4: p.title_fit, 5: p.level_fit,
            6: p.title, 7: p.company, 8: p.location, 9: p.source, 10: p.posted,
            11: "Open" if p.url else "", 12: p.profile,
            13: ", ".join(p.matched), 14: ", ".join(p.missing), 15: p.german, 16: p.confidence,
            17: Path(p.cv_pdf).name if p.cv_pdf else "", 18: p.cv_note,
            19: "To review", 21: p.notes, 22: p.file,
        }
        for col in range(1, len(headers) + 1):
            c = ws.cell(r, col, vals.get(col))
            c.font = Font(name=font)
            c.alignment = Alignment(vertical="top", wrap_text=col in (6, 13, 14, 21))
            c.border = Border(bottom=thin)
        for col in (3, 4, 5):
            ws.cell(r, col).number_format = "0%"
        ws.cell(r, 20).number_format = "yyyy-mm-dd"
        if p.url:
            ws.cell(r, 11).hyperlink = p.url
            ws.cell(r, 11).font = Font(name=font, color="0563C1", underline="single")
        if p.cv_pdf:  # tracker lives in output/, next to the PDFs
            ws.cell(r, 17).hyperlink = Path(p.cv_pdf).name
            ws.cell(r, 17).font = Font(name=font, color="0563C1", underline="single")
        for col in (19, 20, 21):
            ws.cell(r, col).fill = input_fill
            ws.cell(r, col).font = Font(name=font, color="0000FF")

    if n:
        dv = DataValidation(type="list", formula1='"To review,To apply,Applied,Interview,Offer,Rejected,Skipped"',
                            allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"S2:S{last}")
        ws.conditional_formatting.add(f"B2:B{last}", ColorScaleRule(start_type="min", start_color="F8696B",
                                                                    mid_type="percentile", mid_value=50, mid_color="FFEB84",
                                                                    end_type="max", end_color="63BE7B"))
        ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{last}"
    ws.freeze_panes = "G2"
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-build", action="store_true", help="score only; don't build tailored PDFs")
    ap.add_argument("--out", default=str(OUTPUT / "job-matches.xlsx"))
    ap.add_argument("--postings", default=str(POSTINGS_DIR), help="folder of posting files")
    ap.add_argument("--csv", default=str(POSTINGS_CSV), help="CSV of postings")
    args = ap.parse_args()

    postings = load_postings(Path(args.postings), Path(args.csv))
    if not postings:
        print("No postings found. Add files to jobs/postings/ or rows to jobs/postings.csv (see jobs/README.md).")
        return 1
    cv = cv_text()
    cv_skills = find_skills(cv)
    for skill, sources in IMPLIED.items():
        if skill not in cv_skills and sources & cv_skills.keys():
            cv_skills[skill] = skill
    for p in postings:
        score(p, cv, cv_skills)
    postings.sort(key=lambda p: -p.score)
    if not args.no_build:
        for i, p in enumerate(postings, 1):
            print(f"[{i}/{len(postings)}] {p.score:>3}  {p.title} | {p.company}")
            build(p, cv)
    write_workbook(postings, Path(args.out))
    print(f"\nWrote {args.out} with {len(postings)} postings.")
    for p in postings[:10]:
        print(f"  {p.score:>3}  {p.profile:<8} {p.title[:50]:<50} {p.company[:25]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
