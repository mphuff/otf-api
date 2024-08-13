from datetime import datetime
from typing import Any

from attrs import define, field


@define
class MetricEntry:
    title: str = field(alias="Title")
    equipment_id: int = field(alias="EquipmentId")
    entry_type: str = field(alias="EntryType")
    metric_key: str = field(alias="MetricKey")
    min_value: str = field(alias="MinValue")
    max_value: str = field(alias="MaxValue")


@define
class BenchmarkHistory:
    studio_name: str = field(alias="StudioName")
    equipment_id: int = field(alias="EquipmentId")
    result: float | str = field(alias="Result")
    date_created: datetime = field(alias="DateCreated")
    date_updated: datetime = field(alias="DateUpdated")
    class_time: datetime = field(alias="ClassTime")
    challenge_sub_category_id: None = field(alias="ChallengeSubCategoryId")
    class_id: int = field(alias="ClassId")
    substitute_id: int | None = field(alias="SubstituteId")
    weight_lbs: int = field(alias="WeightLBS")
    class_name: str = field(alias="ClassName")
    coach_name: str = field(alias="CoachName")
    coach_image_url: str = field(alias="CoachImageUrl")
    workout_type_id: None = field(alias="WorkoutTypeId")
    workout_id: None = field(alias="WorkoutId")
    linked_challenges: list[Any] = field(alias="LinkedChallenges")  # not sure what this will be, never seen it before


@define
class ChallengeHistory:
    challenge_objective: str = field(alias="ChallengeObjective")
    challenge_id: int = field(alias="ChallengeId")
    studio_id: int = field(alias="StudioId")
    studio_name: str = field(alias="StudioName")
    start_date: datetime = field(alias="StartDate")
    end_date: datetime = field(alias="EndDate")
    total_result: float | str = field(alias="TotalResult")
    is_finished: bool = field(alias="IsFinished")
    benchmark_histories: list[BenchmarkHistory] = field(alias="BenchmarkHistories")


@define
class ChallengeTrackerDetail:
    challenge_category_id: int = field(alias="ChallengeCategoryId")
    challenge_sub_category_id: None = field(alias="ChallengeSubCategoryId")
    equipment_id: int = field(alias="EquipmentId")
    equipment_name: str = field(alias="EquipmentName")
    metric_entry: MetricEntry = field(alias="MetricEntry")
    challenge_name: str = field(alias="ChallengeName")
    logo_url: str = field(alias="LogoUrl")
    best_record: float | str = field(alias="BestRecord")
    last_record: float | str = field(alias="LastRecord")
    previous_record: float | str = field(alias="PreviousRecord")
    unit: str | None = field(alias="Unit")
    goals: None = field(alias="Goals")
    challenge_histories: list[ChallengeHistory] = field(alias="ChallengeHistories")


@define
class ChallengeTrackerDetailList:
    details: list[ChallengeTrackerDetail]
