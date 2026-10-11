"""
Prolog Engine — loads family_kb.pl (rules + dynamic facts)
"""
import pytholog as pl
import os

class PrologEngine:
    def __init__(self, kb_path=None):
        if kb_path is None:
            kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "family_kb.pl")
        self.kb_path = kb_path
        self.kb = pl.KnowledgeBase("family_kb")
        self._load_kb()

    def _load_kb(self):
        facts = []
        with open(self.kb_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("%"):
                    continue
                # Remove inline comments
                line = line.split("%")[0].strip()
                if line.endswith("."):
                    facts.append(line[:-1])
        self.kb(facts)
        print(f"[Prolog] Loaded {len(facts)} clauses from {os.path.basename(self.kb_path)}")

    def reload(self):
        """Reload KB after new facts are written."""
        self.kb = pl.KnowledgeBase("family_kb")
        self._load_kb()

    def query(self, query_str):
        try:
            results = self.kb.query(pl.Expr(query_str))
            return results if results else ["No"]
        except Exception as e:
            return [{"error": str(e)}]

    def get_values(self, results, var_name):
        if not results or results in (["No"], ["Yes"]):
            return []
        values, seen = [], set()
        for r in results:
            if isinstance(r, dict) and var_name in r:
                v = r[var_name]
                if v not in seen:
                    seen.add(v); values.append(v)
        return values

    def find_all(self, relation, target, var="X"):
        results = self.query(f"{relation}({var},{target})")
        values = self.get_values(results, var)
        return [v for v in values if v != target]

    def check_fact(self, relation, person):
        return self.query(f"{relation}({person})") == ["Yes"]

    def check_binary(self, relation, p1, p2):
        return self.query(f"{relation}({p1},{p2})") == ["Yes"]

    def get_age(self, person):
        r = self.query(f"age({person},A)")
        v = self.get_values(r, "A")
        return v[0] if v else None

    def get_dob(self, person):
        r = self.query(f"dob({person},Y)")
        v = self.get_values(r, "Y")
        return v[0] if v else None
