import time

import requests
import random
from copy import deepcopy
import datetime


def random_answer(answers: list, frequencies: list):
    intervals = []
    for i in range(len(frequencies) + 1):
        interval_size = 0
        for j in range(i):
            interval_size += frequencies[j]
        intervals.append(interval_size)
    if intervals[-1] != 0:
        rand = random.randint(0, intervals[-1] - 1)
    else:
        return None
    for i in range(len(intervals)):
        if intervals[i] <= rand < intervals[i + 1]:
            return answers[i]
    return answers[0]


def skip_answer(skip=0):
    if random.randint(0, 100) >= skip:
        return False
    else:
        return True


def one_in_list(answers: list, frequencies: list, skip: int):
    if skip_answer(skip):
        return None
    else:
        return random_answer(answers, frequencies)


def few_in_list(quantity_min_max: list, quantity_frequencies: list, answers: list, frequencies: list):
    quantity_min_max = list(range(quantity_min_max[0], quantity_min_max[1] + 1))
    quantity = random_answer(quantity_min_max, quantity_frequencies)
    randomized_answers = []
    answers_temp = deepcopy(answers)
    frequencies_temp = deepcopy(frequencies)
    for i in range(quantity):
        randomized_answers.append(random_answer(answers_temp, frequencies_temp))
        for j in range(len(answers_temp)):
            if answers_temp[j] == randomized_answers[-1]:
                del answers_temp[j]
                del frequencies_temp[j]
                break
    return randomized_answers


def form_arguments(names: list, quest_type: list, answers_quantity: list, quantity_frequencies: list,
                   answers: list, frequencies: list, skip: list, pages_number: int):
    arguments = {}
    for i in range(len(names)):
        if names[i] == 'entry.947852479':
            if arguments['entry.699313026'] == '14-17':
                frequencies[i] = [85, 13, 4, 0, 0, 2, 0, 0]
            elif arguments['entry.699313026'] == '18-25':
                frequencies[i] = [2, 83, 23, 6, 4, 9, 0, 0]
            elif arguments['entry.699313026'] == '26-30':
                frequencies[i] = [0, 12, 81, 1, 35, 15, 8, 1]
            elif arguments['entry.699313026'] == '31-49':
                frequencies[i] = [0, 1, 76, 0, 36, 14, 19, 1]
            elif arguments['entry.699313026'] == '50 и более':
                frequencies[i] = [0, 0, 53, 0, 39, 6, 31, 45]
            if arguments['entry.399183422'] == 'Мужской':
                frequencies[i][-2] = 0
            elif arguments['entry.399183422'] == 'Женский':
                frequencies[i][3] = 0
        if quest_type[i] == 0:
            arguments[names[i]] = one_in_list(answers[i], frequencies[i], skip[i])
        elif quest_type[i] == 1:
            arguments[names[i]] = few_in_list(answers_quantity[i], quantity_frequencies[i], answers[i], frequencies[i])
    if pages_number > 1:
        arguments['pageHistory'] = format_pages(pages_number)
    return arguments


def format_pages(pages_number: int):
    output = ''
    for i in range(pages_number):
        output += str(i) + ','
    output = output[:-1]
    return output


def time_spread(days: list, hours: list, hours_summary: int):
    current_time = datetime.datetime.utcnow()
    for i in range(len(days)):
        if current_time.day == (i + 1):
            answers_per_day = days[i]
            for j in range(len(hours)):
                if current_time.hour == (j + 1):
                    answers_per_hour_frequencies = hours[j]
                    answers_per_hour = round(float(answers_per_day) / float(hours_summary + random.randint(-100, 100)) *
                                             float(answers_per_hour_frequencies))
                    packet_per_seconds = []
                    for k in range(answers_per_hour):
                        packet_per_seconds.append(random.randint(1, 3599))
                    packet_per_seconds.sort()
                    if len(packet_per_seconds) < 1:
                        return [], current_time
                    packet_intervals_in_seconds = [packet_per_seconds[0]]
                    for k in range(1, len(packet_per_seconds)):
                        packet_intervals_in_seconds.append(packet_per_seconds[k] - packet_per_seconds[k - 1])
                    return packet_intervals_in_seconds, current_time


def send_packet(url: str, names: list, quest_type: list, answers_quantity: list, quantity_frequencies: list,
                answers: list, frequencies: list, skip: list, pages_number: int):
    arguments = form_arguments(names, quest_type, answers_quantity, quantity_frequencies, answers, frequencies, skip,
                               pages_number)
    req = requests.post(url, arguments)


def main():
    #url_ = 'https://docs.google.com/forms/d/e/1FAIpQLSfq4SD0kIkluqlX2gufZOrO00nmcEo8mAgjnfxNadP6iX0omQ/formResponse'
    url_ = 'https://docs.google.com/forms/d/e/1FAIpQLSevvfDKKo8aHr4R6rZCBe7gCQcTPQcePTOXoMYJO7SRfVjzBQ/formResponse'
    names = ['entry.1608551183', 'entry.1045417375', 'entry.696759890', 'entry.970425737', 'entry.1031736866',
             'entry.281351245', 'entry.167714288', 'entry.533949951', 'entry.747425545', 'entry.172285707',
             'entry.294216731', 'entry.186130636', 'entry.92730088', 'entry.1779683831', 'entry.1398138660',
             'entry.1136851723', 'entry.1975858287', 'entry.1514986039', 'entry.1186822588', 'entry.330050858',
             'entry.399183422', 'entry.699313026', 'entry.947852479']
    quest_type = [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    answers_quantity = [None, None, [1, 4], [2, 4], [3, 6], [2, 5], None, [2, 5], None, [1, 3], None, [3, 6], None,
                        [3, 5], None, [2, 3], None, None, None, None, None, None, None]
    quantity_frequencies = [None, None, [8, 64, 19, 9], [50, 35, 15], [53, 19, 34, 13], [46, 62, 23, 8], None,
                            [62, 42, 15, 3], None, [23, 72, 53], None, [45, 24, 24, 9], None, [35, 62, 24], None,
                            [59, 41], None, None, None, None, None, None, None]
    answers = [['Да', 'Нет'],
               ['Раз в год', 'Несколько раз в год', 'Три или более раза в год'],
               ['Социальные сети музеев', 'Наружная реклама', 'Официальные сайты музеев',
                'Интернет-реклама', 'От друзей, коллег, знакомых или членов семьи', 'Реклама на ТВ',
                'Сайты с отзывами и/или туристические сайты (2ГИС, TripAdvisor и т.д.)', 'Радио реклама',
                'Иные виды рекламной активности'],
               ['Приобщение к искусству', 'Проведение досуга', 'Совместное времяпровождение с семьёй, друзьями и т.д.',
                'Самообразование', 'Знакомство с новыми людьми', 'Получение новых эмоций',
                'Повышение своего социального статуса', 'Другое'],
               ['Направленность музея', 'Деятельность музея в интернет-пространстве', 'Разнообразие экспозиций',
                'Наличие образовательных программ на базе музея',
                'Применение новых технологий в выставочной деятельности', 'Стоимость билета', 'Расположение музея',
                'Льготные билеты (в том числе "Пушкинская карта")',
                'Развитая инклюзивная среда (доступность учреждения для людей с особенностями здоровья)',
                'Положительные отзывы от близких или от людей в интернет-пространстве',
                'Участие музея в городских и всероссийских мероприятиях',
                'Экстерьер и интерьер музея (внешнее и внутреннее оформление здания)',
                'Социально-значимая деятельность музея', 'Другое'],
               ['Мне не нравится музейный формат', 'Меня не привлекает тема искусства',
                'У меня недостаточно свободного времени',
                'У меня недостаточно информации о проводимых выставках и мероприятиях',
                'Меня не устраивает стоимость посещения',
                'Не встречал(-а) выставки/мероприятия которые бы меня заинтересовали',
                'Нет подходящей компании для посещения', 'Мне неудобно добираться до заинтересовавших меня музеев',
                'Мне не нравится атмосфера подобных учреждений', 'У меня был неприятный опыт посещения музеев',
                'Я слышал(-а) негативные отзывы от близких или от пользователей в интернет-пространстве',
                'Я предпочитаю иные формы проведения досуга', 'Другое'],
               ['1', '2', '3', '4', '5'],
               ['Внедрение VR и AR технологий (виртуальная и дополненная реальность)', 'Новые выставки',
                'Мобильное приложение для навигации по выставкам с информацией о произведениях',
                'Выступление на базе музея известной личности', 'Возможность бесплатного посещения',
                'Специальные мероприятия на базе музея (Музейная ночь, биеннале и т.д.)', 'Другое'],
               ['Да, был опыт посещения', 'Да, хочу посетить', 'Нет, был опыт посещения', 'Нет, не интересны'],
               ['Красноярский художественный музей имени В. И. Сурикова', 'Красноярский краевой краеведческий музей',
                'Красноярский культурно-исторический музейный комплекс Площадь мира', 'Музей Мемориал победы',
                'Музей-усадьба Г. В. Юдина', 'Музей-усадьба В. И. Сурикова', 'Музей художника Бориса Ряузова',
                'Литературный музей имени В. П. Астафьев', 'Пароход-музей Святитель Николай',
                'Музей геологии Центральной Сибири GEOS', 'Музей истории Красноярской железной дороги'],
               ['1', '2', '3', '4', '5'],
               ['Интерес', 'Счастье', 'Гнев', 'Печаль', 'Скука', 'Восхищение', 'Страх', 'Радость', 'Отвращение',
                'Удивление', 'Волнение', 'Раздражение', 'Покой', 'Наслаждение'],
               ['Один/одна', 'С другом/подругой', 'С младшими родственниками (дети, внуки и т.д.)',
                'В составе экскурсионной группы', 'Со взрослыми родственниками (мама, папа, бабушка, дедушка и т.д.)',
                'Со своей парой'],
               ['Месторасположение', 'Музейная коллекция', 'Стоимость билета', 'Разнообразие выставок',
                'Отношение персонала', 'Внешний вид здания музея', 'Внутреннее оформление музея',
                'Общая атмосфера учреждения', 'Задействование современных технологий в выставочной деятельности',
                'Интерактивная составляющая', 'Другое'],
               ['Самостоятельное ознакомление', 'Экскурсионное обслуживание', 'Аудиогид (выдающийся на базе музея)',
                'Аудиогид (в виде электронного приложения для смартфонов)'],
               ['ВКонтакте', 'Одноклассники', 'Телеграм', 'WhatsApp', 'Viber', 'Другое'],
               ['1', '2', '3', '4', '5'],
               ['Абсолютно согласен', 'Скорее согласен', 'Скорее не согласен', 'Абсолютно не согласен'],
               ['Да, принимал участие', 'Да, хотел бы попробовать', 'Нет, не интересен'],
               ['Текстовый', 'Видео', 'Аудио (подкасты)', 'Ничего из перечисленного'],
               ['Мужской', 'Женский'],
               ['14-17', '18-25', '26-30', '31-49', '50 и более'],
               ['Учусь в школе', 'Учусь в высшем/средне-специальном учебном заведение', 'Работаю', 'Служу',
                'Занимаюсь бизнесом/предпринимательством', 'Временно не работаю', 'Занимаюсь домохозяйством',
                'Нахожусь на пенсии']]
    frequencies = [[97, 3], [19, 45, 36], [67, 23, 32, 25, 29, 2, 12, 1, 1], [52, 50, 34, 42, 6, 27, 9, 1],
                   [59, 35, 54, 8, 26, 57, 32, 29, 2, 34, 28, 31, 15, 2],
                   [9, 6, 62, 2, 7, 42, 32, 28, 3, 1, 14, 59, 2], [5, 12, 32, 76, 39], [45, 86, 34, 7, 59, 55, 5],
                   [3, 42, 1, 34], [52, 34, 63, 12, 2, 15, 8, 4, 16, 18, 1], [1, 4, 9, 68, 68],
                   [65, 28, 1, 25, 12, 34, 1, 59, 1, 58, 11, 5, 38, 32, 0], [61, 59, 12, 9, 4, 39],
                   [39, 62, 45, 59, 48, 19, 23, 31, 9, 7, 2], [89, 19, 17, 25], [65, 9, 49, 12, 5, 32],
                   [5, 4, 25, 59, 25], [83, 25, 7, 3], [21, 65, 9], [75, 32, 12, 0], [41, 59], [15, 46, 19, 48, 3],
                   [10, 10, 10, 10, 10, 10, 10, 10]]
    skip = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pages_number = 6
    days_of_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 93, 59, 21, 39, 16, 38, 0, 0, 0, 0, 0, 0]
    hour_spread = [9, 15, 21, 18, 26, 25, 24, 19, 17, 20, 25, 31, 33, 30, 31, 28, 21, 13, 11, 7, 3, 1, 1, 2]
    hour_values_summary = 0
    for i in hour_spread:
        hour_values_summary += i
    packets_summary = 400
    packets_sent = 0
    for i in range(100):
        time.sleep(1)
        send_packet(url_, names, quest_type, answers_quantity, quantity_frequencies, answers,
                    frequencies, skip, pages_number)
        print('packet №' + str(i + 1) + ' sent')
    #while datetime.datetime.utcnow().minute != 0:
    #    print('sleep 1 sec')
    #    time.sleep(1)
    while packets_sent < packets_summary:
        intervals_of_one_hour_in_seconds, start_datetime = time_spread(days_of_month, hour_spread, hour_values_summary)
        print(intervals_of_one_hour_in_seconds)
        if len(intervals_of_one_hour_in_seconds) > 0:
            for i in range(len(intervals_of_one_hour_in_seconds)):
                time.sleep(intervals_of_one_hour_in_seconds[i])
                send_packet(url_, names, quest_type, answers_quantity, quantity_frequencies, answers,
                            frequencies, skip, pages_number)
                packets_sent += 1
                print('packet №' + str(packets_sent) + ' sent')
                if datetime.datetime.utcnow().day != start_datetime.day or datetime.datetime.utcnow().hour != start_datetime.hour:
                    break
            while datetime.datetime.utcnow().day == start_datetime.day and datetime.datetime.utcnow().hour == start_datetime.hour:
                time.sleep(10)
        else:
            while datetime.datetime.utcnow().day == start_datetime.day and datetime.datetime.utcnow().hour == start_datetime.hour:
                time.sleep(10)


if __name__ == '__main__':
    main()
