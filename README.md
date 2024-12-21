## v0.1.0 - 阿里云盘API初始发布

阿里云盘API的Python实现，提供简单易用的命令行工具，支持文件上传、下载、搜索等功能。

### 主要功能

- 文件操作
  - ✅ 文件上传（支持文件夹）
  - ✅ 文件下载
  - ✅ 文件列表查询
  - ✅ 文件搜索
  
- 使用体验
  - ✅ 秒传支持
  - ✅ 进度条显示
  - ✅ token自动刷新
  - ✅ 中文路径支持
  - ✅ 多级目录支持

### 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/luoluoluo22/aliyundrive-api.git
cd aliyundrive-api
pip install -e .
```

2. 初始化配置：
```bash
aliyundrive --init
```

按照以下步骤获取token：
1. 用浏览器打开阿里云盘官网 https://www.aliyundrive.com/
2. 登录您的账号
3. 按F12打开开发者工具
4. 切换到"应用程序/Application"标签
5. 在左侧找到"本地存储空间/Local Storage" -> "https://www.aliyundrive.com"
6. 找到"token"项并复制其值
7. 粘贴到命令行（粘贴完成后按两次回车）
![参考图片](./doc/get_token.png)

配置文件会自动保存在：
- Windows: `C:\Users\用户名\.aliyundrive\config.ini`
- Linux/Mac: `~/.aliyundrive\config.ini`

如需重新配置，可以：
```bash
# 查看当前配置位置
aliyundrive --debug

# 重新配置
aliyundrive --init
```

3. 开始使用：
```bash
# 列出文件
aliyundrive list

# 上传文件
aliyundrive upload ./test.txt

# 下载文件
aliyundrive download test.txt
```

### 详细使用说明

1. 文件列表
```bash
# 列出根目录
aliyundrive list

# 列出指定文件夹
aliyundrive list "我的文档"

# 列出子文件夹
aliyundrive list "我的文档/子文件夹"
```

2. 文件上传
```bash
# 上传到根目录
aliyundrive upload ./test.txt

# 上传到指定目录
aliyundrive upload ./test.txt "我的文档"

# 上传整个文件夹
aliyundrive upload ./test_folder "我的文档/子文件夹"
```

3. 文件下载
```bash
# 下载到当前目录
aliyundrive download test.txt

# 下载指定路径的文件
aliyundrive download "我的文档/test.txt"

# 下载到指定目录
aliyundrive download test.txt ./downloads/
```

4. 文件搜索
```bash
# 搜索文件
aliyundrive search test.txt

# 搜索文件夹
aliyundrive search 文档
```

### 注意事项

1. 文件名包含空格时，需要使用引号：
```bash
aliyundrive list "我的 文档"
aliyundrive download "测试 文件.txt"
```

2. 路径分隔符使用正斜杠（/）：
```bash
aliyundrive list "文档/子文件夹"
```

3. 配置文件包含敏感信息，请妥善保管

### 更新日志

- 初始版本发布
- 实现基本的文件操作功能
- 添加命令行界面
- 支持配置文件管理

### 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

### 声明

本项目仅供学习研究使用，请勿用于非法用途。

