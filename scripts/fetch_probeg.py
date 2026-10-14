"""Save the public results table for Vladimir Ivanov; keep the old file on errors."""
import re
import urllib.request
from pathlib import Path

SOURCE = 'https://probeg.org/user/21039/full/'
def build(page):
    if not re.search(r'<title>\s*Владимир Иванов\s*[–—-]', page):
        raise ValueError('Unexpected athlete profile')
    tables = re.findall(r'<table\b.*?</table>', page, re.S)
    table = next((t for t in tables if 'id="table_for_sort"' in t), None)
    if not table or not all(h in table for h in ('Дата', 'Забег', 'Дистанция', 'Результат')):
        raise ValueError('Results table missing')
    if len(re.findall(r'<tr\b', table)) < 100:
        raise ValueError('Incomplete results: preserving previous snapshot')
    return '<!doctype html><meta charset="utf-8"><title>Владимир Иванов — результаты ПроБЕГ</title>' + table + '\n'

if __name__ == '__main__':
    request = urllib.request.Request(SOURCE, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        content = build(response.read().decode('utf-8'))
    target = Path(__file__).resolve().parents[1] / 'probeg-results.html'
    temp = target.with_suffix('.tmp')
    temp.write_text(content, encoding='utf-8')
    temp.replace(target)
