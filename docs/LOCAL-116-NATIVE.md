# 本机 11.6.0 适配补丁（2026-10-22）

本地维护的补丁，不代表上游已经发布或完成跨机器验收。适用于官方 11.6.0（13281）及引擎 SHA-256 `a490d9a08b71a2d9af138d24528d3d40d65b37b06911627c53a2915c6cac0754`。

## 首页登记

macOS 26.5.2 会在原索引没有 `com.apple.provenance` 时，给 clonefile 生成的临时索引添加该属性。允许保留系统新增的 provenance，并记录 before/staged/after 与变更列表；不删除属性。已有 provenance 丢失、macl/quarantine 或其他属性变化仍拒绝。实际新草稿登记及回读通过，原首页条目保持不变。

## 无界面原生导出

本机二进制反汇编与隔离试验确认：

- restore helper：`0x22316ec`，参数仍为 session、restore bool、timeline。
- `ExportStartReqStruct` 构造函数：`0x2830110`；shared allocation `0x3f0` 减 control block `0x18`，请求大小 `0x3d8`。
- 输出路径 `0x48`，config `0x60`；尺寸、帧率、码率与 MP4 writer 字段在样本中验证。
- restore callback 使用 `draft_service.cpp:operator():669`；另有 664 分支，不作为本路径完成事件。
- compile callback 仍为 `ve_export_impl.cpp:operator():1203`。
- 不修改剪映应用、库、签名、账号、权益或网络隔离规则。

通过已安装 Skill 的 `export --build BUILD --out WORK/NEW_EXPORT` 调用。剪映无需启动，草稿无需登记首页。仍保持原有隔离进程、禁止网络和账号读取、来源不可变及精确帧数检查。

已验证样本：2 秒 60 帧；10 秒 1080p 300 帧（中文三段标题）；4 秒 120 帧（视频分段、本地音频及音量曲线）。完整解码通过，音频中段约 -35 dBFS，首末衰减。导出画面已抽帧检查；不代表所有参数组合均通过主观视听验收。

11.6 当前仅开放本地视频分段、静态文字、本地音频和音量曲线。画面/文字关键帧、图片/GIF、转场、蒙版、特效和复合片段继续拒绝。文字缩放曲线试验未见预期变化，不能按编码成功认定支持。11.5/11.4.2 原支持范围保持不变。

## 维护

修改核心源文件后同步更新同仓与已安装 Skill 的对应源码 pin。官方引擎指纹和桥接组件 pin 不变。不要直接用上游 Skill 覆盖本机配套入口；重新安装或升级前保留本地补丁与证据。
