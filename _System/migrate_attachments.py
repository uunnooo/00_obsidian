import os
import shutil
import re
import json
import urllib.parse
from collections import defaultdict

VAULT_DIR = r"D:\00_obsidian"
ATTACH_DIR = os.path.join(VAULT_DIR, "_attachments")
ORPHAN_DIR = os.path.join(ATTACH_DIR, "_미참조_보관")
LOG_PATH = os.path.join(VAULT_DIR, "_System", "attachment_migration_log.json")

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp')
WIKI_RE = re.compile(r'!\[\[(.*?)\]\]')
MD_RE = re.compile(r'!\[(.*?)\]\((.*?)\)')

def normalize_path(p):
    return p.replace('\\', '/')

def find_all_files():
    # 1. 첨부파일 스캔
    all_attachments = {}
    for root, dirs, files in os.walk(ATTACH_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            rel_to_vault = os.path.relpath(full_path, VAULT_DIR)
            rel_to_attach = os.path.relpath(full_path, ATTACH_DIR)
            all_attachments[normalize_path(rel_to_vault)] = {
                'full_path': full_path,
                'rel_to_vault': normalize_path(rel_to_vault),
                'rel_to_attach': normalize_path(rel_to_attach),
                'filename': f
            }

    # 2. MD 파일 스캔
    md_files = []
    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if d not in ['.git', '.obsidian', '.trash']]
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    return all_attachments, md_files

def resolve_physical_source(md_path, target_raw, all_attachments):
    md_dir = os.path.dirname(md_path)
    
    # 1. MD 상대경로
    p1 = os.path.normpath(os.path.join(md_dir, target_raw))
    p1_rel = normalize_path(os.path.relpath(p1, VAULT_DIR))
    if p1_rel in all_attachments:
        return all_attachments[p1_rel]

    # 2. 볼트 루트 상대경로
    p2 = os.path.normpath(os.path.join(VAULT_DIR, target_raw))
    p2_rel = normalize_path(os.path.relpath(p2, VAULT_DIR))
    if p2_rel in all_attachments:
        return all_attachments[p2_rel]

    # 3. _attachments 상대경로
    p3 = os.path.normpath(os.path.join(ATTACH_DIR, target_raw))
    p3_rel = normalize_path(os.path.relpath(p3, VAULT_DIR))
    if p3_rel in all_attachments:
        return all_attachments[p3_rel]

    # 4. 파일명 검색
    fname = os.path.basename(target_raw)
    matches = [item for k, item in all_attachments.items() if item['filename'] == fname]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        norm_target = normalize_path(target_raw)
        for m in matches:
            if norm_target in m['rel_to_vault']:
                return m
        return matches[0]

    return None

def plan_migration(dry_run=True):
    all_attachments, md_files = find_all_files()
    print(f"[*] Total physical files in _attachments: {len(all_attachments)}")
    print(f"[*] Total MD files in vault: {len(md_files)}")

    used_physical_sources = set()
    md_plans = defaultdict(list)
    unresolved_refs = []

    for md_path in md_files:
        rel_md = normalize_path(os.path.relpath(md_path, VAULT_DIR))
        with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 위키링크 검색
        for m in WIKI_RE.finditer(content):
            raw_full = m.group(0)
            inner = m.group(1).strip()
            parts = inner.split('|')
            target = parts[0].strip()
            alias = parts[1].strip() if len(parts) > 1 else None

            fname = os.path.basename(target)
            if fname.lower().endswith(IMAGE_EXTENSIONS):
                source_item = resolve_physical_source(md_path, target, all_attachments)
                if source_item:
                    used_physical_sources.add(source_item['rel_to_vault'])
                    md_plans[md_path].append({
                        'type': 'wiki',
                        'raw': raw_full,
                        'target': target,
                        'alias': alias,
                        'source': source_item
                    })
                else:
                    unresolved_refs.append((rel_md, raw_full))

        # 마크다운 링크 검색
        for m in MD_RE.finditer(content):
            raw_full = m.group(0)
            alt = m.group(1)
            target = m.group(2).split()[0].strip()
            target_unquoted = urllib.parse.unquote(target)

            fname = os.path.basename(target_unquoted)
            if fname.lower().endswith(IMAGE_EXTENSIONS):
                source_item = resolve_physical_source(md_path, target_unquoted, all_attachments)
                if source_item:
                    used_physical_sources.add(source_item['rel_to_vault'])
                    md_plans[md_path].append({
                        'type': 'md',
                        'raw': raw_full,
                        'target': target,
                        'alt': alt,
                        'source': source_item
                    })
                else:
                    unresolved_refs.append((rel_md, raw_full))

    print(f"[*] Total referenced instances: {sum(len(v) for v in md_plans.values())}")
    print(f"[*] Distinct physical sources referenced: {len(used_physical_sources)}")
    print(f"[*] Unresolved references: {len(unresolved_refs)}")
    if unresolved_refs:
        print("[!] ERROR: Unresolved references found:")
        for r in unresolved_refs:
            print("   -", r)
        return False

    # Orphaned 파일 식별
    orphan_items = [item for k, item in all_attachments.items() if k not in used_physical_sources]
    print(f"[*] Total orphaned physical files to isolate: {len(orphan_items)}")

    # Step 1: 미참조 파일 이동 계획 수립
    orphan_moves = []
    for item in orphan_items:
        src = item['full_path']
        dst = os.path.join(ORPHAN_DIR, item['rel_to_attach'])
        orphan_moves.append((src, dst))

    # Step 2: 실사용 파일 복사/배치 및 MD 링크 치환 계획 수립
    file_copies = []
    md_replacements = {}
    migration_audit = []

    for md_path, items in md_plans.items():
        rel_md = normalize_path(os.path.relpath(md_path, VAULT_DIR))
        doc_rel_no_ext = os.path.splitext(rel_md)[0]
        target_dir = os.path.join(ATTACH_DIR, doc_rel_no_ext)
        target_dir_rel_vault = normalize_path(os.path.relpath(target_dir, VAULT_DIR))

        with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
            md_content = f.read()

        # 길이 역순으로 정렬하여 서브스트링 충돌 방지
        sorted_items = sorted(items, key=lambda x: len(x['raw']), reverse=True)

        new_content = md_content
        for it in sorted_items:
            src = it['source']['full_path']
            fname = it['source']['filename']
            dst = os.path.join(target_dir, fname)
            file_copies.append((src, dst))

            if it['type'] == 'wiki':
                new_vault_path = f"{target_dir_rel_vault}/{fname}"
                if it['alias']:
                    new_link = f"![[{new_vault_path}|{it['alias']}]]"
                else:
                    new_link = f"![[{new_vault_path}]]"
                new_content = new_content.replace(it['raw'], new_link)
            elif it['type'] == 'md':
                md_dir = os.path.dirname(md_path)
                rel_url = normalize_path(os.path.relpath(dst, md_dir))
                new_link = f"![{it['alt']}]({rel_url})"
                new_content = new_content.replace(it['raw'], new_link)

            migration_audit.append({
                'md_file': rel_md,
                'type': it['type'],
                'old_raw': it['raw'],
                'new_link': new_link,
                'source_path': normalize_path(src),
                'dest_path': normalize_path(dst)
            })

        md_replacements[md_path] = new_content

    print(f"[*] Planned orphan moves: {len(orphan_moves)}")
    print(f"[*] Planned file copies/placements: {len(file_copies)}")
    print(f"[*] Planned MD files to update: {len(md_replacements)}")

    if dry_run:
        print("\n=== DRY RUN COMPLETED SUCCESSFULLY ===")
        print("No changes have been made to disk.")
        return True

    # ================= REAL EXECUTION =================
    print("\n>>> EXECUTING CHANGES TO DISK <<<")

    # 1. Orphan 파일 격리 이동
    print("1. Isolating orphaned files to _미참조_보관...")
    for src, dst in orphan_moves:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
    print(f"   Done isolating {len(orphan_moves)} files.")

    # 2. 실사용 파일 신규 계층 폴더로 복사/배치
    print("2. Copying referenced files to document mirror folders...")
    for src, dst in file_copies:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    print(f"   Done copying {len(file_copies)} files.")

    # 3. MD 파일 링크 갱신
    print("3. Updating image links in MD files...")
    for md_path, new_content in md_replacements.items():
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    print(f"   Done updating {len(md_replacements)} MD files.")

    # 4. 감사 로그 저장
    print("4. Saving migration audit log...")
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(migration_audit, f, indent=2, ensure_ascii=False)
    print(f"   Saved log to {LOG_PATH}")

    # 5. 사전 무결성 검증 (Verification Check before cleanup)
    print("5. Verifying integrity before legacy cleanup...")
    missing_count = 0
    for audit in migration_audit:
        if not os.path.exists(audit['dest_path']):
            print(f"   [!] MISSING FILE: {audit['dest_path']}")
            missing_count += 1
    if missing_count > 0:
        print(f"[!] ABORTING CLEANUP: {missing_count} files missing in destination!")
        return False
    print("   Verification passed: All destination files exist!")

    # 6. 레거시 원본 파일들 정리
    print("6. Cleaning up legacy folders...")
    legacy_folders = [
        os.path.join(ATTACH_DIR, "10_회사_업무"),
        os.path.join(ATTACH_DIR, "20_트레이딩"),
        os.path.join(ATTACH_DIR, "30_자기개발"),
        os.path.join(ATTACH_DIR, "40_이끼도감"),
    ]
    for leg in legacy_folders:
        if os.path.exists(leg):
            shutil.rmtree(leg)
            print(f"   Removed legacy folder: {leg}")

    print("\n>>> ALL MIGRATION STEPS EXECUTED SUCCESSFULLY! <<<")
    return True

if __name__ == '__main__':
    import sys
    dry = '--dry-run' in sys.argv or '-n' in sys.argv
    plan_migration(dry_run=dry)
