"""
Assignment 2 - Main Entry Point
Usage:
    python main.py           -> Step 1-6: Add facts via AIML
    python main.py --query   -> Step 7: Query the updated KB
    python main.py --web     -> Web interface (Flask)
    python main.py --demo    -> Auto-demo (no keyboard input)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_demo():
    """
    Automated demo: adds the full family KB via AIML
    then queries it — no keyboard input needed.
    """
    import aiml
    from add_facts import (fetch_aiml_variables, build_prolog_fact,
                           write_fact_to_kb, load_existing_facts,
                           fact_already_exists, verify_with_prolog, AIML_DATA)

    kernel = aiml.Kernel()
    kernel.setTextEncoding(None)
    kernel.learn(AIML_DATA)

    # ── Simulated natural language inputs
    demo_inputs = [
        # GENDER
        "ali is male", "nasir is male", "awais is male", "yousaf is male",
        "sattar is male", "akhtar is male", "saqib is male", "kamran is male",
        "hamza is male", "zain is male", "usman is male", "tariq is male",
        "samina is female", "shaista is female", "maryam is female",
        "ayesha is female", "qalsoom is female", "suriya is female",
        "shehnaz is female", "zara is female", "mehnaz is female",
        "sara is female", "fatima is female", "alia is female",
        # PARENT
        "ali is the parent of maryam", "ali is the parent of awais",
        "samina is the parent of maryam", "samina is the parent of awais",
        "nasir is the parent of yousaf", "nasir is the parent of ayesha",
        "shaista is the parent of yousaf", "shaista is the parent of ayesha",
        "sattar is the parent of ali", "sattar is the parent of nasir",
        "qalsoom is the parent of ali", "qalsoom is the parent of nasir",
        "akhtar is the parent of samina", "suriya is the parent of samina",
        "saqib is the parent of shaista", "shehnaz is the parent of shaista",
        "zara is the parent of mehnaz", "kamran is the parent of mehnaz",
        "sattar is the parent of zara", "qalsoom is the parent of zara",
        "tariq is the parent of kamran", "tariq is the parent of usman",
        "ali is the parent of hamza", "ali is the parent of alia",
        "ali is the parent of zain",
        "fatima is the parent of hamza", "fatima is the parent of alia",
        "fatima is the parent of zain",
        # MARRIED
        "tariq is married to sara", "ali is married to fatima",
        "ali is married to samina", "nasir is married to shaista",
        "sattar is married to qalsoom", "akhtar is married to suriya",
        "saqib is married to shehnaz", "kamran is married to zara",
        # DOB
        "tariq was born in 1950", "sara was born in 1955",
        "kamran was born in 1975", "ali was born in 1980",
        "fatima was born in 1982", "usman was born in 1985",
        "hamza was born in 2005", "alia was born in 2010",
        "zain was born in 2015", "sattar was born in 1945",
        "qalsoom was born in 1950", "nasir was born in 1978",
        "samina was born in 1982", "shaista was born in 1980",
        "awais was born in 2007", "maryam was born in 2003",
        "yousaf was born in 2001", "ayesha was born in 2005",
        # NATIONALITY
        "add nationality ali pakistani", "add nationality fatima pakistani",
        "add nationality hamza pakistani", "add nationality sattar pakistani",
    ]

    existing = load_existing_facts()
    added = []

    print("\n[DEMO] Adding facts via AIML natural language interface...\n")
    for user_input in demo_inputs:
        aiml_resp = kernel.respond(user_input.upper())
        fact_type, arg1, arg2, ready = fetch_aiml_variables(kernel)
        if ready != "yes":
            continue
        fact_str = build_prolog_fact(fact_type, arg1, arg2)
        if not fact_str or fact_already_exists(fact_str, existing):
            continue
        write_fact_to_kb(fact_str)
        existing.add(fact_str)
        added.append(fact_str)
        kernel.setPredicate("fact_ready", "no")

    print(f"[DEMO] Done! Added {len(added)} new facts to family_kb.pl\n")

    # Show sample facts written
    print("Sample facts added:")
    for f in added[:8]:
        print(f"  {f}")
    if len(added) > 8:
        print(f"  ... and {len(added)-8} more\n")

    verify_with_prolog()


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    elif "--query" in sys.argv:
        from query_chatbot import run_query_bot
        run_query_bot()
    elif "--web" in sys.argv:
        from app import app
        print("\n[Web] Starting at http://127.0.0.1:5000")
        app.run(debug=False, port=5000)
    else:
        from add_facts import run_fact_collector
        run_fact_collector()
