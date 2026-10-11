"""Flask web interface for Assignment 2 — dual mode: Add Facts + Query KB"""
from flask import Flask, render_template, request, jsonify
import aiml, os
from add_facts import (fetch_aiml_variables, build_prolog_fact, write_fact_to_kb,
                       load_existing_facts, fact_already_exists, get_dynamic_facts, AIML_DATA)
from query_chatbot import process_response, _refresh_members, _format
from prolog_engine import PrologEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIML_QUERY = os.path.join(BASE_DIR, "aiml_files", "family.aiml")

app = Flask(__name__)

# ── Initialize engines
engine = PrologEngine()
_refresh_members(engine)
existing_facts = load_existing_facts()

entry_kernel = aiml.Kernel()
entry_kernel.setTextEncoding(None)
entry_kernel.learn(AIML_DATA)

query_kernel = aiml.Kernel()
query_kernel.setTextEncoding(None)
query_kernel.learn(AIML_QUERY)

print("[App] Ready — fact entry + query bots loaded.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_fact", methods=["POST"])
def add_fact():
    global existing_facts
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"response": "Please type something.", "fact": None})

    aiml_resp = entry_kernel.respond(user_msg.upper())

    if aiml_resp.strip() == "DONE_ADDING":
        return jsonify({"response": "All facts saved! Switch to Query mode to explore.", "fact": None, "done": True})

    if aiml_resp.strip() == "SHOW_FACTS":
        facts = get_dynamic_facts()
        if facts:
            return jsonify({"response": f"Facts in KB ({len(facts)}):\n" + "\n".join(facts), "fact": None})
        return jsonify({"response": "No facts added yet.", "fact": None})

    fact_type, arg1, arg2, ready = fetch_aiml_variables(entry_kernel)
    saved_fact = None

    if ready == "yes":
        fact_str = build_prolog_fact(fact_type, arg1, arg2)
        if fact_str:
            if fact_already_exists(fact_str, existing_facts):
                aiml_resp += f"\n(Already in KB: {fact_str})"
            else:
                write_fact_to_kb(fact_str)
                existing_facts.add(fact_str)
                # Reload Prolog engine
                engine.reload()
                _refresh_members(engine)
                saved_fact = fact_str
                aiml_resp += f"\n✓ Saved to KB: {fact_str}"
        entry_kernel.setPredicate("fact_ready", "no")

    return jsonify({"response": aiml_resp.strip(), "fact": saved_fact})


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"response": "Please type a question."})
    aiml_resp = query_kernel.respond(user_msg.upper())
    if "PROLOG:" not in aiml_resp:
        return jsonify({"response": aiml_resp})
    response = process_response(aiml_resp, user_msg, engine)
    return jsonify({"response": response})


@app.route("/kb_facts", methods=["GET"])
def kb_facts():
    return jsonify({"facts": get_dynamic_facts()})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
