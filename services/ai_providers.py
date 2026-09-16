import os,json

SYSTEM="""You are an expert presentation architect. Return ONLY valid JSON.
Schema: {"slides":[{"title":"...","bullets":["..."],"speaker_notes":"...","image_prompt":"...","visual_type":"image|flowchart|chart|none"}]}
Keep bullets concise and technically useful. Never invent precise statistics; flag uncertain numbers in notes."""

def generate_content(provider,topic,slides,language,level):
    prompt=f"""{SYSTEM}
Create a {slides}-slide presentation about: {topic}
Audience: {level} engineering student. Language: {language}.
Make the sequence logical and presentation-ready. Include introduction, technical core,
applications/advantages where relevant, conclusion and references when appropriate.
"""
    provider=(provider or "gemini").lower()
    if provider=="gemini":
        key=os.getenv("GEMINI_API_KEY")
        if not key: raise RuntimeError("GEMINI_API_KEY is not configured.")
        from google import genai
        r=genai.Client(api_key=key).models.generate_content(
            model=os.getenv("GEMINI_TEXT_MODEL","gemini-3.1-flash"),contents=prompt)
        text=r.text
    elif provider=="openai":
        key=os.getenv("OPENAI_API_KEY")
        if not key: raise RuntimeError("OPENAI_API_KEY is not configured.")
        from openai import OpenAI
        r=OpenAI(api_key=key).responses.create(
            model=os.getenv("OPENAI_TEXT_MODEL","gpt-5"),input=prompt)
        text=r.output_text
    elif provider=="anthropic":
        key=os.getenv("ANTHROPIC_API_KEY")
        if not key: raise RuntimeError("ANTHROPIC_API_KEY is not configured.")
        from anthropic import Anthropic
        r=Anthropic(api_key=key).messages.create(
            model=os.getenv("ANTHROPIC_TEXT_MODEL","claude-sonnet-4-5"),
            max_tokens=6000,system=SYSTEM,messages=[{"role":"user","content":prompt}])
        text="".join(getattr(x,"text","") for x in r.content)
    else: raise RuntimeError("Unsupported provider.")
    text=text.strip()
    try: return json.loads(text)
    except json.JSONDecodeError:
        a,b=text.find("{"),text.rfind("}")
        if a>=0 and b>a: return json.loads(text[a:b+1])
        raise RuntimeError("AI returned invalid JSON. Try again.")
