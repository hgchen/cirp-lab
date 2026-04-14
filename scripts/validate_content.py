#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
NEWS_PATH = ROOT_DIR / "news.md"
MEMBERS_PATH = ROOT_DIR / "members.md"
PROJECTS_PATH = ROOT_DIR / "projects.md"
PROJECTS_IMAGE_DIR = ROOT_DIR / "images" / "projects"
URL_FIELDS = {"website", "scholar", "github", "linkedin", "cv"}
FIELD_PATTERN = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
PROJECT_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def is_valid_url(value: str) -> bool:
    return value.startswith("https://") or value.startswith("http://")


def validate_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_news(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    current: dict[str, object] | None = None
    seen_header = False
    seen_items: set[tuple[str, str]] = set()

    def flush_current() -> None:
        nonlocal current
        if not current:
            return
        if current["body_lines"] == 0:
            errors.append(
                f"{path.name}:{current['line']}: news item '{current['title']}' must include at least one body line."
            )
        current = None

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r")
        trimmed = line.strip()

        if not trimmed:
            continue

        if not seen_header:
            seen_header = True
            if trimmed != "# News":
                errors.append(f"{path.name}:{lineno}: first non-empty line must be '# News'.")
            continue

        if trimmed.startswith("## "):
            flush_current()
            payload = trimmed[3:].strip()
            if "|" not in payload:
                errors.append(
                    f"{path.name}:{lineno}: use '## YYYY-MM-DD | Title' for each news heading."
                )
                current = {"date": "", "title": payload, "body_lines": 0, "line": lineno}
                continue

            date_text, title = [part.strip() for part in payload.split("|", 1)]
            if not validate_date(date_text):
                errors.append(
                    f"{path.name}:{lineno}: '{date_text}' is not a valid date. Use YYYY-MM-DD in the heading."
                )
            if not title:
                errors.append(f"{path.name}:{lineno}: news title cannot be empty.")

            duplicate_key = (date_text.casefold(), title.casefold())
            if duplicate_key in seen_items:
                errors.append(
                    f"{path.name}:{lineno}: duplicate news item '{title}' on {date_text}."
                )
            seen_items.add(duplicate_key)
            current = {"date": date_text, "title": title, "body_lines": 0, "line": lineno}
            continue

        if trimmed == "---":
            flush_current()
            continue

        if current is None:
            errors.append(
                f"{path.name}:{lineno}: text must be inside a news item. Start a new item with '## YYYY-MM-DD | Title'."
            )
            continue

        current["body_lines"] = int(current["body_lines"]) + 1

    if not seen_header:
        errors.append(f"{path.name}: file is empty.")

    flush_current()
    return errors


def validate_members(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    seen_header = False
    current_category: dict[str, object] | None = None
    current_member: dict[str, object] | None = None
    seen_categories: set[str] = set()
    seen_members: set[str] = set()

    def flush_member() -> None:
        nonlocal current_member
        if current_member is None:
            return
        current_member = None

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r")
        trimmed = line.strip()

        if not trimmed:
            continue

        if not seen_header:
            seen_header = True
            if trimmed != "# Members":
                errors.append(f"{path.name}:{lineno}: first non-empty line must be '# Members'.")
            continue

        if trimmed.startswith("## "):
            flush_member()
            category_name = trimmed[3:].strip()
            if not category_name:
                errors.append(f"{path.name}:{lineno}: category heading cannot be empty.")
                continue
            if category_name.casefold() in seen_categories:
                errors.append(f"{path.name}:{lineno}: duplicate category '{category_name}'.")
            seen_categories.add(category_name.casefold())
            current_category = {"name": category_name}
            continue

        if trimmed.startswith("### "):
            if current_category is None:
                errors.append(
                    f"{path.name}:{lineno}: member heading must appear inside a category started with '## '."
                )
                continue
            flush_member()
            member_name = trimmed[4:].strip()
            if not member_name:
                errors.append(f"{path.name}:{lineno}: member name cannot be empty.")
                continue
            if member_name.casefold() in seen_members:
                errors.append(f"{path.name}:{lineno}: duplicate member '{member_name}'.")
            seen_members.add(member_name.casefold())
            current_member = {"name": member_name, "fields": set()}
            continue

        if trimmed == "---":
            flush_member()
            continue

        match = FIELD_PATTERN.match(trimmed)
        if match:
            key = match.group(1).lower()
            value = match.group(2).strip()

            if current_member is not None:
                fields = current_member["fields"]
                if key in fields:
                    errors.append(
                        f"{path.name}:{lineno}: duplicate '{key}' field for member '{current_member['name']}'."
                    )
                fields.add(key)

                if key == "image" and value:
                    image_path = ROOT_DIR / value
                    if not image_path.exists():
                        errors.append(
                            f"{path.name}:{lineno}: image path '{value}' does not exist."
                        )
                if key in URL_FIELDS and value and not is_valid_url(value):
                    errors.append(
                        f"{path.name}:{lineno}: field '{key}' must use an absolute http(s) URL."
                    )
                if key == "email" and value and "@" not in value:
                    errors.append(
                        f"{path.name}:{lineno}: email field for '{current_member['name']}' does not look valid."
                    )
                continue

            if current_category is not None:
                continue

            errors.append(
                f"{path.name}:{lineno}: field '{key}' must appear inside a category or member block."
            )
            continue

        if current_member is not None or current_category is not None:
            continue

        errors.append(
            f"{path.name}:{lineno}: text must appear inside a category or member block."
        )

    if not seen_header:
        errors.append(f"{path.name}: file is empty.")

    return errors


def validate_projects(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    seen_header = False
    current_category: dict[str, object] | None = None
    current_project: dict[str, object] | None = None
    seen_categories: set[str] = set()
    seen_projects: set[str] = set()

    def flush_project() -> None:
        nonlocal current_project
        if current_project is None:
            return
        if "folder" not in current_project["fields"]:
            errors.append(
                f"{path.name}:{current_project['line']}: project '{current_project['name']}' must include a 'folder' field."
            )
        current_project = None

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r")
        trimmed = line.strip()

        if not trimmed:
            continue

        if not seen_header:
            seen_header = True
            if trimmed != "# Projects":
                errors.append(f"{path.name}:{lineno}: first non-empty line must be '# Projects'.")
            continue

        if trimmed.startswith("## "):
            flush_project()
            category_name = trimmed[3:].strip()
            if not category_name:
                errors.append(f"{path.name}:{lineno}: category heading cannot be empty.")
                continue
            if category_name.casefold() in seen_categories:
                errors.append(f"{path.name}:{lineno}: duplicate category '{category_name}'.")
            seen_categories.add(category_name.casefold())
            current_category = {"name": category_name}
            continue

        if trimmed.startswith("### "):
            if current_category is None:
                errors.append(
                    f"{path.name}:{lineno}: project heading must appear inside a category started with '## '."
                )
                continue
            flush_project()
            project_name = trimmed[4:].strip()
            if not project_name:
                errors.append(f"{path.name}:{lineno}: project name cannot be empty.")
                continue
            if project_name.casefold() in seen_projects:
                errors.append(f"{path.name}:{lineno}: duplicate project '{project_name}'.")
            seen_projects.add(project_name.casefold())
            current_project = {"name": project_name, "line": lineno, "fields": set()}
            continue

        if trimmed == "---":
            flush_project()
            continue

        match = FIELD_PATTERN.match(trimmed)
        if match:
            key = match.group(1).lower()
            value = match.group(2).strip()

            if current_project is not None:
                fields = current_project["fields"]
                if key in fields:
                    errors.append(
                        f"{path.name}:{lineno}: duplicate '{key}' field for project '{current_project['name']}'."
                    )
                fields.add(key)

                if key == "folder" and value:
                    folder_path = PROJECTS_IMAGE_DIR / value
                    if not folder_path.is_dir():
                        errors.append(
                            f"{path.name}:{lineno}: project folder 'images/projects/{value}' does not exist."
                        )
                    elif not any(
                        child.is_file() and child.suffix.lower() in PROJECT_IMAGE_SUFFIXES
                        for child in folder_path.iterdir()
                    ):
                        errors.append(
                            f"{path.name}:{lineno}: project folder 'images/projects/{value}' does not contain supported images."
                        )
                continue

            if current_category is not None:
                continue

            errors.append(
                f"{path.name}:{lineno}: field '{key}' must appear inside a category or project block."
            )
            continue

        if current_project is not None or current_category is not None:
            continue

        errors.append(
            f"{path.name}:{lineno}: text must appear inside a category or project block."
        )

    if not seen_header:
        errors.append(f"{path.name}: file is empty.")

    flush_project()
    return errors


def main() -> int:
    errors = [
        *validate_news(NEWS_PATH),
        *validate_members(MEMBERS_PATH),
        *validate_projects(PROJECTS_PATH),
    ]

    if errors:
        print("Content validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("Validated news.md, members.md, and projects.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
