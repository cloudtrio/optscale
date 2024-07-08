import date
import uuid
from enum import Enum
from datetime import datetime, timezone
from pydantic import (
    BaseModel, BeforeValidator, ConfigDict, Field, model_validator)
from typing import List, Optional, Union
from typing_extensions import Annotated


class ArceeState:
    STARTED = 1
    FINISHED = 2
    ERROR = 3
    ABORTED = 4


class BaseClass(BaseModel):
    model_config = ConfigDict(extra='forbid')


id_ = Field(default_factory=lambda: str(uuid.uuid4()), alias='_id')
now = Field(
        default_factory=lambda: int(datetime.now(tz=timezone.utc).timestamp()))
now_ms = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc).timestamp())


class ConsolePostIn(BaseClass):
    output: str
    error: str


class Console(ConsolePostIn):
    id: str = id_
    run_id: str


class DatasetPatchIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    labels: List[str] = []
    timespan_from: Optional[int] = None
    timespan_to: Optional[int] = None


class DatasetPostIn(DatasetPatchIn):
    path: str


class Dataset(DatasetPostIn):
    id: str = id_
    token: str
    created_at: int = now
    deleted_at: int = 0


class RunPatchIn(BaseClass):
    finish: Optional[bool] = None
    tags: Optional[dict] = {}
    hyperparameters: Optional[dict] = {}
    reason: Optional[str] = None
    state: Optional[int] = None
    runset_id: Optional[str] = None
    runset_name: Optional[str] = None


class Git(BaseClass):
    remote: str
    branch: str
    commit_id: str
    status: str


class RunPostIn(BaseClass):
    name: str
    imports: list[str] = []
    git: Optional[Git] = None
    command: str


class Run(RunPostIn, RunPatchIn):
    id: str = id_
    task_id: str
    start: int = now
    number: int
    deleted_at: int = 0
    data: dict = {}
    executors: list = []
    dataset_id: Optional[str] = None
    state: int = ArceeState.STARTED
    finish: Optional[int] = None


class TaskPatchIn(BaseClass):
    metrics: Optional[List[str]] = []
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[str] = None


class LeaderboardFilter(BaseClass):
    id: str = Field(description='metric id to filter by')
    min: Optional[float] = None
    max: Optional[float] = None

    @model_validator(mode='after')
    def validate_min_max(self):
        if (self.min is None and self.max is None or
                (self.min is not None and self.max is not None and
                 self.min > self.max)):
            raise ValueError('Invalid min/max filter values')
        return self


class LeaderboardPostIn(BaseClass):
    primary_metric: str
    group_by_hp: bool
    grouping_tags: List[str] = []
    other_metrics: List[str] = []
    filters: List[LeaderboardFilter] = []
    metrics: List[str] = Field(
        [],
        description='list of metrics from primary_metric and other_metrics',
        exclude=True)

    @model_validator(mode='after')
    def validate_filters_values(self):
        metrics_ids = self.other_metrics + [self.primary_metric]
        filters_ids = [x.id for x in self.filters]
        if any(x not in metrics_ids for x in filters_ids):
            raise ValueError('Invalid filters')
        return self

    @model_validator(mode='after')
    def set_metrics(self):
        self.metrics = list(set(self.other_metrics + [self.primary_metric]))
        return self


class LeaderboardPatchIn(LeaderboardPostIn):
    primary_metric: Optional[str] = None
    group_by_hp: Optional[bool] = None

    @model_validator(mode='after')
    def set_metrics(self):
        self.metrics = list(set(self.other_metrics))
        if self.primary_metric:
            self.metrics = list(set(self.metrics + [self.primary_metric]))
        return self


class Leaderboard(LeaderboardPostIn):
    id: str = id_
    task_id: str
    token: str
    created_at: int = now
    deleted_at: int = 0

    class Config:
        allow_population_by_field_name = True


class LeaderboardDatasetPatchIn(BaseModel):
    dataset_ids: Optional[list] = []
    name: Optional[str] = None

    @staticmethod
    def remove_dup_ds_ids(kwargs):
        ds_ids = kwargs.get("dataset_ids")
        if ds_ids:
            kwargs["dataset_ids"] = list(set(ds_ids))


class LeaderboardDatasetPostIn(LeaderboardDatasetPatchIn):
    pass


class LeaderboardDataset(LeaderboardDatasetPostIn):
    id: str = id_
    token: str
    leaderboard_id: str
    created_at: int = now
    deleted_at: int = 0


class PlatformType(str, Enum):
    ali = "ali"
    aws = "aws"
    azure = "azure"
    gcp = "gcp"
    unknown = "unknown"


class InstanceLifeCycle(str, Enum):
    OnDemand = "OnDemand"
    Preemptible = "Preemptible"
    Spot = "Spot"
    Unknown = "Unknown"


class PlatformPostIn(BaseClass):
    platform_type: PlatformType
    instance_id: str
    account_id: str
    local_ip: str
    public_ip: str
    instance_lc: InstanceLifeCycle
    instance_type: str
    instance_region: str
    availability_zone: str


def filter_strings(stats: dict) -> dict:
    return {k: v for k, v in stats.items() if isinstance(v, (int, float))}


StatsData = Annotated[
    dict[str, Union[int, float]], BeforeValidator(filter_strings)]


class StatsPostIn(BaseClass):
    project: str
    run: str
    data: StatsData
    platform: PlatformPostIn


class Platform(PlatformPostIn):
    id: str = id_


class Log(BaseClass):
    project: str
    run_id: str
    data: StatsData
    instance_id: Optional[str]
    id: str = id_
    timestamp: float = now_ms


class ModelPatchIn(BaseClass):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[dict] = {}


class ModelPostIn(ModelPatchIn):
    key: str

    @model_validator(mode='after')
    def set_name(self):
        if not self.name:
            self.name = self.key
        return self


class Model(ModelPostIn):
    id: str = id_
    token: str
    created_at: int = now


class ModelVersionIn(BaseClass):
    path: Optional[str] = None
    aliases: Optional[List[str]] = []
    version: Optional[str] = None
    tags: Optional[dict] = {}

    @model_validator(mode='after')
    def set_aliases(self):
        if self.aliases:
            self.aliases = list(set(self.aliases))
        return self


class ModelVersion(ModelVersionIn):
    id: str = id_
    deleted_at: int = 0
    run_id: str
    model_id: str
    created_at: int = now


class MetricFunc(str, Enum):
    avg = "avg"
    last = "last"
    max = "max"
    sum = "sum"


class MetricTendency(str, Enum):
    less = "less"
    more = "more"


class MetricPostIn(BaseClass):
    name: Optional[str] = None
    key: str
    target_value: float
    func: MetricFunc
    tendency: MetricTendency


class MetricPatchIn(MetricPostIn):
    key: Optional[str] = None
    target_value: Optional[float] = None
    func: Optional[MetricFunc] = None
    tendency: Optional[MetricTendency] = None


class Metric(MetricPatchIn):
    id: str = id_
    token: str
