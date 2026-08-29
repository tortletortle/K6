# -*- coding: utf-8 -*-
"""
Combine refined SiYuan topic notes into a single importable Markdown file,
without rewriting individual topic files.
"""
from pathlib import Path

ROOT = Path(r"D:\spot\K6\siyuan_university_physics")
TOPICS = ROOT / "siyuan_topics_refined"
OUT = ROOT / "siyuan_import_verified.md"

ORDER = [
    "00_foundations.md",
    "01_kinematics.md",
    "02_newtonian_mechanics.md",
    "03_momentum_energy.md",
    "04_rigid_body_rotation.md",
    "05_gravitation.md",
    "06_thermodynamics.md",
    "07_kinetic_theory.md",
    "08_electrostatics.md",
    "09_conductors_dielectrics.md",
    "10_steady_current.md",
    "11_magnetostatics.md",
    "12_magnetic_materials.md",
    "13_em_induction_em_field.md",
    "14_mechanical_oscillation.md",
    "15_mechanical_waves.md",
    "16_em_oscillation_waves.md",
    "17_wave_optics.md",
    "18_relativity.md",
    "19_quantum_physics.md",
    "20_physics_and_technology.md",
    "A_constants_units.md",
]


def build_header() -> str:
    return "\n".join(
        [
            "# 大学物理（思源导入版）",
            "",
            "**目录**",
            "- [00 基础工具与物理量](#toc-00)",
            "- [01 质点运动学](#toc-01)",
            "- [02 牛顿力学](#toc-02)",
            "- [03 动量与能量](#toc-03)",
            "- [04 刚体转动](#toc-04)",
            "- [05 万有引力](#toc-05)",
            "- [06 热力学](#toc-06)",
            "- [07 气体动理论](#toc-07)",
            "- [08 静电场](#toc-08)",
            "- [09 静电场中的导体与电介质](#toc-09)",
            "- [10 恒定电流](#toc-10)",
            "- [11 磁场](#toc-11)",
            "- [12 磁场中的磁介质](#toc-12)",
            "- [13 电磁感应 电磁场](#toc-13)",
            "- [14 机械振动](#toc-14)",
            "- [15 机械波](#toc-15)",
            "- [16 电磁振荡和电磁波](#toc-16)",
            "- [17 波动光学](#toc-17)",
            "- [18 相对论](#toc-18)",
            "- [19 量子物理](#toc-19)",
            "- [20 物理学与新技术](#toc-20)",
            "- [A 常数与公式](#toc-A)",
        ]
    )


def main() -> None:
    parts = [build_header()]
    for name in ORDER:
        parts.append((TOPICS / name).read_text(encoding="utf-8").strip())
    OUT.write_text("\n\n---\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
