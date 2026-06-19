import json
import os
from datetime import datetime

# 内置站点资料配置
SITES = [
    {
        "name": "澳客主站",
        "url": "https://pc-main-aoke.com",
        "keywords": ["澳客", "彩票", "数据", "预测"],
        "tags": ["博彩", "资讯", "分析"],
        "description": "提供澳客彩票数据分析与预测服务，覆盖多种彩种。"
    },
    {
        "name": "澳客备用站",
        "url": "https://backup-aoke.com",
        "keywords": ["澳客", "备用", "彩票", "实时"],
        "tags": ["博彩", "备用", "数据"],
        "description": "主站不可用时使用的备用站点，数据实时同步。"
    },
    {
        "name": "澳客历史站",
        "url": "https://history-aoke.com",
        "keywords": ["澳客", "历史", "开奖", "记录"],
        "tags": ["博彩", "历史", "查询"],
        "description": "查询历史开奖记录，支持按日期与彩种筛选。"
    }
]

def load_sites(file_path=None):
    """从文件加载站点数据，如果文件存在则覆盖内置数据"""
    if file_path and os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"警告：无法从 {file_path} 加载数据，使用内置站点资料。")
    return SITES

def validate_site(site):
    """验证单个站点数据结构是否完整"""
    required_keys = {"name", "url", "keywords", "tags", "description"}
    if not isinstance(site, dict):
        return False
    return required_keys.issubset(site.keys())

def format_tags(tags):
    """将标签列表格式化为带井号的字符串"""
    return " ".join(f"#{tag}" for tag in tags)

def format_keywords(keywords):
    """将关键词列表格式化为逗号分隔的字符串"""
    return ", ".join(keywords)

def generate_summary(site, index):
    """为单个站点生成结构化摘要"""
    return {
        "序号": index + 1,
        "站点名称": site["name"],
        "URL": site["url"],
        "关键词": format_keywords(site["keywords"]),
        "标签": format_tags(site["tags"]),
        "简短说明": site["description"]
    }

def generate_structured_report(sites, title="站点资料摘要"):
    """生成完整的结构化摘要报告"""
    report_lines = []
    report_lines.append("=" * 50)
    report_lines.append(f"{title} (生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    report_lines.append("=" * 50)
    report_lines.append("")

    for idx, site in enumerate(sites):
        if not validate_site(site):
            report_lines.append(f"⚠️ 站点 #{idx+1} 数据不完整，已跳过")
            report_lines.append("")
            continue
        summary = generate_summary(site, idx)
        for key, value in summary.items():
            report_lines.append(f"{key}: {value}")
        report_lines.append("-" * 40)
        report_lines.append("")

    report_lines.append("=" * 50)
    report_lines.append("摘要结束")
    report_lines.append("=" * 50)
    return "\n".join(report_lines)

def save_report(report_text, output_path="summary_report.txt"):
    """将报告保存到文件"""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"报告已保存至 {output_path}")
        return True
    except IOError as e:
        print(f"保存失败: {e}")
        return False

def print_report(report_text):
    """将报告输出到控制台"""
    print(report_text)

def main():
    # 主流程：读取站点数据并生成报告
    print("正在加载站点资料...")
    sites = load_sites()  # 可传入文件路径：load_sites("sites.json")
    print(f"共加载 {len(sites)} 个站点")

    report = generate_structured_report(sites, "澳客站点结构摘要")
    print_report(report)

    # 可选：保存到文件
    save_report(report, "aoke_sites_summary.txt")

if __name__ == "__main__":
    main()