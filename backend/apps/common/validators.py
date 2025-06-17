# validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from lxml import etree


def validate_file_size(value):
    """Validator untuk memastikan ukuran file tidak melebihi batas."""
    # Batas ukuran file 500KB
    limit = 0.5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            _(f"File size cannot exceed {limit/1024:.0f} KB."))


def validate_svg_file(file):
    # ... (kode Anda sudah bagus, tidak perlu diubah)
    file.seek(0)
    try:
        svg_content = file.read()
        parser = etree.XMLParser(resolve_entities=False)
        etree.fromstring(svg_content, parser=parser)
    except etree.XMLSyntaxError:
        raise ValidationError(_("Invalid or corrupted SVG file."))
    except Exception:
        raise ValidationError(_("Cannot process SVG file."))
    file.seek(0)
