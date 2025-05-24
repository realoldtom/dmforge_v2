import sys


def check_render_stack():
    import pydyf
    import weasyprint
    from packaging.version import parse as vparse

    if vparse(weasyprint.__version__) >= vparse("61.0"):
        print("❌ Incompatible weasyprint version:", weasyprint.__version__)
        sys.exit(1)

    if vparse(pydyf.__version__) >= vparse("0.11.0"):
        print("❌ Incompatible pydyf version:", pydyf.__version__)
        sys.exit(1)

    print("✅ PDF render stack OK:", weasyprint.__version__, "/", pydyf.__version__)
