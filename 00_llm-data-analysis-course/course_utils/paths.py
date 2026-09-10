from pathlib import Path


def get_project_root():
    current = Path.cwd().resolve()

    for path in (current, *current.parents):
        if (path / "data").is_dir():
            return path

    raise FileNotFoundError("data 폴더가 있는 프로젝트 루트를 찾을 수 없습니다.")


def get_data_dir():
    return get_project_root() / "data" / "raw"


def get_report_dir():
    return get_project_root() / "reports"


def get_prompt_dir():
    return get_project_root() / "prompts"