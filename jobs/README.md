# Job matching

`tools/match_jobs.py` scores each job posting against your CV, builds a tailored one-page CV for each, and writes a tracker spreadsheet.

## 1. Add postings

You can add postings in either of two ways, or both:

- **One file per posting** in `jobs/postings/`. Copy `_TEMPLATE.txt` to a new name, fill in the header lines, and paste the **full** job description under the `---` line. From LinkedIn or Indeed: open the posting, click "show more", select all of the description text, copy and paste.
- **Many postings at once** in `jobs/postings.csv`, with the columns `title,company,location,url,source,posted,description`. Use this for exports from a job-board API or a spreadsheet you've collected.

Duplicates are dropped by URL, or by title plus company when there's no URL.

## 2. Run

```bash
python3 tools/match_jobs.py            # score + build a tailored CV per posting
python3 tools/match_jobs.py --no-build # score only (fast)
```

It writes:
- `output/job-matches.xlsx`: the tracker, sorted by match score.
- `output/<Name>_CV_<company>-<title>.pdf`: one tailored CV per posting. The tracker links to each one.
- `applications/auto/*.tex`: the generated application files. They're overwritten on every run, so to hand-edit one, copy it to `applications/` and build it from there.

## How the match score works

**Score = 100 × (0.6 × Skills Match + 0.2 × Title Fit + 0.2 × Level Fit).** You can change the weights on the tracker's Settings sheet.

- **Skills Match:** the share of the posting's recognised skills (about 100 terms, in English and German) that your CV shows. Skills that only appear under "nice to have" count half. Your CV skills are read from `cv-master.tex`, `profiles.tex` and `\cvextraskills` in `personal.tex`, so the score follows your CV as it changes.
- **Title Fit:**
  - 1 = the title matches one of your 20 target titles.
  - 0.5 = matched through skills only.
  - 0 = no match.
- **Level Fit:**
  - 1 = Werkstudent, intern, thesis or junior role.
  - 0.7 = level not stated.
  - 0.3 = 3+ years of experience required.
  - 0.1 = senior or lead role.
- **German:** flags postings that require German, or that are written in German. This is shown as a flag and not scored.
- **Data Quality:** "Low" means the description was too short to score reliably. Paste the full text.

## What "tailored" means

Every change is truthful:
- **CV version:** the closest of the 7 (`ml`, `genai`, `nlp`, `cv`, `ds`, `research`, `quant`) is chosen for each posting.
- **Headline:** the posting's own job title, with gender tags like "(m/w/d)" removed.
- **Projects:** reordered so the most relevant one comes first.
- **Spellings:** skills you already have are added in the posting's own wording when it differs from your CV (for example "Segmentierung" for segmentation). That way exact-match ATS filters find them.
- **Nothing you lack is ever added.** Skills the posting asks for that your CV doesn't show appear in the **Missing** column. If one is true for you, add it to `\cvextraskills` in `personal.tex` and run again.

The summary paragraph comes from the chosen CV version. For roles you really want, copy the generated file to `applications/` and rewrite `\cvsummary` in the posting's words.
