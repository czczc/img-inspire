import json
import logging
import re
from pathlib import Path

logging.getLogger("jieba").setLevel(logging.ERROR)
import jieba.posseg as pseg  # noqa: E402

CACHE_FILE = "gallery_words.json"
_MIN_WORD_LEN = 2
# Keep adjectives and verbal-nouns only — they're more evocative than generic nouns
_KEEP_POS = {"a", "vn", "an"}
# Hard reject list: functional/mundane words that pollute creative prompts
_STOP_WORDS = {
    "名字", "字号", "交通", "布局", "颜色", "比例", "数量", "内容", "文字", "文本",
    "内容", "功能", "格式", "界面", "操作", "链接", "按钮", "版本", "用户", "账号",
    "信息", "数据", "图片", "图像", "视频", "音频", "文件", "模板", "示例", "样式",
    "设置", "配置", "参数", "标准", "规范", "要求", "说明", "描述", "介绍", "背景",
}


def _extract_prompts(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"```text\n(.*?)\n```", text, re.DOTALL)


def _is_chinese(word: str) -> bool:
    return any("一" <= ch <= "鿿" for ch in word)


def mine(repo_path: Path) -> dict[str, list[str]]:
    cache = repo_path.parent / CACHE_FILE
    if cache.exists():
        return json.loads(cache.read_text())

    prompts: list[str] = []
    for fname in ("gallery-part-1.md", "gallery-part-2.md"):
        p = repo_path / "docs" / fname
        if p.exists():
            prompts.extend(_extract_prompts(p))

    word_freq: dict[str, int] = {}
    for prompt in prompts:
        seen = set()
        for word, flag in pseg.cut(prompt):
            if len(word) < _MIN_WORD_LEN:
                continue
            if not _is_chinese(word):
                continue
            if not any(flag.startswith(k) for k in _KEEP_POS):
                continue
            if word in _STOP_WORDS:
                continue
            if word not in seen:
                word_freq[word] = word_freq.get(word, 0) + 1
                seen.add(word)

    # Keep words that appear in at least 2 different prompts — filters hyper-specific one-offs
    words = sorted(w for w, freq in word_freq.items() if freq >= 2)
    result = {"zh": words}
    cache.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Mined {len(words)} Chinese words from gallery ({len(prompts)} prompts)")
    return result
