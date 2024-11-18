def intersect_intervals(interval1, interval2):
    """Находит пересечение двух временных интервалов."""
    start = max(interval1[0], interval2[0])
    end = min(interval1[1], interval2[1])
    return (start, end) if start < end else None


def merge_intervals(intervals):
    """Объединяет пересекающиеся интервалы."""
    if not intervals:
        return []
    intervals.sort()  # Сортируем интервалы по началу
    merged = [intervals[0]]

    for current in intervals[1:]:
        prev_start, prev_end = merged[-1]
        cur_start, cur_end = current

        if cur_start <= prev_end:  # Если интервалы пересекаются
            merged[-1] = (prev_start, max(prev_end, cur_end))
        else:
            merged.append(current)

    return merged


def calculate_total_time(intervals):
    """Суммирует длительность всех интервалов."""
    return sum(end - start for start, end in intervals)


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_interval = intervals['lesson']
    pupil_intervals = list(zip(intervals['pupil'][::2], intervals['pupil'][1::2]))
    tutor_intervals = list(zip(intervals['tutor'][::2], intervals['tutor'][1::2]))

    # Найти пересечение урока с учеником и учителем
    combined_intervals = []
    for pupil_interval in pupil_intervals:
        for tutor_interval in tutor_intervals:
            # Пересечение ученик x учитель
            intersect_pt = intersect_intervals(pupil_interval, tutor_interval)
            if intersect_pt:
                # Пересечение ученик x учитель x урок
                intersect_final = intersect_intervals(intersect_pt, lesson_interval)
                if intersect_final:
                    combined_intervals.append(intersect_final)

    # Объединяем пересечения
    merged_intervals = merge_intervals(combined_intervals)

    # Считаем общую продолжительность
    return calculate_total_time(merged_intervals)


# Тесты
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print("All tests passed!")
