CODEXPLAIN is an AI-assisted code review tool for Python that combines traditional static analysis with AI-generated explanations.

The system runs Pylint, Bandit, and Radon on a given Python file, collects their findings, and presents them in a clear, structured format. For medium and high severity issues, it can also generate human-readable explanations using an AI model.

**FEATURES**

* Runs multiple static analysis tools:
  * Pylint (code quality and style)
  * Bandit (security issues)
  * Radon (code complexity)

* Normalizes findings into a consistent structure
* Displays results in a clean, color-coded CLI interface
* Generates AI explanations for:
  * What the issue is
  * Why it matters
  * How to fix it
* Gracefully handles missing AI configuration (no API key required to run basic analysis)

**INSTALLATION**

* Clone the repository:

    git clone https://github.com/fiatolorenzo/CODEXPLAIN.git
    
    cd codexplain
    

* Create a virtual environment:

    python -m venv .venv


* Activate the virtual environment:

    Windows (PowerShell):
..venv\Scripts\activate


* Install dependencies:
    
  pip install -r requirements.txt


**USAGE**

Run the tool on a Python file:

python run_review.py path/to/file.py

Example:

python run_review.py samples/test.py

**OUTPUT**

The tool displays:

* Issues grouped by tool (Pylint, Bandit, Radon)


* Severity levels (LOW, MEDIUM, HIGH)


* AI-generated explanations

Example:

[MEDIUM] Line 3 - eval-used

Issue: Use of eval

Explanation:

Problem: ...

Why: ...

Fix: ...

**AI CONFIGURATION (OPTIONAL)**

CODEXPLAIN uses an OpenAI API key to generate explanations.

To enable AI features, set your API key as an environment variable:

Windows (PowerShell):

setx OPENAI_API_KEY "your_key_here"

Restart your terminal after setting the key.

If no API key is provided, the tool will still run static analysis but will skip AI explanations.

**PROJECT STRUCTURE**

analyzer/ Utility functions for running tools and extracting code context

samples/ Example Python files for testing

run_review.py Main entry point (orchestrates analysis)

run_pylint.py Pylint integration

run_bandit.py Bandit integration

run_radon.py Radon integration

ai_explainer.py AI explanation module

**PURPOSE**

This project was developed as a capstone project to explore how artificial intelligence can enhance traditional software engineering tools.

Instead of replacing static analysis tools, CODEXPLAIN improves their usability by making their output easier to understand, especially for beginner developers.