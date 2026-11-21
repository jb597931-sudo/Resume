# CV master template

One LaTeX source, seven ready-made versions, and a 2-minute way to tailor a CV for any job posting. Every PDF it produces is a single page and ATS-clean: one text layer, real Unicode text, no ligatures, no columns, no icons.

## Files

| File | What it is |
|---|---|
| `cv-master.tex` | All CV content. Bullets are tagged by which profiles show them. |
| `profiles.tex` | Seven profiles. Each sets the default headline, summary, project order and skill rows. |
| `personal.tex` | Your contact details. **Gitignored** because this repo is public. Copy it from `personal.example.tex`. |
| `applications/` | One small file per application: `_template.tex` to copy, plus a worked example. |
| `build.sh` | Builds PDFs into `output/` (also gitignored) and warns when a PDF runs past one page. |
| `job-titles-ats-keywords.md` | The 20 target titles and their ATS keywords, which these profiles are built around. |

## First-time setup

```bash
cp personal.example.tex personal.tex   # then fill in your details
./build.sh all                         # builds all 7 default versions
```

In `personal.tex`, fill in `\cvgraduation` and `\cvlanguages`, and put anything you've really used (pandas, NumPy, OpenCV, SQL, Docker...) into `\cvextraskills`. The build reminds you while the first two are empty.

Requirements: a TeX Live install with `pdflatex`. You can also use **Overleaf**: upload every `.tex` file, then set the application file (for example `applications/_template.tex`) as the *Main document*.

## Tailor for one application (about 2 minutes)

```bash
cp applications/_template.tex applications/2026-12-bosch-perception.tex
# edit 2 lines: \role and \targettitle
./build.sh applications/2026-12-bosch-perception.tex
# -> output/Rohit_Ahire_CV_2026-12-bosch-perception.pdf
```

1. **Choose the profile** (`\role`) nearest to the posting:

   | Profile | Use for |
   |---|---|
   | `ml` | ML Engineer, ML Software Engineer, MLOps (junior), Deep Learning Engineer |
   | `genai` | AI Engineer, Generative AI / LLM Engineer, Conversational AI, Search / IR Engineer |
   | `nlp` | NLP Engineer, Text Analytics |
   | `cv` | Computer Vision, Perception / ADAS, Machine Vision / Quality Inspection, Edge AI |
   | `ds` | Data Scientist, Forecasting, Healthcare Data Science |
   | `research` | Applied Scientist, Research Engineer, HiWi, Master Thesis |
   | `quant` | Quantitative Researcher / Analyst |

2. **Paste the exact job title** from the posting into `\targettitle`, for example `Werkstudent Machine Learning (m/w/d)`. A title match is one of the strongest ATS signals.
3. **Optional:** add posting keywords you really have to `\jobskills`, rewrite `\cvsummary` in the posting's own words, or reorder projects with `\projectorder`.
4. **Before sending,** go through the posting's must-have list. Every term you can honestly claim should appear in the PDF *spelled the way the posting spells it* ("scikit-learn" vs "sklearn", "LLMs" vs "large language models").

## Score many postings and build a CV for each

Add postings to `jobs/postings/`, then run `python3 tools/match_jobs.py`. You get `output/job-matches.xlsx`, ranked by match score, plus a tailored PDF for every posting. See [`jobs/README.md`](jobs/README.md).

## Cover letters

`cover-letter.tex` gives every letter the same header and fonts as your CV, and takes contact details from `personal.tex`. Each letter is a small file in `letters/`: copy `letters/_TEMPLATE.tex`, ideally using the same name as the application file so the two PDFs pair up, then fill in the company, the position and the body. Build them with `./build.sh letters`. Set `\cvavailability` in `personal.tex` (for example "from January 2027 for up to 20 hours per week") and every letter gets one availability sentence. Your letters are gitignored.

## Editing content

- **New bullet in every version:** add a plain `\item ...` in `cv-master.tex`.
- **Bullet for some profiles only:** `\onlyfor{cv,research}{\item ...}`, or `\skipfor{quant}{\item ...}`.
- **New project:** copy one of the `\projRAG` / `\projLane` / `\projHeart` blocks in `cv-master.tex`, give it a new name, and add it to each profile's `\projectorder` in `profiles.tex`.
- **New profile:** copy a `\csdef{profile@...}` block in `profiles.tex` and add the name to `PROFILES` in `build.sh`.

After any edit, run `./build.sh all`. It warns when a version spills onto a second page.

## Writing rules this template follows

- **Reverse chronological order** in Experience.
- **Standard section names** that every ATS recognises: Professional Summary, Education, Experience, Projects, Technical Skills.
- **Every bullet = action + what + measurable result.**
- **Spell out each acronym once**, for example "named entity recognition (NER)" or "retrieval-augmented generation (RAG)", so both forms match.
- **Never edit the PDF afterwards.** Change the source and rebuild. Editing the PDF caused the duplicated, unparseable text layer in the old CV.
