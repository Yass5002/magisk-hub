# Magisk Hub 简体中文（zh-Hans / zh-CN）本地化术语表与编辑规范

本文档为 Magisk Hub 全站及模块文档（`content/zh/modules/*.md` 与 `locales/zh/modules/*.json`）本地化的权威规范，适用于所有人工编辑与 AI 本地化子代理。

---

## 1. 核心原则（严禁机翻腔）

1. **准确性优先于字面直译**：深入理解 Android Root、Linux 内核、Zygisk、LSPosed、KernelSU 与 APatch 机制后，用符合中文 Android 玩机社区与系统工程师习惯的表达撰写。
2. **禁止遗漏与删减**：保留原文所有技术章节、参数说明、表格、架构图、注意事项与 FAQ，不得擅自缩写或跳过段落。
3. **代码与路径绝对保真**：
   - 所有代码块（```` ```bash ````、```` ```json ```` 等）、行内代码（`` `...` ``）、文件路径（如 `/data/adb/modules/`、`/sys/class/power_supply/`）、包名（如 `com.google.android.gms.unstable`）、属性名（如 `ro.build.fingerprint`）、环境变量与 CLI 命令 **禁止翻译或改动**。
   - 代码块内的注释可视上下文保留英文或补充中文说明，但命令本身一字不改。
4. **结构与 Schema 严格对齐**：
   - Markdown Frontmatter 中的 YAML 键名（`id`, `title`, `sidebarTitle`, `description`, `category`, `tier`, `searchQueries`, `prerequisites`, `conflicts`, `configPaths`, `features`, `faq`）必须保持英文原样。
   - `id`、`category`、`tier`、`configPaths` 必须与英文原文件完全一致；仅翻译可读文本字段（`title`, `sidebarTitle`, `description`, `searchQueries`, `prerequisites`, `conflicts`, `features`, `faq[].question`, `faq[].answer`）。
   - `searchQueries` 应改写为真实中文搜索词（如 `"Magisk 模块下载"`, `"Play Integrity 过检测"`, `"小米 FastCharge 快充解锁"`），而非直译英文关键词。

---

## 2. 专有名词与保留规则

### 2.1 保留英文原文（不音译、不强行意译）
- **平台与框架**：`Magisk`（可在 SEO 关键词中辅以“面具”）、`KernelSU`、`APatch`、`KernelPatch`、`Zygisk`、`Zygisk Next`、`ReZygisk`、`LSPosed`、`Xposed`、`Shizuku`、`Dhizuku`、`Sui`、`Riru`、`SUSFS`
- **系统机制与安全概念**：`Play Integrity`、`SafetyNet`、`Keybox`、`Strong Integrity`、`Device Integrity`、`Basic Integrity`、`Bootloader`、`Bootloop`、`SELinux`、`OverlayFS`、`Magic Mount`、`Resetprop`、`DenyList`、`GKI`、`LKM`、`KPM`、`TWRP`、`OrangeFox`、`Fastboot`、`ADB`、`TPROXY`、`Doze`、`Wakelock`
- **模块名称**：`Shamiko`、`TrickyStore`、`PlayIntegrityFix`、`PlayIntegrityFork`、`bindhosts`、`BCR`、`ACC`、`ViPER4Android`、`Dolby Atmos` 等保留官方英文名；若存在中文社区通用简称，可在标题或首次出现时标注，例如 `Advanced Charging Controller (ACC 高级充电控制)` 或 `Shamiko`。

### 2.2 标准术语对照表

| 英文术语 | 标准简体中文译法 |
| --- | --- |
| Systemless | 无系统分区修改（Systemless） / 无侵入式 |
| Flash (a module / image) | 刷入（模块 / 镜像） |
| Root manager | Root 管理器 |
| Superuser | 超级用户 / Root 权限 |
| Boot image (`boot.img` / `init_boot.img`) | Boot 镜像（`boot.img` / `init_boot.img`） |
| Ramdisk | 内存盘（Ramdisk） |
| Partition (`/system`, `/vendor`) | 分区 |
| Spoofing | 伪装 / 欺骗 |
| Attestation (Hardware / Key Attestation) | 密钥证明 / 硬件认证 |
| Fingerprint (Device fingerprint) | 设备指纹 |
| Root hiding / cloaking | Root 隐藏 / 隐藏 Root 环境 |
| Scope (LSPosed) | 作用域（Scope） |
| Method hooking | 方法挂钩（Hook） |
| Daemon | 守护进程 |
| Kernel module / governor | 内核模块 / 调度器（Governor） |
| Thermal throttling | 温控降频 |
| Battery idle / bypass charging | 电池旁路供电 / 充电直通（Idle Mode） |
| Certificate Authority (CA) | CA 根证书 |
| Install from storage | 从本地安装 / 从存储设备安装 |
| Safe Mode | 安全模式 |
| Maintainer | 维护者 |
| Release asset | 发布包 / 发行版附件 |
| Community package | 社区收录包 |
| Prerequisites | 前置要求 / 使用前提 |
| Known conflicts | 已知冲突 |
| Configuration paths | 配置文件路径 |

---

## 3. 中文排版与标点规范

1. **使用全角中文标点**：中文句子中使用 `，。：；（）！？`，避免中英文标点混用（代码块与行内代码内部除外）。
2. **中英文与数字混排留白**：中文与英文字母、数字或行内代码之间保留半角空格（如 `支持 Magisk 26.0+、KernelSU 与 APatch`、`修改 `/data/adb/pif.json` 配置文件`）；中文标点紧邻英文或数字时不额外加空格。
3. **禁止冗余“的”“进行”等翻译腔**：
   - Bad: `它通过修改系统属性来进行设备指纹的伪装操作。`
   - Good: `该模块通过拦截并修改系统属性实现设备指纹伪装。`

---

## 4. SEO 元数据写作规范（`locales/zh/modules/<slug>.json`）

每个模块对应的 JSON 文件结构如下：

```json
{
  "id": "playintegrityfix",
  "displayName": "PlayIntegrityFix (PIF)",
  "description": "主流社区维护的 PlayIntegrityFix 分支，通过 Zygisk 注入与设备指纹伪装修复 Android 设备的 Play Integrity 认证。",
  "seo": {
    "title": "PlayIntegrityFix 下载与配置指南 (Magisk/KSU/APatch) | Magisk Hub",
    "description": "下载最新版 PlayIntegrityFix，支持 Magisk、KernelSU 与 APatch。包含 Zygisk 注入原理、pif.json 指纹配置与 Play Integrity 过检排查指南。"
  },
  "searchAliases": [
    "Play Integrity 过检测",
    "PIF 模块",
    "谷歌完整性认证修复",
    "设备指纹伪装"
  ]
}
```

### 长度与质量红线
- `seo.title`：控制在 **22–58 字符**（避免在 Google / Bing / Baidu 搜索结果标题被截断），必须唯一，包含模块名与中文核心检索词（如 `下载`、`模块`、`指南`、`| Magisk Hub`）。
- `seo.description`：控制在 **55–115 字符**（中文信息密度高，对应 SERP 140–160 英文字符视觉宽度），必须唯一，自然包含支持平台与核心功能，不要堆砌版本号（版本号会自动同步，避免文案过期）。
- `searchAliases`：提供 3–6 个中文玩机用户常搜词条（含中文俗称、功能描述、兼容框架关键词）。
