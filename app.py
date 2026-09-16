import os, uuid
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from services.ai_providers import generate_content
from services.nano_banana import generate_image
from services.ppt_generator import build_ppt

load_dotenv()
BASE=Path(__file__).resolve().parent
GEN=BASE/"generated"
app=Flask(__name__)

@app.get("/")
def index(): return render_template("index.html")

@app.get("/api/config")
def config():
    return jsonify(gemini=bool(os.getenv("GEMINI_API_KEY")),
                   openai=bool(os.getenv("OPENAI_API_KEY")),
                   anthropic=bool(os.getenv("ANTHROPIC_API_KEY")),
                   notebooklm=False)

@app.post("/api/generate-content")
def content():
    d=request.get_json(force=True); topic=(d.get("topic") or "").strip()
    if not topic: return jsonify(error="Topic is required"),400
    try:
        return jsonify(generate_content(d.get("provider","gemini"),topic,
            int(d.get("slides",8)),d.get("language","English"),d.get("level","Diploma")))
    except Exception as e: return jsonify(error=str(e)),500

@app.post("/api/generate-image")
def image():
    d=request.get_json(force=True); prompt=(d.get("prompt") or "").strip()
    if not prompt: return jsonify(error="Image prompt is required"),400
    try:
        fn=generate_image(prompt,d.get("aspect_ratio","16:9"))
        return jsonify(url=f"/generated/images/{fn}",filename=fn)
    except Exception as e: return jsonify(error=str(e)),500

@app.post("/api/make-ppt")
def ppt():
    d=request.get_json(force=True); slides=d.get("slides") or []
    if not slides: return jsonify(error="No slides supplied"),400
    try:
        fn="AI_PPT_"+uuid.uuid4().hex[:8]+".pptx"
        build_ppt(slides,GEN/"presentations"/fn,d.get("title","AI Presentation"),d.get("theme","Professional"))
        return jsonify(url=f"/generated/presentations/{fn}",filename=fn)
    except Exception as e: return jsonify(error=str(e)),500

@app.get("/generated/<folder>/<filename>")
def generated(folder,filename):
    return send_from_directory(GEN/folder,filename)

if __name__=="__main__":
    app.run(host="127.0.0.1",port=int(os.getenv("PORT","5000")),debug=True)
