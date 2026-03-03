# OpenClaw Hardware Daily Xiaohongshu Automation

## 📋 系统概述
自动从小红书帖子生成系统，基于OpenClaw硬件集成监控数据每日生成内容。

## ⏰ 定时任务
- **频率**: 每天上午8点 (Asia/Shanghai)
- **任务ID**: `8c9c9c6b-7b28-4cfd-b19e-7eb711c0ee92`
- **状态**: ✅ 已启用

## 🔄 工作流程
1. **数据抓取**: 从 https://256ericpan.github.io/clawhardware/ 获取最新项目数据
2. **内容生成**: 自动生成小红书格式的帖子内容
3. **私密发布**: 首先在私密模式下发布供审核
4. **人工审核**: 您可以审核后决定是否公开发布

## 📝 今日帖子预览
**标题**: "🦞 OpenClaw硬件生态日报 | 2026-03-03"

**内容摘要**: 
- 活跃项目：4个
- 总Stars：251,155+
- 重点推荐Seeed XIAO ESP32-C3集成方案（仅$13）

**标签**: #OpenClaw #开源硬件 #SeeedStudio #XIAO #ESP32 #IoT #机器人 #AI助手 #每日更新

## 🔧 自定义选项
您可以随时调整：
- 发布时间（当前：每天8:00）
- 内容模板和格式
- 标签和话题
- 是否包含特定项目类别

## 📁 文件位置
- 脚本: `/home/admin/openclaw/workspace/clawhardware/generate_xiaohongshu_post.py`
- 每日帖子: `/home/admin/openclaw/workspace/clawhardware/xiaohongshu_post_YYYY-MM-DD.md`

## ✅ 下一步
1. 今日帖子已生成，请查看内容
2. 如需发布到小红书，请复制内容到小红书编辑器
3. 建议先在私密模式发布，确认效果后再公开