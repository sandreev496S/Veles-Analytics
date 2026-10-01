from pathlib import Path

path = Path("services/report_storage.py")
text = path.read_text()

old = '''                SELECT id, report_type, name, storage_path, file_name, mime_type, file_size_bytes, created_at'''

new = '''                SELECT id, report_type, name, company_name, storage_path, file_name, mime_type, file_size_bytes, created_at'''

if old not in text:
    raise SystemExit("Could not find list_user_reports SELECT line.")

text = text.replace(old, new, 1)

old2 = '''            "storage_path": row[3],
            "file_name": row[4],
            "mime_type": row[5],
            "file_size_bytes": row[6],
            "created_at": str(row[7]),'''

new2 = '''            "company_name": row[3],
            "storage_path": row[4],
            "file_name": row[5],
            "mime_type": row[6],
            "file_size_bytes": row[7],
            "created_at": str(row[8]),'''

if old2 not in text:
    raise SystemExit("Could not find list_user_reports return mapping.")

text = text.replace(old2, new2, 1)

path.write_text(text)
print("list_user_reports now returns company_name.")
