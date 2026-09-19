from pathlib import Path
import json

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
METADATA_FILE = BASE_DIR / "metadata" / "sources.json"

COLLECTION_NAME = "environmental_knowledge"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DOCUMENT_SOURCE_MAP = {
    "soil_biodiversity.txt": "FAO_SOIL_BIODIVERSITY",
    "land_use_impact.txt": "FAO_AGROFORESTRY",
    "biodiversity_indicators.txt": "IPCC_AR6_WGII",
    "climate_biodiversity.txt": "IPCC_AR6_WGII",
    "human_impact.txt": "IPCC_AR6_WGII",
}


def create_chunks(text):
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    return [
        paragraph
        for paragraph in paragraphs
        if len(paragraph.split()) >= 8
    ]


def build_knowledge_base(reset=False):
    """
    Build the ChromaDB collection from the repository knowledge documents.

    reset=False is used by the deployed app so an existing collection
    is preserved. The standalone command below uses reset=True.
    """

    print("Loading source metadata...")

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        source_metadata = json.load(file)

    source_lookup = {
        source["source_id"]: source
        for source in source_metadata
    }

    print(f"Loaded {len(source_lookup)} scientific sources.")

    print("\nLoading embedding model...")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("Embedding model loaded.")

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(VECTORSTORE_DIR)
    )

    if reset:
        try:
            client.delete_collection(name=COLLECTION_NAME)
            print("Old knowledge collection deleted.")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = []
    metadatas = []
    ids = []
    document_number = 0

    print("\nScanning knowledge documents...")

    for file_path in sorted(DOCUMENTS_DIR.rglob("*.txt")):
        print(f"Reading: {file_path}")

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        chunks = create_chunks(text)
        category = file_path.parent.name
        filename = file_path.name

        source_id = DOCUMENT_SOURCE_MAP.get(filename)

        if source_id is None:
            print(
                f"WARNING: No source mapping found for {filename}"
            )
            source_id = "LOCAL_KNOWLEDGE_DOCUMENT"

        source = source_lookup.get(source_id, {})

        for chunk_number, chunk in enumerate(chunks):
            documents.append(chunk)

            metadatas.append({
                "source_id": source_id,
                "source": source.get("title", filename),
                "organization": source.get(
                    "organization",
                    "Darukaa.Earth Knowledge Base"
                ),
                "year": str(source.get("year", "")),
                "topic": source.get("topic", category),
                "source_type": source.get(
                    "source_type",
                    "knowledge_document"
                ),
                "url": source.get("url", ""),
                "category": category,
                "document": filename,
                "chunk_number": str(chunk_number),
            })

            ids.append(
                f"doc_{document_number}_{chunk_number}"
            )

        document_number += 1

    if not documents:
        raise RuntimeError(
            "No knowledge documents found under "
            f"{DOCUMENTS_DIR}"
        )

    print(
        f"\nCreating embeddings for "
        f"{len(documents)} fine-grained chunks..."
    )

    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("\n" + "=" * 70)
    print("SCIENTIFIC KNOWLEDGE BASE CREATED")
    print("=" * 70)

    print(
        f"\nTotal chunks stored: {len(documents)}"
    )

    print("\nIndexed categories:")
    for category in sorted(
        set(metadata["category"] for metadata in metadatas)
    ):
        print(f"- {category}")

    print("\nSource mapping:")
    for filename, source_id in DOCUMENT_SOURCE_MAP.items():
        source = source_lookup.get(source_id, {})
        print(
            f"- {filename} → "
            f"{source.get('title', source_id)}"
        )

    return collection


if __name__ == "__main__":
    build_knowledge_base(reset=True)
