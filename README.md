# 毛概答题练习系统 - Android/Kivy 版本

基于 Kivy 框架的跨平台答题练习应用，可运行在 Android、Windows、Linux、macOS 上。

## 项目结构

```
quiz_app_kivy/
├── main.py              # Kivy 主程序
├── model/               # 数据模型（复用自原项目）
│   └── question.py
├── controller/          # 控制逻辑（复用自原项目）
│   └── quiz_controller.py
├── utils/               # 工具类（复用自原项目，已适配）
│   └── docx_parser.py
├── buildozer.spec       # Android 打包配置
├── requirements.txt     # Python 依赖
├── 给学生的练习题（单选300）.docx
├── 给学生的练习题（多选200）.docx
└── 给学生的练习题（判断100）.docx
```

## 本地开发运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python main.py
```

## Android 打包

### 前置要求
- Linux 或 macOS 环境（或 WSL2）
- 安装 Java JDK 8+
- 安装 Android SDK（可选，buildozer 会自动下载）

### 安装 Buildozer

```bash
pip install buildozer
```

### 打包 APK

```bash
cd quiz_app_kivy
buildozer android debug deploy run
```

只打包不安装运行：
```bash
buildozer android debug
```

生成的 APK 文件在 `bin/` 目录下。

### 清理构建

```bash
buildozer android clean
```

## 功能特性

- ✅ 支持单选题、多选题、判断题
- ✅ 自动评分和正确率显示
- ✅ 答题计时
- ✅ 题目标记功能
- ✅ 移动端适配界面
