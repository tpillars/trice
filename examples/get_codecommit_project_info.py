from subprocess import call
from re import match
import csv


def get_repo_info():
    """Return .txt with every 'repositoryName' and 'repositoryId'"""
    file = open("data/aws-list-repositories-output.txt", "w")
    call(
        [
            "aws",
            "codecommit",
            "list-repositories",
        ],
        stdout=file,
    )
    file.close()


def make_repo_list():
    """Return consise list of unique repo project names (including date and user)"""
    # setting variables
    repo_str = '"repositoryName":'
    repo_list = []
    # read file with repo info
    file = open("data/aws-list-repositories-output.txt", "r")
    lines = file.readlines()
    # add unique project name to repo list
    for line in lines:
        split_line = line.split()
        if split_line[0] == repo_str:
            repo_name = split_line[1].strip(",").strip('"')
            if repo_name in repo_list:
                pass
            else:
                repo_list.append(repo_name)
    return repo_list


def repo_table(repo_list, user_list):
    """Format of repo must be <0000-00>-<unique-name>-<user>
    # setting variables
    format = "^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[a-z]"
    with open("results/repo-table.csv", "w") as file:
        header = ["date", "project", "user"]
        writer = csv.writer(file)
        writer.writerow(header)
        for repo in repo_list:
            if match(format, repo):
                date = repo[:7]
                user = repo.split("-")[-1]
                if user in user_list:
                    project_and_user = repo[8:]
                    project = project_and_user.rsplit("-", 1)[0]

                    writer.writerow([date, project, user])
                if user not in user_list:
                    project = repo[8:]
                    writer.writerow([date, project, "NA"])
            else:  # if the regular expression does not match
                project = repo
                writer.writerow(["NA", project, "NA"])
    file.close()
