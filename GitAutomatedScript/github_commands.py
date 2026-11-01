import os
import subprocess
import shutil
import json
import stat

def run_command(command):
    """Helper function to run shell commands and display output cleanly."""
    print(f"👉 Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"   Output:\n{result.stdout.strip()}")
    if result.stderr.strip() and result.returncode != 0:
        print(f"   ⚠️ Notice/Error: {result.stderr.strip()}")
    return result.returncode

def remove_readonly(func, path, excinfo):
    """Clear the readonly bit and reattempt removal to handle Windows file locks."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    print("==================================================")
    print("🚀 CISCO FRESHERS: GIT, GITHUB & PR WORKSHOP 🚀")
    print("==================================================\n")

    # 1. Load configuration from config.json
    config_file = "config.json"
    if not os.path.exists(config_file):
        print(f"❌ Error: '{config_file}' not found! Please create it using the template.")
        return

    with open(config_file, "r") as f:
        config = json.load(f)

    repo_url = config.get("github_repo_url")
    user_name = config.get("git_user_name")
    user_email = config.get("git_user_email")

    if not repo_url or "your-username" in repo_url:
        print("❌ Please update 'config.json' with your actual GitHub repository URL first!")
        return

    demo_dir = "netpulse"
    if os.path.exists(demo_dir):
        shutil.rmtree(demo_dir, onerror=remove_readonly)
    os.makedirs(demo_dir)
    os.chdir(demo_dir)
    print(f"📁 Created local workspace: {os.getcwd()}\n")

    print("=== STEP 1: INITIALIZE LOCAL REPOSITORY ===")
    run_command("git init")
    run_command("git branch -M main")
    run_command(f"git config user.name '{user_name}'")
    run_command(f"git config user.email '{user_email}'")

    print(f"\n=== STEP 2: LINK TO GITHUB REMOTE ===")
    run_command(f"git remote add origin {repo_url}")
    run_command("git remote -v")

    print("\n=== STEP 3: CREATE FILE, COMMIT, AND PUSH MAIN ===")
    with open("config.txt", "w") as f:
        f.write("Environment: production\nTimeout: 30\n")
    run_command("git add config.txt")
    run_command('git commit -m "Initial commit on main with base config"')
    run_command("git push -u origin main")

    print("\n=== STEP 4: CREATE PR FEATURE BRANCH & PUSH ===")
    run_command("git switch -c feature/add-database-config")
    
    # Create database configuration file for PR exercise
    with open("db_config.txt", "w") as f:
        f.write("DB_HOST=localhost\nDB_PORT=5432\n")
    
    run_command("git add db_config.txt")
    run_command('git commit -m "Add initial database configuration file"')
    
    print("\n🚀 Pushing PR feature branch to GitHub...")
    run_command("git push -u origin feature/add-database-config")

    print("\n==================================================")
    print("🎉 SCRIPT COMPLETED! NOW DO YOUR PULL REQUEST:")
    print("1. Open your GitHub repository in your web browser.")
    print("2. Click the green 'Compare & pull request' button.")
    print("3. Title it 'Add Database Configuration' and click 'Create pull request'.")
    print("4. Review the files changed, then click 'Merge pull request'.")
    print("==================================================")

if __name__ == "__main__":
    main()