# YuNi - AI语音识别与3D模型管理系统

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)![Python](https://img.shields.io/badge/python-3.8+-green.svg)![FastAPI](https://img.shields.io/badge/fastapi-0.116.1-teal.svg)![License](https://img.shields.io/badge/license-MIT-orange.svg)

**现代化分层架构的AI应用平台，集成语音识别、3D模型展示与管理功能**

[快速开始](#快速开始) • [API文档](#核心功能模块) • [部署指南](#部署流程) • [贡献指南](#贡献规范)

</div>

* * *

## 📋 目录

* [项目概述](#项目概述)
* [快速开始](#快速开始)
* [核心功能模块](#核心功能模块)
* [测试指南](#测试指南)
* [部署流程](#部署流程)
* [贡献规范](#贡献规范)
* [版权与许可](#版权与许可)
* [TODO](#todo)

* * *

## 项目概述

### 核心功能

YuNi 是一个企业级AI应用平台，提供以下核心功能：

| 功能模块 | 描述  | 技术实现 |
| --- | --- | --- |
| **语音识别** | 离线语音转文字，支持99+种语言 | OpenAI Whisper (Large V3 / Turbo) |
| **3D模型管理** | 多格式3D模型上传、预览、管理 | Three.js + WebGL |
| **用户系统** | 注册登录、个人资料、权限管理 | JWT + SQLAlchemy |
| **RAG问答** | 基于检索增强生成的心理健康问答 | BM25 + Vector Retrieval |

### 应用场景

* **企业内训系统**：语音会议记录、培训内容转录
* **3D内容管理**：产品展示、设计评审、模型归档
* **心理健康支持**：AI心理咨询、情感分析、知识问答
* **多媒体处理**：音频文件批量处理、格式转换

### 技术栈选型

#### 后端技术栈

| 类别  | 技术  | 版本  | 用途  |
| --- | --- | --- | --- |
| **Web框架** | FastAPI | 0.116.1 | 高性能异步API框架 |
| **ASGI服务器** | Uvicorn | 0.35.0 | ASGI应用服务器 |
| **ORM框架** | SQLAlchemy | 2.0.36 | 数据库ORM映射 |
| **认证** | PyJWT | 2.10.1 | JWT Token生成与验证 |
| **数据验证** | Pydantic | 内置  | 请求/响应数据验证 |
| **语音识别** | OpenAI Whisper | 20250625 | 离线语音转文字 |
| **中文分词** | jieba | 0.42.1 | 中文文本处理 |
| **机器学习** | scikit-learn | 1.7.2 | 传统检索算法（BM25/VSM） |
| **图像处理** | Pillow | 11.2.1 | 头像图片处理 |

#### 前端技术栈

| 类别  | 技术  | 版本  | 用途  |
| --- | --- | --- | --- |
| **3D渲染** | Three.js | r152+ | WebGL 3D模型渲染 |
| **模板引擎** | Jinja2 | 3.1.6 | HTML模板渲染 |
| **样式** | CSS3 | -   | 现代化UI设计 |
| **脚本** | JavaScript ES6+ | -   | 前端交互逻辑 |

#### 数据库与中间件

| 类别  | 技术  | 版本  | 用途  |
| --- | --- | --- | --- |
| **数据库** | SQLite | 3.x | 轻量级关系型数据库（开发） |
| **文件存储** | 本地文件系统 | -   | 用户上传文件存储 |
| **音频处理** | FFmpeg | 7.1.1 | 音频格式转换 |

### 系统架构

    graph TB
        subgraph "客户端层"
            A[Web浏览器] --> B[HTML/CSS/JS]
            B --> C[Three.js 3D渲染]
        end
    
        subgraph "应用层"
            D[FastAPI应用] --> E[路由层 /api/v1]
            E --> F[认证中间件]
            E --> G[业务逻辑层]
        end
    
        subgraph "服务层"
            G --> H[ASR服务Whisper]
            G --> I[RAG服务BM25/VSM]
            G --> J[文件服务上传/存储]
            G --> K[用户服务JWT认证]
        end
    
        subgraph "数据层"
            L[(SQLite数据库)] --> M[用户表]
            L --> N[历史记录表]
            L --> O[模型表]
            P[文件系统] --> Q[音频文件]
            P --> R[3D模型文件]
            P --> S[用户头像]
        end
    
        B --> D
        F --> K
        G --> H
        G --> I
        G --> J
        K --> L
        J --> P
    
        style D fill:#4A90E2
        style H fill:#50C878
        style I fill:#FF6B6B
        style L fill:#FFD93D

**架构说明**：

1. **客户端层**：基于现代Web标准，使用Three.js实现3D模型渲染
2. **应用层**：FastAPI提供RESTful API，支持异步处理
3. **服务层**：模块化服务设计，支持语音识别、RAG检索、文件管理等
4. **数据层**：SQLite数据库存储结构化数据，文件系统存储二进制文件

* * *

## 快速开始

### 环境要求

#### 必需环境

| 组件  | 最低版本 | 推荐版本 | 说明  |
| --- | --- | --- | --- |
| **Python** | 3.8 | 3.11+ | 支持类型提示和异步特性 |
| **pip** | 20.0+ | 23.0+ | Python包管理器 |
| **操作系统** | Windows 10 / Linux / macOS | -   | 跨平台支持 |

#### 可选组件

| 组件  | 用途  | 说明  |
| --- | --- | --- |
| **FFmpeg** | 音频格式转换 | 已包含在 `tools/` 目录 |
| **Node.js** | 前端构建（如需要） | 当前版本无需 |

### 安装步骤

#### 1. 克隆项目

    git clone https://github.com/your-org/YuNi.git
    cd YuNi

#### 2. 创建虚拟环境（推荐）

    # Windows
    python -m venv venv
    venv\Scripts\activate
    
    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate

#### 3. 安装依赖

    # 生产环境（推荐）
    pip install -r requirements.txt
    
    # 开发环境（包含测试工具）
    pip install -r requirements-dev.txt
    
    # 精确版本锁定（生产部署）
    pip install -r requirements-locked.txt

#### 4. 初始化数据库

数据库会在首次启动时自动创建，无需手动初始化。

### 配置说明

#### 环境变量配置

创建 `.env` 文件（或设置系统环境变量）：

    # ==================== 必需配置（生产环境）====================
    # JWT密钥：必须设置，建议使用32+字符的随机字符串
    export YUNI_JWT_SECRET="your-secret-key-here-min-32-chars"
    
    # ==================== 可选配置 ====================
    # 服务器地址（默认：127.0.0.1）
    export YUNI_HOST="127.0.0.1"
    
    # 服务器端口（默认：8003）
    export YUNI_PORT="8003"
    
    # 调试模式（默认：False，生产环境必须为False）
    export YUNI_DEBUG="False"
    
    # JWT Token过期时间（分钟，默认：60）
    export YUNI_JWT_EXPIRE_MINUTES="60"
    
    # 环境类型（development/production/testing）
    export YUNI_ENV="development"

#### 配置文件说明

项目支持YAML配置文件（`config/` 目录）：

| 配置文件 | 用途  | 说明  |
| --- | --- | --- |
| `config/development.yaml` | 开发环境 | 启用调试、允许所有CORS |
| `config/production.yaml` | 生产环境 | 禁用调试、限制CORS |
| `config/testing.yaml` | 测试环境 | 独立数据库、测试端口 |

**配置优先级**：环境变量 > YAML配置文件 > 代码默认值

#### 关键参数释义

| 参数  | 类型  | 默认值 | 说明  |
| --- | --- | --- | --- |
| `YUNI_JWT_SECRET` | string | 随机生成 | JWT签名密钥，生产环境必须设置 |
| `YUNI_HOST` | string | 127.0.0.1 | 服务器监听地址，生产环境建议0.0.0.0 |
| `YUNI_PORT` | int | 8003 | 服务器监听端口 |
| `YUNI_DEBUG` | bool | False | 调试模式，生产环境必须False |
| `YUNI_JWT_EXPIRE_MINUTES` | int | 60  | Token有效期（分钟） |

**⚠️ 安全提示**：

* 开发环境未设置 `YUNI_JWT_SECRET` 时会使用随机密钥，每次重启后Token会失效
* 生产环境**必须**设置 `YUNI_JWT_SECRET`，否则存在安全风险
* 生产环境**必须**设置 `YUNI_DEBUG=False`，避免泄露敏感信息

### 启动命令

#### 开发模式

    # 方式1：使用启动脚本（推荐）
    python run.py
    
    # 方式2：直接使用uvicorn
    uvicorn backend.main:app --host 127.0.0.1 --port 8003 --reload

**开发模式特性**：

* 自动重载（代码修改后自动重启）
* 详细错误信息
* 允许所有CORS来源

#### 生产模式

    # 使用gunicorn + uvicorn workers（推荐）
    gunicorn backend.main:app \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:8003 \
        --access-logfile - \
        --error-logfile -
    
    # 或使用uvicorn（单进程）
    uvicorn backend.main:app \
        --host 0.0.0.0 \
        --port 8003 \
        --workers 4 \
        --no-access-log

**生产模式特性**：

* 多进程/多线程处理
* 访问日志记录
* 错误日志记录
* 性能优化

### 访问地址

启动成功后，访问以下地址：

| 页面  | 地址  | 说明  |
| --- | --- | --- |
| **首页** | http://127.0.0.1:8003/ | 项目介绍页面 |
| **登录** | http://127.0.0.1:8003/login | 用户登录 |
| **注册** | http://127.0.0.1:8003/register | 用户注册 |
| **主界面** | http://127.0.0.1:8003/main | 3D模型管理 |
| **语音识别** | http://127.0.0.1:8003/whisper | 语音转文字 |
| **心理健康** | http://127.0.0.1:8003/mental-health | AI心理咨询 |
| **账户设置** | http://127.0.0.1:8003/account | 用户设置 |
| **API文档** | http://127.0.0.1:8003/docs | Swagger UI |
| **ReDoc文档** | http://127.0.0.1:8003/redoc | ReDoc文档 |

* * *

## 核心功能模块

### 1. 用户认证模块

#### 功能描述

提供用户注册、登录、Token认证等核心功能，基于JWT实现无状态认证。

#### API接口

| 方法  | 路径  | 说明  | 认证  |
| --- | --- | --- | --- |
| `POST` | `/api/register` | 用户注册 | 否   |
| `POST` | `/api/login` | 用户登录 | 否   |
| `GET` | `/api/check_username` | 检查用户名可用性 | 否   |
| `GET` | `/api/me` | 获取当前用户信息 | 是   |

#### 调用示例

**用户注册**：

    POST /api/register
    Content-Type: application/json
    
    {
      "username": "testuser",
      "password": "Test123",
      "confirm_password": "Test123",
      "name": "Test User",
      "email": "test@example.com"
    }

**响应**：

    {
      "message": "注册成功",
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "uid": 100000,
        "username": "testuser",
        "name": "Test User"
      }
    }

**用户登录**：

    POST /api/login
    Content-Type: application/json
    
    {
      "username": "testuser",
      "password": "Test123"
    }

**响应**：

    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "uid": 100000,
        "username": "testuser",
        "name": "Test User"
      }
    }

#### 关键算法说明

* **密码哈希**：使用Werkzeug的PBKDF2算法，盐值随机生成
* **JWT生成**：使用HS256算法，包含用户ID、过期时间等claims
* **Token验证**：中间件自动验证Token有效性和过期时间

### 2. 语音识别模块（ASR）

#### 功能描述

基于OpenAI Whisper模型实现离线语音转文字，支持99+种语言自动识别。

#### API接口

| 方法  | 路径  | 说明  | 认证  |
| --- | --- | --- | --- |
| `GET` | `/models` | 获取可用Whisper模型列表 | 否   |
| `POST` | `/api/transcribe_json` | 语音转文字 | 是   |
| `GET` | `/api/history` | 获取识别历史记录 | 是   |
| `DELETE` | `/api/history/{history_id}` | 删除历史记录 | 是   |
| `POST` | `/api/history/clear` | 清空所有历史记录 | 是   |

#### 调用示例

**语音转文字**：

    POST /api/transcribe_json
    Authorization: Bearer <token>
    Content-Type: multipart/form-data
    
    file: <audio_file>
    model_name: large-v3-turbo

**响应**：

    {
      "text": "转录的文本内容",
      "language": "zh",
      "history_id": 1
    }

#### 关键算法说明

* **模型选择**：支持Large V3（高精度）和Large V3 Turbo（快速）两种模型
* **语言检测**：Whisper自动检测音频语言，无需指定
* **离线处理**：完全离线运行，无需网络连接
* **历史记录**：所有识别记录自动保存，支持查询和删除

### 3. 3D模型管理模块

#### 功能描述

支持多格式3D模型上传、预览、管理，基于Three.js实现Web端3D渲染。

#### API接口

| 方法  | 路径  | 说明  | 认证  |
| --- | --- | --- | --- |
| `POST` | `/api/upload_model` | 上传3D模型 | 是   |
| `GET` | `/api/models` | 获取用户模型列表 | 是   |
| `POST` | `/api/models/{model_id}/set_active` | 设置激活模型 | 是   |
| `DELETE` | `/api/models/{model_id}` | 删除模型 | 是   |
| `GET` | `/api/models/active` | 获取当前激活模型 | 是   |

#### 调用示例

**上传模型**：

    POST /api/upload_model
    Authorization: Bearer <token>
    Content-Type: multipart/form-data
    
    file: <model_file>
    name: 我的模型名称（可选）

**支持格式**：`.glb`, `.gltf`, `.obj`, `.fbx`, `.stl`, `.ply`, `.dae`, `.3ds`

**大小限制**：最大 100MB

**响应**：

    {
      "message": "上传成功",
      "model": {
        "id": 1,
        "name": "我的模型名称",
        "filename": "model.glb",
        "file_path": "/models/100000/xxx.glb",
        "is_active": 0,
        "created_at": 1234567890
      }
    }

#### 关键算法说明

* **格式支持**：使用Three.js的多种Loader（GLTFLoader、OBJLoader等）
* **用户隔离**：每个用户的模型完全隔离，互不可见
* **交互控制**：基于OrbitControls实现旋转、缩放、平移
* **文件管理**：删除操作同时删除数据库记录和服务器文件

### 4. RAG问答模块

#### 功能描述

基于检索增强生成（RAG）技术实现心理健康问答，支持BM25、VSM、Boolean等检索算法。

#### API接口

| 方法  | 路径  | 说明  | 认证  |
| --- | --- | --- | --- |
| `POST` | `/api/qa/ask` | 提问  | 否   |
| `GET` | `/api/qa/health` | 健康检查 | 否   |
| `POST` | `/api/qa/reload` | 重新加载知识库 | 否   |

#### 调用示例

**提问**：

    POST /api/qa/ask
    Content-Type: application/json
    
    {
      "query": "我最近很焦虑",
      "mode": "rag",
      "top_k": 3
    }

**响应**：

    {
      "answer": "焦虑是一种常见的情绪反应...",
      "confidence": 0.85,
      "method": "rag",
      "sources": [
        {
          "content": "相关文档内容...",
          "score": 0.85,
          "doc_id": 1
        }
      ],
      "context_count": 3
    }

#### 关键算法说明

* **检索算法**：支持BM25（关键词检索）、VSM（向量空间模型）、Boolean（布尔检索）
* **知识库**：基于EmoLLM数据集，包含心理咨询对话数据
* **置信度计算**：使用归一化算法将检索分数映射到0-1范围
* **答案生成**：直接返回检索到的医生回答，无需生成模型

### 5. 用户资料模块

#### 功能描述

提供用户头像上传、个人信息管理等功能。

#### API接口

| 方法  | 路径  | 说明  | 认证  |
| --- | --- | --- | --- |
| `POST` | `/api/upload_avatar` | 上传头像 | 是   |
| `GET` | `/api/user/{username}` | 获取用户资料 | 否   |

#### 调用示例

**上传头像**：

    POST /api/upload_avatar
    Authorization: Bearer <token>
    Content-Type: multipart/form-data
    
    file: <image_file>

**支持格式**：`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`

**大小限制**：最大 5MB

* * *

## 测试指南

### 测试框架

项目使用 `pytest` 作为测试框架，支持单元测试和集成测试。

### 测试目录结构

    tests/
    ├── unit/              # 单元测试
    │   ├── test_auth.py
    │   ├── test_asr.py
    │   └── test_models.py
    ├── integration/       # 集成测试
    │   ├── test_api.py
    │   └── test_workflow.py
    └── fixtures/          # 测试数据
        ├── test_audio.wav
        └── test_model.glb

### 执行测试

#### 运行所有测试

    # 运行所有测试
    pytest
    
    # 运行并显示覆盖率
    pytest --cov=backend --cov-report=html
    
    # 运行特定测试文件
    pytest tests/unit/test_auth.py
    
    # 运行特定测试函数
    pytest tests/unit/test_auth.py::test_register_user

#### 测试覆盖率要求

| 模块  | 覆盖率要求 | 当前状态 |
| --- | --- | --- |
| **API路由** | ≥80% | ⏳ 待完善 |
| **业务逻辑** | ≥70% | ⏳ 待完善 |
| **工具函数** | ≥90% | ⏳ 待完善 |
| **整体覆盖率** | ≥75% | ⏳ 待完善 |

### 常见问题排查

#### 1. 测试数据库连接失败

**问题**：`sqlite3.OperationalError: unable to open database file`

**解决方案**：

    # 检查测试数据库路径
    export YUNI_ENV=testing
    
    # 确保测试数据库目录存在
    mkdir -p instance

#### 2. 测试文件上传失败

**问题**：`FileNotFoundError: test fixtures not found`

**解决方案**：

    # 创建测试数据目录
    mkdir -p tests/fixtures/data/uploads
    mkdir -p tests/fixtures/data/avatars

#### 3. JWT Token测试失败

**问题**：`jwt.exceptions.InvalidTokenError`

**解决方案**：

    # 设置测试环境JWT密钥
    export YUNI_JWT_SECRET="test-secret-key-for-testing-only"

* * *

## 部署流程

### 打包命令

#### 1. 依赖锁定

    # 生成精确版本依赖文件
    pip freeze > requirements-locked.txt

#### 2. 代码打包

    # 创建发布包（排除不必要文件）
    tar -czf yuni-release-1.0.0.tar.gz \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.git' \
        --exclude='venv' \
        --exclude='instance/*.db' \
        backend/ frontend/ config/ requirements*.txt run.py

### 部署架构

#### 单机部署

    graph LR
        A[用户] --> B[Nginx反向代理]
        B --> C[Gunicorn + Uvicorn]
        C --> D[FastAPI应用]
        D --> E[(SQLite数据库)]
        D --> F[文件系统]
    
        style B fill:#4A90E2
        style C fill:#50C878
        style D fill:#FF6B6B

**部署步骤**：

1. **安装依赖**：

    pip install -r requirements-locked.txt

2. **配置Nginx**：

    server {
        listen 80;
        server_name your-domain.com;
    
        location / {
            proxy_pass http://127.0.0.1:8003;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    
        location /static {
            alias /path/to/YuNi/frontend/static;
        }
    }

3. **启动服务**：

    gunicorn backend.main:app \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 127.0.0.1:8003 \
        --daemon

#### 集群部署（推荐生产环境）

    graph TB
        A[负载均衡器] --> B[应用服务器1]
        A --> C[应用服务器2]
        A --> D[应用服务器3]
    
        B --> E[(共享数据库)]
        C --> E
        D --> E
    
        B --> F[共享文件存储]
        C --> F
        D --> F
    
        style A fill:#4A90E2
        style E fill:#FFD93D
        style F fill:#50C878

**部署要求**：

* 使用PostgreSQL或MySQL替代SQLite
* 使用NFS或对象存储（如MinIO）存储文件
* 使用Redis存储Session（如需要）
* 配置负载均衡器（Nginx/HAProxy）

### 运维监控指标

#### 关键指标

| 指标  | 监控项 | 告警阈值 | 说明  |
| --- | --- | --- | --- |
| **CPU使用率** | 系统CPU | >80% | 持续5分钟 |
| **内存使用率** | 系统内存 | >85% | 持续5分钟 |
| **磁盘使用率** | 数据目录 | >90% | 立即告警 |
| **API响应时间** | P95延迟 | >2秒 | 持续10分钟 |
| **错误率** | 5xx错误 | >1% | 持续5分钟 |
| **并发连接数** | 活跃连接 | >1000 | 持续5分钟 |

#### 监控工具推荐

* **Prometheus** + **Grafana**：指标收集与可视化
* **ELK Stack**：日志收集与分析
* **Sentry**：错误追踪与告警

### 更新回滚方案

#### 更新流程

1. **备份数据**：

    # 备份数据库
    cp instance/users.db instance/users.db.backup.$(date +%Y%m%d)
    
    # 备份文件
    tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

2. **停止服务**：

    # 停止Gunicorn进程
    pkill -f gunicorn

3. **更新代码**：

    # 拉取最新代码
    git pull origin main
    
    # 更新依赖
    pip install -r requirements-locked.txt

4. **启动服务**：

    # 启动新版本
    gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8003

#### 回滚流程

1. **停止当前服务**：

    pkill -f gunicorn

2. **恢复代码**：

    # 回滚到上一个版本
    git checkout <previous-version-tag>
    
    # 恢复依赖（如需要）
    pip install -r requirements-locked.txt

3. **恢复数据**（如需要）：

    # 恢复数据库
    cp instance/users.db.backup.$(date +%Y%m%d) instance/users.db
    
    # 恢复文件
    tar -xzf data-backup-$(date +%Y%m%d).tar.gz

4. **启动服务**：

    gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8003

* * *

## 贡献规范

### 分支管理策略

项目采用 **Git Flow** 工作流：

    graph LR
        A[main] --> B[develop]
        B --> C[feature/xxx]
        B --> D[hotfix/xxx]
        B --> E[release/xxx]
    
        C --> B
        D --> A
        D --> B
        E --> A
        E --> B
    
        style A fill:#FF6B6B
        style B fill:#4A90E2
        style C fill:#50C878
        style D fill:#FFD93D
        style E fill:#9B59B6

**分支说明**：

| 分支  | 用途  | 合并目标 | 说明  |
| --- | --- | --- | --- |
| `main` | 生产环境 | -   | 仅接受release和hotfix合并 |
| `develop` | 开发环境 | `main` | 主要开发分支 |
| `feature/*` | 新功能 | `develop` | 功能开发分支 |
| `hotfix/*` | 紧急修复 | `main`, `develop` | 生产环境bug修复 |
| `release/*` | 版本发布 | `main`, `develop` | 版本发布准备 |

### 代码提交规范

#### 提交消息格式

采用 **Conventional Commits** 规范：

    <type>(<scope>): <subject>
    
    <body>
    
    <footer>

**类型（type）**：

| 类型  | 说明  | 示例  |
| --- | --- | --- |
| `feat` | 新功能 | `feat(auth): 添加JWT刷新Token功能` |
| `fix` | Bug修复 | `fix(asr): 修复音频文件格式验证问题` |
| `docs` | 文档更新 | `docs(readme): 更新API文档` |
| `style` | 代码格式 | `style(api): 统一代码缩进` |
| `refactor` | 代码重构 | `refactor(service): 重构ASR服务层` |
| `test` | 测试相关 | `test(auth): 添加用户注册单元测试` |
| `chore` | 构建/工具 | `chore(deps): 更新FastAPI版本` |

**示例**：

    feat(asr): 添加批量语音识别功能
    
    - 支持多文件同时上传
    - 添加进度查询接口
    - 优化错误处理逻辑
    
    Closes #123

#### 提交前检查

    # 代码格式化
    black backend/ --check
    
    # 代码检查
    flake8 backend/
    
    # 类型检查
    mypy backend/
    
    # 运行测试
    pytest

### PR审核流程

#### 1. 创建PR

* 从 `feature/*` 分支向 `develop` 分支创建PR
* PR标题遵循提交消息规范
* 填写PR描述，说明变更内容和测试情况

#### 2. 代码审查

**审查清单**：

* [x] 代码符合项目规范（PEP 8）
* [x] 添加了必要的测试用例
* [x] 更新了相关文档
* [x] 通过了CI/CD检查
* [x] 无安全漏洞

#### 3. 合并要求

* 至少1位维护者批准
* 所有CI检查通过
* 无冲突代码

### 版本发布规则

#### 版本号规范

采用 **语义化版本**（Semantic Versioning）：`MAJOR.MINOR.PATCH`

* **MAJOR**：不兼容的API修改
* **MINOR**：向后兼容的功能新增
* **PATCH**：向后兼容的问题修复

#### 发布流程

1. **创建release分支**：

    git checkout -b release/1.1.0 develop

2. **更新版本号**：

    # 更新版本号文件
    echo "1.1.0" > VERSION
    
    # 更新CHANGELOG.md

3. **合并到main和develop**：

    git checkout main
    git merge --no-ff release/1.1.0
    git tag -a v1.1.0 -m "Release version 1.1.0"
    
    git checkout develop
    git merge --no-ff release/1.1.0

4. **删除release分支**：

    git branch -d release/1.1.0

* * *

## 版权与许可

### 开源协议

本项目采用 **MIT License** 开源协议。

    MIT License
    
    Copyright (c) 2025 YuNi Team
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

### 团队信息

| 角色  | 职责  | 联系方式 |
| --- | --- | --- |
| **项目维护者** | 项目整体规划与维护 | maintainer@yuni.dev |
| **技术负责人** | 技术架构与代码审查 | tech-lead@yuni.dev |
| **安全团队** | 安全漏洞报告 | security@yuni.dev |

### 联系方式

* **项目主页**：https://github.com/your-org/YuNi
* **问题反馈**：https://github.com/your-org/YuNi/issues
* **讨论区**：https://github.com/your-org/YuNi/discussions
* **邮件联系**：contact@yuni.dev

* * *

## TODO

### 功能优化

* [ ] **数据库迁移**：从SQLite迁移到PostgreSQL/MySQL
* [ ] **文件存储**：集成对象存储（MinIO/S3）支持
* [ ] **缓存系统**：添加Redis缓存支持
* [ ] **消息队列**：集成Celery处理异步任务
* [ ] **WebSocket支持**：实时语音识别进度推送
* [ ] **批量处理**：支持批量音频文件上传和处理
* [ ] **多语言支持**：国际化（i18n）支持
* [ ] **移动端适配**：响应式设计优化

### 技术债务

* [ ] **测试覆盖**：提高单元测试和集成测试覆盖率至75%+
* [ ] **API文档**：完善Swagger/OpenAPI文档
* [ ] **日志系统**：统一日志格式和级别管理
* [ ] **配置管理**：实现YAML配置文件加载器
* [ ] **错误处理**：统一错误响应格式
* [ ] **性能优化**：数据库查询优化、缓存策略
* [ ] **安全加固**：添加速率限制、CSRF保护
* [ ] **监控告警**：集成Prometheus和Grafana

### 文档完善

* [ ] **架构文档**：详细的系统架构设计文档
* [ ] **API文档**：完整的API接口文档
* [ ] **部署文档**：详细的部署和运维文档
* [ ] **开发指南**：新开发者入门指南
* [ ] **故障排查**：常见问题解决方案文档

### 代码质量

* [ ] **类型提示**：完善所有函数的类型提示
* [ ] **代码审查**：建立代码审查流程和规范
* [ ] **CI/CD**：集成GitHub Actions自动化测试和部署
* [ ] **代码格式化**：统一代码格式化工具配置
* [ ] **依赖管理**：定期更新依赖版本，修复安全漏洞

* * *

## 相关文档

* [SECURITY.md](SECURITY.md) - 安全文档
* [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
* [REFACTORING_PLAN.md](REFACTORING_PLAN.md) - 重构计划
* [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - 重构执行总结

* * *

<div align="center">

**YuNi** - 让AI更简单，让3D更直观

Made with ❤️ by YuNi Team

</div>
