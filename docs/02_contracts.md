# 📜 DMForge v2 Contracts

This document defines the **explicit interfaces** (contracts) between architecture layers in DMForge v2.  
Every layer depends on **abstractions, not implementations**. These contracts are the glue — and the firewalls.

---

## 🧩 Contract Categories

- **Domain Types**: `SpellCard`, `Deck`, `DeckOptions`
- **Service Interfaces**: `DeckBuilder`, `RenderService`, `ArtService`
- **Repository Interfaces**: `SpellRepository`, `DeckStorage`
- **DTOs & Adapters**: CLI-facing objects like `DeckDTO`, `SummaryText`, etc.

---

## 🧱 Domain Contracts

### `SpellCard`
```python
@dataclass(frozen=True)
class SpellCard:
    name: str
    level: int
    school: School
    classes: list[str]
    description: str
    duration: str
    art_path: str | None = None
Deck

@dataclass(frozen=True)
class Deck:
    cards: list[SpellCard]
    name: str
    version: str

    def to_json(self) -> str
    def to_dict(self) -> dict
DeckOptions

@dataclass(frozen=True)
class DeckOptions:
    classes: list[str] = field(default_factory=list)
    levels: list[int] = field(default_factory=list)
    schools: list[str] = field(default_factory=list)
    name: str = "Untitled"
🧰 Service Contracts
DeckBuilder
python
Copy
Edit
class DeckBuilder(Protocol):
    def build(self, options: DeckOptions) -> Deck:
        ...
RenderService
python
Copy
Edit
class RenderService(Protocol):
    def render_pdf(self, deck: Deck, output_path: Path) -> None:
        ...
    def render_html(self, deck: Deck, output_path: Path) -> None:
        ...
ArtService
python
Copy
Edit
class ArtService(Protocol):
    def generate_prompt(self, card: SpellCard) -> str:
        ...
    def assign_art(self, card: SpellCard, prompt: str) -> SpellCard:
        ...
💾 Repository Contracts
SpellRepository
python
Copy
Edit
class SpellRepository(Protocol):
    def load_all_spells(self) -> list[dict]:
        ...
DeckStorage
python
Copy
Edit
class DeckStorage(Protocol):
    def save(self, deck: Deck, path: Path) -> None:
        ...
    def load(self, path: Path) -> Deck:
        ...
🎯 Adapter Contract (CLI ↔ App Layer)
DeckController
python
Copy
Edit
class DeckController:
    def __init__(self, builder: DeckBuilder)
    def build_from_cli(self, options_dict: dict) -> Deck
Used by CLI only — accepts CLI-native types (dicts, strings), returns typed results.

🚫 Anti-Patterns to Avoid
Mistake	Fix
CLI accesses SpellCard directly	Use DeckController only
App layer uses Path or file system	Go through DeckStorage or injected path
No Protocol on services	Write one, then inject
Domain returns JSON blobs	Domain returns pure Python; only adapter serializes

🔒 Rules
All app/infrastructure dependencies must be injected via interface

No service uses another without a testable interface

No domain object should ever import from infrastructure or application