from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PATHS / MODEL
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VECTORSTORE_DIR = (
    PROJECT_ROOT
    / "rag"
    / "vectorstore"
)

COLLECTION_NAME = "environmental_knowledge"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


_model = None
_client = None
_collection = None


# ============================================================
# LAZY INITIALIZATION
# ============================================================

def _get_collection():

    global _model
    global _client
    global _collection

    if _model is None:
        _model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    if _client is None:
        VECTORSTORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        _client = chromadb.PersistentClient(
            path=str(VECTORSTORE_DIR)
        )

    if _collection is None:

        # IMPORTANT FOR STREAMLIT CLOUD:
        # Do not use get_collection() here because the vectorstore
        # is intentionally not committed to GitHub. Create the
        # collection if it does not exist.
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME
        )

        # A newly created collection has zero documents.
        # Build the scientific knowledge base from the repository
        # documents on first use.
        try:
            collection_count = _collection.count()
        except Exception:
            collection_count = 0

        if collection_count == 0:

            print(
                "Chroma collection is empty. "
                "Building the scientific knowledge base..."
            )

            from rag.ingest import build_knowledge_base

            _collection = build_knowledge_base(
                reset=False
            )

    return _collection


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def _normalize(text):

    return re.sub(
        r"[^a-z0-9\s%\-]",
        " ",
        str(text).lower()
    )


def _tokens(text):

    return set(
        _normalize(text).split()
    )


# ============================================================
# RECOMMENDATION-SPECIFIC TERMS
# ============================================================

ACTION_TERMS = {

    # --------------------------------------------------------
    # COVER CROPS
    # --------------------------------------------------------

    "cover_crop": {

        "terms": {

            "cover crop",
            "cover crops",

            "legume",
            "legumes",

            "organic matter",

            "soil organic carbon",
            "soil carbon",

            "soil biodiversity",
            "soil biological activity",
            "biological activity",

            "biomass",

            "water retention",
            "soil moisture",
            "soil health",
        },

        "categories": {
            "soil",
        },

        "preferred_sources": {

            "FAO_SOIL_BIODIVERSITY",

            "FAO_SOIL_ORGANIC_CARBON",

            "FAO_SOIL_BIODIVERSITY_MANAGEMENT",

            "FAO_SOIL_CARBON",
        },
    },


    # --------------------------------------------------------
    # INTERCROPPING
    # --------------------------------------------------------

    "intercropping": {

        "terms": {

            "intercropping",
            "intercrop",

            "crop diversification",
            "diversified farming",
            "crop diversity",

            "vegetation diversity",

            "habitat diversity",

            "species richness",

            "soil biodiversity",

            "resource diversity",

            "water availability",

            "land use",
        },

        "categories": {

            "land_use",
            "biodiversity",
            "soil",
        },

        "preferred_sources": {

            "FAO_AGROFORESTRY",

            "FAO_AGROFORESTRY_FAQ",

            "IPCC_AR6_WGII",
        },
    },


    # --------------------------------------------------------
    # AGROFORESTRY
    # --------------------------------------------------------

    "agroforestry": {

        "terms": {

            "agroforestry",

            "trees",
            "tree",

            "native vegetation",
            "vegetation zones",

            "habitat structure",

            "connectivity",

            "soil carbon",
            "soil organic carbon",

            "water management",

            "biodiversity",

            "diversification",

            "tree-based",
        },

        "categories": {

            "land_use",
            "soil",
            "biodiversity",
        },

        "preferred_sources": {

            "FAO_AGROFORESTRY",

            "FAO_AGROFORESTRY_FAQ",

            "FAO_SOIL_CARBON",

            "IPCC_AR6_WGII",
        },
    },


    # --------------------------------------------------------
    # HABITAT CORRIDORS
    # --------------------------------------------------------

    "corridor": {

        "terms": {

            "corridor",
            "corridors",

            "connected habitat",

            "habitat connectivity",

            "landscape connectivity",

            "habitat fragmentation",
            "fragmentation",

            "species movement",

            "species richness",

            "habitat diversity",

            "native vegetation",

            "connectivity",
        },

        "categories": {

            "biodiversity",
            "land_use",
        },

        "preferred_sources": {

            "IPCC_AR6_WGII",
        },
    },


    # --------------------------------------------------------
    # RESTORATION
    # --------------------------------------------------------

    "restoration": {

        "terms": {

            "restoration",
            "ecosystem restoration",

            "native vegetation",

            "habitat restoration",

            "habitat loss",

            "habitat connectivity",

            "biodiversity",

            "species richness",

            "vegetation recovery",
        },

        "categories": {

            "biodiversity",
            "land_use",
        },

        "preferred_sources": {

            "IPCC_AR6_WGII",

            "FAO_AGROFORESTRY",
        },
    },


    # --------------------------------------------------------
    # POLLUTION REDUCTION
    # --------------------------------------------------------

    "pollution_reduction": {

        "terms": {

            "pollution",
            "pollutant",

            "water quality",
            "soil quality",

            "organism stress",

            "environmental stress",

            "contamination",

            "species richness",
        },

        "categories": {

            "human_impact",
            "biodiversity",
        },

        "preferred_sources": {

            "IPCC_AR6_WGII",
        },
    },
}


# ============================================================
# ACTION DETECTION
# ============================================================

def _detect_action(recommendation):

    text = _normalize(
        recommendation
    )


    if (
        "cover crop" in text
        or "legume" in text
    ):

        return "cover_crop"


    if "intercropp" in text:

        return "intercropping"


    if "agroforestry" in text:

        return "agroforestry"


    if (
        "corridor" in text
        or "connected native vegetation" in text
    ):

        return "corridor"


    if (
        "restoration" in text
        or "restore" in text
    ):

        return "restoration"


    if (
        "pollution" in text
        or "pollutant" in text
    ):

        return "pollution_reduction"


    return None


# ============================================================
# DOCUMENT SCORING
# ============================================================

def _score_document(
    document,
    metadata,
    distance,
    query_terms,
    action_config,
    requested_metrics,
    pathways,
):

    text = _normalize(

        f"{document} "
        f"{metadata.get('topic', '')} "
        f"{metadata.get('category', '')} "
        f"{metadata.get('source', '')}"

    )


    doc_tokens = _tokens(
        text
    )


    score = 0.0


    # ========================================================
    # SEMANTIC SIMILARITY
    # ========================================================

    if distance is not None:

        try:

            score += max(
                0.0,
                1.0 - float(distance)
            )

        except (
            TypeError,
            ValueError
        ):

            pass


    # ========================================================
    # QUERY TOKEN OVERLAP
    # ========================================================

    score += min(

        len(
            query_terms
            & doc_tokens
        ) * 0.08,

        0.80
    )


    # ========================================================
    # ACTION-SPECIFIC EVIDENCE
    # ========================================================

    if action_config:

        action_hits = sum(

            1

            for term
            in action_config["terms"]

            if _normalize(term)
            in text

        )


        # Strong action relevance.

        score += min(
            action_hits * 0.28,
            2.20
        )


        # ====================================================
        # CATEGORY MATCH
        # ====================================================

        if (
            metadata.get("category")
            in action_config["categories"]
        ):

            score += 0.50


        # ====================================================
        # PREFERRED SOURCE MATCH
        # ====================================================

        source_id = metadata.get(
            "source_id"
        )


        preferred_sources = action_config.get(
            "preferred_sources",
            set()
        )

        if source_id in preferred_sources:
            score += 1.15
        elif preferred_sources:
            score -= 0.20


    # ========================================================
    # REQUESTED METRIC MATCH
    # ========================================================

    metric_hits = 0


    for metric in (
        requested_metrics or []
    ):

        metric_text = (
            _normalize(
                metric
            )
            .replace(
                "_",
                " "
            )
        )


        if (
            metric_text
            and metric_text in text
        ):

            metric_hits += 1


    score += min(

        metric_hits * 0.18,

        0.90
    )


    # ========================================================
    # KNOWLEDGE GRAPH / REASONING PATHWAY MATCH
    # ========================================================

    pathway_text = _normalize(

        " ".join(

            " ".join(pathway)
            if isinstance(
                pathway,
                list
            )

            else str(pathway)

            for pathway
            in (pathways or [])

        )

    )


    pathway_tokens = _tokens(
        pathway_text
    )


    pathway_hits = sum(

        1

        for token
        in pathway_tokens

        if (
            token in doc_tokens
            and len(token) > 3
        )

    )


    score += min(

        pathway_hits * 0.03,

        0.30
    )


    # ========================================================
    # IRRELEVANT CLIMATE/POLLUTION PENALTY
    # ========================================================

    if (

        action_config

        and
        metadata.get(
            "category"
        ) == "climate"

        and
        "pollution" in text

        and
        not any(

            term in text

            for term in [

                "soil carbon",
                "soil biodiversity",
                "agroforestry",
                "intercropping",
                "cover crop",
                "vegetation",

            ]

        )

    ):

        score -= 0.80


    return score


# ============================================================
# GENERAL KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_knowledge(
    query,
    top_k=5
):

    collection = _get_collection()


    results = collection.query(

        query_texts=[
            query
        ],

        n_results=max(
            top_k,
            1
        ),

        include=[
            "documents",
            "metadatas",
            "distances"
        ],

    )


    documents = results.get(
        "documents",
        [[]]
    )[0]


    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    distances = results.get(
        "distances",
        [[]]
    )[0]


    output = []


    for (
        document,
        metadata,
        distance
    ) in zip(

        documents,
        metadatas,
        distances

    ):

        item = dict(
            metadata or {}
        )


        item["passage"] = (
            document
        )


        item["distance"] = (
            distance
        )


        output.append(
            item
        )


    return output


# ============================================================
# EVIDENCE RETRIEVAL
# ============================================================

def retrieve_evidence(
    recommendation,
    metrics,
    pathways=None,
    top_k=3,
):

    """
    Retrieve evidence for one specific recommendation.

    Pipeline:

    1. Detect recommendation type.
    2. Build action + metric + pathway query.
    3. Retrieve a large semantic candidate pool.
    4. Score candidates using:
         - semantic similarity
         - action relevance
         - category relevance
         - preferred source
         - metric relevance
         - reasoning-pathway relevance
    5. Prefer strong evidence from different sources.
    6. Fill remaining slots with strongest evidence.
    """


    # ========================================================
    # DETECT ACTION
    # ========================================================

    action = _detect_action(
        recommendation
    )


    action_config = (
        ACTION_TERMS.get(
            action
        )
    )


    # ========================================================
    # METRIC TEXT
    # ========================================================

    metric_text = " ".join(

        str(metric)
        .replace(
            "_",
            " "
        )

        for metric
        in (metrics or [])

    )


    # ========================================================
    # PATHWAY TEXT
    # ========================================================

    pathway_text = " ".join(

        " ".join(pathway)
        if isinstance(
            pathway,
            list
        )

        else str(pathway)

        for pathway
        in (pathways or [])

    )


    # ========================================================
    # ACTION QUERY TERMS
    # ========================================================

    action_text = (

        " ".join(
            action_config["terms"]
        )

        if action_config

        else str(
            recommendation
        )

    )


    # ========================================================
    # FINAL SEMANTIC QUERY
    # ========================================================

    query = (

        f"{recommendation}. "

        f"Environmental metrics: "
        f"{metric_text}. "

        f"Reasoning pathway: "
        f"{pathway_text}. "

        f"Scientific evidence needed: "
        f"{action_text}."

    )


    # ========================================================
    # LARGE CANDIDATE POOL
    # ========================================================

    candidate_count = max(
        15,
        top_k * 5
    )


    collection = _get_collection()


    results = collection.query(

        query_texts=[
            query
        ],

        n_results=candidate_count,

        include=[
            "documents",
            "metadatas",
            "distances"
        ],

    )


    documents = results.get(
        "documents",
        [[]]
    )[0]


    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    distances = results.get(
        "distances",
        [[]]
    )[0]


    # ========================================================
    # QUERY TOKENS
    # ========================================================

    query_terms = _tokens(

        f"{recommendation} "
        f"{metric_text} "
        f"{pathway_text}"

    )


    candidates = []


    # ========================================================
    # SCORE CANDIDATES
    # ========================================================

    for (
        document,
        metadata,
        distance
    ) in zip(

        documents,
        metadatas,
        distances

    ):

        metadata = dict(
            metadata or {}
        )


        score = _score_document(

            document=document,

            metadata=metadata,

            distance=distance,

            query_terms=query_terms,

            action_config=action_config,

            requested_metrics=metrics,

            pathways=pathways,

        )


        item = {

            "source_id":
                metadata.get(
                    "source_id"
                ),

            "source":
                metadata.get(
                    "source",
                    "Unknown source"
                ),

            "organization":
                metadata.get(
                    "organization",
                    ""
                ),

            "year":
                metadata.get(
                    "year",
                    ""
                ),

            "topic":
                metadata.get(
                    "topic",
                    ""
                ),

            "source_type":
                metadata.get(
                    "source_type",
                    ""
                ),

            "url":
                metadata.get(
                    "url",
                    ""
                ),

            "category":
                metadata.get(
                    "category",
                    ""
                ),

            "document":
                metadata.get(
                    "document",
                    ""
                ),

            "chunk_number":
                metadata.get(
                    "chunk_number"
                ),

            "passage":
                document,

            "distance":
                distance,

            "relevance_score":
                round(
                    score,
                    4
                ),

            "retrieval_action":
                action,

        }


        candidates.append(
            item
        )


    # ========================================================
    # SORT BY RELEVANCE
    # ========================================================

    candidates.sort(

        key=lambda item:
            item[
                "relevance_score"
            ],

        reverse=True

    )


    # ========================================================
    # EVIDENCE SELECTION
    # ========================================================

    selected = []


    seen_chunks = set()


    selected_sources = set()


    # --------------------------------------------------------
    # PASS 1
    #
    # Prefer the recommendation's explicitly preferred sources.
    # Within that set, use the strongest passages first while
    # retaining source diversity where quality is comparable.
    # --------------------------------------------------------

    preferred_sources = set(
        (action_config or {}).get(
            "preferred_sources",
            set()
        )
    )

    preferred_candidates = [
        item for item in candidates
        if item.get("source_id") in preferred_sources
    ]

    fallback_candidates = [
        item for item in candidates
        if item.get("source_id") not in preferred_sources
    ]

    ordered_candidates = (
        preferred_candidates
        + fallback_candidates
    )

    for item in ordered_candidates:

        chunk_key = (
            item.get("source_id"),
            item.get("chunk_number"),
            _normalize(
                item.get("passage", "")
            )[:180],
        )

        if chunk_key in seen_chunks:
            continue

        source_id = item.get("source_id")

        if source_id in selected_sources:
            continue

        seen_chunks.add(chunk_key)
        selected_sources.add(source_id)
        selected.append(item)

        if len(selected) >= top_k:
            break

    # --------------------------------------------------------
    # PASS 2
    #
    # If we don't have enough unique sources,
    # fill remaining slots with strongest passages.
    # --------------------------------------------------------

    if (
        len(selected)
        < top_k
    ):

        selected_keys = {

            (

                item.get(
                    "source_id"
                ),

                item.get(
                    "chunk_number"
                ),

                _normalize(

                    item.get(
                        "passage",
                        ""
                    )

                )[:180],

            )

            for item
            in selected

        }


        for item in candidates:

            chunk_key = (

                item.get(
                    "source_id"
                ),

                item.get(
                    "chunk_number"
                ),

                _normalize(

                    item.get(
                        "passage",
                        ""
                    )

                )[:180],

            )


            if (
                chunk_key
                in selected_keys
            ):

                continue


            selected.append(
                item
            )


            selected_keys.add(
                chunk_key
            )


            if (
                len(selected)
                >= top_k
            ):

                break


    return selected


# ============================================================
# QUICK MANUAL TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "DARUKAA RAG RETRIEVAL TEST"
    )
    print("=" * 70)


    evidence = retrieve_evidence(

        recommendation=(
            "Introduce suitable "
            "crop intercropping."
        ),

        metrics=[

            "habitat_diversity",

            "species_richness",

            "soil_biodiversity",

        ],

        pathways=[

            [

                "monoculture",

                "reduced vegetation diversity",

                "habitat diversity pressure",

            ]

        ],

        top_k=3,

    )


    print()
    print(
        "Retrieved evidence:",
        len(evidence)
    )


    for index, item in enumerate(
        evidence,
        start=1
    ):

        print()
        print(
            f"--- Evidence {index} ---"
        )

        print(
            "Source:",
            item[
                "source"
            ]
        )

        print(
            "Organization:",
            item[
                "organization"
            ]
        )

        print(
            "Category:",
            item[
                "category"
            ]
        )

        print(
            "Score:",
            item[
                "relevance_score"
            ]
        )

        print(
            "Passage:",
            item[
                "passage"
            ]
        )


    print()
    print("=" * 70)
    print(
        "RAG RETRIEVAL TEST COMPLETED"
    )
    print("=" * 70)