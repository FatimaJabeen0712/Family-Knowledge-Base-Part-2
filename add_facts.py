"""
Assignment 2 - Core Module
============================================================
Steps covered:
  Step 3 → Load data_entry.aiml (new AIML file for fact input)
  Step 4 → Fetch stored data from AIML variables (getPredicate)
  Step 5 → String handling to build Prolog fact strings
  Step 6 → File handling to write facts into family_kb.pl
  Step 7 → Prolog KB is now updated and queryable
============================================================
"""

import aiml
import os
import re
from datetime import datetime


# ─────────────────────────────────────────────────────────
#  PATHS
# ─────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
KB_FILE   = os.path.join(BASE_DIR, "family_kb.pl")
AIML_DATA = os.path.join(BASE_DIR, "aiml_files", "data_entry.aiml")
AIML_QUERY= os.path.join(BASE_DIR, "aiml_files", "family.aiml")


# ─────────────────────────────────────────────────────────
#  STEP 4: Fetch AIML variables into Python
# ─────────────────────────────────────────────────────────
def fetch_aiml_variables(kernel):
    """
    Read the three AIML predicates set by data_entry.aiml.
    Returns (fact_type, arg1, arg2) as lowercase strings.
    """
    fact_type = kernel.getPredicate("fact_type").strip().lower()
    fact_arg1 = kernel.getPredicate("fact_arg1").strip().lower()
    fact_arg2 = kernel.getPredicate("fact_arg2").strip().lower()
    fact_ready= kernel.getPredicate("fact_ready").strip().lower()
    return fact_type, fact_arg1, fact_arg2, fact_ready


# ─────────────────────────────────────────────────────────
#  STEP 5: String handling → build Prolog fact string
# ─────────────────────────────────────────────────────────
def build_prolog_fact(fact_type, arg1, arg2):
    """
    Using string handling techniques, construct a valid
    Prolog fact string from the acquired AIML variable data.

    Unary facts  → fact_type(arg1).
    Binary facts → fact_type(arg1, arg2).
    """
    # ── sanitize: strip whitespace, lowercase, replace spaces with underscore
    arg1 = re.sub(r'\s+', '_', arg1.strip().lower())
    arg2 = re.sub(r'\s+', '_', arg2.strip().lower())
    fact_type = fact_type.strip().lower()

    # Validate
    if not fact_type or not arg1:
        return None

    # ── unary facts (male, female)
    UNARY = {"male", "female"}
    if fact_type in UNARY:
        return f"{fact_type}({arg1})."

    # ── binary facts (parent, married, dob, nationality)
    BINARY = {"parent", "married", "dob", "nationality"}
    if fact_type in BINARY:
        if not arg2 or arg2 == "none":
            return None
        # For dob: ensure arg2 is numeric year
        if fact_type == "dob":
            year = re.sub(r'\D', '', arg2)  # keep digits only
            if not year:
                return None
            return f"dob({arg1},{year})."
        return f"{fact_type}({arg1},{arg2})."

    return None


# ─────────────────────────────────────────────────────────
#  STEP 6: File handling → update family_kb.pl
# ─────────────────────────────────────────────────────────
MARKER = "% DYNAMICALLY ADDED FACTS WILL APPEAR BELOW"

def load_existing_facts():
    """Read the KB file and return the set of already-present fact lines."""
    existing = set()
    with open(KB_FILE, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("%"):
                existing.add(stripped)
    return existing


def fact_already_exists(fact_str, existing_facts):
    """Check for duplicate before writing."""
    return fact_str in existing_facts


def write_fact_to_kb(fact_str):
    """
    Append the new Prolog fact after the MARKER line in family_kb.pl.
    Uses file handling: read entire file, find marker, insert fact,
    write back.
    """
    with open(KB_FILE, "r") as f:
        content = f.read()

    # Find insertion point
    if MARKER in content:
        insert_pos = content.index(MARKER) + len(MARKER)
        # Skip to end of marker line
        newline_pos = content.find('\n', insert_pos)
        if newline_pos == -1:
            newline_pos = len(content)
        # Build new content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_fact_line = f"\n{fact_str}  % added {timestamp}"
        content = content[:newline_pos] + new_fact_line + content[newline_pos:]
    else:
        # Marker not found → append at end
        content += f"\n{fact_str}"

    with open(KB_FILE, "w") as f:
        f.write(content)


def get_dynamic_facts():
    """Return all dynamically added facts from the KB file."""
    facts = []
    marker_found = False
    with open(KB_FILE, "r") as f:
        for line in f:
            if MARKER in line:
                marker_found = True
                continue
            if marker_found:
                stripped = line.strip()
                if stripped and not stripped.startswith("%"):
                    # Remove inline comment
                    fact = stripped.split("%")[0].strip()
                    if fact:
                        facts.append(fact)
    return facts


# ─────────────────────────────────────────────────────────
#  STEP 7: Reload KB and verify with Prolog
# ─────────────────────────────────────────────────────────
def verify_with_prolog():
    """Load updated KB into Prolog and run sample queries."""
    from prolog_engine import PrologEngine
    print("\n" + "="*55)
    print("  STEP 7: Verifying updated KB with Prolog queries")
    print("="*55)
    engine = PrologEngine()

    # Test all known members
    import pytholog as pl
    results = engine.query("male(X)")
    males = engine.get_values(results, "X")
    print(f"  Males in KB   : {', '.join(males) if males else 'none'}")

    results = engine.query("female(X)")
    females = engine.get_values(results, "X")
    print(f"  Females in KB : {', '.join(females) if females else 'none'}")

    results = engine.query("parent(X,Y)")
    parents_raw = engine.get_values(results, "X")
    print(f"  Parents in KB : {', '.join(set(parents_raw)) if parents_raw else 'none'}")

    results = engine.query("married(X,Y)")
    married_raw = engine.get_values(results, "X")
    print(f"  Married (P1)  : {', '.join(set(married_raw)) if married_raw else 'none'}")

    print("\n  Running relationship queries:")
    for name in males[:3]:
        fathers = engine.find_all("father", name)
        if fathers:
            print(f"    father of {name} → {fathers}")
        brothers = engine.find_all("brother", name)
        if brothers:
            print(f"    brothers of {name} → {brothers}")

    print("="*55)


# ─────────────────────────────────────────────────────────
#  MAIN: Console-based Fact Collector
# ─────────────────────────────────────────────────────────
def run_fact_collector():
    print("\n" + "="*60)
    print("  FAMILY FACT COLLECTOR  (Assignment 2)")
    print("  Collects facts via AIML → saves to Prolog KB")
    print("="*60)
    print("  Type HELP for usage, SHOW FACTS to review,")
    print("  DONE when finished.\n")

    # ── Step 3: Load data_entry.aiml
    kernel = aiml.Kernel()
    kernel.setTextEncoding(None)
    kernel.learn(AIML_DATA)
    print(f"[AIML] Loaded data_entry.aiml ({kernel.numCategories()} patterns)\n")

    session_facts = []   # facts added this session
    existing_facts = load_existing_facts()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        # ── Get AIML response
        aiml_resp = kernel.respond(user_input.upper())

        # ── Handle special commands
        if aiml_resp.strip() == "DONE_ADDING":
            print(f"\nBot: Finished! Added {len(session_facts)} fact(s) this session.")
            if session_facts:
                print("     Facts saved:")
                for f in session_facts:
                    print(f"       {f}")
            print()
            break

        if aiml_resp.strip() == "SHOW_FACTS":
            dynamic = get_dynamic_facts()
            if dynamic:
                print(f"Bot: {len(dynamic)} fact(s) currently in the KB:")
                for f in dynamic:
                    print(f"       {f}")
            else:
                print("Bot: No dynamic facts added yet.")
            print()
            continue

        # ── Print AIML response
        print(f"Bot: {aiml_resp.strip()}\n")

        # ── Step 4: Fetch AIML variables
        fact_type, arg1, arg2, ready = fetch_aiml_variables(kernel)

        if ready != "yes":
            continue

        # ── Step 5: Build Prolog fact string via string handling
        fact_str = build_prolog_fact(fact_type, arg1, arg2)

        if not fact_str:
            print("  [Warning] Could not form a valid Prolog fact from that input.\n")
            # Reset
            kernel.setPredicate("fact_ready", "no")
            continue

        # ── Duplicate check
        if fact_already_exists(fact_str, existing_facts):
            print(f"  [Info] Fact already exists in KB: {fact_str}\n")
            kernel.setPredicate("fact_ready", "no")
            continue

        # ── Step 6: File handling — write to KB
        write_fact_to_kb(fact_str)
        existing_facts.add(fact_str)
        session_facts.append(fact_str)
        print(f"  ✓ Written to KB: {fact_str}\n")

        # Reset ready flag
        kernel.setPredicate("fact_ready", "no")

    # ── Step 7: Verify
    if session_facts:
        verify_with_prolog()


if __name__ == "__main__":
    run_fact_collector()
