# img-inspire

[English](./README.md)

一个本地 Web 应用，一键生成可直接粘贴到 ChatGPT 的 [GPT Image 2](https://openai.com/index/image-generation-api/) 提示词。

**背景：** 免费版 ChatGPT 每天只能生成 3 张图片，每天想好一个好提示词才是难事——这个工具帮你搞定。

## 功能

- 从 **429 个素材**中随机挑选：32 个可填充模板（随机替换占位符）+ 397 个社区精选真实案例
- 支持 **13 个模板分类**（UI 设计、海报、信息图、摄影、插画等），另有 **精选案例** 画廊
- **中文 / EN 切换** — 占位符填充值在中英文之间切换
- **重新生成** — 保留当前模板，重新随机填充内容
- **参考图片** — 上传本地照片，提示词自动加入参考图说明
- 生成后可直接在文本框内编辑，再复制

## 安装

需要 Python 3.12+ 和 [uv](https://docs.astral.sh/uv/)。

```bash
git clone https://github.com/czczc/img-inspire
cd img-inspire
uv sync
```

## 使用方法

```bash
python main.py
```

浏览器会自动打开 `http://localhost:8000`。

首次运行时会自动克隆 [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) 模板仓库（约 10 秒）。之后启动即时生效。

### 更新模板

从上游仓库拉取最新模板：

```bash
cd awesome-gpt-image-2 && git pull
```

然后删除词语缓存，下次启动时自动重建：

```bash
rm gallery_words.json
```

## 使用流程

1. 选择分类（或保持**随机**）
2. 切换**中文 / EN**选择占位符语言
3. 点击**生成**
4. 可选：上传本地参考图片
5. 按需编辑提示词，点击**复制**
6. 粘贴到 ChatGPT（如有参考图，同步上传）

## 致谢

提示词模板与精选案例来源于 [@freestylefly](https://github.com/freestylefly) 的 [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2)，所有提示词内容的版权归原作者及贡献者所有。

## 开源协议

本项目基于 MIT 协议开源。你可以自由使用、修改、分发和二次开发，保留协议声明即可。
