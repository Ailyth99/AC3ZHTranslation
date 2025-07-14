## 1. 生成补丁文件

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

## 2. 构建补丁工具

1.  打开 `patcher.go` 文件，修改其中 `patcher.exe` 的路径以及补丁文件（默认为 `.ac3` 扩展名）的路径。
2.  使用以下命令编译生成 `patcher.exe`：
    ```shell
    go build .
    ```

## 支持的镜像版本

本工具支持以下经过验证的 Redump.org 镜像版本（通过文件大小判断）：

-   http://redump.org/disc/3175/
-   http://redump.org/disc/3176/
-   http://redump.org/disc/582/
-   http://redump.org/disc/584/