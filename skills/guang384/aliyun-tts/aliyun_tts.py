#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
阿里云语音合成 TTS - 完整脚本（带签名）
"""

import base64
import hashlib
import hmac
import http.client
import json
import os
import sys
import time
import urllib.parse
from urllib import parse
import uuid
import argparse

# ============ 配置区 ============
ALIYUN_APP_KEY = os.getenv("ALIYUN_APP_KEY")
ALIYUN_ACCESS_KEY_ID = os.getenv("ALIYUN_ACCESS_KEY_ID")
ALIYUN_ACCESS_KEY_SECRET = os.getenv("ALIYUN_ACCESS_KEY_SECRET")

if not ALIYUN_APP_KEY or not ALIYUN_ACCESS_KEY_ID or not ALIYUN_ACCESS_KEY_SECRET:
    print("请设置环境变量: ALIYUN_APP_KEY, ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET", file=sys.stderr)
    sys.exit(1)

REGION = "cn-shanghai"  # Token 服务只有上海
# ============ 配置区结束 ============

def percent_encode(text):
    """RFC 3986 URL 编码"""
    if text is None:
        return None
    encoded = parse.quote_plus(text)
    return encoded.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

def encode_dict(dic):
    """将字典参数排序并编码"""
    keys = dic.keys()
    dic_sorted = [(key, dic[key]) for key in sorted(keys)]
    encoded = parse.urlencode(dic_sorted)
    return encoded.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

def get_token():
    """获取访问令牌（带签名）"""
    # 1. 构造请求参数
    params = {
        'AccessKeyId': ALIYUN_ACCESS_KEY_ID,
        'Action': 'CreateToken',
        'Format': 'JSON',
        'RegionId': REGION,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'SignatureVersion': '1.0',
        'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        'Version': '2019-02-28'
    }
    
    # 2. 构造规范化的请求字符串
    query_string = encode_dict(params)
    
    # 3. 构造待签名字符串
    string_to_sign = 'GET' + '&' + percent_encode('/') + '&' + percent_encode(query_string)
    
    # 4. 计算签名
    secreted_string = hmac.new(
        bytes(ALIYUN_ACCESS_KEY_SECRET + '&', encoding='utf-8'),
        bytes(string_to_sign, encoding='utf-8'),
        hashlib.sha1
    ).digest()
    signature = base64.b64encode(secreted_string)
    signature = percent_encode(signature)
    
    # 5. 发送请求
    full_url = f"http://nls-meta.{REGION}.aliyuncs.com/?Signature={signature}&{query_string}"
    
    host = f"nls-meta.{REGION}.aliyuncs.com"
    conn = http.client.HTTPConnection(host)
    conn.request("GET", full_url)
    resp = conn.getresponse()
    body = resp.read().decode()
    
    data = json.loads(body)
    if "Token" in data and "Id" in data["Token"]:
        token = data["Token"]["Id"]
        return token
    else:
        print(f"获取 Token 失败: {body}", file=sys.stderr)
        return None

def tts_synthesize(text, voice="siyue", format="mp3", sample_rate=16000, output_file="/tmp/tts_output.mp3"):
    """语音合成"""
    token = get_token()
    if not token:
        return False
    
    host = f"nls-gateway-{REGION}.aliyuncs.com"
    
    # URL 编码（RFC 3986）
    text_encoded = percent_encode(text)
    
    url = f"/stream/v1/tts?appkey={ALIYUN_APP_KEY}&token={token}&text={text_encoded}&format={format}&sample_rate={sample_rate}&voice={voice}"
    
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", url)
    resp = conn.getresponse()
    
    content_type = resp.getheader("Content-Type")
    body = resp.read()
    
    if "audio" in content_type:
        with open(output_file, "wb") as f:
            f.write(body)
        print(f"✅ 语音已保存: {output_file}")
        return True
    else:
        print(f"❌ 失败: {body.decode()[:300]}", file=sys.stderr)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="阿里云 TTS 语音合成")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument("-o", "--output", default="/tmp/tts_output.mp3", help="输出文件路径")
    parser.add_argument("-v", "--voice", default="siyue", help="声音名称")
    parser.add_argument("-f", "--format", default="mp3", help="音频格式")
    parser.add_argument("-r", "--sample-rate", default="16000", help="采样率")
    
    args = parser.parse_args()
    
    success = tts_synthesize(
        text=args.text,
        voice=args.voice,
        format=args.format,
        sample_rate=int(args.sample_rate),
        output_file=args.output
    )
    
    sys.exit(0 if success else 1)
