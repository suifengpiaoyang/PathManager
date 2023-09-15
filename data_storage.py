import json
import os


class JsonDb(dict):

    def __init__(self, data):
        super().__init__(data)
        self.data = self

    @classmethod
    def from_json(cls, file):
        with open(file, 'r', encoding='utf-8')as fl:
            data = json.load(fl)
        return cls(data)

    def pretty_print(self):
        print(json.dumps(self, indent=4, ensure_ascii=False))

    def save(self, file):
        with open(file, 'w', encoding='utf-8')as fl:
            json.dump(self, fl, indent=4, ensure_ascii=False)


class ConfigStorage(JsonDb):

    @classmethod
    def from_json(cls, file):
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8')as fl:
                data = json.load(fl)
        else:
            data = {}
        return cls(data)


class DataStorage(JsonDb):

    @classmethod
    def from_json(cls, file):
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8')as fl:
                data = json.load(fl)
            data['totalCount'] = len(data['dataList'])
        else:
            data = {'totalCount': 0, 'dataList': []}
        return cls(data)

    def add_empty_item(self):
        """
        :type item: dict
        """
        self.data['dataList'].append({'name': '', 'path': '', 'comment': ''})
        self.data['totalCount'] += 1

    def delete_item(self, index):
        self.data['dataList'].pop(index)
        self.data['totalCount'] -= 1

    def get_data_from_index(self, index, key=None):
        data = self.data['dataList'][index]
        return data if key is None else data[key]

    def handle_drop_items(self, urlist):
        for QUrl in urlist:
            path = QUrl.toLocalFile()
            filename = os.path.basename(path)
            datalist = {
                'name': filename,
                'path': path
            }
            self.data['dataList'].append(datalist)
            self.data['totalCount'] += 1

    def move_row(self, startrow, endrow):
        pop_dict = self.data['dataList'].pop(startrow)
        self.data['dataList'].insert(endrow, pop_dict)

    def move_first(self, index):
        data = self.data['dataList'].pop(index)
        self.data['dataList'].insert(0, data)

    def move_last(self, index):
        data = self.data['dataList'].pop(index)
        self.data['dataList'].append(data)

    @property
    def datalist(self):
        # only for read
        return self.data.get('dataList', {})

    @property
    def total_count(self):
        return self.data['totalCount']


if __name__ == '__main__':
    d = JsonDb({'a': 1})
    print(d)
