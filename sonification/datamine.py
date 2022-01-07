import requests
import csv
import json

from datetime import datetime


def userTaskEvents(site, pw, file):  # function for 6RS userTaskEvent data

    events_url = "https://{}.6river.org/cfs/task-coordinator/v1/UserTaskEvents?filter=%7B%22where%22%3A%7B%22eventType%22%3A%22putEnd%22%7D%2C%20%22limit%22%3A100%7D".format(
        site.lower())

    # locations_url = "https://{}.6river.org/cfs/asset-manager/v1/storageLocations/{}".format(
    #     site.lower())

    raw = json.loads(requests.get(events_url, auth=(site, pw)).text)

    print('Mashing...')

    with open(file, 'w') as writeFile:

        writer = csv.writer(writeFile)
        writer.writerow(['started', 'ended', 'location', 'aisle', 'quantity'])

        print('Distilling...')

        distilled = [[
            task['data']['putStartHappenedAt'],
            task['happenedAt'],
            json.loads(requests.get("https://{}.6river.org/cfs/asset-manager/v1/storageLocations/{}".format(
                site.lower(), task['data']['moveFrom']), auth=(site, pw)).text)['address'],
            json.loads(requests.get("https://{}.6river.org/cfs/asset-manager/v1/storageLocations/{}".format(
                site.lower(), task['data']['moveFrom']), auth=(site, pw)).text)['externalAisleId'],
            task['data']['quantityMoved']


        ] for task in raw if 'moveFrom' in task['data'].keys()]

        print('Maturing...')

        ordered = sorted(distilled, key=lambda task: task[0])

        for item in ordered:

            # print(item['data']['putStartHappenedAt'])

            writer.writerow(item)

        print('Done!')


userTaskEvents('MEDMAN', 'HKVzx0VxKJU0', 'soup.csv')
