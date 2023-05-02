class Quiz:
    def __init__(self, name):
        self.name = name
        self.is_start = False


def country_check(text):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        for line in f.read().splitlines()[1:]:
            name, action, industry, country, rus_name = line.split(";")
            if country == text:
                return True
    return False


def name_check(text):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        for line in f.read().splitlines()[1:]:
            name, action, industry, country, rus_name = line.split(";")
            if name == text:
                return True
    return False


def get_info(name_info='', country_info=''):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        if name_info != '':
            for line in f.read().splitlines()[1:]:
                name, action, industry, country, rus_name = line.split(";")
                if name_info == name:
                    if rus_name == 'None':
                        return [name, action, industry, country]
                    else:
                        return [name, action, industry, country, rus_name]

        elif country_info != '':
            res = []
            cnt = 0
            for line in f.read().splitlines()[1:]:
                name, action, industry, country, rus_name = line.split(";")
                if country_info == country and cnt < 100:
                    res.append(name)
                    cnt += 1
            return res


def get_countries():
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        lines = []
        for line in f.read().splitlines()[1:]:
            name, action, industry, country, rus_name = line.split(";")
            if country not in lines:
                lines += [f'{country}']
        return sorted(lines)


def write_rus_name(name_info, rus_name_info):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        lines = []
        for line in f.read().splitlines():
            name, action, industry, country, rus_name = line.split(";")
            if name_info == name:
                new_line = f'{name};{action};{industry};{country};{rus_name_info}'
                lines += [new_line]
            else:
                lines += [line]
    with open("./data/brands.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def rebranded():
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        lines = []
        for line in f.read().splitlines()[1:]:
            name, action, industry, country, rus_name = line.split(";")
            if rus_name != 'None':
                lines += [f'{name} ➡ {rus_name}']
        return "\n\n".join(lines)
