from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
    "from services.auth import auth_ui, is_authenticated, get_current_user, logout_button",
    "from services.auth import auth_ui, is_authenticated, get_current_user",
    1,
)

text = text.replace("logout_button()\n", "", 1)

path.write_text(text)
print("Removed old logout import and call from app.py.")
