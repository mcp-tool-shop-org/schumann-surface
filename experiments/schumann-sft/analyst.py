"""The Schumann analyst with the router in front.

    python analyst.py "Why does the data stop at 25 Hz?"
    python analyst.py --route-only "What was the mean mode-1 frequency in June 2013?"
    python analyst.py --serve 8770           # tiny local HTTP: POST /ask {"question": "..."}

Routing (router.py, deterministic): a question that names a month of the archive AND asks for a
statistic goes to the adapter alone (it memorised the per-month statistics; 0.944 on held-out data
questions); everything else goes to the BASE model with the knowledge base in context, which reads
the material literally (0.60 on facts the corpus never contained) instead of inventing plausible
numbers. Routed held-out accuracy: 0.635, against 0.573 for the best single condition. `--else adapter`
puts the adapter on the context route too: 0.646 overall on this set but 0.35 on unseen facts, with
confabulation to match.

Every answer is returned with its route and the model that produced it, so a reader can see which
regime they are in. The adapter is a convenience; the Parquet tables are the record.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252; answers carry Ω and √
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from router import route  # noqa: E402

SYSTEM = ("You are the analyst for the schumann-sierra-nevada dataset: calibrated Schumann resonance products "
          "derived from the Sierra Nevada ELF station's open raw archive. Answer precisely, give numbers and units "
          "when you know them, and say plainly when something is a model rather than a measurement.")
ADAPTER_ID = "mcp-tool-shop/schumann-analyst-qwen2.5-3b-lora"


class Analyst:
    def __init__(self, adapter=None, else_route="base", context_path=None, max_new_tokens=160):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        cfg = json.loads((HERE / "lora-config.json").read_text(encoding="utf-8"))
        self.base_name = cfg["base_model"]; self.else_route = else_route; self.max_new_tokens = max_new_tokens
        self.tok = AutoTokenizer.from_pretrained(self.base_name); self.tok.padding_side = "left"
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        base = AutoModelForCausalLM.from_pretrained(self.base_name, dtype=torch.bfloat16, device_map="cuda")
        local = HERE / "runs" / "run2-30ep" / "epoch30"
        self.model = PeftModel.from_pretrained(base, adapter or (str(local) if local.exists() else ADAPTER_ID))
        self.model.eval()
        ctx = Path(context_path) if context_path else HERE / "data" / "kb-context.md"
        self.context = ctx.read_text(encoding="utf-8")

    def ask(self, question: str) -> dict:
        import torch
        r = route(question)
        use_adapter = (r == "adapter") or (self.else_route == "adapter")
        msgs = [{"role": "system", "content": SYSTEM}]
        if r == "context":
            msgs.append({"role": "user", "content": "Reference material:\n\n" + self.context + "\n\nAnswer the question using the reference material. Be concise and give numbers where the material has them.\n\nQuestion: " + question})
        else:
            msgs.append({"role": "user", "content": question})
        prompt = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        enc = self.tok(prompt, return_tensors="pt", add_special_tokens=False).to("cuda")
        t0 = time.time()
        with torch.no_grad():
            if use_adapter:
                gen = self.model.generate(**enc, max_new_tokens=self.max_new_tokens, do_sample=False, pad_token_id=self.tok.pad_token_id)
            else:
                with self.model.disable_adapter():
                    gen = self.model.generate(**enc, max_new_tokens=self.max_new_tokens, do_sample=False, pad_token_id=self.tok.pad_token_id)
        text = self.tok.decode(gen[0][enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        return {"question": question, "route": r, "model": ("adapter" if use_adapter else "base") + (" + knowledge base in context" if r == "context" else ", no context"),
                "answer": text, "seconds": round(time.time() - t0, 2)}


def serve(analyst, port):
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0)); body = json.loads(self.rfile.read(n) or b"{}")
            out = analyst.ask(body.get("question", "")) if self.path == "/ask" else {"error": "POST /ask {question}"}
            data = json.dumps(out, ensure_ascii=False).encode("utf-8")
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
        def log_message(self, *a): pass
    print(f"analyst listening on http://127.0.0.1:{port}/ask (POST {{\"question\": ...}})", flush=True)
    HTTPServer(("127.0.0.1", port), H).serve_forever()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?"); ap.add_argument("--route-only", action="store_true")
    ap.add_argument("--else", dest="else_route", choices=["base", "adapter"], default="base", help="model for the non-month route")
    ap.add_argument("--adapter", default=None); ap.add_argument("--serve", type=int, default=None)
    a = ap.parse_args()
    if a.route_only:
        print(json.dumps({"question": a.question, "route": route(a.question or "")})); return
    an = Analyst(adapter=a.adapter, else_route=a.else_route)
    if a.serve:
        serve(an, a.serve); return
    if not a.question:
        raise SystemExit("give a question, or --serve <port>")
    print(json.dumps(an.ask(a.question), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
