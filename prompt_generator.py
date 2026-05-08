import random
import re

from placeholder_registry import Lang, random_value
from template_parser import Template
from votes import weight as vote_weight


Segment = dict  # {"text": str, "random": bool}


def fill_template(template: Template, lang: Lang) -> tuple[str, list[Segment]]:
    body = template.body
    if not template.placeholders:
        return body, [{"text": body, "random": False}]

    segments: list[Segment] = []
    last_end = 0
    for m in re.finditer(r"\[([^\[\]]+)\]", body):
        if m.start() > last_end:
            segments.append({"text": body[last_end:m.start()], "random": False})
        segments.append({"text": random_value(m.group(1), lang), "random": True})
        last_end = m.end()
    if last_end < len(body):
        segments.append({"text": body[last_end:], "random": False})

    return "".join(s["text"] for s in segments), segments


_IMAGE_PREFIX: dict[Lang, str] = {
    "zh": "以上传的照片为参考，根据以下创意方向生成图片：\n\n",
    "en": "Using the uploaded photo as a reference, generate an image based on the following creative direction:\n\n",
}


GALLERY_CATEGORY = "精选案例"


def _pick(pool: list[Template], votes: dict) -> Template:
    weights = [vote_weight(t.id, votes) for t in pool]
    return random.choices(pool, weights=weights, k=1)[0]


def generate(
    templates: dict[str, list[Template]],
    lang: Lang,
    category: str | None = None,
    template_id: str | None = None,
    has_image: bool = False,
    gallery: list[Template] | None = None,
    votes: dict | None = None,
) -> tuple[str, list[Segment], Template]:
    gallery = gallery or []
    votes = votes or {}
    if template_id is not None:
        template = _find_by_id(templates, template_id, gallery)
    elif category == GALLERY_CATEGORY:
        template = _pick(gallery, votes)
    elif category and category in templates:
        template = _pick(templates[category], votes)
    else:
        all_templates = [t for tmps in templates.values() for t in tmps] + gallery
        template = _pick(all_templates, votes)

    prompt, segments = fill_template(template, lang)
    if has_image:
        prefix = _IMAGE_PREFIX[lang]
        segments = [{"text": prefix, "random": False}] + segments
        prompt = prefix + prompt
    return prompt, segments, template


def _find_by_id(templates: dict[str, list[Template]], tid: str, gallery: list[Template]) -> Template:
    for tmps in templates.values():
        for t in tmps:
            if t.id == tid:
                return t
    for t in gallery:
        if t.id == tid:
            return t
    raise ValueError(f"Template {tid!r} not found")
