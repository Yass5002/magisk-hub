import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dist_dirs = [
    os.path.join(REPO_ROOT, 'dist', 'modules'),
    os.path.join(REPO_ROOT, 'dist', 'zh', 'modules'),
]
zero_links = 0
total_modules = 0

for dist_dir in dist_dirs:
    if not os.path.isdir(dist_dir):
        print(f"Missing directory: {dist_dir}", file=sys.stderr)
        sys.exit(1)
    for root, _, files in os.walk(dist_dir):
        for file in files:
            if file == 'index.html':
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'More in' in content or '更多「' in content:
                    links = len(re.findall(r'data-umami-event="related-module-click"', content))
                    if links == 0:
                        print(f"Module {filepath} has 0 related links!", file=sys.stderr)
                        zero_links += 1
                else:
                    print(f"Module {filepath} does not have related-modules section", file=sys.stderr)
                    zero_links += 1
                total_modules += 1

print(f"Total module pages checked (EN+ZH): {total_modules}")
print(f"Modules with 0 related links: {zero_links}")
sys.exit(1 if zero_links > 0 else 0)

