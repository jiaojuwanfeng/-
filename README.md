# oracle-pulse
🤖 Oracle-Pulse：一个生产级自动化数据库监控与 AI 分析代理
📖 项目介绍
Oracle-Pulse 是一款基于 Docker 部署的轻量化数据监控与分析工具。
它能自动盯守 Oracle 数据库，定时提取关键运营数据，并通过本地部署的 DeepSeek R1 大模型进行深度分析，最后将具有业务洞察力的报告实时推送到你的企业微信。

核心能力：

1、自动提数：定时轮询 Oracle 数据库，无需人工干预。

2、AI 深度解析：利用 DeepSeek 模型对原始数据进行“脱水”处理，识别异常和趋势。

3、零侵入部署：通过 Docker 镜像打包，不影响本地 Python 环境。

4、长驻运行：支持后台运行，具备崩溃自启机制。

🛠️ 环境准备
1、Docker Desktop：确保已安装并启动。

2、Ollama：在宿主机安装，并确保 deepseek-r1:1.5b（或你喜欢的模型）已 pull 成功。

3、Oracle 数据库：确保数据库可被网络访问。

4、企业微信机器人：在群聊中添加机器人并获取 Webhook KEY。

🚀 快速启动说明
1. 配置文件修改
打开工程根目录下的 docker-compose.yml，根据实际情况修改以下环境变量：
- ORACLE_USER=数据库用户名
- ORACLE_PASSWORD=密码
- ORACLE_DSN=地址
- OLLAMA_URL=ollama模型地址
- MODEL_NAME=模型选择
- SYSTEM_PROMPT=提示词
- WECOM_WEBHOOK_URL=你的企业微信机器人地址
- SLEEP_HOURS=执行频率（小时）

2. 一键部署
在当前文件夹打开终端（CMD 或 PowerShell），输入：
  docker-compose up -d --build

3. 监控与维护
查看实时日志（在屏幕上观察）：docker logs -f oracle-ai-bot

查看本地文件日志：
直接打开项目目录下的 logs/app.log

停止服务：docker-compose down
