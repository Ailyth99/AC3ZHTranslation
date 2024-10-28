package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	// 欢迎词
	welcomeMessage := `
    ___    ______ ______   ______ ____   __  ___ ____   ___   ______   _____
   /   |  / ____// ____/  / ____// __ \ /  |/  // __ ) /   | /_  __/  |__  /
  / /| | / /    / __/    / /    / / / // /|_/ // __  |/ /| |  / /      /_ <
 / ___ |/ /___ / /___   / /___ / /_/ // /  / // /_/ // ___ | / /     ___/ /
/_/  |_|\____//_____/   \____/ \____//_/  /_//_____//_/  |_|/_/     /____/

欢迎使用《皇牌空战3》汉化镜像处理工具！
PATCH VERSION: 20241028


正在检测当前目录中的镜像文件...
`
	fmt.Println(welcomeMessage)

	currentDir, err := os.Getwd()
	if err != nil {
		fmt.Println("获取当前目录时出错:", err)
		return
	}

	files, err := ioutil.ReadDir(currentDir)
	if err != nil {
		fmt.Println("读取目录时出错:", err)
		return
	}

	const (
		CD1Size = 716287488
		CD2Size = 723813888
	)

	processedCD1 := false
	processedCD2 := false

	for _, file := range files {
		if filepath.Ext(file.Name()) == ".bin" {
			fileSize := file.Size()
			fmt.Printf("发现 .bin 文件: %s, 大小: %d 字节\n", file.Name(), fileSize)

			if fileSize == CD1Size {
				fmt.Printf("文件 %s 被识别为 CD1 镜像，开始重建。\n", file.Name())
				processedCD1 = true
			} else if fileSize == CD2Size {
				fmt.Printf("文件 %s 被识别为 CD2 镜像，开始重建。\n", file.Name())
				processedCD2 = true
			} else {
				fmt.Printf("文件 %s 的大小不符合CD1或CD2的要求，请使用正确的镜像。\nCD1 716287488字节，CD2 723813888字节\n", file.Name())
				continue
			}

			imagePath := filepath.Join(currentDir, file.Name())
			cmd1 := exec.Command("bin/psx-mode2", imagePath, "/ACE.BPB", "patch/BPB")
			cmd2 := exec.Command("bin/psx-mode2", imagePath, "/ACE.BPH", "patch/BPH")

			if err := cmd1.Run(); err != nil {
				fmt.Printf("执行命令时出错: %s (未替换: /ACE.BPB): %v\n", file.Name(), err)
			} else {
				fmt.Printf("命令成功执行: %s (已替换: /ACE.BPB)\n", file.Name())
			}

			if err := cmd2.Run(); err != nil {
				fmt.Printf("执行命令时出错: %s (未替换: /ACE.BPH): %v\n", file.Name(), err)
			} else {
				fmt.Printf("命令成功执行: %s (已替换: /ACE.BPH)\n", file.Name())
			}
		}
	}

	if processedCD1 && processedCD2 {
		fmt.Println("CD1和CD2镜像重建完毕，请配合原来的cue文件使用。")
	} else if processedCD1 {
		fmt.Println("CD1镜像重建完毕，请配合原来的cue文件使用。")
	} else if processedCD2 {
		fmt.Println("CD2镜像重建完毕，请配合原来的cue文件使用。")
	} else {
		fmt.Println("未找到符合条件的镜像文件。请检查文件大小是否正确。")
	}

	fmt.Println("按回车键退出...")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
}
