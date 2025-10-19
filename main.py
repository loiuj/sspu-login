import requests
from cookie import get_jx_cookies
from tool.load_score import LoadScore, get_score_html

cookies = get_jx_cookies()
score_html = get_score_html(cookies)
score = LoadScore(score_html)
score.print_table()
