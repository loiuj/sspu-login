from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional, Any
import re
import requests


# 这部分ai处理的
@dataclass
class Course:
    term: str  # 学年学期 (e.g. "2024-2025 秋季")
    course_code: Optional[str]  # 原始课程代码 (例如 g2065025) — 解析时保留，但格式化输出时不显示
    seq_no: Optional[str]  # 课程序号 (例如 0626) — 同上
    name: str  # 课程名称
    category: Optional[str]  # 课程类别 (例如 "专业基础课")
    credit: Optional[float]  # 学分
    assessment: Optional[str]  # 总评（可能是文字或数字）
    final: Optional[str]  # 最终（可能是文字或数字）
    gpa: Optional[float]  # 绩点（若能解析为 float）

    def formatted(self) -> str:
        """返回单行格式化输出（不包含 course_code、seq_no）。"""
        cred = f"{self.credit:g}" if self.credit is not None else ""
        gpa = f"{self.gpa:g}" if self.gpa is not None else (self.gpa if self.gpa is not None else "")
        return f"{self.term:16} | {self.name:30} | {cred:>4} | {self.assessment:>6} | {self.final:>6} | {gpa:>4}"

    def to_dict(self) -> dict:
        return {
            "term": self.term,
            "course_code": self.course_code,
            "seq_no": self.seq_no,
            "name": self.name,
            "category": self.category,
            "credit": self.credit,
            "assessment": self.assessment,
            "final": self.final,
            "gpa": self.gpa,
        }


class LoadScore:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")
        self.courses: List[Course] = []
        self._parse_course_table()

    @staticmethod
    def _try_float(text: Optional[str]) -> Optional[float]:
        if text is None:
            return None
        text = text.strip()
        # Accept things like "4.7", "5", "3.0", maybe "4,7" -> replace comma
        if text == "":
            return None
        text = text.replace(",", ".")
        # if purely numeric (possibly with trailing non-digit) extract numeric part
        m = re.search(r"-?\d+(\.\d+)?", text)
        if m:
            try:
                return float(m.group(0))
            except:
                return None
        return None

    def _parse_course_table(self):
        # 找到包含课程行的 tbody；在你的 HTML 里 id 是 "grid593030458_data"
        tbody = self.soup.find("tbody", id=re.compile(r".*_data$"))
        if not tbody:
            # 退回到第一个 gridtable 的 tbody（更宽容）
            tbody = self.soup.find("table", class_="gridtable")
            if tbody:
                tbody = tbody.find("tbody")
        if not tbody:
            return

        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            if not tds or len(tds) < 6:
                continue
            # 按照页面列顺序：学年学期, 课程代码, 课程序号, 课程名称, 课程类别, 学分, 总评, 最终, 绩点
            # 有时有 style 的 td，get_text(strip=True) 可处理换行多空格
            get = lambda i: tds[i].get_text(strip=True) if i < len(tds) else None

            term = get(0) or ""
            course_code = get(1) or None
            seq_no = get(2) or None
            name = get(3) or ""
            category = get(4) or None

            # 学分可能是小数或整数
            cred_raw = get(5)
            credit = None
            if cred_raw:
                try:
                    credit = float(cred_raw)
                except:
                    # 有可能是 "0.5" 或 "2"，尽量清洗
                    credit = self._try_float(cred_raw)

            assessment = get(6)
            final = get(7)
            gpa_raw = get(8)
            gpa = self._try_float(gpa_raw)

            # 创建 Course 对象
            course = Course(
                term=term,
                course_code=course_code,
                seq_no=seq_no,
                name=name,
                category=category,
                credit=credit,
                assessment=assessment,
                final=final,
                gpa=gpa,
            )
            self.courses.append(course)

    def print_table(self):
        # 第一行是标题
        header = f"{'学年学期':16} | {'课程名称':30} | {'学分':>4} | {'总评':>6} | {'最终':>6} | {'绩点':>4}"
        print(header)
        print("-" * len(header))
        for c in self.courses:
            print(c.formatted())

    def search_by_name(self, keyword: str) -> List[Course]:
        """按课程名搜索，包含即可，大小写/空白敏感度已降低。"""
        k = keyword.strip().lower()
        return [c for c in self.courses if k in (c.name or "").lower()]

    def search_by_category(self, category_keyword: str) -> List[Course]:
        k = category_keyword.strip().lower()
        return [c for c in self.courses if c.category and k in c.category.lower()]

    def as_list_of_dicts(self) -> List[dict]:
        return [c.to_dict() for c in self.courses]


def get_score_html(jx_cookies):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        'Origin': 'https://jx.sspu.edu.cn',
        'Referer': 'https://jx.sspu.edu.cn/eams/teach/grade/course/person.action',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'Array_xuanke=web66; JSESSIONID=11E164C1497B28F8EBE1CE859533F951.-worker2; Array_xuanke=web66; Array_xuanke=web66',
    }

    params = {
        'projectType': 'MAJOR',
    }

    response = requests.post(
        'https://jx.sspu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action',
        params=params,
        cookies=jx_cookies,
        headers=headers,
    )
    return response.text


# ----------------- 示例用法 -----------------
if __name__ == "__main__":
    # 假设你把从 response.text 得到的 HTML 放进 html_str
    html_str = """（把你贴的大段 HTML 字符串粘贴到这里）"""

    parser = LoadScore(html_str)
    parser.print_table()

    # 按科目名搜索（例如查找“网络”相关课程）
    print("\n查找课程名包含 '网络' 的条目：")
    for c in parser.search_by_name("网络"):
        print(c.formatted())

    # 按课程类别搜索（例如查找 "专业实践"）
    print("\n查找课程类别包含 '专业实践' 的条目：")
    for c in parser.search_by_category("专业实践"):
        print(c.formatted())

    # 如果需要 JSON-ifiable 的结果：
    import json

    print("\n全部课程（JSON）：")
    print(json.dumps(parser.as_list_of_dicts(), ensure_ascii=False, indent=2))
