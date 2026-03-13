import oracledb
import requests
import logging
import json
from datetime import datetime

# --- 日志配置 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
# --- 配置 ---
# Oracle 连接配置，请根据你的环境修改
ORACLE_CONFIG = {
    "user": "",#你的服务器用户名
    "password": "",#密码
    "dsn": "localhost:1521/orcl"  # 地址
OLLAMA_URL = "http://localhost:11434/api/generate"#默认的本地ollama服务地址
WECOM_WEBHOOK_URL = ""#企业微信机器人地址

def get_data_from_oracle():
    """从 Oracle 数据库获取数据并记录日志"""
    logging.info("开始从 Oracle 获取数据...")
    try:
        # 使用 oracledb.connect 进行连接
        with oracledb.connect(**ORACLE_CONFIG) as conn:
            with conn.cursor() as cursor:
                # 执行 SQL
                cursor.execute("SELECT * FROM ttraycurr WHERE ROWNUM <= 5")#你的sql查询
                # 获取列名以便于数据解析
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                logging.info(f"成功获取数据，共 {len(data)} 条记录。")
                return json.dumps(data, default=str) # 转为 JSON 字符串方便 LLM 阅读
    except oracledb.Error as e:
        logging.error(f"Oracle 数据库读取失败: {e}")
        return None

def analyze_with_ollama(data):
    """调用 Ollama 并捕获异常"""
    logging.info("正在发送数据给 deepseek-r1:1.5b 进行分析...")
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": f"你是一位专业的数据分析师。请分析以下数据库数据，并给出简洁的业务洞察：\n{data}",
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json().get('response', '模型未返回内容')
        logging.info("大模型分析完成。")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Ollama 服务调用异常: {e}")
        return None

def send_to_wecom(content):
    """发送推送"""
    logging.info("正在推送到企业微信...")
    payload = {
        "msgtype": "text",
        "text": {"content": f"【数据分析报告】\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{content}"}
    }
    try:
        response = requests.post(WECOM_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            logging.info("企业微信消息发送成功！")
        else:
            logging.error(f"企业微信发送失败，状态码: {response.status_code}，响应: {response.text}")
    except Exception as e:
        logging.error(f"网络错误导致无法发送到企业微信: {e}")

# --- 主逻辑 ---
if __name__ == "__main__":
    logging.info("=== 系统任务开始 ===")
    
    raw_data = get_data_from_oracle()
    if raw_data:
        analysis = analyze_with_ollama(raw_data)
        if analysis:
            send_to_wecom(analysis)
        else:
            logging.warning("由于分析失败，跳过本次推送。")
    else:
        logging.warning("未获取到有效数据，任务终止。")
        
    logging.info("=== 系统任务结束 ===")