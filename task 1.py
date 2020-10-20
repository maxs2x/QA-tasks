import aiohttp
import asyncio
import time


async def request(client):
    """
    :param client: session aiohtp
    :return: resp.json - dictionary response jsone
    """
    params = {'sort': 'volume_24h',
              'limit': '10'}
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': '3ec21ba8-08c5-4f41-8215-c2d3d1249f4a'}

    async with client.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
                          params=params,
                          headers=headers) as resp:
        assert resp.status == 200
        return await resp.json()


async def validation_time():
    """
    выполняем проверку на длительность ответа от сервера
    :return: time_and_json - array содержит в первой ячейке время за которое выполнился запрос, во торой dictionary response jsone
    """
    max_time_response = 0.5
    async with aiohttp.ClientSession() as client:
        start = time.time()
        json = await request(client)
        end = time.time()
        bench = end - start
        time_and_json = [max_time_response, json]
        if max_time_response > bench:
            time_and_json[0] = bench
        return time_and_json



async def validation_data(json):
    """
    смотрим что бы обновления данных на сервере о каждом из 10 тикеров было менее 24 часов назад
    :param json: dictionary response jsone
    :return:
    """
    now_day = int(time.asctime()[8:-14])
    now_h = int(time.asctime()[11:-11])
    data = json['data']
    for i in range(len(data)):
        update_day = int(data[i]['last_updated'][8:10])
        update_h = int(data[i]['last_updated'][11:13])
        if now_day - update_day == 0:
            return True
        elif now_day - update_day < 2:
            if update_h - now_h <= 0:
                return True
        else:
            return False


async def validation_size(json):
    """
    конвертируем ответ от сервера в строку и смотрим размер в байтах
    :param json: dictionary response jsone
    :return:
    """
    string = ' '.join([f'{key}:{value}' for key, value in json.items()])
    size_response = getsizeof(string)
    if size_response < 10000:
        return True


async def validation_response():
    """
    если одно из условий не выполнено, записываем баг
    :return: valid_time_and_json - массив с багами
    """
    bug_report = []
    valid_time_and_json = await validation_time()
    valid_data = await validation_data(valid_time_and_json[1])
    valid_size = await validation_size(valid_time_and_json[1])

    if valid_time_and_json[0] == 0.5:
        bug_report.append('long respons server')
    if valid_data == False:
        bug_report.append('data is out of date')
    if valid_size != True:
        bug_report.append('size response out of range')
    if len(bug_report) != 0:
        valid_time_and_json.append(bug_report)

    return valid_time_and_json


async def validation_stage_2(history_banchmark, history_bug_report):
    """
    находим количество ответов от сервера дольше 450мс и среднее значение rps
    проверяем наличие багов в предидущих шагах
    :param history_banchmark: массив длительности ответов от сервера
    :param history_bug_report: массив предидущих баг-репортов
    :return:
    """
    print(history_banchmark)
    bug_report_stage_2 = []
    latency_case = 0
    all_time_response = 0
    for i in range(1, len(history_banchmark) + 1):
        if 0.45 >= int(history_banchmark[i - 1]):
            latency_case += 1
            all_time_response += history_banchmark[i - 1]
    latency = latency_case / len(history_banchmark) * 100
    rps = 1 / (all_time_response  / len(history_banchmark))
    if len(history_bug_report) != 0:
        for elem in history_bug_report:
            bug_report_stage_2.append(elem)
    if latency < 80:
        bug_report_stage_2.append('latency < 80%')
    if rps <= 5:
        bug_report_stage_2.append('rps < 5')
    return bug_report_stage_2


async def main(repeat):
    history_banchmark = []
    history_bug_report = []
    for i in range(repeat):
        info_about_case = await validation_response()
        if len(info_about_case) > 2:
            history_bug_report.append(info_about_case[2])
        history_banchmark.append(info_about_case[0])
    bug_report_stage_2 = await validation_stage_2(history_banchmark, history_bug_report)
    if len(bug_report_stage_2) == 0:
        print('Test complesat PASS')
    else:
        for elem in bug_report_stage_2:
            print(elem)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(8))