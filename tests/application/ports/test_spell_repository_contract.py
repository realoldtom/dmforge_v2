import tempfile
from pathlib import Path

from dmforge.application.ports.spell_repository import SpellRepository
from dmforge.infrastructure.repository.json_spell_repository import JSONSpellRepository


def test_json_repository_implements_protocol():
    path = Path(tempfile.gettempdir()) / "fake.json"
    impl: SpellRepository = JSONSpellRepository(path)
    assert hasattr(impl, "load_all_spells")
    assert callable(impl.load_all_spells)
