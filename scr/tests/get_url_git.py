import os

import git


def get_git_remote_url_gitpython(local_path):
    try:
        # Инициализируем объект репозитория по указанному пути
        repo = git.Repo(local_path)
        # Получаем URL удаленного репозитория с именем 'origin'
        remote_url = repo.remotes.origin.url
        return remote_url
    except git.exc.InvalidGitRepositoryError:
        return "Ошибка: Указанная директория не является Git-репозиторием."
    except AttributeError:
        return "Ошибка: У репозитория нет удаленного источника (remote) с именем 'origin'."


# Пример использования:
path_dir = r'C:\Users\yakovlev_nd\PycharmProjects\ArchiveIntegrator-'
print(path_dir)
repo_path = path_dir # Укажите ваш путь
url = get_git_remote_url_gitpython(repo_path)
print(f"URL репозитория: {url}")
