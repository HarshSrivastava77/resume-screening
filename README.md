# Resume Screening

An LLM-powered tool that extracts structured data from resumes and job
descriptions, then scores how well a candidate matches a role. It reads
`.pdf` and `.docx` resumes, converts free-form text into validated data
models, and produces a match report with strengths, gaps, and a fit score.

Built with [Groq](https://groq.com/) for fast inference and
[Pydantic](https://docs.pydantic.dev/) for strict schema validation.

---

## Features

- **Job description parsing** — turns raw job text into structured fields
  (role, required/preferred skills, experience, education, responsibilities)
- **Resume parsing** — extracts contact details, skills, experience,
  education, projects, and certifications from PDF or DOCX files
- **Resume-to-job matching** — produces an overall fit score (0–100),
  matched/missing skills, strengths, weaknesses, and a hiring recommendation
- **Schema-validated output** — every LLM reply is validated against a
  Pydantic model, so malformed responses fail loudly instead of silently
- **Simple CLI** — run the whole pipeline with a single command

---

## Project Structure

resume-screening/
├── app.py                        # CLI entry point
├── pyproject.toml                # Project metadata and dependencies (uv)
├── .env.example                  # Template for the required API key
├── .gitignore
├── LICENSE
├── README.md
├── data/
│   └── sample_job_description.txt
├── resumes/                      # Put input resumes here (git-ignored)
├── output/                       # Match results saved here (git-ignored)
└── resume_screening/             # Application package
├── init.py
    ├── config.py                 # Model name, paths, API key loading
├── models.py                 # Pydantic data models
├── llm.py                    # Reusable LLM client + prompt builder
├── readers.py                # PDF / DOCX text extraction
  └── analysis.py               # Parse job, parse resume, match

---

## Requirements

- Python **3.10+**
- [uv](https://docs.astral.sh/uv/) — fast Python package manager
- A Groq API key → [get one here](https://console.groq.com/keys)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/HarshSrivastava77/resume-screening.git
cd resume-screening
```

### 2. Install uv (if you don't have it)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Create a virtual environment and install dependencies

```bash
uv venv
uv pip install -r requirements.txt
```

### 4. Activate the virtual environment

```bash
# Windows
.venv\Scripts\Activate.ps1

# Mac / Linux
source .venv/bin/activate
```

### 5. Add your Groq API key

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Then open `.env` and set your key:

---

## Usage

```bash
# Screen a resume against the bundled sample job description
python app.py --resume resumes/candidate.pdf

# Use your own job description
python app.py --resume resumes/candidate.docx --job data/my_job.txt

# Save the match result as JSON in the output folder
python app.py --resume resumes/candidate.pdf --save
```

| Argument   | Required | Description |
|------------|----------|-------------|
| `--resume` | Yes | Path to a `.pdf` or `.docx` resume |
| `--job`    | No  | Path to a job description `.txt` file (defaults to the bundled sample) |
| `--save`   | No  | Write the match result to `output/<resume>_match.json` |

---

## How It Works

1. `readers.py` extracts plain text from the resume file
2. `parse_job_description()` sends job text to the LLM and validates the reply
3. `parse_resume()` sends resume text to the LLM and validates the reply
4. `match_resume()` compares both and returns a scored `MatchResult`
5. `app.py` prints the results and optionally saves them as JSON

All three LLM calls share one helper — `llm.extract_structured()` — which
handles the API request, empty-response errors, and schema validation in one place.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Groq](https://groq.com/) | LLM inference (fast, free tier available) |
| [Pydantic v2](https://docs.pydantic.dev/) | JSON schema generation + validation |
| [pypdf](https://pypdf.readthedocs.io/) | PDF text extraction |
| [python-docx](https://python-docx.readthedocs.io/) | DOCX text extraction |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` file loading |
| [uv](https://docs.astral.sh/uv/) | Virtual environment + package management |

---

## Future Improvements

- Batch mode — screen many resumes against one role and rank candidates
- Web UI using Streamlit or FastAPI
- Unit tests with a mocked LLM client
- Export reports to PDF or CSV
- Support for more file formats (`.txt`, `.odt`)
- Configurable model selection via environment variable

---

## License

Released under the [MIT License](LICENSE).

