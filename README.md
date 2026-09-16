# AI PPT Maker — Deploy Ready

## Deploy on Render
1. Put this project in a GitHub repository.
2. In Render, choose **New → Web Service** and connect the repository.
3. Build command:
   `pip install -r requirements.txt`
4. Start command:
   `gunicorn app:app`
5. Add your API keys as Environment Variables:
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
6. Deploy. Render will provide a public HTTPS URL.

## Local
```bash
pip install -r requirements.txt
python app.py
```

## Important
This is a deploy-ready Flask foundation. AI providers may require valid API keys and may have usage limits or charges. NotebookLM is not represented as a fake generic API. Review provider model names if your account/API version differs.
