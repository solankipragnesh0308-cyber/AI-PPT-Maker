let deck=[];
const $=id=>document.getElementById(id);
function setStatus(x){$("status").textContent=x}
async function generate(){
 const topic=$("topic").value.trim(); if(!topic)return setStatus("Enter a topic.");
 setStatus("Generating...");
 try{
  const r=await fetch("/api/generate-content",{method:"POST",headers:{"Content-Type":"application/json"},
   body:JSON.stringify({topic,slides:+$("slides").value,language:$("language").value,level:$("level").value,provider:$("provider").value})});
  const d=await r.json(); if(!r.ok)throw Error(d.error||"Generation failed"); deck=d.slides||[]; render();
  setStatus("Content generated. Edit slides if needed, then export.");
 }catch(e){setStatus(e.message)}
}
function render(){
 $("editor").innerHTML=deck.map((s,i)=>`<div class="slide"><b>Slide ${i+1}</b>
 <input value="${esc(s.title||"")}" oninput="deck[${i}].title=this.value">
 <textarea oninput="deck[${i}].bullets=this.value.split('\\n')">${(s.bullets||[]).join("\n")}</textarea>
 <textarea placeholder="Speaker notes" oninput="deck[${i}].speaker_notes=this.value">${esc(s.speaker_notes||"")}</textarea>
 </div>`).join("");
}
function esc(x){return String(x).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;")}
async function makeImage(){
 const p=$("imagePrompt").value.trim(); if(!p)return;
 const r=await fetch("/api/generate-image",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt:p})});
 const d=await r.json(); if(!r.ok)return alert(d.error);
 $("preview").src=d.url;
}
async function makePpt(){
 if(!deck.length)return alert("Generate content first.");
 const r=await fetch("/api/make-ppt",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({slides:deck,title:$("topic").value,theme:$("theme").value})});
 const d=await r.json(); if(!r.ok)return alert(d.error);
 $("download").href=d.url;$("download").textContent="Download "+d.filename;
}
