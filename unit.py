from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint

from equipment import Weapon, Armor
from classes import UnitClass
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self.is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def equip_armor(self, armor: Armor):
        self.armor = armor

    def _count_damage(self, target: BaseUnit) -> int:
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack

        if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        if damage > 0:
            self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self.is_skill_used:
            return 'Навык уже был использован'

        result = self.unit_class.skill.use(self, target)
        self.is_skill_used = True
        return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina < self.weapon.stamina_per_hit:
            f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} "
                f"соперника и наносит {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} "
            f"cоперника его останавливает."
        )


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if not self.is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и "
                f"наносит Вам {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар, но "
            f"Ваш(а) {target.armor.name} его останавливает."
        )
