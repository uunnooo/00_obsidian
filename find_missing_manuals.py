import os

base_dir = r"C:\Users\uunnoo\PycharmProjects\unoUtil\unoUtil"
missing = []
for root, dirs, files in os.walk(base_dir):
    if any(x in root.lower() for x in ['_archive', 'archive', 'example', 'test_data', 'oldver']):
        continue
    for file in files:
        if file.endswith('.py'):
            if file.lower() == '__init__.py' or file.lower().startswith('test_'):
                continue
            py_path = os.path.join(root, file)
            md_path = py_path[:-3] + '.md'
            if not os.path.exists(md_path):
                missing.append(py_path)

bridges = []
real_logic = []

for m in missing:
    try:
        with open(m, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()
    except Exception as e:
        print(f"Error reading {m}: {e}")
        continue
    
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    is_bridge = False
    
    # Let's check if the file is a bridge
    # Bridge files are very short, usually only imports everything from a snake_case module
    # Or contains comments plus a single from .xxx import *
    non_comment_import = [l for l in lines if not l.startswith('#') and not l.startswith('"""') and not l.startswith("'''")]
    if len(non_comment_import) <= 3 and all(l.startswith('from ') or l.startswith('import ') or l.strip() == '' for l in non_comment_import):
        is_bridge = True
    
    if is_bridge:
        bridges.append(m)
    else:
        real_logic.append(m)

print(f"Total Missing: {len(missing)}")
print(f"Bridges: {len(bridges)}")
print(f"Real Logic: {len(real_logic)}")
print("\n--- BRIDGES ---")
for b in sorted(bridges):
    print(os.path.relpath(b, base_dir))
print("\n--- REAL LOGIC ---")
for r in sorted(real_logic):
    print(os.path.relpath(r, base_dir))
