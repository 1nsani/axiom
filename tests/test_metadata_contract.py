import os
import sys
import pytest
import yaml

AXIOM_KNOWLEDGE_PATH = os.environ.get("AXIOM_KNOWLEDGE_PATH", "/tmp/axiom/Axiom-knowledge")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from renderer_registry import SUPPORTED_DIRECTIONS, SUPPORTED_COLORS

def get_metadata_files():
    domain_dir = os.path.join(AXIOM_KNOWLEDGE_PATH, "metadata", "domain")
    if not os.path.isdir(domain_dir):
        raise FileNotFoundError(f"Folder domain tidak ditemukan: {domain_dir}")
    return [f for f in os.listdir(domain_dir) if f.endswith(".md")]

def parse_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}
    return {}

@pytest.mark.parametrize("md_file", get_metadata_files())
def test_metadata_vectors_supported(md_file):
    filepath = os.path.join(AXIOM_KNOWLEDGE_PATH, "metadata", "domain", md_file)
    fm = parse_frontmatter(filepath)
    vectors = fm.get("visual_hooks", {}).get("vectors_template", [])
    for vec in vectors:
        vec_id = vec.get("id", "unknown")
        
        # Hanya periksa jika vektor memiliki direction_logic (beberapa domain mungkin tidak menggunakannya)
        logic = vec.get("direction_logic")
        if logic is not None:
            assert logic in SUPPORTED_DIRECTIONS, \
                f"{md_file}: vektor '{vec_id}' pakai direction_logic '{logic}' tidak terdaftar di renderer"
        
        # Hanya periksa color jika ada
        color = vec.get("color")
        if color is not None:
            assert color in SUPPORTED_COLORS, \
                f"{md_file}: vektor '{vec_id}' pakai color '{color}' tidak terdaftar di renderer"
