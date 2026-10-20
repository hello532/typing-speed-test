#!/usr/bin/env python3
"""页面骨架归一（skeleton normalisation）—— 把每页的「可变槽位」替换成 {{槽}}，
其余 HTML 结构逐字节保留，从而得到该页的**结构指纹**。

设计目标（替代脆弱的 EXEMPT/逐条豁免表）：
- 全站所有页面的骨架必须**唯一**——任何未声明为槽位的结构差异都会立刻暴露；
- 新增功能/新页时，只要它落在已声明的槽位内（正文/FAQ/hero/nav/head 元信息），
  本检查自动通过，**零维护**；
- 若新功能引入了新的全站结构块（例如新的结果面板区块），骨架检查会失败并
  精确打印差异行，提示把它登记为槽位——这正是「有意变更需显式声明」的正确约束。

槽位（可跨页不同）：
  {{TITLE}} {{DESC}} {{KEYWORDS}} {{CANONICAL}} {{OG}} {{TW}}   —— head 元信息（TDK）
  {{ALT}}      —— hreflang alternate 引用
  {{HEADJS}}   —— 首屏主题/语言内联脚本
  {{HLANG}}    —— <html lang/dir>（RTL 语种页需要 dir="rtl"）
  {{NAV}}      —— 顶栏导航链接
  {{CRUMBS}}   —— 面包屑
  {{HERO}}     —— H1 + 导语
  {{SEO}}      —— 正文 SEO 段落
  {{FAQ}}      —— FAQ 区块
  {{LD}}       —— JSON-LD 结构化数据块
  {{VAR}}      —— 引擎 VAR_INIT 行（dur/mode/layout/variant）
  {{PR}}       —— aria-pressed 状态位
  {{STIME}}    —— 静态初始倒计时
  {{FOOT}}     —— 页脚内链枢纽
  {{V}}        —— 静态资源缓存版本号
引擎块 <script>(function(){...})</script> 与内联 <style> 整体归一（其正确性由
check 4/5/11 与 src/style.css、harness 单独守卫）。
"""
import re

ENGINE_BLOCK_RE = re.compile(r"<script>\n\(function\(\)\{\n.*?\n</script>", re.S)
STYLE_BLOCK_RE = re.compile(r"<style>.*?</style>", re.S)

# (正则, 替换) —— 顺序敏感：先剥大块，再剥小面
_RULES = [
    (ENGINE_BLOCK_RE, "<script>{{ENGINE}}</script>"),
    (STYLE_BLOCK_RE, "<style>{{CSS}}</style>"),
    # 首屏内联脚本（主题/语言 + 可选页面语言）
    (re.compile(r"<script>try\{var _t=localStorage.*?</script>", re.S), "<script>{{HEADJS}}</script>"),
    # TDK / 社交元信息
    (re.compile(r'<html lang="[^"]*"(?: dir="[^"]*")?>'), '<html lang="{{HLANG}}">'),
    (re.compile(r"<title>.*?</title>", re.S), "<title>{{TITLE}}</title>"),
    (re.compile(r'<meta name="description" content=".*?">', re.S), '<meta name="description" content="{{DESC}}">'),
    (re.compile(r'<meta name="keywords" content=".*?">', re.S), '<meta name="keywords" content="{{KEYWORDS}}">'),
    (re.compile(r'<link rel="canonical" href="[^"]*">'), '<link rel="canonical" href="{{CANONICAL}}">'),
    (re.compile(r'<link rel="alternate"[^>]*>\n?'), ""),
    (re.compile(r'<link rel="describedby"[^>]*>\n?'), ""),
    # Round-6 GEO：OG/Twitter 补齐行（全站静态，剥除以保金标稳定）
    (re.compile(r'<meta property="og:(?:image:width|image:height|image:alt|locale)"[^>]*>\n?'), ""),
    (re.compile(r'<meta name="twitter:image:alt"[^>]*>\n?'), ""),
    (re.compile(r'<meta property="og:title" content=".*?">', re.S), '<meta property="og:title" content="{{OG}}">'),
    (re.compile(r'<meta property="og:description" content=".*?">', re.S), '<meta property="og:description" content="{{OG}}">'),
    (re.compile(r'<meta property="og:url" content="[^"]*">'), '<meta property="og:url" content="{{OG}}">'),
    (re.compile(r'<meta name="twitter:title" content=".*?">', re.S), '<meta name="twitter:title" content="{{TW}}">'),
    (re.compile(r'<meta name="twitter:description" content=".*?">', re.S), '<meta name="twitter:description" content="{{TW}}">'),
    # Round-6 GEO：首页专属 Organization / WebSite 块（按 @type 预剥离，金标不动）
    (re.compile(r'<script type="application/ld\+json">\s*\{"@context":\s*"https://schema\.org",\s*"@type":\s*"(?:Organization|WebSite)".*?\}\s*</script>\n?', re.S), ""),
    # JSON-LD（三块，内容随页）
    (re.compile(r'<script type="application/ld\+json">\s*\{.*?\}\s*</script>', re.S),
     '<script type="application/ld+json">{{LD}}</script>'),
    # 结构槽位
    (re.compile(r'<header class="top">.*?</header>', re.S), '<header class="top">{{NAV}}</header>'),
    (re.compile(r'<nav class="crumbs"[^>]*>.*?</nav>\n?', re.S), "{{CRUMBS}}\n"),
    (re.compile(r'<section class="hero">.*?</section>', re.S), '<section class="hero">{{HERO}}</section>'),
    (re.compile(r'<section class="seo">.*?</section>\n?', re.S), '<section class="seo">{{SEO}}</section>\n'),
    (re.compile(r'<section class="seo faq">.*?</section>\n?', re.S), '<section class="seo faq">{{FAQ}}</section>\n'),
    (re.compile(r"<footer>.*?</footer>", re.S), "<footer>{{FOOT}}</footer>"),
    # 状态位/初值
    (re.compile(r'(<button[^>]*class="chip (?:dur|mode)) on(")'), r"\1\2"),
    (re.compile(r'aria-pressed="(?:true|false)"'), 'aria-pressed="{{PR}}"'),
    (re.compile(r'(id="sTime"[^>]*>)[^<]*<'), r"\1{{STIME}}<"),
    (re.compile(r"var dur=\d+, mode=\"\w+\", layout=\"\w+\", VARIANT=.*?;/\*VAR_INIT\*/"), "{{VAR}}"),
    (re.compile(r'<script src="(ui|egg)\.js\?v=\d+'), r'<script src="\1.js?v={{V}}'),
    # 模板占位符 → 规范槽位（src/template.html 渲染前名字与产物不同，需对齐）
    (re.compile(r"\{\{HREFLANG\}\}"), ""),
    (re.compile(r"\{\{LD_(?:WEBAPP|FAQ|BREADCRUMB|ORG|SITE)\}\}"), "<script type=\"application/ld+json\">{{LD}}</script>"),
    (re.compile(r"\{\{HEAD_SNIPPET\}\}"), "{{HEADJS}}"),
    (re.compile(r"(\{\{LD\}\}\s*\n?)+"), "{{LD}}\n"),
    # 行首缩进属纯排版，结构闸门只比 token 结构；统一剥除（末尾空行归一已在上面）
    (re.compile(r"(?m)^[ \t]+"), ""),
    # 冗余空行归一
    (re.compile(r"\n\s*\n+"), "\n"),
]


def skeleton(html: str) -> str:
    """返回归一后的骨架文本。"""
    for rx, rep in _RULES:
        html = rx.sub(rep, html)
    return html.strip()
