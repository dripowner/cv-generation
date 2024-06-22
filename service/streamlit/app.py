import streamlit as st
import requests
import re


def create_request(text: str, server_url: str = "http://localhost:8080/generate"):
	data = {"text": text}
	return requests.post(
		server_url, json=data, timeout=8000
	)


def generate_prompt(sex,
					age,
					city,
					wanted_pos,
					salary,
					driving_license,
					work_experience,
					skills):
	prompt = f"Пол {sex}. "
	prompt += f"Возраст {int(age)} лет. "
	prompt += f"Опыт работы: {work_experience}. "
	prompt += f"Умения и навыки: {skills}. "
	prompt += f"Желаемая должность: {wanted_pos}"
	prompt += f"Город проживания - {city.lower()}. "
	if driving_license != "не указано":
		driving_license = [x.lower() for x in driving_license]
		driving_license = ",".join(driving_license)
	prompt += f"Водительское удостоверение: {{{driving_license}}}. "
	prompt += f"Желаемая зарплата от {int(salary)} рублей. "
	
	return prompt



def main():
	
	st.title("Генерация поля \"О себе\"")

	with st.form("Generation"):

		sex = st.selectbox("Пол", ("мужской", "женский", "не указано"), index=2)
		age = st.number_input(label="Возраст", step=1, format="%d")
		city = st.text_input(label="Место проживания", value="не указано")
		wanted_pos = st.text_input(label="Желаемая должность/позиция", value="не указано")

		is_driving_license = st.sidebar.toggle("У меня есть водительское удостоверение")
		if is_driving_license:
			driving_license = st.multiselect("Водительское удостоверение", ["A", "B", "C", "D", "E", "M"])
		else:
			driving_license = "не указано"
		salary = st.number_input(label="Желаемая зарплата (рубли)", step=500, format="%d")

		is_work_exp = st.sidebar.toggle('У меня есть опыт работы')
		if is_work_exp:
			work_experience = st.text_area(label="Опыт работы", 
										   placeholder="организация - \"Наименование организации\"; должность - \"должность\"; количество лет в должности \"x.x лет\"",
										   value="не указано")
		else:
			work_experience = "нет опыта работы"
		skills = st.text_area(label="Навыки", value="не указано")


		if st.form_submit_button('Сгенерировать'):

			if all([sex, age, city, driving_license, work_experience, skills]):

				# Generating cv text based on user input
				aboutme = generate_prompt(sex, age, city, wanted_pos, salary, driving_license, work_experience, skills)

				response = create_request(aboutme)
				if response.status_code == 200:
					generated_cv = response.text

					# Displaying the generated 'about me' text in a markdown widget
					st.markdown("### Сгенерированное поле \"О себе\"\n")
					st.markdown(generated_cv)

				pass
				
			else:
				st.error('Пожалуйста, заполните все поля')
		

if __name__ == "__main__":
	main()