import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re


#Scraper de una categoria de productos
def main(url):
    
    options = Options()
    options.add_argument("--headless=new") #Usa el driver de navegador sin interfaz
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Type user agent here')
    options.add_argument("--disable-notifications")

    #inicializa el driver de Chrome cargando las opciones establecidas
    driver = selenium.webdriver.Chrome(options=options)

    #Se pasa el url al que se va a acceder
    driver.get(url)

    #Espera que la pagina se cargue
    wait = WebDriverWait(driver, 20)
    
    # Inicializa la lista de productos
    productos = []

    # Realiza un ciclo mientras el botón "Siguiente página" esté presente
    while True:

        # Hace clic en el botón "Siguiente página"
        try:
            boton_siguiente = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-next.s-pagination-button")))

            # Obtiene los resultados de la página actual
            soup = BeautifulSoup(driver.page_source, "html.parser")
            productos_actuales = soup.find_all(attrs={"data-component-type": "s-search-result"})

            # Agrega los resultados de la página actual a la lista
            productos.extend(productos_actuales)

            # Hace clic en el botón "Siguiente página" usando JavaScript
            driver.execute_script("arguments[0].click();", boton_siguiente)

        except:
            break

    count=0
    #Obtiene los atributos de cada producto y los imprime
    for producto in productos:
        link = producto.find("a", class_="a-link-normal s-no-outline")
        link="https://www.amazon.es"+link["href"]
        name = producto.find("span",class_="a-size-base-plus a-color-base a-text-normal").text
        name = re.sub("[^\w\s]", "",name)
        precio = producto.find("span",class_="a-price").text
        print(f"Producto: {name}")
        print(f"Precio: {precio}")
        print(f"Enlace: {link}")
        count+=1
        print(f"--------------SALTO DE LINEA {count}-----------")

    
enlace="https://www.amazon.es/s?i=specialty-aps&srs=21469578031&rh=n%3A21469578031&fs=true&ref=lp_21469578031_sar"
main(enlace)
