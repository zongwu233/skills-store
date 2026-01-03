# Skills Store v0.2.0 发布说明

**发布日期**：2026-01-03
**版本**：v0.2.0
**状态**：✅ Plugin 版本

---

## 🎉 Plugin 集成

Skills Store v0.2.0 是一个重大更新，将 Skills Store 转换为完整的 Claude Code Plugin，提供无缝的命令集成和自动技能发现。

### 核心特性

✅ **Plugin 架构** - 转换为 Claude Code Plugin，可通过 `/plugins` 安装
✅ **Slash 命令** - 提供 `/skills` 系列命令，更符合 Claude Code 使用习惯
✅ **自动发现** - 通过符号链接让已安装技能立即可用，无需重启
✅ **跨平台符号链接** - Windows/macOS/Linux 全平台支持，带降级策略
✅ **完整命令集** - list/search/install/uninstall/update/info 7个命令
✅ **向后兼容** - 现有用户可继续使用 Python 脚本

---

## 📦 新增功能

### 1. Plugin 结构

创建了完整的 Claude Code Plugin 结构：

```
.claude-plugin/
├── plugin.json              # Plugin 清单
└── hooks/
    └── post-install.sh      # 安装后钩子

plugin-skills/
└── skills-store-manager/    # 主管理技能
    └── SKILL.md

commands/                    # Slash 命令
├── skills.md                # 主分发器
├── skills-list.md
├── skills-search.md
├── skills-install.md
├── skills-uninstall.md
├── skills-update.md
└── skills-info.md
```

### 2. 符号链接集成

**特性**：
- 自动创建符号链接到 `plugin-skills/`
- Claude Code 自动扫描并加载技能
- 安装后立即可用，无需重启

**跨平台支持**：
- **Unix/Linux/macOS**: 原生符号链接
- **Windows**:
  1. 尝试符号链接（Developer Mode 或 Admin）
  2. 降级到目录连接（Junction，无需权限）
  3. 最终降级到复制（Copy，兼容性最好）

**实现**：
```python
# scripts/install_skill.py
def create_skill_symlink(skill_path, skill_name):
    """创建跨平台符号链接，带降级策略"""
    # Unix: 符号链接
    # Windows: symlink → junction → copy
```

### 3. Slash 命令

提供 7 个 `/skills` 子命令：

#### `/skills` - 主命令分发器
显示帮助和可用子命令。

#### `/skills list` - 列出已安装技能
```
/skills list
/skills list --validate
/skills list --json
```

#### `/skills search` - 搜索技能
```
/skills search "pdf"
/skills search "" --category document
```

#### `/skills install` - 安装技能
```
/skills install pdf
/skills install pdf --force
/skills install my-skill --local /path/to/skill
```

#### `/skills uninstall` - 卸载技能
```
/skills uninstall pdf
```

#### `/skills update` - 更新技能
```
/skills update pdf
```

#### `/skills info` - 显示技能详情
```
/skills info pdf
```

### 4. 主管理技能

创建了 `skills-store-manager` 技能，提供：
- 完整的用户指南
- 命令参考文档
- 故障排查章节
- 高级用法示例
- 贡献指南

### 5. 卸载脚本

新增 `scripts/uninstall_skill.py`：
- 移除符号链接
- 移除技能文件
- 更新注册表

---

## 🔧 改进

### 安装流程增强

**之前**：
```bash
python scripts/install_skill.py pdf
# 技能安装到 skills/pdf/
# 但 Claude Code 不会自动发现
```

**现在**：
```bash
/skills install pdf
# 技能安装到 skills/pdf/
# 自动创建符号链接到 plugin-skills/pdf/
# Claude Code 立即发现并可用
```

### Windows 兼容性

- **三层降级策略**：symlink → junction → copy
- **清晰的错误消息**：指导用户启用 Developer Mode
- **自动降级**：无需用户干预

### 错误处理

- 符号链接失败时自动降级
- 友好的错误消息和修复建议
- 详细的故障排查文档

---

## 📝 文档更新

- **plugin-skills/skills-store-manager/SKILL.md** - 完整的 Plugin 使用指南
- **commands/*.md** - 7个命令的详细文档
- **CHANGELOG.md** - 本文件

---

## 🔄 迁移指南

### 从 v0.1.0 升级

**现有用户**（使用 Python 脚本）：
1. ✅ 继续使用 Python 脚本，完全兼容
2. ✅ 或者开始使用 `/skills` 命令

**新用户**：
1. 安装 Plugin：
   ```bash
   /plugin marketplace add https://github.com/your-username/skills-store
   /plugin install skills-store
   ```
2. 使用命令：
   ```bash
   /skills search "pdf"
   /skills install pdf
   ```

### 数据兼容性

- `data/skills-registry.json` - ✅ 完全兼容
- `data/installed-skills.json` - ✅ 完全兼容
- `skills/` 目录 - ✅ 完全兼容

---

## 🐛 已知问题

1. **Windows 符号链接权限**
   - **症状**：某些 Windows 配置无法创建符号链接
   - **影响**：技能仍可用，但使用复制而非链接
   - **解决方案**：自动降级到复制，或启用 Developer Mode

2. **Plugin 更新覆盖用户数据**
   - **症状**：理论上可能覆盖 `installed-skills.json`
   - **缓解**：已添加到 `.gitignore`，不包含在 Plugin 中

---

## 🚀 后续计划

### v0.3.0（规划中）

- 自动注册表更新
- 依赖管理
- 版本管理（多版本共存）
- Web 界面

---

## 📊 统计

- **新增文件**: 14 个
- **修改文件**: 1 个（install_skill.py）
- **新增代码行**: ~1500 行
- **开发时间**: 6-9 小时

---

## 👥 贡献者

- @your-username - 核心开发和设计

---

## 📄 许可证

MIT License

---

*详细的项目创建过程和技术决策，请参考 [CREATION_PROCESS.md](CREATION_PROCESS.md)*
*关键设计决策，请参考 [DECISIONS.md](DECISIONS.md)*

---

# Skills Store v0.1.0 发布说明

**发布日期**：2026-01-03
**版本**：v0.1.0
**状态**：✅ 稳定可用

---

## 🎉 首次发布

Skills Store v0.1.0 是 Claude Skills 的首个包管理系统，提供技能发现、安装、管理和验证功能。

### 核心特性

✅ **集中式索引** - 统一管理来自 9 个 GitHub 仓库的 21 个技能
✅ **搜索功能** - 按关键词、分类、标签搜索技能
✅ **一键安装** - 从 GitHub 自动下载并安装技能
✅ **已安装管理** - 列出、验证、管理已安装技能
✅ **质量验证** - 自动验证技能格式和必需字段
✅ **跨平台** - 支持 Windows、macOS、Linux
✅ **可移植** - 使用相对路径，支持任意目录安装

---

## 📦 包含的功能

### 1. 搜索技能

```bash
python scripts/search_skills.py <query>
```

- 支持关键词搜索（name, description, tags）
- 支持分类过滤
- 支持来源类型过滤

### 2. 安装技能

```bash
python scripts/install_skill.py <skill_name>
```

- 从 GitHub 自动下载
- 验证技能格式
- 安装到本地 skills/ 目录
- 更新已安装索引

### 3. 列出已安装技能

```bash
python scripts/list_skills.py
```

- 显示所有已安装技能
- 显示安装时间、来源、验证状态
- 支持重新验证

### 4. 查看技能详情

```bash
python scripts/show_skill_info.py <skill_name>
```

- 显示完整元数据
- 预览 SKILL.md 内容
- 显示文件结构

### 5. 验证技能

```bash
python scripts/validate_skill.py <skill_name>
```

- 验证 SKILL.md 格式
- 验证必需字段
- 检查路径安全性

### 6. 索引管理工具

```bash
# 验证索引
python tools/validate_registry.py

# 生成 README
python tools/generate_readme.py
```

---

## 🗂️ 项目结构

```
skills-store/
├── SKILL.md                             # Skills Store skill 定义
├── skills/                              # 本地技能存储
│   └── skill-creator/                   # 已安装的技能
├── scripts/                             # 核心脚本
│   ├── install_skill.py                 # 安装技能
│   ├── search_skills.py                 # 搜索技能
│   ├── list_skills.py                   # 列出已安装
│   ├── show_skill_info.py               # 显示详情
│   ├── validate_skill.py                # 验证技能
│   └── utils/
│       ├── registry.py                  # 索引管理
│       ├── github_client.py             # GitHub API
│       └── skill_validator.py           # 验证逻辑
├── data/                                # 数据文件
│   ├── skills-registry.json             # 主索引（21 个技能）
│   └── installed-skills.json            # 已安装技能记录
├── references/                          # 参考文档
│   ├── user-guide.md                    # 用户指南
│   └── registry-schema.md               # Schema 文档
├── tools/                               # 维护工具
│   ├── validate_registry.py             # 验证索引
│   └── generate_readme.py               # 生成 README
├── CREATION_PROCESS.md                  # 创建过程记录
├── DECISIONS.md                         # 关键决策摘要
├── FIX_RELATIVE_PATHS.md                # 路径问题修复记录
└── CHANGELOG.md                         # 版本变更日志
```

---

## 📊 技能索引统计

### 覆盖的仓库（9 个）

| 仓库 | 技能数 | 类别 |
|------|--------|------|
| anthropics/skills | 8 | 官方技能 |
| obra/superpowers | 20+ | 生产力 |
| alirezarezvani/claude-skills | 3 | 架构、产品、DevOps |
| K-Dense-AI/claude-scientific-skills | 138 | 科学计算 |
| mrgoonie/claudekit-skills | 10 | 代理技能 |
| czlonkowski/n8n-skills | 5 | 工作流自动化 |
| huggingface/skills | 5 | 机器学习 |
| bear2u/my-skills | 3 | 常用技能 |
| yusufkaraaslan/Skill_Seekers | 1 | 工具转换 |

### 索引技能（21 个代表技能）

**文档处理**：pdf, docx, pptx, xlsx
**开发工具**：frontend-design, mcp-builder, senior-architect, skill-creator
**科学计算**：bioinformatics, data-analysis, cheminformatics, hf-llm-trainer, hf-dataset-creator
**生产力**：superpowers, sequential-thinking, code-documentation
**创意设计**：algorithmic-art
**自动化**：n8n-workflow
**产品管理**：product-management
**DevOps**：devops-engineer
**工具**：skill-seekers

### 分类（9 个）

- Document Processing (4)
- Development Tools (4)
- Scientific Computing & ML (5)
- Productivity & Workflow (3)
- Operations & DevOps (1)
- Business & Product (1)
- Creative & Design (1)
- Automation & Workflow (1)
- Tools & Utilities (1)

---

## ✅ 已测试场景

### 基本功能测试

- ✅ 搜索所有技能（空关键词）
- ✅ 搜索特定技能（pdf, superpowers 等）
- ✅ 查看技能详情（registry 和 installed）
- ✅ 安装技能（skill-creator）
- ✅ 列出已安装技能
- ✅ 验证已安装技能
- ✅ Windows 编码兼容（emoji 显示）
- ✅ 相对路径存储和显示

### 错误处理测试

- ✅ 安装不存在的技能
- ✅ 验证无效的技能目录
- ✅ GitHub API 错误处理
- ✅ 网络超时重试

### 跨平台测试

- ✅ Windows 10/11 (MSYS/Git Bash)
- ⏳ macOS (待测试)
- ⏳ Linux (待测试)

---

## 🐛 已知问题

### 限制

1. **技能集成**
   - 已安装的技能需要手动配置到 Claude Code
   - 自动化集成待实现

2. **版本管理**
   - 不支持技能版本管理
   - 总是安装最新版本

3. **依赖管理**
   - 不检查技能依赖
   - 不自动安装依赖

4. **更新机制**
   - 没有自动更新索引
   - 需要手动更新 skills-registry.json

5. **卸载功能**
   - 没有卸载技能的命令
   - 需要手动删除目录

### 兼容性

- Python 3.7+ (测试环境：Python 3.9)
- 需要网络连接（安装 GitHub 技能）
- GitHub API 限流（60 次/小时，未认证）

---

## 🔧 技术栈

### 核心依赖

- **Python 3.7+** - 核心语言
- **pathlib** - 路径操作
- **requests** - HTTP 请求（GitHub API）
- **yaml** - YAML 解析（SKILL.md frontmatter）
- **json** - JSON 处理

### 开发工具

- Git - 版本控制
- GitHub - 代码托管
- VS Code / 推荐编辑器

---

## 📚 文档

### 用户文档

- [用户指南](references/user-guide.md) - 详细使用说明
- [Schema 文档](references/registry-schema.md) - 索引格式说明

### 开发文档

- [创建过程记录](CREATION_PROCESS.md) - 完整设计思路
- [关键决策](DECISIONS.md) - 设计决策和原因
- [路径问题修复](FIX_RELATIVE_PATHS.md) - 技术问题修复

### 社区资源

- [skills-registry 仓库](../skills-registry/) - 集中式技能索引
- [awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) - 技能精选列表

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/skills-store.git
cd skills-store
```

### 2. 搜索技能

```bash
python scripts/search_skills.py ""
```

### 3. 安装技能

```bash
python scripts/install_skill.py pdf
```

### 4. 列出已安装

```bash
python scripts/list_skills.py
```

---

## 📝 下一步计划

### v0.2.0 规划

**优先级 P0**（必须有）：
- [ ] 卸载技能命令
- [ ] 更新索引命令
- [ ] 批量安装支持

**优先级 P1**（重要）：
- [ ] 自动更新索引（GitHub 定期扫描）
- [ ] 版本管理
- [ ] 依赖检查

**优先级 P2**（增强）：
- [ ] 与 Claude Code 集成
- [ ] 配置文件支持
- [ ] 环境变量支持

### 长期愿景

- Web 界面
- 社区贡献平台
- 技能评分系统
- 智能推荐

---

## 🤝 贡献指南

### 如何贡献

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 添加新技能

1. 编辑 `data/skills-registry.json`
2. 添加技能信息
3. 运行 `python tools/validate_registry.py`
4. 运行 `python tools/generate_readme.py`（如果维护 skills-registry）
5. 提交 PR

### 报告问题

请在 GitHub Issues 中报告问题，包含：
- 问题描述
- 复现步骤
- 错误信息
- 环境信息（OS、Python 版本）

---

## 📄 许可证

MIT License

---

## 🙏 致谢

### 核心 Skills

感谢以下项目提供优秀技能：

- [Anthropic Skills](https://github.com/anthropics/skills) - 官方技能
- [Superpowers](https://github.com/obra/superpowers) - 生产力技能
- [Claude Scientific Skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 科学计算技能
- [Hugging Face Skills](https://github.com/huggingface/skills) - ML 训练技能
- [n8n Skills](https://github.com/czlonkowski/n8n-skills) - 工作流自动化
- [Claude Skills](https://github.com/alirezarezvani/claude-skills) - 专业技能
- [ClaudeKit Skills](https://github.com/mrgoonie/claudekit-skills) - 代理技能
- [My Skills](https://github.com/bear2u/my-skills) - 常用技能
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - 文档转换工具

### Awesome Lists

- [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)
- [VoltAgent/awesome-claude-skills](https://github.com/VoltAgent/awesome-claude-skills)
- [travvn/awesome-claude-skills](https://github.com/travvn/awesome-claude-skills)

---

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/skills-store/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/skills-store/discussions)

---

**v0.1.0 - 2026-01-03**

🎉 感谢使用 Skills Store！
