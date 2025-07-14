## 1. 生成补丁文件

使用的是xdelta补丁工具。

**命令格式：**
```shell
patcher.exe -e -s <原版镜像路径> <新镜像路径> <补丁名称>
```

**示例：**
```shell
patcher.exe -e -s "C:\AC3ES\原版CD\JA\cd1.bin" "C:\AC3ES\repack_toolkit\cd\cd1.bin" ja1.ac3
patcher.exe -e -s "C:\AC3ES\原版CD\JA\cd2.bin" "C:\AC3ES\CD2\REPACK_CD2\cd2.bin" ja2.ac3
patcher.exe -e -s "C:\AC3ES\原版CD\JP\jpcd1.bin" "C:\AC3ES\repack_toolkit\cd\cd1.bin" jp1.ac3
patcher.exe -e -s "C:\AC3ES\原版CD\JP\jpcd2.bin" "C:\AC3ES\CD2\REPACK_CD2\cd2.bin" jp2.ac3
```

## 2. 构建自动打补丁工具（请确保电脑拥有Go语言环境）

1.  打开 `patcher.go` 文件，修改其中 `patcher.exe` 的路径以及补丁文件（默认为 `.ac3` 扩展名）的路径。
2.  使用以下命令编译生成 `自动补丁工具`，建议命名为`ac3_patcher.exe`：
    ```shell
    go build .
    ```

## 支持的镜像版本

本工具支持以下经过验证的 Redump.org 镜像版本（通过文件大小判断）：

-   http://redump.org/disc/3175/
-   http://redump.org/disc/3176/
-   http://redump.org/disc/582/
-   http://redump.org/disc/584/

## 自动补丁工具使用说明
以下内容可以附带到补丁发布里面。

1.把游戏光盘的镜像文件（BIN格式）复制到此文件夹，支持日版和日语亚洲版的镜像：
Ace Combat 3 - Electrosphere (Japan) (Disc 1)-日版CD1，容量 716240448 字节
Ace Combat 3 - Electrosphere (Japan) (Disc 2)-日版CD2，容量 723766848 字节
Ace Combat 3 - Electrosphere (Japan, Asia) (Disc 1) (Rev 1)-日亚版CD1，容量 716287488 字节
Ace Combat 3 - Electrosphere (Japan, Asia) (Disc 2) (Rev 1)-日亚版CD2，容量 723813888 字节

2.双击ac3_patcher.exe，会自动识别是否为支持的镜像，如果是，则开始打补丁，并生成一个新的bin文件和cue文件。
3.汉化版本支持读取原来日版，日亚版存档。但日版和日亚版不能互相换碟，所以不要把日版和日亚版的镜像混用。
4.某些场合可能需要cue文件配合镜像一起使用，使用生成的cue即可。