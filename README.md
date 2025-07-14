## ACE COMBAT 3: ELECTROSPHERE 中文化项目

本项目基于《皇牌空战3：电脑空间》日版游戏进行汉化翻译。

- [项目主页](https://ailyth99.github.io/ac3es/)

![游戏预览](https://cdn-fusion.imgcdn.store/i/2024/234ecbef0a1057f1.png)

## 汉化内容

- ✈️ **游戏对话与剧情文本**
- 🔍 **"搜索引擎"词条**
- 📡 **战场无线电通讯**
- 🎬 **即时动画字幕**
- 🎮 **游戏菜单界面** (部分保留英文以维持原版风格)

## 补丁下载

前往 [**GitHub Releases**](https://github.com/Ailyth99/AC3ZHTranslation/releases) 页面下载最新补丁。

> **提示：**
> 具体使用方法请参考压缩包内的说明文件。

---

## 🛠️ 修改此汉化版本

如果您希望在当前汉化版的基础上进行二次修改并发布新版本，请遵循以下原则。

### 核心原则
- **开源协议**: 您的修改版必须遵守本项目的 [GPL-3.0](https://github.com/Ailyth99/AC3ZHTranslation/blob/main/LICENSE) 协议，并同样以 GPL-3.0 协议开源。
- **作者署名**: 您可以署上自己的名字，但**必须保留**原始汉化项目作者的署名。

### 整体修改流程
- **修改流程**: 修改游戏内容的核心流程分为三步：**解包 → 修改 → 重新打包**。
- **必备环境**: 请务必确保PC安装有Python和Java环境，以及可选的golang环境。

---

### 步骤一：完全解包游戏资源

本步骤的目的是从游戏镜像中提取出所有可编辑的素材，主要是图像文件。

#### 1. 提取核心资源文件

使用 `UltraISO` 等镜像管理工具，从游戏镜像文件 (`.bin` 格式) 中提取 `ACE.BPB` 和 `ACE.BPH` 这两个文件。所有游戏素材都被封装在 `ACE.BPB` 这个大封包里。

#### 2. 拆解 BPB 封包

使用 `BPB_Unpack_Repack` 目录下的 `ac3es_tools.exe` 工具来拆解 `ACE.BPB`。

> **语法格式：**
> ```shell
> ac3es_tools.exe bpb --bpb <ACE.BPB文件路径> --bph <ACE.BPH文件路径> -u <输出目录>
> ```
> **使用示例：**
> ```shell
> ac3es_tools.exe bpb --bpb "REPACK_CD2/ACE.BPB" --bph "REPACK_CD2/ACE.BPH" -u "BPB"
> ```
> 执行后，所有子文件会被解包到 `BPB` 文件夹中。

 **⚠️ 重要：创建备份**
 操作完成后，请将 `BPB` 文件夹**复制三份**：
 1.  一份作为**原始备份**，防止后续操作失误。
 2.  一份复制到 `rebuild_cd/cd1_build` 目录，用于最终重新打包。
 3.  一份用于接下来的深度解包和修改。

#### 3. 批量解压 ULZ 文件

运行辅助脚本 `批量解压ulz.bat`。按提示输入上一步解包出的 `BPB` 目录路径。
此脚本会自动解压目录中所有的 `.ulz` 压缩文件。解压后通常会得到 `.tim` (图像) 或 `.dat` (封包) 文件。

#### 4. 批量拆分 DAT 封包

上一步解压出的部分 `.dat` 文件是二级封包，需要进一步拆分。
运行 `dat_splitter.py` 脚本，按提示输入 `BPB` 目录路径。脚本会自动拆分其中的 `.dat` 文件，暴露出最终的可编辑素材。

> **拆包产物说明：**
> 拆分每个 `.dat` 文件后，会生成一个 `filelist.txt`。这个文件记录了其包含的所有子文件的信息，在后续重新打包时将作为索引使用。

#### 5. 整理贴图文件

运行辅助脚本 `移动TIM并重新命名movetim.bat`。
此脚本会将所有 `.tim` 贴图文件从深层子目录中提取出来，统一存放到一个新文件夹，并根据其原始路径重命名 (例如 `0005_0011_0011_001.tim`)。这样做便于集中预览和快速定位需要修改的图像。但修改还是要修改BPB目录里面的，这里只是集中TIM做一个统一预览，方便定位。

---

### 步骤二：修改图像资源 (核心汉化工作)

**核心机制：** 游戏中的所有文本（对话、菜单、字幕等）都是以**TIM图像**的形式存在的。因此，汉化工作本质上就是**替换这些图像**。原始文本放在了**Script**目录里面。

#### 1. 图像类型与工具

- **文件格式**: 所有需要修改的都是 `.tim` 格式的贴图文件。
- **主要工具**:
    - `AC3TimSwallow`: 用于预览、导出 `.tim` 文件，查询关键信息（如色板、显存坐标），以及最终合成新 `.tim` 文件。
    - `AC3-Text-Editor`: 用于快速生成带游戏字体的**对话文本**图像。
    - `OPTPix iMageStudio for PS2`: 专业的PS2图像工具，用于处理**菜单、UI**等复杂图像，可手动调整CLUT(色板/调色板)。(注：此为商业软件，请自行获取)
    - `Photoshop` 或其他图像编辑软件。

#### 2. 工作流①：修改剧情对话、CG字幕等文本图像

这类图像结构相对简单，可以使用半自动化工具完成。

1.  **启动工具**:
    - 打开 `AC3_Text_Editor` 目录，运行 `java -jar AC3-Text-Editor.jar`。
    - 打开 `AC3TimSwallow` 目录，运行 `main.py`。

2.  **获取模板**:
    - 使用 `AC3TimSwallow` 打开一个原始的对话 `.tim` 文件。
    - 右键点击图像，导出为 `.bmp` 格式。这张 `.bmp` 可以作为模板，保留了正确的尺寸和背景色（如乳白色、蓝色、黑色等）。
    - 工具可以查询同一个图，不同调色板对应的图像。
      ![](https://pic1.imgdb.cn/item/68751e8e58cb8da5c8adc2c5.webp)
3.  **生成新文本图像**:
    - 在 `AC3-Text-Editor` 中，选择上一步导出的 `.bmp` 作为底图。
    - 在文本框中输入翻译好的中文。选择 `BIG FONT` 以匹配游戏中的主要字体。
    - 点击生成，得到一张新的 `.bmp` 图像，注意命名为新的名字方便区分。
    ![](https://pic1.imgdb.cn/item/68751dd058cb8da5c8adc29b.png)
4.  **处理色板 (CLUT)**:
    > **关键概念：调色板/色板 (CLUT)**
    > `.tim` 图像使用一个或两个色板来显示颜色。
    > - **单色板**: 图像只有一种显示效果。
    > - **双色板**: 一张 `.tim` 包含两种画面，通过切换色板显示。
    > **必须严格匹配原始 `.tim` 的色板数量，否则游戏会出错！**

    - **如果原始 `.tim` 是单色板**: 直接使用上一步生成的 `.bmp` 即可。
    - **如果原始 `.tim` 是双色板**: 你需要生成两张 `.bmp`，分别对应两个色板的显示效果。例如，命名为 `1.bmp` 和 `2.bmp`。
    ![](https://pic1.imgdb.cn/item/68751cf258cb8da5c8adc237.png)
    ![](https://pic1.imgdb.cn/item/68751cf258cb8da5c8adc236.png)
5.  **合成为新 `.tim` 文件**:
    - 在 `AC3TimSwallow` 中，点击“BMP转TIM”按钮。
    - **单色板**: 选择“单层TIM”，导入你的 `.bmp` 和**原始 `.tim` 文件** (用于获取重要的显存坐标)。
    - **双色板**: 选择“双层TIM”，**按顺序**导入 `1.bmp` 和 `2.bmp`，再选择**原始 `.tim` 文件**。
    - 点击“开始处理”即可生成新的 `.tim` 文件。
    <br>![](https://pic1.imgdb.cn/item/68751cf158cb8da5c8adc235.png)
6.  **压缩与替换**:
    - 你可以在合成时直接勾选“压缩为ULZ”，一步到位生成最终的 `.ulz` 替换文件。
    - 也可以先生成 `.tim`，在 `AC3TimSwallow` 中预览确认效果无误后，再使用“ULZ压缩”功能手动压缩。
    - 将生成的新 `.ulz` 文件，放到 `rebuild_cd/cd1_build/BPB...` 对应目录下，替换原文件。

#### 3. 工作流②：修改菜单、任务内对话等复杂图像

这类图像需要更精细的手动处理。

1.  **导出与编辑**:
    - 使用 `AC3TimSwallow` 将原始 `.tim` 导出为 `.bmp`。
    - 使用 `Photoshop` 等工具打开 `.bmp` 进行编辑。
    > **清晰小字体技巧**: 对于任务内对话（黑底白字/绿色的无线电对话），为追求清晰度，可在 Photoshop 中使用像素字体，并关闭“字体边缘抗锯齿”功能，选择“[缝合像素（FUSION PIXEL）](https://github.com/TakWolf/fusion-pixel-font)”字体。

2.  **颜色量化 (Color Reduction)**:
    - 将编辑好的图像导入 `OPTPix iMageStudio for PS2`。
    - **必须**将新图像的颜色数减至与**原始 `.tim` 文件**一致。
        - 如果原始是 16 色 (4bpp)，就减到 16 色。
        - 如果原始是 256 色 (8bpp)，就减到 256 色。<br>![](https://pic1.imgdb.cn/item/68751f8958cb8da5c8adc30e.png)
    - 对于双色板图像，可能需要手动将原始 `.tim` 的两个色板分别复制到你制作的两张新图上，以确保颜色完全匹配。单色版则无需这样，直接使用减色后得到的新色板数据即可。

3.  **单色版图可以直接保存为新 `.tim`**:
    - 在 `OPTPix` 中，另存为 `.tim` 格式。<br>![](https://pic1.imgdb.cn/item/68751fde58cb8da5c8adc32a.png)
    - **务必**在保存时手动输入正确的显存坐标 (可以用 `AC3TimSwallow` 查询原始 `.tim` 的坐标)。
    - 注意，双色板任务对话图必须减色后导出BMP，再使用`AC3TimSwallow` 合并生成新TIM。		
---

### 步骤三：重新打包游戏

完成所有文件修改后，需要执行与解包相反的流程，生成新的游戏镜像。所有待打包的新文件都应已放置在 `rebuild_cd` 目录的对应位置。

1.  **打包 `.tim` 到 `.dat` (如需要)**:
    - 如果你修改的是从 `.dat` 中拆分出的 `.tim` (如菜单图像)，需要先将它们重新打包回 `.dat`。
    - 使用 `AC3TimSwallow` 的“封包BIN/DAT”功能，加载之前拆包时生成的 `filelist.txt`，它会引导工具生成新的 `.dat` 文件。

2.  **打包 `.tim` 到 `.ulz` (如需要)**:
    - 如果你修改的是直接封装在 `.ulz` 里的对话 `.tim`，在步骤二中应该已经生成了新的 `.ulz` 文件。
    - 也有部分上一条提到的dat文件需要压缩为ulz，请使用`AC3TimSwallow` 进行ulz压缩。

3.  **将新文件放入重建目录**:
    - 将所有新生成的 `.ulz` 和 `.dat` 文件，覆盖到 `rebuild_cd/cd1_build/BPB...` 目录中的同名旧文件。

4.  **生成新镜像**:
    - 最后，参考 `rebuild_cd` 目录内的说明文档，运行批处理脚本，即可将整个目录重新打包成 `ACE.BPB` 和 `ACE.BPH`后，自动生成可供测试的新游戏镜像BIN格式。

---

### 步骤四：制作发布补丁

如果你想将你的修改版分享给他人，可以制作一个补丁。

- **方法一 (推荐)**: 直接使用 `xdelta` 等通用补丁制作工具，对比原始游戏镜像和你的修改版镜像，生成一个 `.xdelta` 补丁文件。并提供 `xdelta` 的使用说明。
- **方法二 (高级)**: 参考 `Patcher` 目录里的说明文档，可以制作一个自定义的补丁程序，它可以自动判断镜像，并自动打补丁（需要使用go语音编译环境）。


### 补充
你可以可以看这个文章得到一些信息：[皇牌空战3 汉化说明 - 基本实现方式](https://www.bilibili.com/opus/997381746516295686)

## 致谢Acknowledgments
*  [AC3-Layer-Merger](https://github.com/DashmanGC/AC3-Layer-Merger)
*  [ac3es-tools](https://github.com/loadwordteam/ac3es-tools)
*  [tim2bmp](https://github.com/simias/psxsdk/blob/c68f12c05b0da85b44c3d7d3fa81236cbb9a9d7c/tools/tim2bmp.c#L197)
*  [FUSION PIXEL](https://github.com/TakWolf/fusion-pixel-font)
*  [寒蝉全圆体](https://github.com/Warren2060/ChillRound)
*  [PSX-MODE2](https://www.romhacking.net/utilities/848/)
