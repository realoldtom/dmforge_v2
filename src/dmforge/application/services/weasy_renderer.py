# Complete weasy_renderer.py file - ONLY the class definition
# src/dmforge/application/services/weasy_renderer.py

import logging
import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from dmforge.domain.models import Deck
from packaging.version import parse as vparse
import weasyprint
import pydyf

if vparse(weasyprint.__version__) >= vparse("61.0"):
    raise RuntimeError("❌ weasyprint >= 61.0 breaks PDF rendering. Pin to 60.1.")

if vparse(pydyf.__version__) >= vparse("0.11.0"):
    raise RuntimeError("❌ pydyf >= 0.11.0 breaks PDF constructor compatibility. Pin to 0.10.0.")


class WeasyRenderer:
    def __init__(self, template_dir: Path, asset_dir: Path, verbose: bool = False):
        self.template_dir = template_dir
        self.asset_dir = asset_dir
        self.verbose = verbose
        self.env = self._setup_jinja_env()
        
        # Set up logging level based on verbose flag
        if verbose:
            logging.getLogger('weasyprint').setLevel(logging.DEBUG)
        else:
            logging.getLogger('weasyprint').setLevel(logging.WARNING)

    def _setup_jinja_env(self) -> Environment:
        """Setup Jinja2 environment with custom filters."""
        env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        return env

    def render_html(self, deck: Deck, output_path: str) -> None:
        """Render deck to HTML."""
        try:
            html_content = self._render_html_content(deck)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            if self.verbose:
                logging.info(f"✅ HTML rendered successfully: {output_path}")
        except Exception as e:
            logging.error(f"❌ HTML rendering failed: {str(e)}")
            raise RuntimeError(f"HTML rendering failed: {str(e)}")

    def render_pdf(self, deck: Deck, output_path: Path) -> None:
        """Render deck to PDF using WeasyPrint (public API only)."""
        try:
            html_string = self._render_html_content(deck)
            html = HTML(string=html_string, base_url=str(self.asset_dir))
            
            if self.verbose:
                logging.info(f"🔍 Rendering PDF to: {output_path}")
                logging.info(f"🔍 HTML content size: {len(html_string)} characters")
            
            html.write_pdf(target=str(output_path))  # Safe, single public API call

            if self.verbose:
                logging.info(f"✅ PDF rendered successfully: {output_path}")
                
        except Exception as e:
            logging.error(f"❌ PDF rendering failed: {str(e)}")
            raise RuntimeError(f"PDF rendering failed: {str(e)}")


    @staticmethod
    def check_pdf_dependencies() -> dict:
        try:
            import weasyprint
            import pydyf
            return {
                'weasyprint_installed': True,
                'pydyf_installed': True,
                'available': True,
                'weasyprint_version': weasyprint.__version__,
                'recommendations': [],
                'error': None
            }
        except ImportError as e:
            return {
                'weasyprint_installed': False,
                'pydyf_installed': False,
                'available': False,
                'weasyprint_version': None,
                'recommendations': [
                    'poetry add weasyprint',
                    'poetry add pydyf'
                ],
                'error': str(e)
            }



    def _render_html_content(self, deck: Deck) -> str:
        """Render the HTML content for a deck."""
        autoescape=select_autoescape(['html', 'xml', 'j2'])
        template = self.env.get_template('deck.html.j2')
        return template.render(deck=deck)