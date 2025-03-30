from datetime import date
from app.database.models.user_model import User

class ProfileService:
    @staticmethod
    def calculate_work_experience(hire_date: date) -> dict:
        if not hire_date:
            return {"text": "Не указан"}
        
        today = date.today()
        work_experience_years = today.year - hire_date.year
        work_experience_months = today.month - hire_date.month
        
        if today.month < hire_date.month or (today.month == hire_date.month and today.day < hire_date.day):
            work_experience_years -= 1
            work_experience_months += 12
        
        if today.day < hire_date.day:
            work_experience_months -= 1
            if work_experience_months < 0:
                work_experience_years -= 1
                work_experience_months += 12
        
        years_form = ProfileService.get_years_form(work_experience_years)
        months_form = ProfileService.get_months_form(work_experience_months)
        
        if work_experience_years > 0 and work_experience_months > 0:
            experience_text = f"{work_experience_years} {years_form} {work_experience_months} {months_form}"
        elif work_experience_years > 0:
            experience_text = f"{work_experience_years} {years_form}"
        elif work_experience_months > 0:
            experience_text = f"{work_experience_months} {months_form}"
        else:
            experience_text = "Менее месяца"
        
        return {
            "text": experience_text,
            "years": work_experience_years,
            "months": work_experience_months
        }

    @staticmethod
    def calculate_age(birth_date: date) -> str:
        if not birth_date:
            return "Не указан"
        
        today = date.today()
        age_years = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age_years -= 1
        
        age_form = ProfileService.get_years_form(age_years)
        return f"{age_years} {age_form}"

    @staticmethod
    def get_years_form(years: int) -> str:
        if years % 10 == 1 and years % 100 != 11:
            return "год"
        elif 2 <= years % 10 <= 4 and (years % 100 < 10 or years % 100 >= 20):
            return "года"
        else:
            return "лет"

    @staticmethod
    def get_months_form(months: int) -> str:
        if months % 10 == 1 and months % 100 != 11:
            return "месяц"
        elif 2 <= months % 10 <= 4 and (months % 100 < 10 or months % 100 >= 20):
            return "месяца"
        else:
            return "месяцев"

    @staticmethod
    def format_profile_text(user: User, experience_text: str, age_text: str) -> str:
        profile_text = f"📋 <b>Ваш профиль:</b>\n\n"
        profile_text += f"👤 <b>Username:</b> @{user.username if user.username else 'Не указан'}\n"
        profile_text += f"👤 <b>Имя:</b> {user.name if user.name else 'Не указано'}\n"
        
        if user.birth_date:
            profile_text += f"🎂 <b>Дата рождения:</b> {user.birth_date.strftime('%d.%m.%Y')} ({age_text})\n"
        else:
            profile_text += f"🎂 <b>Дата рождения:</b> Не указана\n"
        
        profile_text += f"📅 <b>Дата найма:</b> {user.hire_date.strftime('%d.%m.%Y') if user.hire_date else 'Не указана'}\n"
        profile_text += f"👔 <b>Должность:</b> {user.position if user.position else 'Не указана'}\n"
        profile_text += f"⏱ <b>Стаж в компании:</b> {experience_text}\n"
        profile_text += f"💵 <b>T-point:</b> {user.t_points}\n"
        profile_text += f"🔑 <b>Роль:</b> {user.role.value}\n"
        profile_text += f"🔄 <b>Статус:</b> {'Активен' if user.is_active else 'Неактивен'}\n"
        
        return profile_text
    
    @staticmethod
    def format_admin_profile_text(user_info: dict) -> str:
        """Форматирует текст профиля для админ-панели"""
        profile_text = f"📋 <b>Информация о сотруднике:</b>\n\n"
        profile_text += f"🆔 <b>ID:</b> {user_info['telegram_id']}\n"
        profile_text += f"👤 <b>Username:</b> @{user_info['username'] if user_info['username'] else 'Не указан'}\n"
        profile_text += f"👤 <b>Имя:</b> {user_info['name'] if user_info['name'] else 'Не указано'}\n"
        
        if user_info['birth_date']:
            profile_text += f"🎂 <b>Дата рождения:</b> {user_info['birth_date']} ({user_info['age_text']})\n"
        else:
            profile_text += f"🎂 <b>Дата рождения:</b> Не указана\n"
        
        profile_text += f"📅 <b>Дата найма:</b> {user_info['hire_date'] if user_info['hire_date'] else 'Не указана'}\n"
        profile_text += f"👔 <b>Должность:</b> {user_info['position'] if user_info['position'] else 'Не указана'}\n"
        profile_text += f"🏢 <b>Отдел:</b> {user_info['department'] if user_info['department'] else 'Не указан'}\n"
        profile_text += f"⏱ <b>Стаж в компании:</b> {user_info['experience_text']}\n"
        profile_text += f"🔑 <b>Роль:</b> {user_info['role']}\n"
        profile_text += f"🔄 <b>Статус:</b> {'Активен' if user_info['is_active'] else 'Неактивен'}\n"
        profile_text += f"💵 <b>T-Point:</b> {user_info['t_points']}\n"
        
        return profile_text