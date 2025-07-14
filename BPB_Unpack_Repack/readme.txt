用法：

打包bpb，同时会生成bph

`ac3es_tools.exe bpb  --pack <BPB拆分后的子文件的目录>`

示例：
`ac3es_tools.exe bpb  --pack F:\PSXISO\AC3\CD2\REPACK_CD2\BPB`

拆包BPB
`ac3es_tools.exe bpb --bpb <ACE.BPB路径> --bph <ACE.BPH路径> -u <拆分后子文件路径>`

示例：
`ac3es_tools.exe bpb --bpb REPACK_CD2/ACE.BPB --bph REPACK_CD2/ACE.BPH -u BPB`