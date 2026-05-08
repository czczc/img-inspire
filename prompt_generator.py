import random
import re

from placeholder_registry import Lang, random_value
from template_parser import Template


def fill_template(template: Template, lang: Lang) -> str:
    if not template.placeholders:
        return template.body  # gallery examples are complete — no filling needed
    body = template.body
    for placeholder in template.placeholders:
        value = random_value(placeholder, lang)
        body = body.replace(f"[{placeholder}]", value, 1)
    # Catch any brackets missed by the placeholder list
    body = re.sub(r"\[([^\[\]]+)\]", lambda m: random_value(m.group(1), lang), body)
    return body


_IMAGE_PREFIX: dict[Lang, str] = {
    "zh": "以上传的照片为参考，根据以下创意方向生成图片：\n\n",
    "en": "Using the uploaded photo as a reference, generate an image based on the following creative direction:\n\n",
}


GALLERY_CATEGORY = "精选案例"


def generate(
    templates: dict[str, list[Template]],
    lang: Lang,
    category: str | None = None,
    template_id: str | None = None,
    has_image: bool = False,
    gallery: list[Template] | None = None,
) -> tuple[str, Template]:
    gallery = gallery or []
    if template_id is not None:
        template = _find_by_id(templates, template_id, gallery)
    elif category == GALLERY_CATEGORY:
        template = random.choice(gallery)
    elif category and category in templates:
        template = random.choice(templates[category])
    else:
        all_templates = [t for tmps in templates.values() for t in tmps] + gallery
        template = random.choice(all_templates)

    prompt = fill_template(template, lang)
    if has_image:
        prompt = _IMAGE_PREFIX[lang] + prompt
    return prompt, template


def _find_by_id(templates: dict[str, list[Template]], tid: str, gallery: list[Template]) -> Template:
    for tmps in templates.values():
        for t in tmps:
            if t.id == tid:
                return t
    for t in gallery:
        if t.id == tid:
            return t
    raise ValueError(f"Template {tid!r} not found")
