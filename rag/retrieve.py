from pathlib import Path
import json
import re
import math

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "rag" / "documents"
METADATA_FILE = PROJECT_ROOT / "rag" / "metadata" / "sources.json"

_ACTION_TERMS = {
    "cover_crop": ["cover crop", "soil organic carbon", "soil biodiversity", "soil moisture", "soil health", "organic matter"],
    "intercropping": ["intercropping", "crop diversity", "vegetation diversity", "habitat diversity", "species richness", "soil biodiversity"],
    "agroforestry": ["agroforestry", "trees", "crops", "habitat diversity", "biodiversity", "soil health", "water management"],
    "corridor": ["habitat connectivity", "habitat fragmentation", "species movement", "corridor", "species richness", "connectivity"],
    "restoration": ["restoration", "deforestation", "habitat loss", "native vegetation", "biodiversity", "connectivity"],
    "pollution_reduction": ["pollution", "water quality", "soil quality", "organism stress", "biodiversity"],
}

def _load_sources():
    try:
        return {
            x["source_id"]: x
            for x in json.loads(METADATA_FILE.read_text(encoding="utf-8"))
        }
    except Exception:
        return {}

def _chunks():
    sources = _load_sources()
    source_map = {
        "soil_biodiversity.txt": "FAO_SOIL_BIODIVERSITY",
        "land_use_impact.txt": "FAO_AGROFORESTRY",
        "biodiversity_indicators.txt": "IPCC_AR6_WGII",
        "climate_biodiversity.txt": "IPCC_AR6_WGII",
        "human_impact.txt": "IPCC_AR6_WGII",
    }
    rows = []
    for path in sorted(DOCUMENTS_DIR.rglob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        source_id = source_map.get(path.name, "LOCAL_KNOWLEDGE_DOCUMENT")
        source = sources.get(source_id, {})
        for i, paragraph in enumerate(text.split("\n\n")):
            paragraph = paragraph.strip()
            if len(paragraph.split()) < 8:
                continue
            rows.append({
                "text": paragraph,
                "source_id": source_id,
                "source": source.get("title", path.name),
                "organization": source.get("organization", "Darukaa.Earth Knowledge Base"),
                "year": str(source.get("year", "")),
                "topic": source.get("topic", path.parent.name),
                "source_type": source.get("source_type", "knowledge_document"),
                "url": source.get("url", ""),
                "category": path.parent.name,
                "document": path.name,
                "chunk_number": i,
            })
    return rows

_CACHE = None

def _get_rows():
    global _CACHE
    if _CACHE is None:
        _CACHE = _chunks()
    return _CACHE

def _words(text):
    return set(re.findall(r"[a-z0-9%]+", str(text).lower()))

def _score(query, row, action=None):
    q = _words(query)
    d = _words(row["text"])
    score = len(q & d) / max(1, len(q))
    if action:
        terms = _ACTION_TERMS.get(action, [])
        qt = _words(" ".join(terms))
        score += 2.0 * len(qt & d) / max(1, len(qt))
    return score

def retrieve_knowledge(query, top_k=5, **kwargs):
    rows = _get_rows()
    ranked = sorted(
        rows,
        key=lambda r: _score(query, r, kwargs.get("recommendation")),
        reverse=True,
    )
    return ranked[:top_k]

def retrieve_evidence(
    recommendation,
    environmental_data=None,
    reasoning_result=None,
    metrics=None,
    pathway=None,
    top_k=3,
    **kwargs
):
    environmental_data = environmental_data or {}
    reasoning_result = reasoning_result or {}

    parts = [
        str(recommendation),
        str(environmental_data),
        str(metrics or reasoning_result.get("affected_metrics", "")),
        str(pathway or reasoning_result.get("graph_reasoning", "")),
    ]
    query = " ".join(parts)

    results = retrieve_knowledge(
        query,
        top_k=max(3, top_k),
        recommendation=recommendation,
    )

    evidence = []
    for row in results[:top_k]:
        evidence.append({
            "source_id": row["source_id"],
            "source": row["source"],
            "organization": row["organization"],
            "year": row["year"],
            "topic": row["topic"],
            "source_type": row["source_type"],
            "url": row["url"],
            "category": row["category"],
            "document": row["document"],
            "chunk_number": row["chunk_number"],
            "text": row["text"],
            "passage": row["text"],
            "score": round(_score(query, row, recommendation), 4),
        })

    return evidence

if __name__ == "__main__":
    result = retrieve_evidence(
        "agroforestry",
        {"soil_organic_carbon": 0.3, "rainfall": "low", "land_use": "monoculture"},
        top_k=3,
    )
    for item in result:
        print(item["source"], item["score"], item["passage"])
