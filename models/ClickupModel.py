from dataclasses import dataclass


@dataclass(frozen=True)
class ItemTask:
    id: int
    name: str
    description: str
    status: str
    assignee: str
    tags: list[str]
    priority: str
    due_date: str | None
    start_date: None
    points: None
    time_estimate: None
    custom_fields: list
    dependencies: list
    linked_tasks: list

    date_created: str
    date_updated: str
    date_closed: str | None
    date_done: str | None


@dataclass(frozen=True)
class ItemTeams:
    id: int
    name: str


@dataclass(frozen=True)
class ItemSpaces:
    id: int
    name: str


@dataclass(frozen=True)
class ItemList:
    id: int
    name: str


@dataclass(frozen=True)
class ItemFolder:
    id: int
    name: str

@dataclass(frozen=True)
class ItemWebhooks:
    id: str
    endpoint: str
    events: list[str]


@dataclass(frozen=True)
class HistoryWebhooks:
    event: str
    history_items: str
    events: list[str]

@dataclass(frozen=True)
class Webhooks:
    event: str
    history_items: list[HistoryWebhooks]
    task_id: str
    webhook_id: str
