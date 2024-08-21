# 本模块用于读和写 json 文件
import json


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return None
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的JSON格式。")
        return None
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误：{e}")
        return None


def write_json_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"数据已成功写入到文件 {file_path}")
    except Exception as e:
        print(f"写入文件 {file_path} 时发生错误：{e}")


data = read_json_file("data.json")
