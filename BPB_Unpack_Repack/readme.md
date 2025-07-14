# BPB 文件处理工具 (ac3es_tools.exe) 使用指南

本工具用于打包和拆包游戏中的 `BPB` 格式资源文件。

## 命令参考 

### 1. 打包 BPB 文件 (`--pack`)

此命令将指定的子文件目录打包成一个新的 `ACE.BPB` 和 `ACE.BPH` 文件。

**语法格式：**
```shell
ac3es_tools.exe bpb --pack <包含子文件的目录路径>
```

**使用示例：**
```shell
ac3es_tools.exe bpb --pack "F:\PSXISO\AC3\CD2\REPACK_CD2\BPB"
```

---

### 2. 拆包 BPB 文件 (`-u`)

此命令根据现有的 `ACE.BPB` 和 `ACE.BPH` 文件，将其内容解包为子文件，以便进行修改。

**语法格式：**
```shell
ac3es_tools.exe bpb --bpb <ACE.BPB文件路径> --bph <ACE.BPH文件路径> -u <指定输出子文件的目录>
```

**使用示例：**
```shell
ac3es_tools.exe bpb --bpb "REPACK_CD2/ACE.BPB" --bph "REPACK_CD2/ACE.BPH" -u "BPB"
```

---

## 推荐工作流程 

对于修改游戏内资源，推荐遵循以下步骤：

1.  **拆包 BPB**
    使用 **拆包** 命令将原始的 `ACE.BPB` 文件解构成包含多个子文件的目录。

2.  **解压子文件 (可选)**
    运行辅助脚本 **`批量解压ulz.bat`**，可以深入到各个子文件夹中，对所有 `.ulz` 格式的压缩文件进行批量解压，暴露出可编辑的资源。

3.  **整理贴图文件 (可选)**
    运行辅助脚本 **`移动TIM并重新命名movetim.bat`**，可以将所有 `.tim` 格式的贴图文件从复杂的子目录结构中提取出来，统一存放到一个文件夹。文件会根据其原始路径重命名（例如 `0005_0011_0011_001.tim`），方便了资源的预览、查找和管理。

4.  **修改文件**
    现在你可以对解压和整理后的文件进行你想要的修改。

5.  **打包 BPB**
    修改完成后，使用AC3TIMSWALLOW对TIM进行ULZ压缩，最后放入重建文件文件夹（rebuild目录里面），进行BPB重建。