project_id = 'b61f7ef9-a44e-43de-8591-7e5636da25ff'

salary_period = {
    "project_id": project_id,
    "object_type": "salary_period",
    "data": {
        "hour": {
            "name": "в час",
            "code": "hour",
            "description": "Почасовая оплата труда"
        },
        "week": {
            "name": "в неделю",
            "code": "week",
            "description": "Еженедельная оплата труда"
        },
        "month": {
            "name": "в месяц",
            "code": "month",
            "description": "Ежемесячная зарплата"
        },
        "year": {
            "name": "за год",
            "code": "year",
            "description": "Годовой оклад (часто используется на Западе)"
        },
        "project": {
            "name": "за проект",
            "code": "project",
            "description": "Одноразовая выплата за выполнение задачи"
        }
    }
}



employment_basis = {
    "project_id": project_id,
    "object_type": "employment_basis",
    "data": {
        "contract": {
            "name": "по договору (штат)",
            "code": "contract",
            "description": "Официальное трудоустройство по ТК РФ"
        },
        "selfemployed": {
            "name": "самозанятый",
            "code": "selfemployed",
            "description": "Самозанятость с уплатой налога через приложение"
        },
        "project": {
            "name": "проект (контракт)",
            "code": "project",
            "description": "По договору ГПХ или контракту на срок проекта"
        }
    }
}

employment_type = {
    "project_id": project_id,
    "object_type": "employment_type",
    "data": {
        "fulltime": {
            "name": "Полная занятость",
            "code": "fulltime",
            "description": "40 часов в неделю"
        },
        "parttime": {
            "name": "Частичная занятость",
            "code": "parttime",
            "description": "Менее 40 часов в неделю"
        },
        "internship": {
            "name": "Стажировка",
            "code": "internship",
            "description": "Обучение с возможностью трудоустройства"
        },
        "project": {
            "name": "Проектная занятость",
            "code": "project",
            "description": "На срок выполнения проекта"
        },
        "volunteer": {
            "name": "Волонтёрство",
            "code": "volunteer",
            "description": "Без оплаты, на общественных началах"
        }
    }
}

work_format = {
    "project_id": project_id,
    "object_type": "work_format",
    "data": {
        "remote": {
            "name": "Удалённая работа",
            "code": "remote",
            "description": "Работа из любой локации"
        },
        "office": {
            "name": "Офисная работа",
            "code": "office",
            "description": "Работа в офисе компании"
        },
        "hybrid": {
            "name": "Гибридная работа",
            "code": "hybrid",
            "description": "Комбинированный формат: часть времени в офисе, часть удалённо"
        },
        "shift": {
            "name": "Сменный график",
            "code": "shift",
            "description": "Например, день/ночь или 2 через 2"
        },
        "rotation": {
            "name": "Вахтовый метод",
            "code": "rotation",
            "description": "Работа в отдалённых регионах по сменам (например, 30/30)"
        }
    }
}

experience_required = {
    "project_id": project_id,
    "object_type": "experience_required",
    "data": {
        "none": {
            "name": "без опыта",
            "code": "none",
            "description": "Подходит для выпускников и начинающих специалистов"
        },
        "less_1": {
            "name": "до года",
            "code": "less_1",
            "description": "Начинающий специалист"
        },
        "1_to_3": {
            "name": "от 1 года до 3 лет",
            "code": "1_to_3",
            "description": "Junior–Middle уровень"
        },
        "3_to_6": {
            "name": "от 3 до 6 лет",
            "code": "3_to_6",
            "description": "Middle–Senior уровень"
        },
        "more_6": {
            "name": "от 6 лет",
            "code": "more_6",
            "description": "Экспертный уровень"
        }
    }
}

taxes = {
    "project_id": project_id,
    "object_type": "taxes",
    "data": {
        "before": {
            "name": "до вычета налогов",
            "code": "before",
            "description": "Указан \"грязный\" оклад"
        },
        "after": {
            "name": "после вычета налогов",
            "code": "after",
            "description": "Указан \"чистый\" оклад"
        },
        "not_specified": {
            "name": "не указано",
            "code": "not_specified",
            "description": "Информация о налогах отсутствует"
        }
    }
}

currency = {
    "project_id": project_id,
    "object_type": "currency",
    "data": {
        "RUB": {
            "name": "Российский рубль",
            "code": "RUB",
            "description": "Официальная валюта Российской Федерации"
        },
        "USD": {
            "name": "Доллар США",
            "code": "USD",
            "description": "Американский доллар, валюта Соединённых Штатов Америки"
        },
        "EUR": {
            "name": "Евро",
            "code": "EUR",
            "description": "Официальная валюта стран Европейского союза, использующих евро"
        },
        "KZT": {
            "name": "Тенге",
            "code": "KZT",
            "description": "Национальная валюта Республики Казахстан"
        },
        "CNY": {
            "name": "Юань",
            "code": "CNY",
            "description": "Официальная валюта Китайской Народной Республики"
        },
        "BYN": {
            "name": "Белорусский рубль",
            "code": "BYN",
            "description": "Валюта Республики Беларусь"
        },
        "AMD": {
            "name": "Армянский драм",
            "code": "AMD",
            "description": "Национальная валюта Республики Армения"
        },
        "GEL": {
            "name": "Грузинский лари",
            "code": "GEL",
            "description": "Валюта Грузии"
        },
        "KGS": {
            "name": "Киргизский сом",
            "code": "KGS",
            "description": "Валюта Кыргызской Республики"
        },
        "TJS": {
            "name": "Таджикский сомони",
            "code": "TJS",
            "description": "Валюта Республики Таджикистан"
        },
        "UZS": {
            "name": "Узбекский сум",
            "code": "UZS",
            "description": "Валюта Узбекистана"
        },
        "TRY": {
            "name": "Турецкая лира",
            "code": "TRY",
            "description": "Валюта Турецкой Республики"
        },
        "JPY": {
            "name": "Японская иена",
            "code": "JPY",
            "description": "Официальная валюта Японии"
        },
        "GBP": {
            "name": "Фунт стерлингов",
            "code": "GBP",
            "description": "Национальная валюта Великобритании"
        },
        "CHF": {
            "name": "Швейцарский франк",
            "code": "CHF",
            "description": "Официальная валюта Швейцарии"
        },
        "KRW": {
            "name": "Южнокорейская вона",
            "code": "KRW",
            "description": "Валюта Республики Корея"
        },
        "INR": {
            "name": "Индийская рупия",
            "code": "INR",
            "description": "Валюта Индии"
        },
        "AED": {
            "name": "Дирхам ОАЭ",
            "code": "AED",
            "description": "Официальная валюта Объединённых Арабских Эмиратов"
        },
        "SGD": {
            "name": "Сингапурский доллар",
            "code": "SGD",
            "description": "Валюта Сингапура"
        },
        "HKD": {
            "name": "Гонконгский доллар",
            "code": "HKD",
            "description": "Валюта Особого административного района Китая — Гонконга"
        }
    }
}