from abc import ABC, abstractmethod
import json
from datetime import datetime
from typing import Dict, List, Union, Optional


class Animal(ABC):
    def __init__(self, name: str, age: int, species: str):
        self.name = name
        self.age = age
        self.species = species
        self.health = 100
        self.hunger = 0

    @abstractmethod
    def make_sound(self) -> str:
        pass

    def eat(self, food_amount: int) -> str:
        self.hunger = max(0, self.hunger - food_amount)
        return f"{self.name} has eaten. Hunger level: {self.hunger}"

    def to_dict(self) -> Dict[str, Union[str, int, float, bool]]:
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age,
            "species": self.species,
            "health": self.health,
            "hunger": self.hunger
        }


class Bird(Animal):
    def __init__(self, name: str, age: int, species: str, wingspan: float):
        super().__init__(name, age, species)
        self.wingspan = wingspan

    def make_sound(self) -> str:
        return f"{self.name} chirps: Tweet tweet!"

    def fly(self) -> str:
        return f"{self.name} is flying with its {self.wingspan}m wingspan!"

    def to_dict(self) -> Dict[str, Union[str, int, float, bool]]:
        data = super().to_dict()
        data["wingspan"] = self.wingspan
        return data


class Mammal(Animal):
    def __init__(self, name: str, age: int, species: str, fur_color: str):
        super().__init__(name, age, species)
        self.fur_color = fur_color

    def make_sound(self) -> str:
        return f"{self.name} roars: Roar!"

    def run(self) -> str:
        return f"{self.name} is running on its legs!"

    def to_dict(self) -> Dict[str, Union[str, int, float, bool]]:
        data = super().to_dict()
        data["fur_color"] = self.fur_color
        return data


class Reptile(Animal):
    def __init__(self, name: str, age: int, species: str, is_venomous: bool):
        super().__init__(name, age, species)
        self.is_venomous = is_venomous

    def make_sound(self) -> str:
        return f"{self.name} hisses: Hiss!"

    def crawl(self) -> str:
        return f"{self.name} is crawling!"

    def to_dict(self) -> Dict[str, Union[str, int, float, bool]]:
        data = super().to_dict()
        data["is_venomous"] = self.is_venomous
        return data


class Employee(ABC):
    def __init__(self, name: str, id_number: str, specialization: str):
        self.name = name
        self.id_number = id_number
        self.specialization = specialization

    @abstractmethod
    def work(self) -> str:
        pass

    def to_dict(self) -> Dict[str, str]:
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "id_number": self.id_number,
            "specialization": self.specialization
        }


class ZooKeeper(Employee):
    def __init__(self, name: str, id_number: str, specialization: str):
        super().__init__(name, id_number, specialization)

    def work(self) -> str:
        return f"Zookeeper {self.name} is taking care of the animals"

    def feed_animal(self, animal: Animal, food_amount: int) -> str:
        result = animal.eat(food_amount)
        return f"Zookeeper {self.name} fed {animal.name}. {result}"


class Veterinarian(Employee):
    def __init__(self, name: str, id_number: str, specialization: str):
        super().__init__(name, id_number, specialization)

    def work(self) -> str:
        return f"Veterinarian {self.name} is checking animals' health"

    def heal_animal(self, animal: Animal) -> str:
        if animal.health < 100:
            animal.health = min(100, animal.health + 20)
            return f"Veterinarian {self.name} treated {animal.name}. Health now: {animal.health}"
        return f"{animal.name} is already healthy"


class Zoo:
    def __init__(self, name: str):
        self.name = name
        self.animals: List[Animal] = []
        self.employees: List[Employee] = []
        self.founded_date = datetime.now().strftime("%Y-%m-%d")

    def add_animal(self, animal: Animal) -> None:
        self.animals.append(animal)

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def list_animals(self) -> str:
        return "\n".join([f"{animal.species} {animal.name}" for animal in self.animals])

    def list_employees(self) -> str:
        return "\n".join([f"{employee.__class__.__name__} {employee.name}" for employee in self.employees])

    def animal_sounds(self) -> str:
        return "\n".join([animal.make_sound() for animal in self.animals])

    def save_to_file(self, filename: str) -> None:
        data = {
            "name": self.name,
            "founded_date": self.founded_date,
            "animals": [animal.to_dict() for animal in self.animals],
            "employees": [employee.to_dict() for employee in self.employees]
        }
        json.dump(data, open(filename, 'w', encoding='utf-8'), indent=4)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Zoo':
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        zoo = cls(data["name"])
        zoo.founded_date = data["founded_date"]

        # Восстановление животных
        for animal_data in data["animals"]:
            animal: Optional[Animal] = None

            if animal_data["type"] == "Bird":
                animal = Bird(animal_data["name"], animal_data["age"],
                              animal_data["species"], animal_data["wingspan"])
            elif animal_data["type"] == "Mammal":
                animal = Mammal(animal_data["name"], animal_data["age"],
                                animal_data["species"], animal_data["fur_color"])
            elif animal_data["type"] == "Reptile":
                animal = Reptile(animal_data["name"], animal_data["age"],
                                 animal_data["species"], animal_data["is_venomous"])

            if animal:
                animal.health = animal_data["health"]
                animal.hunger = animal_data["hunger"]
                zoo.add_animal(animal)

        # Восстановление сотрудников
        for employee_data in data["employees"]:
            employee: Optional[Employee] = None

            if employee_data["type"] == "ZooKeeper":
                employee = ZooKeeper(employee_data["name"], employee_data["id_number"],
                                     employee_data["specialization"])
            elif employee_data["type"] == "Veterinarian":
                employee = Veterinarian(employee_data["name"], employee_data["id_number"],
                                        employee_data["specialization"])

            if employee:
                zoo.add_employee(employee)

        return zoo


def main() -> None:
    # Создание зоопарка
    zoo = Zoo("Central Zoo")

    # Добавление животных
    eagle = Bird("Eddie", 5, "Eagle", 2.1)
    lion = Mammal("Leo", 8, "Lion", "golden")
    snake = Reptile("Sid", 3, "Python", False)

    zoo.add_animal(eagle)
    zoo.add_animal(lion)
    zoo.add_animal(snake)

    # Добавление сотрудников
    keeper = ZooKeeper("John", "ZK001", "Large mammals")
    vet = Veterinarian("Dr. Smith", "VET001", "Avian medicine")

    zoo.add_employee(keeper)
    zoo.add_employee(vet)

    # Демонстрация работы
    print("Zoo animals:")
    print(zoo.list_animals())
    print("\nZoo employees:")
    print(zoo.list_employees())
    print("\nAnimal sounds:")
    print(zoo.animal_sounds())

    # Демонстрация работы сотрудников
    print("\nEmployee actions:")
    print(keeper.feed_animal(lion, 30))
    print(vet.heal_animal(eagle))

    # Сохранение состояния зоопарка
    zoo.save_to_file("zoo_state.json")

    # Загрузка состояния зоопарка
    loaded_zoo = Zoo.load_from_file("zoo_state.json")
    print("\nLoaded zoo animals:")
    print(loaded_zoo.list_animals())


if __name__ == "__main__":
    main()