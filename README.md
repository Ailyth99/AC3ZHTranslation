## ACE COMBAT 3: ELECTROSPHERE 中文化项目

基于《皇牌空战3：电脑空间》日版游戏进行翻译。

- [项目主页](https://ailyth99.github.io/ac3es/)

## 翻译内容

- ✈️ 游戏对话与剧情文本
- 🔍 "搜索引擎"词条
- 📡 战场无线电通讯
- 🎬 即时动画字幕
- 🎮 游戏菜单界面（保留部分英文）

![预览图](https://cdn-fusion.imgcdn.store/i/2024/234ecbef0a1057f1.png)

## 补丁
下载 [release](https://github.com/Ailyth99/AC3ZHTranslation/releases)
- 使用方法见下载的文件包含的说明。

## 修改
你如果对翻译结果不满意，想继续调整并推出修订后的版本，可以对本汉化版本进行修改。
但请一定遵守本项目的开源协议[GPL3.0](https://github.com/Ailyth99/AC3ZHTranslation/blob/main/LICENSE)，完成自己的项目后进行开源（依然使用GPL3.0协议），
你当然可以署上自己的名字，但别忘了保留原始作者署名。

## 修改流程

### 第一步.对游戏进行充分解包
首先使用UltraISO等常规镜像管理工具，提取镜像（BIN格式）里面的文件。游戏需要汉化的素材都放在ACE.BPB里面，另外还需要一个索引文件ACE.BPH。
找到目录BPB_Unpack_Repack里面的工具：ac3es_tools.exe，
本工具据现有的 `ACE.BPB` 和 `ACE.BPH` 文件，将其内容解包为子文件，以便进行修改。
**语法格式：**
```shell
ac3es_tools.exe bpb --bpb <ACE.BPB文件路径> --bph <ACE.BPH文件路径> -u <指定输出子文件的目录>
```
**使用示例：**
```shell
ac3es_tools.exe bpb --bpb "REPACK_CD2/ACE.BPB" --bph "REPACK_CD2/ACE.BPH" -u "BPB"
```
以上命令会把BPB所有文件拆分到一个叫做BPB的文件夹里面，请备份一份BPB拆分数据。

