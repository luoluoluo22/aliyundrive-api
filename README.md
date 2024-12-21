# 阿里云盘API

阿里云盘API的Python实现，提供简单易用的命令行工具，支持文件上传、下载、搜索等功能。本项目目前没有实现登录的接口，因此需要用户自行登录之后获取登录凭证。

## 功能特点

- 支持文件上传（包括文件夹）
- 支持文件下载（支持路径方式）
- 支持文件列表查询（支持目录层级）
- 支持文件搜索（支持模糊匹配）
- 支持秒传
- 支持进度条显示
- 支持 token 自动刷新
- 支持中文路径
- 支持多级目录

## 环境要求

- Python >= 3.6
- requests >= 2.25.1
- tqdm >= 4.61.0

## 安装方法

### 从源码安装

```bash
git clone https://github.com/Litt1eQ/aliyundrive-api.git
cd aliyundrive-api
pip install -e .
```

### 从 PyPI 安装（即将支持）

```bash
pip install aliyundrive-api
```

## 配置文件

在项目根目录创建 `config.ini` 文件，内容如下:

```ini
[account]
access_token = AccessToken
refresh_token = RefreshToken
drive_id = YourDriveId
```

参数获取方法：

1. 打开阿里云盘网页版 (https://www.aliyundrive.com/)
2. 按 F12 打开开发者工具
3. 找到 Application -> Local Storage -> token
4. 复制相应的 token 值：
   - `access_token`: token 中的 "access_token" 字段
   - `refresh_token`: token 中的 "refresh_token" 字段
   - `drive_id`: token 中的 "default_drive_id" 字段（可选）

注意：拥有 access_token 和 refresh_token 就可以控制整个网盘，请务必妥善保管，**不要泄露**！

## 使用方法

### 命令行使用

#### 1. 列出文件

```bash
# 列出根目录文件
aliyundrive list

# 列出指定文件夹内容
aliyundrive list 充电
aliyundrive list "我的文档"

# 列出子文件夹内容
aliyundrive list 充电/子文件夹
```

#### 2. 下载文件

```bash
# 下载根目录的文件
aliyundrive download test.txt

# 下载指定文件夹中的文件
aliyundrive download 充电/file.txt

# 下载到指定目录
aliyundrive download 充电/file.txt ./downloads/
```

#### 3. 上传文件

```bash
# 上传文件到根目录
aliyundrive upload ./test.txt

# 上传到指定目录
aliyundrive upload ./test.txt 充电

# 上传整个文件夹
aliyundrive upload ./test_folder 充电/子文件夹
```

#### 4. 搜索文件

```bash
# 搜索文件
aliyundrive search test.txt

# 搜索文件夹
aliyundrive search 充电

# 模糊搜索
aliyundrive search txt
```

### 作为模块使用

```python
from aliyundrive import AliyunDriveApi

# 初始化API
api = AliyunDriveApi()

# 列出文件
files = api.list_files()  # 根目录
folder = api.get_file_by_path("充电")  # 获取文件夹信息
if folder:
    files = api.list_files(folder['file_id'])  # 列出文件夹内容

# 下载文件
api.download_by_path("充电/file.txt")  # 按路径下载
api.download_by_path("充电/file.txt", "./downloads/")  # 指定保存位置

# 上传文件
api.upload_file('./test.txt')  # 上传到根目录
api.upload_file('./test.txt', '充电')  # 上传到指定目录
api.upload_folders('./test_folder', '充电')  # 上传整个文件夹

# 搜索文件
files = api.search_file('test.txt')  # 搜索文件
```

## 开发计划

- [ ] 支持分片上传大文件
- [ ] 支持文件夹下载
- [ ] 支持文件分享
- [ ] 支持更多文件操作（移动、复制、删除等）
- [ ] 支持更多搜索选项
- [ ] 添加单元测试
- [ ] 发布到 PyPI

## 常见问题

1. **文件名包含空格？**
   ```bash
   # 使用引号括起来
   aliyundrive list "我的 文档"
   aliyundrive download "我的 文档/测试 文件.txt"
   ```

2. **找不到文件？**
   ```bash
   # 1. 先列出目录内容
   aliyundrive list
   
   # 2. 或者使用搜索
   aliyundrive search 关键词
   ```

3. **下载失败？**
   ```bash
   # 1. 确保路径正确，区分大小写
   # 2. 使用 list 命令查看完整路径
   # 3. 如果路径包含特殊字符，使用引号括起来
   ```

## 贡献代码

1. Fork 本仓库
2. 创建新的分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 声明

> 如有侵权，联系删除
>
> 本项目仅供研究学习使用，请勿将本项目用于非法用途，违反者后果自负

