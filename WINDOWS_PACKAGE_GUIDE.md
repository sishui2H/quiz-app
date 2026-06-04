# Windows 下 Android APK 打包指南

## 方案一：使用 WSL2（推荐）

WSL2 是 Windows 内置的 Linux 子系统，是最简单的方案。

### 步骤

1. **启用 WSL2**
   
   以管理员身份打开 PowerShell，运行：
   ```powershell
   wsl --install
   ```
   安装完成后重启电脑。

2. **在 WSL2 中安装 Python 和依赖**
   
   打开 WSL2 Ubuntu 终端：
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip openjdk-11-jdk
   pip install buildozer
   ```

3. **复制项目到 WSL2**
   
   ```bash
   cd ~
   cp -r /mnt/d/1/ai/quiz_app_kivy .
   cd quiz_app_kivy
   ```

4. **开始打包**
   
   ```bash
   buildozer android debug
   ```
   
   首次打包会下载 SDK/NDK，需要较长时间。

5. **获取 APK**
   
   打包完成后，APK 在 `~/quiz_app_kivy/bin/` 目录。
   复制回 Windows：
   ```bash
   cp bin/*.apk /mnt/d/1/ai/
   ```

---

## 方案二：使用在线打包服务（最简单）

使用 Google Colab 或 GitHub Actions 进行云端打包。

### Google Colab 打包

1. 打开 [Google Colab](https://colab.research.google.com/)
2. 创建新笔记本
3. 运行以下代码：

```python
# 安装依赖
!pip install buildozer

# 上传项目（或从 GitHub 克隆）
# 可以在左侧文件面板上传 quiz_app_kivy 文件夹

# 打包
!cd quiz_app_kivy && buildozer android debug
```

---

## 方案三：使用 Docker（适合有基础的用户）

1. 安装 Docker Desktop
2. 使用现成的 Kivy 打包镜像：

```powershell
docker run --rm -v ${PWD}:/home/user/hostcwd kivy/buildozer android debug
```

---

## 方案四：使用 Python-for-android 配合虚拟机

安装 VirtualBox + Ubuntu 虚拟机，在虚拟机中打包。

---

## 对比

| 方案 | 难度 | 速度 | 推荐度 |
|------|------|------|--------|
| WSL2 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Colab | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Docker | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 虚拟机 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

---

## 先测试本地版本！

在尝试打包 APK 之前，先确保 Kivy 版本能在 Windows 本地正常运行：

```powershell
cd d:\1\ai\quiz_app_kivy
pip install -r requirements.txt
python main.py
```

如果能正常运行，再进行 APK 打包。
