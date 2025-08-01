from uuid import uuid4
from app.schemas.vacancy_schemas import VacancyRegistryObject, VacancyData


def serialize_vacancy_data_to_registry_object(data: dict | VacancyData) -> VacancyRegistryObject:
    """
    Сериализатор для преобразования данных вакансии в объект реестра
    """
    try:
        print(f"Получены данные для сериализации: {data}")

        if isinstance(data, dict):
            print("Преобразование словаря в VacancyData")
            try:
                vacancy_data = VacancyData(**data)
                print("Успешно создан объект VacancyData")
            except Exception as e:
                error_msg = f"Ошибка при создании VacancyData: {str(e)}"
                print(error_msg)
                raise ValueError(error_msg) from e
        else:
            vacancy_data = data

        registry_object_id = str(uuid4())

        # Создаем объект реестра
        registry_object = VacancyRegistryObject(
            id=registry_object_id,
            object_type='vacancy',
            object_code=registry_object_id,
            data=vacancy_data,
        )

        print(f"Сериализованные данные: {registry_object.model_dump()}")
        print("Успешно создан VacancyRegistryObject")

        return registry_object

    except Exception as e:
        error_msg = (
            f"Ошибка сериализации в методе serialize_vacancy_data_to_registry_object\n"
            f"Тип исключения: {type(e).__name__}\n"
            f"Сообщение: {str(e)}\n"
        )
        print(error_msg)
        raise ValueError(error_msg) from e


y = {"title": "Dev", "required_employees": 1, "position": "", "short_description": "", "requirements": "",
     "responsibilities": "", "benefits": "", "status": "активная", "organization_name": "Avito",
     "organization_uuid": "", "teams": "", "customer_name": "", "contact_person_name": "",
     "organization_description": "", "contact_person_phone": "", "contact_person_email": "", "contact_person_tg": "",
     "country": "", "region": "", "city": "", "work_format": "гибридный", "employment_type": "частичная",
     "employment_basis": "договор ГПХ", "schedule": "2/2", "salary_from": 110000, "salary_to": 120000, "currency": "₽",
     "taxes": false, "salary_period": "за смену", "frequency": "раз в месяц",
     "skills": ["Потенциал", "Лидер корпоративной культуры"], "education": "", "experience_required": "1 - 3 года",
     "recruiter_name": "", "recruiter_phone": "", "recruiter_email": "", "recruiter_tg": "", "recruiter_wa": "",
     "opened_date": "2025-08-02", "deadline_date": "2025-08-10", "budget_to": 111233343, "responsible": "",
     "vacancy_url": "", "vacancy_img": "", "preview_img": ""}

x = serialize_vacancy_data_to_registry_object(y)
print(x)
