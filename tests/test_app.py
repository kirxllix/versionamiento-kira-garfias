"""
Pruebas automatizadas con Selenium para la app "Cinnamoroll Product List".

Uso:
    pip install -r tests/requirements.txt
    BASE_URL=https://tu-app.onrender.com pytest tests/ -v
(En Windows CMD:  set BASE_URL=https://tu-app.onrender.com  y luego  pytest tests -v)
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
SHOTS = os.environ.get("SHOTS_DIR", "evidencias")


@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS", "1") == "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    if os.environ.get("CHROME_BINARY"):
        opts.binary_location = os.environ["CHROME_BINARY"]
    service = webdriver.ChromeService(executable_path=os.environ.get("CHROMEDRIVER")) \
        if os.environ.get("CHROMEDRIVER") else webdriver.ChromeService()
    d = webdriver.Chrome(options=opts, service=service)
    d.get(BASE_URL)
    # Render (plan gratuito) puede tardar en "despertar": espera generosa
    WebDriverWait(d, 90).until(EC.presence_of_element_located((By.ID, "addProduct")))
    os.makedirs(SHOTS, exist_ok=True)
    yield d
    d.quit()


def rows(d):
    return d.find_elements(By.CSS_SELECTOR, "#productsTable tbody tr")


def test_1_pagina_carga_correctamente(driver):
    """La pagina responde y muestra titulo, formulario, tabla y contador."""
    assert "Cinnamoroll Product List" in driver.find_element(By.TAG_NAME, "h1").text
    assert driver.find_element(By.ID, "name").is_displayed()
    assert driver.find_element(By.ID, "price").is_displayed()
    assert driver.find_element(By.ID, "productsTable").is_displayed()
    assert driver.find_element(By.ID, "productCount").text == "0"
    driver.save_screenshot(f"{SHOTS}/selenium_1_carga.png")


def test_2_agregar_producto(driver):
    """Agregar un producto lo muestra en la tabla y actualiza el contador."""
    driver.find_element(By.ID, "name").send_keys("Peluche Cinnamoroll")
    driver.find_element(By.ID, "price").send_keys("250")
    driver.find_element(By.ID, "addProduct").click()
    WebDriverWait(driver, 10).until(lambda d: len(rows(d)) == 1)
    celdas = rows(driver)[0].find_elements(By.TAG_NAME, "td")
    assert celdas[1].text == "Peluche Cinnamoroll"
    assert celdas[2].text == "$250"
    assert driver.find_element(By.ID, "productCount").text == "1"
    driver.save_screenshot(f"{SHOTS}/selenium_2_agregar.png")


def test_3_eliminar_producto(driver):
    """Eliminar un producto lo quita de la tabla y el contador vuelve a 0."""
    driver.find_element(By.ID, "name").send_keys("Taza")
    driver.find_element(By.ID, "price").send_keys("80")
    driver.find_element(By.ID, "addProduct").click()
    WebDriverWait(driver, 10).until(lambda d: len(rows(d)) == 1)
    driver.find_element(By.CSS_SELECTOR, ".delete-btn").click()
    WebDriverWait(driver, 10).until(lambda d: len(rows(d)) == 0)
    assert driver.find_element(By.ID, "productCount").text == "0"
    driver.save_screenshot(f"{SHOTS}/selenium_3_eliminar.png")


def test_4_validacion_datos_invalidos(driver):
    """Con datos vacios se muestra una alerta y no se agrega nada."""
    driver.find_element(By.ID, "addProduct").click()
    alerta = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert "valid name and price" in alerta.text
    alerta.accept()
    assert len(rows(driver)) == 0
