"""
Query Chatbot — Step 7
Uses the existing family.aiml + updated KB to answer queries.
"""
import aiml, os
from prolog_engine import PrologEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIML_QUERY = os.path.join(BASE_DIR, "aiml_files", "family.aiml")

ALL_MEMBERS_CACHE = set()

def _refresh_members(engine):
    global ALL_MEMBERS_CACHE
    r1 = engine.get_values(engine.query("male(X)"), "X")
    r2 = engine.get_values(engine.query("female(X)"), "X")
    ALL_MEMBERS_CACHE = set(r1 + r2)

def _extract_name(text):
    text_lower = text.lower()
    for name in ALL_MEMBERS_CACHE:
        if name in text_lower:
            return name
    return None

def _format(relation, target, values):
    if not values:
        return f"Sorry, I could not find any {relation.replace('_',' ')} for {target.capitalize()} in the knowledge base."
    names = [v.capitalize() for v in values]
    ns = ", ".join(names[:-1]) + (" and " + names[-1] if len(names) > 1 else names[0])
    tpl = {
        "father": f"The father of {target.capitalize()} is {ns}.",
        "mother": f"The mother of {target.capitalize()} is {ns}.",
        "son":    f"The son(s) of {target.capitalize()} are: {ns}.",
        "daughter":f"The daughter(s) of {target.capitalize()} are: {ns}.",
        "brother": f"The brother(s) of {target.capitalize()} are: {ns}.",
        "sister":  f"The sister(s) of {target.capitalize()} are: {ns}.",
        "sibling": f"The sibling(s) of {target.capitalize()} are: {ns}.",
        "husband": f"The husband of {target.capitalize()} is {ns}.",
        "wife":    f"The wife/wives of {target.capitalize()} are: {ns}.",
        "spouse":  f"The spouse of {target.capitalize()} is {ns}.",
        "grandfather": f"The grandfather of {target.capitalize()} is {ns}.",
        "grandmother": f"The grandmother of {target.capitalize()} is {ns}.",
        "grandson":    f"The grandson(s) of {target.capitalize()} are: {ns}.",
        "granddaughter":f"The granddaughter(s) of {target.capitalize()} are: {ns}.",
        "uncle":   f"The uncle(s) of {target.capitalize()} are: {ns}.",
        "aunt":    f"The aunt(s) of {target.capitalize()} are: {ns}.",
        "nephew":  f"The nephew(s) of {target.capitalize()} are: {ns}.",
        "niece":   f"The niece(s) of {target.capitalize()} are: {ns}.",
        "cousin":  f"The cousin(s) of {target.capitalize()} are: {ns}.",
        "father_in_law": f"The father-in-law of {target.capitalize()} is {ns}.",
        "mother_in_law": f"The mother-in-law of {target.capitalize()} is {ns}.",
        "son_in_law":    f"The son-in-law of {target.capitalize()} is {ns}.",
        "daughter_in_law":f"The daughter-in-law(s) of {target.capitalize()} are: {ns}.",
        "taya":    f"The Taya (elder paternal uncle) of {target.capitalize()} is {ns}.",
        "chacha":  f"The Chacha (younger paternal uncle) of {target.capitalize()} is {ns}.",
        "dada":    f"The Dada (paternal grandfather) of {target.capitalize()} is {ns}.",
        "dadi":    f"The Dadi (paternal grandmother) of {target.capitalize()} is {ns}.",
        "nana":    f"The Nana (maternal grandfather) of {target.capitalize()} is {ns}.",
        "nani":    f"The Nani (maternal grandmother) of {target.capitalize()} is {ns}.",
        "ancestor":    f"The ancestors of {target.capitalize()} are: {ns}.",
        "descendant":  f"The descendants of {target.capitalize()} are: {ns}.",
        "elder_brother":f"The elder brother of {target.capitalize()} is {ns}.",
        "younger_brother":f"The younger brother of {target.capitalize()} is {ns}.",
    }
    return tpl.get(relation, f"Results for {relation} of {target}: {ns}.")

def process_response(aiml_resp, user_input, engine):
    responses = []
    for token in aiml_resp.split("|"):
        token = token.strip()
        if not token.startswith("PROLOG:"):
            if token: responses.append(token)
            continue
        parts = token.split(":")
        if len(parts) < 3: continue
        relation = parts[1].lower()
        arg1 = parts[2] if len(parts) > 2 else "_"
        arg2 = parts[3] if len(parts) > 3 else None
        person = _extract_name(user_input)

        if relation == "age":
            target = (arg2 or person or "").lower()
            age = engine.get_age(target)
            responses.append(f"{target.capitalize()} is {age} years old." if age else f"No DOB data for {target.capitalize()}.")
            continue
        if relation == "dob":
            target = (arg2 or person or "").lower()
            dob = engine.get_dob(target)
            responses.append(f"{target.capitalize()} was born in {dob}." if dob else f"No DOB data for {target.capitalize()}.")
            continue
        if relation == "gender":
            target = (arg2 or person or "").lower()
            if engine.check_fact("male", target): responses.append(f"{target.capitalize()} is male.")
            elif engine.check_fact("female", target): responses.append(f"{target.capitalize()} is female.")
            else: responses.append(f"No gender data for {target.capitalize()}.")
            continue
        if relation in ("male","female"):
            target = (arg2 or person or "").lower()
            result = engine.check_fact(relation, target)
            responses.append(f"Yes, {target.capitalize()} is {relation}." if result else f"No, {target.capitalize()} is not recorded as {relation}.")
            continue
        if relation == "older" and arg1 != "_" and arg2 and arg2 != "_":
            result = engine.check_binary("older", arg1.lower(), arg2.lower())
            responses.append(f"Yes, {arg1.capitalize()} is older than {arg2.capitalize()}." if result else f"No, {arg1.capitalize()} is not older than {arg2.capitalize()}.")
            continue
        if relation == "related" and arg1 != "_" and arg2 and arg2 != "_":
            result = engine.check_binary("related", arg1.lower(), arg2.lower())
            responses.append(f"Yes, {arg1.capitalize()} and {arg2.capitalize()} are related." if result else f"No, they do not appear related.")
            continue

        target = (arg2 if arg2 and arg2 != "_" else arg1 if arg1 != "_" else person or "").lower()
        if not target:
            responses.append("Please mention a family member's name.")
            continue
        values = engine.find_all(relation, target)
        responses.append(_format(relation, target, values))
    return " ".join(responses) if responses else "I could not find that information."

def run_query_bot():
    engine = PrologEngine()
    _refresh_members(engine)

    kernel = aiml.Kernel()
    kernel.setTextEncoding(None)
    kernel.learn(AIML_QUERY)
    print(f"[AIML] Loaded family.aiml ({kernel.numCategories()} patterns)")

    print("\n" + "="*55)
    print("  FAMILY KB QUERY BOT  (Assignment 2 - Step 7)")
    print("  Querying the dynamically updated knowledge base")
    print("="*55)
    print("  Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input: continue
        if user_input.lower() in ("quit","exit","bye"):
            print("Bot: Goodbye!")
            break
        aiml_resp = kernel.respond(user_input.upper())
        if "PROLOG:" not in aiml_resp:
            print(f"Bot: {aiml_resp}\n")
        else:
            print(f"Bot: {process_response(aiml_resp, user_input, engine)}\n")

if __name__ == "__main__":
    run_query_bot()
