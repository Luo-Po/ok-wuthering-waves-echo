# 提交消息规范指南

本规范基于 Conventional Commits，适用于 Python 项目和 ok-script 框架。

## 提交格式

```
<type>(<scope>): <subject>
// 空行
<body>
// 空行
<footer>
```

## 1. 提交类型 (Type)

| 类型         | 描述            | 示例                           |
|------------|---------------|------------------------------|
| `feat`     | 新增功能          | `feat(core): 添加缓存模块`         |
| `fix`      | 修复错误          | `fix(tests): 修复数据竞争问题`       |
| `refactor` | 代码重构（不改变功能）   | `refactor(utils): 优化字符串处理`   |
| `build`    | 构建系统或依赖变更     | `build(deps): 升级 requests 库` |
| `chore`    | 日常维护任务        | `chore(config): 更新配置文件`      |
| `style`    | 代码格式化（空格、分号等） | `style: 统一缩进格式`              |
| `test`     | 测试相关变更        | `test(unit): 添加用户模型测试`       |
| `docs`     | 文档更新          | `docs(readme): 添加安装说明`       |
| `perf`     | 性能优化          | `perf: 优化数据库查询`              |
| `ci`       | CI/CD 配置变更    | `ci(github): 添加自动化测试`        |
| `revert`   | 回滚之前的提交       | `revert: 回滚错误的合并`            |

## 2. 作用域 (Scope)

| 类型         | 可用作用域                  | 描述                 |
|------------|------------------------|--------------------|
| `feat`     | `core`, `api`          | 核心功能/API接口         |
| `fix`      | `core`, `tests`        | 核心功能/测试修复          |
| `refactor` | `core`, `utils`        | 核心功能/工具函数          |
| `build`    | `deps`, `docker`, `ci` | 依赖/Docker/CI配置     |
| `chore`    | `config`, `scripts`    | 配置文件/脚本文件          |
| `test`     | `unit`, `integration`  | 单元测试/集成测试          |
| `docs`     | `readme`, `apidocs`    | README/API文档       |
| `ci`       | `github`, `gitlab`     | GitHub/GitLab CI配置 |

> 注意：`style`, `perf`, `revert` 类型不需要指定作用域

## 3. 主题 (Subject)

- 使用祈使句（如"添加"而非"添加了"）
- 首字母小写
- 不超过50个字符
- 避免使用句号结尾

**正确示例**：

```
feat(core): 实现用户认证中间件
```

**错误示例**：

```
添加了用户认证中间件功能。
```

## 4. 正文 (Body) - 可选

- 详细描述变更内容和原因
- 使用空行与主题分隔
- 每行不超过72字符

**示例**：

```
重构用户验证逻辑以支持多种认证方式：
- 添加OAuth2支持
- 优化JWT令牌验证流程
- 移除旧的身份验证模块
```

## 5. 页脚 (Footer) - 可选

| 标记                | 用途      | 示例                                              |
|-------------------|---------|-------------------------------------------------|
| `BREAKING-CHANGE` | 标识不兼容变更 | `BREAKING-CHANGE: 移除旧API`                       |
| `Closes`          | 关联关闭的问题 | `Closes #123`                                   |
| `Related`         | 关联相关问题  | `Related #45, #78`                              |
| `Refs`            | 引用其他提交  | `Refs a1b2c3d`                                  |
| `Signed-off-by`   | 开发者签名   | `Signed-off-by: John Doe <john@example.com>`    |
| `Co-authored-by`  | 标识共同作者  | `Co-authored-by: Jane Smith <jane@example.com>` |

## 完整示例

### 功能新增

```
feat(api): 添加用户注册端点

实现POST /api/v1/register接口：
- 支持邮箱和密码注册
- 添加输入数据验证
- 生成JWT访问令牌

Closes #15
```

### 错误修复

```
fix(core): 解决并发写入问题

修复在多线程环境下数据竞争问题：
- 添加线程锁保护共享资源
- 优化数据库会话管理

BREAKING-CHANGE: 移除旧的线程池实现
```

### 依赖更新

```
build(deps): 升级SQLAlchemy到2.0

更新依赖版本：
- sqlalchemy==2.0.15
- alembic==1.12.0

需要运行迁移脚本：
python manage.py db upgrade
```

> 提示：在PyCharm中使用 **Conventional Commit** 插件可自动生成符合规范的提交消息

```

### 使用说明

1. 将配置文件保存为：  
   `.idea/conventionalCommit/conventionalcommit.settings.json`

2. 将规范文档保存为：  
   `COMMIT_CONVENTION.md`（项目根目录）

3. 在 PyCharm 中：
   - 安装 **Conventional Commit** 插件
   - 提交时使用 `Ctrl+K` 打开提交面板
   - 插件会自动提供类型和作用域提示
   - 参考规范文档填写完整提交消息

这个配置和文档完全适配您的 Python 项目和 ok-script 框架，移除了 CLI 相关部分，同时保持了提交历史的清晰性和一致性。