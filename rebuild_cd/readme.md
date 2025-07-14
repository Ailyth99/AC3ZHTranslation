# 镜像重建工具 (rebuild_cd) 使用指南

本工具集用于为游戏光盘镜像重建文件，主要包含对 `BPB` 文件的重新打包，并生成新的 `.bin` 格式光盘镜像。

本指南以 `CD1` 的重建为例，重建 `CD2` 的流程相同，只需修改相应的文件路径即可。

> **注意**：`CD1` 和 `CD2` 的 `ACE.BPB`和 `ACE.BPH`文件内容一致，可以复用。

## 目录结构

```
rebuild_cd/
├── ace.bph               # BPB 文件头，用于重建
├── CD1_build.bat         # [核心] CD1 一键重建脚本
│
├─ cd/                     # 存放镜像文件
│  ├─ orig/                # 存放原版镜像
│  │  ├── cd1.bin
│  │  └── cd1.cue
│  └─ (此目录)              # 新生成的镜像 cd1.bin 会保存在这里
│
├─ cd1_build/              # CD1 重建所需文件
│  ├─ BPB/                 # 存放解包及修改后的 BPB 子文件
│  │  ├── 0000
│  │  ├── 0005
│  │  └── ...
│  └─ ACE.BPH
│
└─ tools/                  # 依赖的工具
   ├── ac3_repack.exe
   └── psx-mode2.exe
```

## 使用方法

**准备工作：**

1.  **放置原版镜像**：将 **原版 `cd1.bin` 和 `cd1.cue`** 文件放入 `cd/orig/` 目录。
2.  **准备 BPB 子文件**：
    *   使用 `BPB_Unpack_Repack` 工具（详情请参考其说明文档）解包原汉化版镜像中的 `ACE.BPB` 文件。
    *   将解包得到的 **所有子文件**（包括你修改过的文件）放入 `cd1_build/BPB/` 目录。

**执行重建：**

1.  回到根目录，双击运行 **`CD1_build.bat`** 批处理文件。
2.  脚本会自动执行所有步骤，等待其运行完毕即可。
3.  成功后，新生成的 `cd1.bin` 镜像文件会出现在 `cd/` 目录下，并覆盖已有的同名文件。

## `CD1_build.bat` 工作流程详解

该脚本将自动完成以下操作，其内部代码及注释如下：

```batch
@echo off 

REM --- 1. 清理环境：删除上次生成的文件，确保全新构建 ---
echo Deleting old CD1 BPB and BPH files...
del ACE.BPB
del ACE.BPH
echo.

REM --- 2. 重新打包：将修改后的子文件打包成新的 BPB 文件 ---
echo -----------------------------
echo Repacking CD1 BPB file...
echo -----------------------------
copy cd1_build\ace.bph ace.bph                       REM 复制一个标准的文件头
tools\ac3_repack ace.bpb ace.bph cd1_build\bpb       REM 使用 ac3_repack 工具打包
echo.

REM --- 3. 准备基础镜像：复制一份原版镜像用于修改 ---
del cd\cd1.bin                                        REM 删除上一次生成的镜像
copy cd\orig\cd1.bin cd\cd1.bin                       REM 复制原版镜像作为底本
echo.

REM --- 4. 注入文件：将新生成的文件替换进镜像中 ---
echo -----------------------------
echo Rebuilding CD1 image...
echo -----------------------------
tools\psx-mode2 cd\cd1.bin /ACE.BPB ACE.BPB           REM 将新的 BPB 文件注入镜像
tools\psx-mode2 cd\cd1.bin /ACE.BPH ACE.BPH           REM 将新的 BPH 文件注入镜像
echo.

echo -----------------------------
echo Build complete!
echo -----------------------------
echo.
echo Press any key to exit...
pause > nul
```