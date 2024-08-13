from datetime import datetime
from enum import Enum

import cattrs
import pint
from attr import asdict
from attrs import define, field, fields, has
from cattrs.gen import make_dict_structure_fn
from cattrs.strategies._class_methods import use_class_methods

ureg = pint.UnitRegistry()

DEFAULT_WEIGHT_DIVIDERS = [55.0, 70.0, 85.0, 100.0, 115.0, 130.0, 145.0, 160.0, 175.0, 190.0, 205.0]
DEFAULT_SKELETAL_MUSCLE_MASS_DIVIDERS = [70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
DEFAULT_BODY_FAT_MASS_DIVIDERS = [40.0, 60.0, 80.0, 100.0, 160.0, 220.0, 280.0, 340.0, 400.0, 460.0, 520.0]


class AverageType(str, Enum):
    BELOW_AVERAGE = "BELOW_AVERAGE"
    AVERAGE = "AVERAGE"
    ABOVE_AVERAGE = "ABOVE_AVERAGE"
    MINIMUM = "MINIMUM"  # unused


class BodyFatPercentIndicator(str, Enum):
    NO_INDICATOR = "NO_INDICATOR"
    MINIMUM_BODY_FAT = "MINIMUM_BODY_FAT"  # unused
    LOW_BODY_FAT = "LOW_BODY_FAT"  # unused
    HEALTHY_BODY_FAT = "HEALTHY_BODY_FAT"
    GOAL_SETTING_FAT = "GOAL_SETTING_FAT"
    HIGH_BODY_FAT = "HIGH_BODY_FAT"
    OBESE_BODY_FAT = "OBESE_BODY_FAT"  # unused


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"


def get_percent_body_fat_descriptor(
    percent_body_fat: float, body_fat_percent_dividers: list[float]
) -> BodyFatPercentIndicator:
    if not percent_body_fat or not body_fat_percent_dividers[3]:
        return BodyFatPercentIndicator.NO_INDICATOR

    if percent_body_fat < body_fat_percent_dividers[1]:
        return BodyFatPercentIndicator.HEALTHY_BODY_FAT

    if percent_body_fat < body_fat_percent_dividers[2]:
        return BodyFatPercentIndicator.GOAL_SETTING_FAT

    return BodyFatPercentIndicator.HIGH_BODY_FAT


def get_relative_descriptor(in_body_value: float, in_body_dividers: list[float]) -> AverageType:
    if in_body_value <= in_body_dividers[2]:
        return AverageType.BELOW_AVERAGE

    if in_body_value <= in_body_dividers[4]:
        return AverageType.AVERAGE

    return AverageType.ABOVE_AVERAGE


def get_body_fat_percent_dividers(age: int, gender: Gender) -> list[float]:
    if gender == Gender.MALE:
        return get_body_fat_percent_dividers_male(age)

    return get_body_fat_percent_dividers_female(age)


def get_body_fat_percent_dividers_male(age: int) -> list[float]:
    match age:
        case age if 0 <= age < 30:
            return [0.0, 13.1, 21.1, 100.0]
        case age if 30 <= age < 40:
            return [0.0, 17.1, 23.1, 100.0]
        case age if 40 <= age < 50:
            return [0.0, 20.1, 25.1, 100.0]
        case age if 50 <= age < 60:
            return [0.0, 21.1, 26.1, 100.0]
        case age if 60 <= age < 70:
            return [0.0, 22.1, 27.1, 100.0]
        case _:
            return [0.0, 0.0, 0.0, 0.0]


def get_body_fat_percent_dividers_female(age: int) -> list[float]:
    match age:
        case age if 0 <= age < 30:
            return [0.0, 19.1, 26.1, 100.0]
        case age if 30 <= age < 40:
            return [0.0, 20.1, 27.1, 100.0]
        case age if 40 <= age < 50:
            return [0.0, 22.1, 30.1, 100.0]
        case age if 50 <= age < 60:
            return [0.0, 25.1, 32.1, 100.0]
        case age if 60 <= age < 70:
            return [0.0, 26.1, 33.1, 100.0]
        case _:
            return [0.0, 0.0, 0.0, 0.0]


@define
class LeanBodyMass:
    left_arm: float = field(alias="lbmOfLeftArm")
    left_leg: float = field(alias="lbmOfLeftLeg")
    right_arm: float = field(alias="lbmOfRightArm")
    right_leg: float = field(alias="lbmOfRightLeg")
    trunk: float = field(alias="lbmOfTrunk")


@define
class LeanBodyMassPercent:
    left_arm: float = field(alias="lbmPercentOfLeftArm")
    left_leg: float = field(alias="lbmPercentOfLeftLeg")
    right_arm: float = field(alias="lbmPercentOfRightArm")
    right_leg: float = field(alias="lbmPercentOfRightLeg")
    trunk: float = field(alias="lbmPercentOfTrunk")


@define
class BodyFatMass:
    control: float = field(alias="bfmControl")
    left_arm: float = field(alias="bfmOfLeftArm")
    left_leg: float = field(alias="bfmOfLeftLeg")
    right_arm: float = field(alias="bfmOfRightArm")
    right_leg: float = field(alias="bfmOfRightLeg")
    trunk: float = field(alias="bfmOfTrunk")


@define
class BodyFatMassPercent:
    left_arm: float = field(alias="bfmPercentOfLeftArm")
    left_leg: float = field(alias="bfmPercentOfLeftLeg")
    right_arm: float = field(alias="bfmPercentOfRightArm")
    right_leg: float = field(alias="bfmPercentOfRightLeg")
    trunk: float = field(alias="bfmPercentOfTrunk")


@define
class TotalBodyWeight:
    right_arm: float = field(alias="tbwOfRightArm")
    left_arm: float = field(alias="tbwOfLeftArm")
    trunk: float = field(alias="tbwOfTrunk")
    right_leg: float = field(alias="tbwOfRightLeg")
    left_leg: float = field(alias="tbwOfLeftLeg")


@define
class IntraCellularWater:
    right_arm: float = field(alias="icwOfRightArm")
    left_arm: float = field(alias="icwOfLeftArm")
    trunk: float = field(alias="icwOfTrunk")
    right_leg: float = field(alias="icwOfRightLeg")
    left_leg: float = field(alias="icwOfLeftLeg")


@define
class ExtraCellularWater:
    right_arm: float = field(alias="ecwOfRightArm")
    left_arm: float = field(alias="ecwOfLeftArm")
    trunk: float = field(alias="ecwOfTrunk")
    right_leg: float = field(alias="ecwOfRightLeg")
    left_leg: float = field(alias="ecwOfLeftLeg")


@define()
class ExtraCellularWaterOverTotalBodyWater:
    right_arm: float = field(alias="ecwOverTBWOfRightArm")
    left_arm: float = field(alias="ecwOverTBWOfLeftArm")
    trunk: float = field(alias="ecwOverTBWOfTrunk")
    right_leg: float = field(alias="ecwOverTBWOfRightLeg")
    left_leg: float = field(alias="ecwOverTBWOfLeftLeg")


@define
class BodyCompositionData:
    member_uuid: str = field(alias="memberUUId")
    member_id: str = field(alias="memberId")
    scan_result_uuid: str = field(alias="scanResultUUId")
    inbody_id: str = field(alias="id", metadata={"description": "InBody ID, same as email address"})
    email: str
    height: str = field(metadata={"description": "Height in cm"})
    gender: Gender
    age: int
    scan_datetime: datetime = field(alias="testDatetime")
    provided_weight: float = field(
        alias="weight", metadata={"description": "Weight in pounds, provided by member at time of scan"}
    )

    lean_body_mass_details: LeanBodyMass
    lean_body_mass_percent_details: LeanBodyMassPercent

    total_body_weight: float = field(
        alias="tbw", metadata={"description": "Total body weight in pounds, based on scan results"}
    )
    dry_lean_mass: float = field(alias="dlm")
    body_fat_mass: float = field(alias="bfm")
    lean_body_mass: float = field(alias="lbm")
    skeletal_muscle_mass: float = field(alias="smm")
    body_mass_index: float = field(alias="bmi")
    percent_body_fat: float = field(alias="pbf")
    basal_metabolic_rate: float = field(alias="bmr")
    in_body_type: str = field(alias="inBodyType")

    body_fat_mass: float = field(alias="bfm")
    skeletal_muscle_mass: float = field(alias="smm")

    # excluded because they are only useful for end result of calculations
    body_fat_mass_dividers: list[float] = field(alias="bfmGraphScale", metadata={"exclude": True})
    body_fat_mass_plot_point: float = field(alias="pfatnew", metadata={"exclude": True})
    skeletal_muscle_mass_dividers: list[float] = field(alias="smmGraphScale", metadata={"exclude": True})
    skeletal_muscle_mass_plot_point: float = field(alias="psmm", metadata={"exclude": True})
    weight_dividers: list[float] = field(alias="wtGraphScale", metadata={"exclude": True})
    weight_plot_point: float = field(alias="pwt", metadata={"exclude": True})

    # excluded due to 0 values
    body_fat_mass_details: BodyFatMass = field(metadata={"exclude": True})
    body_fat_mass_percent_details: BodyFatMassPercent = field(metadata={"exclude": True})
    total_body_weight_details: TotalBodyWeight = field(metadata={"exclude": True})
    intra_cellular_water_details: IntraCellularWater = field(metadata={"exclude": True})
    extra_cellular_water_details: ExtraCellularWater = field(metadata={"exclude": True})
    extra_cellular_water_over_total_body_water_details: ExtraCellularWaterOverTotalBodyWater = field(
        alias="ecwOverTBW", metadata={"exclude": True}
    )
    visceral_fat_level: float = field(alias="vfl", metadata={"exclude": True})
    visceral_fat_area: float = field(alias="vfa", metadata={"exclude": True})
    body_comp_measurement: float = field(alias="bcm", metadata={"exclude": True})
    total_body_weight_over_lean_body_mass: float = field(alias="tbwOverLBM")
    intracellular_water: float = field(alias="icw", metadata={"exclude": True})
    extracellular_water: float = field(alias="ecw", metadata={"exclude": True})
    lean_body_mass_control: float = field(alias="lbmControl", metadata={"exclude": True})

    def _unstructure(self):
        data = asdict(self)

        for f in fields(type(self)):
            if f.metadata.get("exclude"):
                data.pop(f.name, None)

        return data

    @classmethod
    def _structure(cls, data: dict):
        c = cattrs.Converter()
        c.register_structure_hook(datetime, lambda v, _: datetime.fromisoformat(v))
        c.register_structure_hook_factory(has, lambda cl: make_dict_structure_fn(cl, c, _cattrs_use_alias=True))
        use_class_methods(c, "_structure", "_unstructure")

        for f in fields(cls):
            if has(f.type):
                sub_data = c.structure(data, f.type)
                data[f.alias] = sub_data
                for k in fields(f.type):
                    data.pop(k.alias, None)
            elif f.alias in ["wtGraphScale", "smmGraphScale", "bfmGraphScale"]:
                data[f.alias] = [float(i) for i in data[f.alias].split(";")]
            elif f.alias == "tbw":
                val = data.pop(f.alias, None)
                data[f.alias] = ureg.Quantity(val, ureg.kilogram).to(ureg.pound).magnitude
            elif f.alias == "member_id":
                data[f.alias] = str(data.pop(f.alias))

        known_data = {k: v for k, v in data.items() if k in [f.alias for f in fields(cls)]}

        return cls(**known_data)

    @property
    def body_fat_mass_relative_descriptor(self) -> AverageType:
        """Get the relative descriptor for the body fat mass plot point.

        For this item, a lower value is better.

        Returns:
            AverageType: The relative descriptor for the body fat mass plot point
        """
        dividers = self.body_fat_mass_dividers or DEFAULT_BODY_FAT_MASS_DIVIDERS
        return get_relative_descriptor(self.body_fat_mass_plot_point, dividers)

    @property
    def skeletal_muscle_mass_relative_descriptor(self) -> AverageType:
        """Get the relative descriptor for the skeletal muscle mass plot point.

        For this item, a higher value is better.

        Returns:
            AverageType: The relative descriptor for the skeletal muscle mass plot point

        """
        dividers = self.skeletal_muscle_mass_dividers or DEFAULT_SKELETAL_MUSCLE_MASS_DIVIDERS
        return get_relative_descriptor(self.skeletal_muscle_mass_plot_point, dividers)

    @property
    def weight_relative_descriptor(self) -> AverageType:
        """Get the relative descriptor for the weight plot point.

        For this item, a lower value is better.

        Returns:
            AverageType: The relative descriptor for the weight
        """
        dividers = self.weight_dividers or DEFAULT_WEIGHT_DIVIDERS
        return get_relative_descriptor(self.weight_plot_point, dividers)

    @property
    def body_fat_percent_relative_descriptor(self) -> BodyFatPercentIndicator:
        """Get the relative descriptor for the percent body fat.

        Returns:
            BodyFatPercentIndicator: The relative descriptor for the percent body fat
        """
        return get_percent_body_fat_descriptor(
            self.percent_body_fat, get_body_fat_percent_dividers(self.age, self.gender)
        )


@define
class BodyCompositionList:
    data: list[BodyCompositionData]
