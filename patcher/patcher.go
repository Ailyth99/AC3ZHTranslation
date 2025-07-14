package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
)

// 新增函数：生成 cue 文件内容
func generateCueSheet(binFileName string) string {
	// PlayStation 格式的 cue 文件
	// 对于中文文件名，需要确保使用双引号包围
	return fmt.Sprintf(`FILE "%s" BINARY
TRACK 01 MODE2/2352
INDEX 01 00:00:00
`, binFileName)
}

func main() {
	// 欢迎词
	welcomeMessage := `
    ___    ______ ______   ______ ____   __  ___ ____   ___   ______   _____
   /   |  / ____// ____/  / ____// __ \ /  |/  // __ ) /   | /_  __/  |__  /
  / /| | / /    / __/    / /    / / / // /|_/ // __  |/ /| |  / /      /_ <
 / ___ |/ /___ / /___   / /___ / /_/ // /  / // /_/ // ___ | / /     ___/ /
/_/  |_|\____//_____/   \____/ \____//_/  /_//_____//_/  |_|/_/     /____/

欢迎使用《皇牌空战3》汉化镜像处理工具！
PATCH VERSION: 


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
		JA1Size = 716287488
		JA2Size = 723813888
		JP1Size = 716240448
		JP2Size = 723766848
	)

	processedJA1 := false
	processedJA2 := false
	processedJP1 := false
	processedJP2 := false

	// 新增变量记录成功状态
	successJA1 := false
	successJA2 := false
	successJP1 := false
	successJP2 := false

	for _, file := range files {
		if filepath.Ext(file.Name()) == ".bin" {
			fileSize := file.Size()
			fmt.Printf("\n发现 .bin 文件: %s, 大小: %d 字节\n", file.Name(), fileSize)

			var patchFile string
			var newFileName string

			switch fileSize {
			case JA1Size:
				fmt.Printf("\n文件 %s 被识别为日亚版CD1镜像，\n开始打补丁……\n", file.Name())
				patchFile = "patch/ja1.ac3"
				newFileName = file.Name()[:len(file.Name())-4] + "_中文.bin"
				processedJA1 = true
			case JA2Size:
				fmt.Printf("\n文件 %s 被识别为日亚版CD2镜像，\n开始打补丁……\n", file.Name())
				patchFile = "patch/ja2.ac3"
				newFileName = file.Name()[:len(file.Name())-4] + "_中文.bin"
				processedJA2 = true
			case JP1Size:
				fmt.Printf("\n文件 %s 被识别为日版CD1镜像，\n开始打补丁……\n", file.Name())
				patchFile = "patch/jp1.ac3"
				newFileName = file.Name()[:len(file.Name())-4] + "_中文.bin"
				processedJP1 = true
			case JP2Size:
				fmt.Printf("\n文件 %s 被识别为日版CD2镜像，\n开始打补丁……\n", file.Name())
				patchFile = "patch/jp2.ac3"
				newFileName = file.Name()[:len(file.Name())-4] + "_中文.bin"
				processedJP2 = true
			default:
				fmt.Printf("镜像 %s 不符合要求，请使用正确的日版/日亚版AC3镜像。\n", file.Name())
				continue
			}

			imagePath := filepath.Join(currentDir, file.Name())
			cmd := exec.Command("bin/patcher.exe", "-d", "-s", imagePath, patchFile, newFileName)

			if err := cmd.Run(); err != nil {
				fmt.Printf("\n执行命令时出错: %s (未打补丁): %v\n", file.Name(), err)
			} else {
				fmt.Printf("\n成功生成新镜像文件: %s\n", newFileName)

				// 记录成功状态
				switch fileSize {
				case JA1Size:
					successJA1 = true
				case JA2Size:
					successJA2 = true
				case JP1Size:
					successJP1 = true
				case JP2Size:
					successJP2 = true
				}

				// 为新生成的 bin 文件创建对应的 cue 文件
				cueContent := generateCueSheet(newFileName)
				cueFileName := newFileName[:len(newFileName)-4] + ".cue"
				if err := os.WriteFile(cueFileName, []byte(cueContent), 0644); err != nil {
					fmt.Printf("创建 cue 文件失败: %v\n", err)
				} else {
					fmt.Printf("成功生成新镜像的cue文件: %s\n", cueFileName)
				}
			}
		}
	}

	// 修改最终输出逻辑
	if successJA1 || successJA2 || successJP1 || successJP2 {
		fmt.Println("\n镜像打补丁完毕，成功处理的镜像包括：")
		if successJA1 {
			fmt.Println("- 日亚版CD1")
		}
		if successJA2 {
			fmt.Println("- 日亚版CD2")
		}
		if successJP1 {
			fmt.Println("- 日版CD1")
		}
		if successJP2 {
			fmt.Println("- 日版CD2")
		}

	} else {
		if processedJA1 || processedJA2 || processedJP1 || processedJP2 {
			fmt.Println("\n检测到以下镜像文件，但打补丁过程失败：")
			if processedJA1 && !successJA1 {
				fmt.Println("- 日亚版CD1")
			}
			if processedJA2 && !successJA2 {
				fmt.Println("- 日亚版CD2")
			}
			if processedJP1 && !successJP1 {
				fmt.Println("- 日版CD1")
			}
			if processedJP2 && !successJP2 {
				fmt.Println("- 日版CD2")
			}
			fmt.Println("请检查补丁文件是否完整，或重试。")
		} else {
			fmt.Println("未找到符合条件的镜像文件。请检查文件大小是否正确。")
		}
	}

	fmt.Println("\n按回车键退出...")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
}
