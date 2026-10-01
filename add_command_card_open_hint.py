from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

old = '''        <div class="veles-command-subtitle">{subtitle}</div>
    </div>'''

new = '''        <div class="veles-command-subtitle">{subtitle}</div>
        <div class="veles-command-open">Open →</div>
    </div>'''

if old not in text:
    raise SystemExit("Could not find command card subtitle block.")

if "veles-command-open" not in text:
    text = text.replace(old, new, 1)

path.write_text(text)
print("Added Open hint to command cards.")
