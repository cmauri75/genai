from typing import TypedDict, Union, Optional, Any

#Tipizzazione in python
class Movie(TypedDict):
    name: str
    year: int
    director: str
    cast: list[str]
movieNT = {"name":"Avenger endgame", "year":2019, "director":"Anthony Russo, Joe Russo", "cast":["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth", "Scarlett Johansson"]}
print(movieNT["name"])

movie = Movie(name="Avenger endgame", year=2019, director="Anthony Russo, Joe Russo", cast=["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth", "Scarlett Johansson"])

movie["director"]="A"
print(movie)


# Union is used to specify that a variable can be of multiple types
def square(x: Union[int, float]) -> float: return x*x;
x=5
print(f"The square of {x} is {square(x)}")

#Optional is used to specify that a variable can be of a certain type or None
def nice_message(name: Optional[str]) -> str:
    if name is None:
        return "Hello, World!"
    else:
        return f"Hello, {name}!"

print(nice_message(movieNT["name"]))
print(nice_message(None))

#Any is used to specify that a variable can be of any type
def print_value(value: Any) -> None:
    print(f"The value is: {value}")

#lambda is a small anonymous function
add = lambda x, y: x + y
add(5, 3)
nums = [1, 2, 3]
list(map(lambda x: x*x, nums))
