import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class Parser:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get('http://timetable.ait.ie/students.htm')

    @property
    def department_names(self):
        """Return a list containing a list of all departments."""
        dropdown = self.driver.find_elements_by_css_selector('select[onchange*="Filter"] option')
        blacklist = ['Unfiltered', 'Central Department', 'Design', 'Research and External Services']
        return [department.text for department in dropdown
                if department.text not in blacklist and 'ZZ' not in department.text]

    def to_json(self):
        dropdown = Select(self.driver.find_element_by_css_selector('select[onchange*="Filter"]'))
        all_courses = {}
        for department in self.department_names:
            dropdown.select_by_visible_text(department)
            courses = self.driver.find_elements_by_css_selector('select[name="identifier"] option')
            all_courses[department] = {c.text: c.get_attribute('value') for c in courses}
        return all_courses

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.driver.close()


if __name__ == '__main__':
    with Parser() as departments, open('departments.json', 'w') as f:
        json.dump(departments.to_json(), f, indent=4)
