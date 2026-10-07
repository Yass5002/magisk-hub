import os
import re

dist_dir = 'dist/modules'
zero_links = 0
total_modules = 0

for root, _, files in os.walk(dist_dir):
    for file in files:
        if file == 'index.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            # check if there are any <a> tags in the 'More in' section
            # The section looks like:
            # <h3 class="text-sm font-semibold text-zinc-900 border-b border-zinc-200 pb-2 mb-3">
            #  More in
            if 'More in' in content:
                # count links with data-umami-event="related-module-click"
                links = len(re.findall(r'data-umami-event="related-module-click"', content))
                if links == 0:
                    print(f"Module {filepath} has 0 related links!")
                    zero_links += 1
            else:
                print(f"Module {filepath} does not have 'More in' section (maybe the only one in its category)")
                # Check category size
            total_modules += 1

print(f"Total modules checked: {total_modules}")
print(f"Modules with 0 links: {zero_links}")

