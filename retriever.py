import math

class FAQRetriever:
    def __init__(self, faq_path: str):
        self.faq_path = faq_path
        self.lines = self._load_faq()

    def _load_faq(self):
        with open(self.faq_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]

    def _bow_vector(self, text: str):
        words = text.lower().split()
        vec = {}
        for w in words:
            vec[w] = vec.get(w, 0) + 1
        return vec

    def _cosine_similarity(self, v1: dict, v2: dict):
        # ensure numeric values
        v1 = {k: float(v) for k, v in v1.items()}
        v2 = {k: float(v) for k, v in v2.items()}

        common = set(v1.keys()) & set(v2.keys())
        dot = sum(v1[w] * v2[w] for w in common)

        mag1 = math.sqrt(sum(v**2 for v in v1.values()))
        mag2 = math.sqrt(sum(v**2 for v in v2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot / (mag1 * mag2)

    def search(self, query: str, top_k=3):
        # Ensure query is a string and not empty
        if not query or not isinstance(query, str):
            return []
        
        query = query.strip()
        if not query:
            return []
        
        # Create vector from query
        q_vec = self._bow_vector(query)
        
        # If query vector is empty (no words), return empty results
        if not q_vec:
            return []
        
        scored = []

        for line in self.lines:
            l_vec = self._bow_vector(line)
            sim = self._cosine_similarity(q_vec, l_vec)
            scored.append((line, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
