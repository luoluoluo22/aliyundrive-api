import json
import os
import configparser
from pathlib import Path

class AliyundriveAuth:
    def __init__(self):
        self.config_path = os.path.join(str(Path.home()), '.aliyundrive', 'config.ini')
        
    def get_tokens_from_web(self):
        print("\n请按以下步骤操作：")
        print("1. 用浏览器打开阿里云盘官网 https://www.aliyundrive.com/")
        print("2. 按F12打开开发者工具")
        print("3. 切换到'应用程序/Application'标签")
        print("4. 在左侧找到'本地存储空间/Local Storage' -> 'https://www.aliyundrive.com'")
        print("5. 找到'token'项并复制其值")
        
        print("\n请粘贴token值 (粘贴完成后按两次回车):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        token_str = ''.join(lines)
        
        try:
            token_data = json.loads(token_str)
            if not isinstance(token_data, dict):
                raise ValueError("Invalid token format")
                
            required_fields = ['access_token', 'refresh_token', 'default_drive_id']
            if not all(field in token_data for field in required_fields):
                raise ValueError("Token missing required fields")
                
            self._save_config(token_data)
            return token_data
            
        except (json.JSONDecodeError, ValueError) as e:
            print("\n错误：token格式不正确")
            print("请确保复制了完整的token值，包括开头的{和结尾的}")
            print("提示：可以直接复制整个token值，包含换行符也没关系")
            return self.get_tokens_from_web()
    
    def _save_config(self, token_data):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        config = configparser.ConfigParser()
        config['account'] = {
            'access_token': token_data.get('access_token', ''),
            'refresh_token': token_data.get('refresh_token', ''),
            'drive_id': token_data.get('default_drive_id', '')
        }
        
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        print(f"\n配置已保存到: {self.config_path}")
    
    def get_config(self):
        """获取配置，如果不存在则引导用户手动输入token"""
        if not os.path.exists(self.config_path):
            print("未找到配置文件，需要手动配置...")
            return self.get_tokens_from_web()
        
        config = configparser.ConfigParser()
        config.read(self.config_path)
        
        if not config.has_section('account'):
            return self.get_tokens_from_web()
        
        return {
            'access_token': config.get('account', 'access_token'),
            'refresh_token': config.get('account', 'refresh_token'),
            'default_drive_id': config.get('account', 'drive_id')
        } 