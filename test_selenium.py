__author__ = 'Miguel R.'

import unittest
from selenium import webdriver
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains

class Contacts(unittest.TestCase):

    xpaths = {
        'search_box': '/html/body/div/div[1]/input',
        'contacts_list': '/html/body/div/table/tbody/tr',
        'toggle_form': '/html/body/div/button'
    }

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.miguelrivero.info/contacts_book")

    def test_title(self):
        print('test_title')
        driver = self.driver
        self.assertIn("Contacts", driver.title)

    def test_count_after_search(self):
        print('count after search')
        driver = self.driver
        search_box = driver.find_element_by_xpath(self.xpaths['search_box'])
        search_box.send_keys("Migu")
        coincidences = driver.find_elements_by_xpath(self.xpaths['contacts_list'])
        self.assertEqual(len(coincidences), 1, "There should be only one element in the list")

    def test_remove_random_contact(self):
        driver =  self.driver
        random_xpath = '/html/body/div/table/tbody/tr[{}]/td[8]/a'.format(random.randint(1,6))
        print(random_xpath)
        contacts_init = len(driver.find_elements_by_xpath(self.xpaths['contacts_list']))
        remove_button = driver.find_element_by_xpath(random_xpath)
        remove_button.click()
        driver.implicitly_wait(1)
        contacts_end = len(driver.find_elements_by_xpath(self.xpaths['contacts_list']))
        self.assertEqual(contacts_init - 1, contacts_end, 'One element should have been removed')


    def test_remove_all_contacts(self):
        driver = self.driver
        elements = driver.find_elements_by_xpath(self.xpaths['contacts_list'])
        number_remove_buttons = len(elements)
        for x in range(number_remove_buttons):
            remove_button = driver.find_element_by_name("remove")
            remove_button.click()
            driver.implicitly_wait(1)
        contacts_end = driver.find_elements_by_tag_name("tr")
        self.assertIn('Your contact list is empty', driver.page_source)
        self.assertEqual(len(contacts_end) - 1 , 0, "The list should have no elements")


    def test_add_contact(self):
        print('add contact')
        driver = self.driver
        contacts_init = driver.find_elements_by_xpath(self.xpaths['contacts_list'])
        self.assertNotIn( 'Prueba', driver.page_source)
        self.add_contact_fill_in_form(name="Prueba", email="prueba@gmail.com", phone="12341234", country="spain", favourite=True)
        contacts_end = driver.find_elements_by_xpath(self.xpaths['contacts_list'])
        for elem in contacts_end:
            print(str(elem.text))
        self.assertIn('Prueba' , driver.page_source)
        self.assertTrue(len(contacts_init) + 1 == len(contacts_end), "The list should not have been modified")


    def test_add_invalid_contact(self):
        print('add invalid contact')
        driver = self.driver
        driver.implicitly_wait(5)
        contacts_init = driver.find_elements_by_xpath(self.xpaths['contacts_list'])
        #print(len(contacts_init))
        self.assertIn( 'Miguel Rivero' , driver.page_source, "Miguel Rivero should appear in the page")
        if 'Miguel Rivero' in driver.page_source:
            self.add_contact_fill_in_form(name="Miguel Rivero", email="prueba@gmail.com", phone="12341234", country="spain", favourite=True)
            text_alert = Alert(driver).text
            self.assertEqual("This person is already in the list.", text_alert)
            driver.switch_to.alert.accept()
        contacts_end = driver.find_elements_by_xpath(self.xpaths['contacts_list'])
        self.assertEqual(len(contacts_init), len(contacts_end), "The list should not have been modified")

    def add_contact_fill_in_form(self, name, email, phone, country, favourite, update=False):
        """
        It click on add new contact button and modal window appears in order to be fulfilled and submitted
        """
        driver = self.driver
        toggle_form = driver.find_element_by_xpath(self.xpaths['toggle_form'])
        toggle_form.click()
        driver.implicitly_wait(10)
        name_box = driver.find_element_by_id('InputName')
        name_box.send_keys(name)
        email_box = driver.find_element_by_id('InputEmail')
        email_box.send_keys(email)
        phone_box = driver.find_element_by_id('InputPhone')
        phone_box.send_keys(phone)
        country_box = driver.find_element_by_id('Inputcountry')
        country_box.send_keys(country)
        if favourite:
            favourite_box = driver.find_element_by_id('InputFavourite')
            favourite_box.click()
        country_box.submit()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)