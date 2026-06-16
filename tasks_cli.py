#!/usr/bin/env python3
"""Simple CLI for managing tasks: add-task and complete-task.

Usage examples:
  python tasks_cli.py add-task "Buy milk"
  python tasks_cli.py complete-task 1
  python tasks_cli.py list-tasks
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from typing import List

TASKS_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    description: str
    completed: bool = False


class TaskManager:
    def __init__(self, path: str = TASKS_FILE):
        self.path = path
        self.tasks: List[Task] = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.tasks = [Task(**t) for t in data]
            except Exception:
                self.tasks = []

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, indent=2)

    def add_task(self, description: str) -> Task:
        next_id = 1 + max((t.id for t in self.tasks), default=0)
        task = Task(id=next_id, description=description)
        self.tasks.append(task)
        self._save()
        return task

    def complete_task(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                t.completed = True
                self._save()
                return t
        raise ValueError(f"Task with id {task_id} not found")

    def list_tasks(self) -> List[Task]:
        return self.tasks


def main(argv=None):
    parser = argparse.ArgumentParser(description="Task CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add-task", help="Add a new task")
    p_add.add_argument("description", help="Task description")

    p_complete = sub.add_parser("complete-task", help="Mark a task complete")
    p_complete.add_argument("id", type=int, help="Task id")

    p_list = sub.add_parser("list-tasks", help="List all tasks")

    args = parser.parse_args(argv)
    manager = TaskManager()

    if args.cmd == "add-task":
        task = manager.add_task(args.description)
        print(f"Added task {task.id}: {task.description}")
    elif args.cmd == "complete-task":
        try:
            task = manager.complete_task(args.id)
            print(f"Completed task {task.id}: {task.description}")
        except ValueError as e:
            print(e)
            return 2
    elif args.cmd == "list-tasks":
        for t in manager.list_tasks():
            status = "✔" if t.completed else " "
            print(f"[{status}] {t.id}: {t.description}")
    else:
        parser.print_help()


if __name__ == "__main__":
    raise SystemExit(main())
