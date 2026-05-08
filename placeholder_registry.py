import random
from typing import Literal

Lang = Literal["en", "zh"]

# Evocative adjectives that work well in any image prompt context
_EN_FALLBACK = [
    "ethereal", "weathered", "luminous", "raw", "cinematic", "intimate",
    "stark", "lush", "tactile", "haunting", "pristine", "gritty",
    "dreamlike", "monumental", "delicate", "bold", "serene", "fractured",
    "ancient", "hyperreal", "translucent", "geometric", "organic", "vast",
]

# Patterns: (keywords_in_placeholder, zh_values, en_values)
# First match wins. Keywords checked against lowercased placeholder text.
_CURATED: list[tuple[list[str], list[str], list[str]]] = [
    (
        ["颜色", "主色", "辅色", "配色", "色系", "色调", "主色+辅", "黑色/白色"],
        ["深蓝", "金色", "珊瑚红", "薄荷绿", "象牙白", "炭黑", "玫瑰金", "暗紫", "橘橙", "冰川蓝",
         "荧光黄", "烟灰", "莫兰迪绿", "砖红", "奶油白", "孔雀蓝", "草木灰", "锈橙", "丁香紫", "月白"],
        ["deep blue", "gold", "coral red", "mint green", "ivory", "charcoal", "rose gold",
         "dark violet", "burnt orange", "glacier blue", "neon yellow", "slate grey", "dusty sage",
         "terracotta", "cream", "teal", "rust orange", "lavender"],
    ),
    (
        ["平台", "ios", "android", "web", "如 x", "如抖音", "如 ios", "x/抖音", "抖音/快手", "抖音/b站"],
        ["iOS", "Android", "Web", "小红书", "抖音", "微信", "B站", "微博", "快手", "X (Twitter)"],
        ["iOS", "Android", "Web", "Instagram", "TikTok", "YouTube", "Twitter/X", "Pinterest"],
    ),
    (
        ["比例", "9:16", "3:4", "1:1", "16:9", "21:9", "高清/4k", "4k"],
        ["9:16", "1:1", "3:4", "16:9", "4:5", "2:3"],
        ["9:16", "1:1", "3:4", "16:9", "4:5", "2:3"],
    ),
    (
        ["风格", "极简/科技", "复古/未来", "现代极简", "日式", "奢华", "视觉风格", "画风",
         "日漫/水彩", "工笔/写意", "纪实/电影", "写实直播", "黑白线稿"],
        ["极简", "科技感", "复古", "未来主义", "日式留白", "奢华编辑", "电影感",
         "国潮", "水彩手绘", "工笔重彩", "暗黑系", "赛博朋克", "新中式", "ins风", "超现实"],
        ["minimalist", "futuristic", "retro", "editorial", "wabi-sabi", "brutalist",
         "cinematic", "surrealist", "art nouveau", "neo-noir", "vaporwave", "hyperrealistic"],
    ),
    (
        ["布局", "构图", "顶部导航", "双栏", "卡片流", "居中/左对齐", "构图方式",
         "版式", "栏数", "封面区", "近景/中景", "广角建立"],
        ["居中对称", "对角构图", "三分法", "双栏布局", "卡片流", "全出血", "对称留白", "Z型动线"],
        ["centered symmetry", "diagonal composition", "rule of thirds", "two-column", "full bleed", "Z-pattern"],
    ),
    (
        ["主题", "题材", "故事主题", "主题词", "活动/产品", "你要生成的内容类型"],
        ["都市孤独感", "自然与人类共生", "赛博朋克", "童年记忆", "四季更替", "海洋深处",
         "山野晨雾", "街头烟火气", "星际漫游", "文明碰撞", "时间流逝", "生命轮回"],
        ["urban solitude", "nature and humanity", "cyberpunk", "childhood nostalgia", "changing seasons",
         "deep ocean", "mountain mist", "street life", "space travel", "clash of civilizations"],
    ),
    (
        ["情绪", "氛围", "情感", "紧张/温暖", "通勤 / 温柔", "信任 / 兴奋"],
        ["静谧", "张力", "温暖", "忧郁", "振奋", "孤独", "浪漫", "神秘", "热血", "凄美", "空灵"],
        ["serene", "tense", "warm", "melancholic", "uplifting", "solitary", "romantic", "mysterious", "ethereal"],
    ),
    (
        ["场景", "地点", "空间类型", "环境", "街头/室外", "宫廷/市井", "时间+地点", "材质表面/空间"],
        ["深夜便利店", "竹林小径", "废弃工厂", "屋顶花园", "地铁站台", "雨后街道",
         "沙漠绿洲", "古镇石板路", "霓虹夜市", "雪山营地", "渔村码头", "书院庭院"],
        ["late-night convenience store", "bamboo forest path", "abandoned factory", "rooftop garden",
         "subway platform", "rain-soaked street", "desert oasis", "neon night market", "mountain camp"],
    ),
    (
        ["角色", "人物", "主体", "主体元素", "角色/主体", "角色身份", "人物/角色",
         "运动员/模特", "人物描述"],
        ["独行的旅人", "都市白领", "武侠侠客", "未来战士", "街头艺术家", "老渔夫",
         "赛博格少女", "山野隐士", "少年剑客", "机器人厨师"],
        ["lone traveler", "urban professional", "martial artist", "futuristic soldier",
         "street artist", "old fisherman", "cyborg girl", "hermit", "robot chef"],
    ),
    (
        ["光线", "光照", "采光", "照明", "自然光", "侧光", "逆光", "路灯", "暖色/冷色",
         "正午强光", "柔光/侧光"],
        ["自然侧光", "柔和散射光", "黄金时刻逆光", "夜间霓虹灯光", "硬质顶光", "烛光暖调", "冷蓝月光"],
        ["natural side light", "soft diffused light", "golden hour backlight", "neon night light",
         "hard top light", "warm candlelight", "cold moonlight"],
    ),
    (
        ["产品", "商品名", "产品类型", "产品/家具", "核心产品"],
        ["咖啡杯", "运动耳机", "护肤精华", "智能手表", "无线键盘", "香水", "背包", "竹制文具"],
        ["coffee mug", "wireless earbuds", "facial serum", "smartwatch", "keyboard", "perfume bottle", "backpack"],
    ),
    (
        ["品牌", "品牌名", "品牌气质", "品牌元素", "品牌身份", "业务名", "logo/品牌",
         "dior / ysl", "口红品牌"],
        ["极光", "素然", "Lumina", "CloudBase", "墨迹", "Aura", "简界", "Veda", "无极", "清风"],
        ["Lumina", "CloudBase", "Aura", "Veda", "Nexus", "Solara", "Bloom", "Forge", "Drift"],
    ),
    (
        ["行业", "业务", "品类", "行业/生活方式"],
        ["健康科技", "可持续时尚", "金融科技", "新能源", "教育", "餐饮", "宠物", "文化创意", "航天"],
        ["health tech", "sustainable fashion", "fintech", "clean energy", "edtech", "food & beverage", "aerospace"],
    ),
    (
        ["关键词", "5个关键词", "标题/词语", "短句/数据", "标题/姓名"],
        ["流动感", "极致细节", "情绪张力", "空间留白", "质感光影", "故事性", "层次感", "呼吸感"],
        ["fluid motion", "hyper detail", "emotional tension", "negative space", "textural light", "narrative depth"],
    ),
    (
        ["标题", "主标题", "副标题", "主题词", "核心信息"],
        ["突破边界", "自由生长", "光与影的对话", "未来已来", "静默之美", "无界探索", "归途", "共鸣"],
        ["Break Boundaries", "Grow Wild", "Light & Shadow", "Future Now", "Silent Beauty", "Resonance"],
    ),
    (
        ["人群", "受众", "目标"],
        ["年轻职场女性", "Z世代学生", "35岁中产男性", "健身爱好者", "科技极客", "亲子家庭", "独居青年"],
        ["young professional women", "Gen Z students", "mid-career professionals", "fitness enthusiasts", "tech geeks"],
    ),
    (
        ["材质", "质地", "纹理", "木/石/金属", "肤质/材质", "液体扩散", "环境纹理"],
        ["磨砂金属", "原木纹理", "丝绒面料", "水波纹", "粗糙混凝土", "玻璃折射", "皮革压纹", "冰晶结构"],
        ["brushed metal", "raw wood grain", "velvet fabric", "water ripple", "rough concrete", "glass refraction", "leather emboss"],
    ),
    (
        ["图表类型", "流程图/对比图"],
        ["流程图", "对比图", "时间线", "关系图", "气泡图", "桑基图", "热力图"],
        ["flowchart", "comparison chart", "timeline", "relationship map", "bubble chart", "Sankey diagram"],
    ),
    (
        ["朝代", "古风", "历史"],
        ["唐朝", "宋朝", "明朝", "汉朝", "战国", "清朝", "魏晋", "隋朝"],
        ["Tang Dynasty", "Song Dynasty", "Ming Dynasty", "Han Dynasty", "Qing Dynasty"],
    ),
    (
        ["镜头", "35mm", "85mm", "广角", "近景/中景"],
        ["35mm标准镜头", "85mm人像镜头", "广角24mm", "微距镜头", "长焦200mm"],
        ["35mm standard", "85mm portrait", "24mm wide-angle", "macro lens", "200mm telephoto"],
    ),
    (
        ["用途", "功能", "输出格式"],
        ["品牌宣传", "社交媒体封面", "产品展示", "活动海报", "内容配图", "个人创作"],
        ["brand promotion", "social media cover", "product showcase", "event poster", "editorial illustration"],
    ),
    (
        ["灵感", "象征", "元素", "纹样", "品牌元素"],
        ["折纸结构", "贝壳螺旋", "星云形态", "水墨晕染", "机械齿轮", "树根脉络", "珊瑚分支", "云纹"],
        ["origami structure", "shell spiral", "nebula form", "ink diffusion", "mechanical gears", "root network", "coral branch"],
    ),
    (
        ["运动", "球拍", "球鞋", "坐姿/冲刺"],
        ["篮球", "足球", "网球", "游泳", "跑步", "攀岩", "自行车", "拳击"],
        ["basketball", "football", "tennis", "swimming", "running", "rock climbing", "cycling", "boxing"],
    ),
    (
        ["深色/浅色", "浅色/深色", "暖色/冷色", "白天/夜景", "冷/暖/高反差"],
        ["深色", "浅色", "暖色调", "冷色调", "高对比"],
        ["dark mode", "light mode", "warm tones", "cool tones", "high contrast"],
    ),
    (
        ["姿态", "坐姿/站立", "站姿", "动作", "姿势"],
        ["自然站立", "侧身回望", "低头沉思", "昂首挺立", "奔跑中", "席地而坐", "伸展双臂"],
        ["standing tall", "looking back over shoulder", "head down in thought", "mid-stride running", "seated cross-legged", "arms outstretched"],
    ),
    (
        ["服装", "衣物", "穿着", "服饰"],
        ["飘逸白袍", "皮质机车夹克", "传统汉服", "宽松亚麻衬衫", "赛博朋克战甲", "旗袍", "街头卫衣"],
        ["flowing white robe", "leather biker jacket", "traditional hanfu", "linen shirt", "cyberpunk armor", "cheongsam", "oversized hoodie"],
    ),
    (
        ["背景描述", "直播间背景", "环境描述"],
        ["极简纯白棚", "赛博朋克城市夜景", "日式榻榻米", "工业风砖墙", "星空旷野", "霓虹酒吧", "书卷气书房"],
        ["minimal white studio", "cyberpunk cityscape", "Japanese tatami room", "industrial brick wall", "starry wilderness", "neon bar", "cozy library"],
    ),
    (
        ["卖点", "功能点", "核心功能"],
        ["快速充电", "轻量设计", "超长续航", "防水防尘", "智能降噪", "触感丝滑", "极简操控"],
        ["fast charging", "lightweight design", "long battery life", "waterproof", "active noise cancellation", "silky haptics", "minimal controls"],
    ),
]

# Mined gallery words — loaded at startup via init()
_mined_zh: list[str] = []


def init(mined: dict[str, list[str]]) -> None:
    _mined_zh.extend(mined.get("zh", []))


def get_values(placeholder: str, lang: Lang) -> list[str]:
    key = placeholder.lower()
    for keywords, zh_vals, en_vals in _CURATED:
        if any(kw in key for kw in keywords):
            return zh_vals if lang == "zh" else en_vals
    return _fallback(lang)


def _fallback(lang: Lang) -> list[str]:
    if lang == "zh":
        return _mined_zh if _mined_zh else ["创意", "质感", "灵感", "叙事", "意境"]
    return _EN_FALLBACK


def random_value(placeholder: str, lang: Lang) -> str:
    return random.choice(get_values(placeholder, lang))
