from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем аннотации аргументов
        annotations = func.__annotations__
        # Проверяем, что количество аргументов совпадает с количеством аннотаций
        param_names = func.__code__.co_varnames[:func.__code__.co_argcount]

        for i, (arg_name, arg_value) in enumerate(zip(param_names, args)):
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' at position {i} must be of type {expected_type.__name__}, "
                        f"but got {type(arg_value).__name__}."
                    )

        # Вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper


# Пример использования
@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Тесты
print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
