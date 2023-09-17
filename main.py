import time
import json
from enum import IntEnum
from datetime import date
from dataclasses import dataclass, asdict
from typing import Optional, Dict


class Priority(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __str__(self):
        return {
            Priority.NONE: "None",
            Priority.LOW: "Low",
            Priority.MEDIUM: "Medium",
            Priority.HIGH: "High"
        }.get(self)


# Python 3.7 or higher required
@dataclass
class TodoItem:
    id: str = ""
    content: str = ""
    priority: int = 0
    done: bool = False
    due_date: Optional[date] = None

    def with_priority(self, priority):
        self.priority = priority
        return self

    def with_due_date(self, due_date):
        self.due_date = due_date
        return self

    def __str__(self):
        done_str = "x" if self.done is True else " "
        out = f"[{done_str}] {self.content}"
        if self.priority != Priority.NONE:
            out = out + f" [{Priority(self.priority)}]"
        if self.due_date is not None:
            out = out + f" ({self.due_date})"
        return out

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class TodoList:
    items: Dict[str, TodoItem]

    def print(self):
        for item in self.items.values():
            print(str(item))

    def __init__(self, items=None):
        if items is None:
            items = {}
        self.items = items

    def to_json(self) -> str:
        return json.dumps([asdict(item) for item in self.items.values()])

    @classmethod
    def from_json(cls, data: str):
        json_array = json.loads(data)
        return cls({item['id']: TodoItem.from_dict(item) for item in json_array})


if __name__ == '__main__':
    with open("todo.json", "r") as file:
        content = file.read()
        start_time = time.time_ns()
        items = TodoList.from_json(content)
        end_time = time.time_ns()
        elapsed_from = (end_time - start_time) * 0.000000001

        # items.print()

        start_time = time.time_ns()
        new_content = items.to_json()
        end_time = time.time_ns()
        elapsed_to = (end_time - start_time) * 0.000000001

        # print(new_content)

        print(f"from_json - elapsed: {elapsed_from}s, to_json - elapsed: {elapsed_to}s")