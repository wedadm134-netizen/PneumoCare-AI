from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = Path(__file__).resolve().parent / "rag_db"
COLLECTION_NAME = "pneumocare_medical_knowledge"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_model = None
_collection = None


def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def get_collection():
    global _collection

    if _collection is None:
        print("Opening ChromaDB...")
        client = chromadb.PersistentClient(path=str(DB_DIR))
        _collection = client.get_collection(COLLECTION_NAME)

    return _collection


def normalize_words(text):
    return set(re.findall(r"[a-zA-Z]+", text.lower()))


def is_low_value_chunk(item):
    text = item["text"].lower().strip()

    bad_patterns = [
        "bibliography",
        "suggested citation",
        "all rights reserved",
        "statement of endorsement",
        "downloaded from publications",
        "isbn ",
    ]

    if re.search(r'(^|\n)\s*(references|bibliography)\b', text, re.IGNORECASE):
        return True

    if any(pattern in text for pattern in bad_patterns):
        return True

    # Ignore chunks that are basically only a title/header.
    words = re.findall(r"[a-zA-Z]+", text)

    if len(words) < 20:
        return True

    return False


def source_priority(source_name):
    name = source_name.lower()

    if "who 2024" in name:
        return 0

    if "nice" in name:
        return 1

    if "oxygen therapy" in name:
        return 2

    if "pocket book" in name:
        return 3

    if "aap" in name:
        return 10

    return 5


def lexical_relevance(query, text):
    query_words = normalize_words(query)
    text_words = normalize_words(text)

    if not query_words or not text_words:
        return 0.0

    overlap = query_words.intersection(text_words)

    return len(overlap) / len(query_words)


def topic_bonus(query, text):
    q = query.lower()
    t = text.lower()

    bonus = 0.0

    topic_groups = [
        (
            ["oxygen", "hypoxaemia", "hypoxemia", "saturation", "pulse oximetry"],
            ["oxygen", "hypoxaemia", "hypoxemia", "saturation", "pulse oximetry"],
            0.25,
        ),
        (
            ["severe pneumonia", "danger sign", "respiratory distress"],
            ["severe pneumonia", "danger sign", "respiratory distress"],
            0.25,
        ),
        (
            ["antibiotic", "amoxicillin", "penicillin", "gentamicin"],
            ["antibiotic", "amoxicillin", "penicillin", "gentamicin"],
            0.25,
        ),
        (
            ["hospital", "referral", "refer"],
            ["hospital", "referral", "refer", "danger sign"],
            0.20,
        ),
    ]

    for query_terms, text_terms, value in topic_groups:
        if any(term in q for term in query_terms):
            if any(term in t for term in text_terms):
                bonus += value

    return bonus


def score_candidate(query, item):
    distance = float(item.get("distance", 999))

    semantic_score = max(0.0, 1.0 - distance)
    lexical_score = lexical_relevance(query, item["text"])
    topic_score = topic_bonus(query, item["text"])
    priority_penalty = source_priority(item["source_name"]) * 0.01

    return (
        semantic_score * 0.55
        + lexical_score * 0.30
        + topic_score
        - priority_penalty
    )


def search_knowledge(query: str, top_k: int = 5):
    if not query or not query.strip():
        return []

    query = query.strip()

    # Expand severe-pneumonia questions toward the WHO danger-sign terminology.
    q_lower = query.lower()
    if any(term in q_lower for term in ['severe pneumonia','danger sign','general danger sign','severe breathing','التهاب رئوي شديد','علامات الخطر','الالتهاب الرئوي الشديد']):
        query += ' child is not able to drink or breastfeed, vomits everything, convulsions, lethargic or unconscious, stridor, hypoxaemia, fast breathing, chest indrawing, respiratory distress WHO 2024'

    model = get_model()
    collection = get_collection()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    ).tolist()

    raw = collection.query(
        query_embeddings=query_embedding,
        n_results=min(max(top_k * 6, 20), collection.count())
    )

    documents = raw.get("documents", [[]])[0]
    metadatas = raw.get("metadatas", [[]])[0]
    distances = raw.get("distances", [[]])[0]

    candidates = []

    for i, document in enumerate(documents):

        metadata = metadatas[i] if i < len(metadatas) else {}
        distance = distances[i] if i < len(distances) else 999

        item = {
            "text": document,
            "source_name": metadata.get(
                "source_name",
                "Unknown source"
            ),
            "source_file": metadata.get("source_file"),
            "page": metadata.get("page"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": distance,
        }

        if is_low_value_chunk(item):
            continue

        item["retrieval_score"] = score_candidate(query, item)

        candidates.append(item)

    candidates.sort(
        key=lambda x: x["retrieval_score"],
        reverse=True
    )

    return candidates[:top_k]


def format_context(results):
    blocks = []

    for i, item in enumerate(results, start=1):
        blocks.append(
            f"""[SOURCE {i}]
Source: {item['source_name']}
Page: {item['page']}
Text:
{item['text']}
"""
        )

    return "\n".join(blocks)


if __name__ == "__main__":

    test_questions = [
        "What are the recommendations for oxygen therapy in children with pneumonia?",
        "What signs indicate severe pneumonia in a child?",
        "How should pneumonia be managed in children?",
        "When should a child with pneumonia be referred to hospital?",
        "What antibiotics are recommended for childhood pneumonia?",
    ]

    for question in test_questions:

        print("\n" + "=" * 100)
        print("QUERY:", question)
        print("=" * 100)

        results = search_knowledge(
            question,
            top_k=5
        )

        print("RESULTS:", len(results))

        for i, item in enumerate(results, start=1):

            print(f"\nRESULT {i}")
            print("SOURCE:", item["source_name"])
            print("PAGE:", item["page"])
            print("DISTANCE:", item["distance"])
            print("SCORE:", round(item["retrieval_score"], 4))
            print("TEXT:")
            print(item["text"][:1200])



