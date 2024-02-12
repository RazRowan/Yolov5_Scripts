import git
from termcolor import colored

def check_for_updates(directory: str) -> None:
    repo = git.Repo(directory)
    try:
        repo.remotes.origin.pull()
        print(colored("The repository is up to date!", "green"))
    except git.exc.GitCommandError:
        print(colored("Error pulling updates from the remote repository.", "red"))

if __name__ == "__main__":
    check_for_updates("../")

