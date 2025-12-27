PySide6 GitHub Backup Workflow

1️⃣ Check what changed
In the terminal, check which files are new or modified:
git status

2️⃣ Stage files for commit
Add all changes:
git add .

Or only specific files:
git add main.py ui/main_window.ui

3️⃣ Create a commit
Short, clear commit message:
git commit -m "Add main window UI"

Optional: longer description:
git commit -m "Implement login validation

- Check username and password
- Show error message if invalid
- Connect validation to login button"

4️⃣ Push changes to GitHub
git push origin master

5️⃣ Next step
After completing a part of the project, repeat the workflow:
git status → git add → git commit → git push

6️⃣ Example commit messages for PySide6
Change type                  Example message
New UI                        Add main window UI
Button / Signal               Connect login button signal
Function implemented          Implement login validation
Bugfix                        Fix crash on loading UI
Refactoring                   Refactor main window initialization
Styles / Layout               Update main window layout
New file / resource           Add icons for toolbar
README / Documentation        Add project README
Temporary progress / backup   Save progress on UI forms

Tips:
- Use imperative form in commit messages: "Add", "Fix", "Implement"
- Keep messages short and clear (50-70 characters)
- Optional: add more details in the commit body
- Push regularly after completing meaningful steps
