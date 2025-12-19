from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code


class UrbanRoutesPage:

    # ──────────────── LOCALIZADORES ────────────────

    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")

    COMFORT_TARIFF = (By.XPATH, "//div[text()='Comfort']")

    PHONE_BUTTON = (By.ID, "phone-button")
    PHONE_INPUT = (By.ID, "phone")

    ADD_CARD_BUTTON = (By.ID, "add-card")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    SMS_CODE_INPUT = (By.ID, "sms-code")
    LINK_CARD_BUTTON = (By.ID, "link")

    MESSAGE_INPUT = (By.ID, "comment")

    EXT
