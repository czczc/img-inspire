# img-inspire

[中文](./README.zh.md)

A local web app that generates ready-to-use [GPT Image 2](https://openai.com/index/image-generation-api/) prompts. One click gives you a complete, filled-in prompt you can paste directly into ChatGPT.

**Why:** The free ChatGPT plan includes 3 image generations per day. Coming up with a good prompt every day is the hard part — this tool does it for you.

## What it does

- Picks a random prompt from a pool of **429 sources**: 32 fillable templates (with randomized placeholders) + 397 real curated examples from the community
- Supports **13 template categories** (UI design, posters, infographics, photography, illustration, etc.) plus a **精选案例** gallery of real examples
- **EN / ZH toggle** — placeholder values switch between English and Chinese
- **Regenerate** — keep the same template, re-roll the fill values
- **Reference image** — attach a local photo; the prompt is automatically framed to use it as a visual reference
- Edit the generated prompt directly before copying

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/czczc/img-inspire
cd img-inspire
uv sync
```

## Usage

```bash
python main.py
```

The browser opens automatically at `http://localhost:8000`.

On first run the app clones the [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) template repository (~10 seconds). Subsequent starts are instant.

### Updating templates

Pull the latest templates from the upstream repo:

```bash
cd awesome-gpt-image-2 && git pull
```

Then delete the word cache so it's rebuilt on the next start:

```bash
rm gallery_words.json
```

## Workflow

1. Pick a category (or leave it on **Random**)
2. Toggle **中文 / EN** for the language of the fill values
3. Click **Generate**
4. Optionally attach a reference image from your local files
5. Edit the prompt if needed, then **Copy**
6. Paste into ChatGPT (attach the reference image alongside if you selected one)

## Acknowledgements

Prompt templates and gallery examples are sourced from [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) by [@freestylefly](https://github.com/freestylefly). All credit for the prompt content goes to the original contributors.

## License

This project is open source under the MIT License. You can use, modify, distribute, and build on it freely while preserving the license notice.
