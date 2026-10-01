from pathlib import Path

path = Path("services/report_storage.py")
text = path.read_text()

text = text.replace(
    '''    valuation_id=None,
):''',
    '''    valuation_id=None,
    company_name=None,
):''',
    1,
)

text = text.replace(
    '''                    name,
                    storage_path,''',
    '''                    name,
                    company_name,
                    storage_path,''',
    1,
)

text = text.replace(
    '''                    :name,
                    :storage_path,''',
    '''                    :name,
                    :company_name,
                    :storage_path,''',
    1,
)

text = text.replace(
    '''                "name": file_name,
                "storage_path": storage_path,''',
    '''                "name": file_name,
                "company_name": company_name,
                "storage_path": storage_path,''',
    1,
)

path.write_text(text)
print("Report storage now supports company_name.")
