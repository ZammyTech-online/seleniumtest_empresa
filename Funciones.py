import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver



class Funciones_Globales():
    def __init__(self, driver):
        self.driver = driver

    def Tiempo(self, tie):
        t = time.sleep(tie)
        return t

    def Navegar(self, Url, Tiempo):
        self.driver.get(Url)
        self.driver.maximize_window()
        print("Página abierta: " + str(Url))
        t = time.sleep(Tiempo)
        return t



    # Esto estaría en un archivo de pruebas, donde ya has importado y/o instanciado la clase Funciones_Globales
    def test_automatizacion_wikipedia(self, Url, Tiempo, campo_busqueda, texto_busqueda, tiempo_texto, xpath_clic,
                                      tiempo_clic):
        self.Navegar(Url, Tiempo)  # Usamos las funciones globales ya definidas
        self.Texto_Mixto("xpath", campo_busqueda, texto_busqueda,
                         tiempo_texto)  # campo_busqueda sería el selector para el campo de texto
        self.Click_Mixto("xpath", xpath_clic, tiempo_clic)  # xpath_clic sería el selector para el elemento clickeable
        # Aquí podrías añadir más acciones, como verificar que la página correcta fue abierta, etc.




    def _action(self, tipo, selector, action, *args):
        locator = (By.XPATH, selector) if tipo == "xpath" else (By.ID, selector)
        try:
            element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return action(element, *args)
        except TimeoutException as ex:
            print(ex.msg)
            print("No se encontró el Elemento " + selector)

    def Texto_Mixto(self, tipo, selector, texto, tiempo):
        def action(element, texto):
            element.clear()
            element.send_keys(texto)
            print(f"Escribiendo en el campo {selector} el texto -> {texto}")
            time.sleep(tiempo)

        self._action(tipo, selector, action, texto)



    def Click_Mixto(self, tipo, selector, tiempo):
        def action(element, _):
            element.click()
            print(f"Dando click en {selector}")
            time.sleep(tiempo)

        self._action(tipo, selector, action, None)

    def Salida(self):
        print("Se termina la prueba Exitosamente")

    def Select_Xpath_Type(self, xpath, tipo, dato, tiempo):
        def action(element, tipo, dato):
            select_elem = Select(element)
            if tipo == "text":
                select_elem.select_by_visible_text(dato)
            elif tipo == "index":
                select_elem.select_by_index(dato)
            elif tipo == "value":
                select_elem.select_by_value(dato)
            print(f"El campo Seleccionado es {dato}")
            time.sleep(tiempo)

        self._action("xpath", xpath, action, tipo, dato)

    def Select_ID_Type(self, id, tipo, dato, tiempo):
        self.Select_Xpath_Type(id, tipo, dato, tiempo)

    def Upload_Xpath(self, xpath, ruta, tiempo):
        def action(element, ruta):
            element.send_keys(ruta)
            print(f"Se carga la imagen {ruta}")
            time.sleep(tiempo)

        self._action("xpath", xpath, action, ruta)

    def Upload_ID(self, id, ruta, tiempo):
        self.Upload_Xpath(id, ruta, tiempo)

    def Esperar_Elemento(self, selector, Tiempo):
        """
        Espera un elemento hasta que esté presente.
        """
        if "name=" in selector:
            element = WebDriverWait(self.driver, Tiempo).until(
                EC.presence_of_element_located((By.NAME, selector.replace("name=", "")))
            )
        else:
            element = WebDriverWait(self.driver, Tiempo).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
        return element





    def Esperar_Elemento_xpath(self, xpath, Tiempo):
        """
        Espera un elemento hasta que esté presente.
        """
        element = WebDriverWait(self.driver, Tiempo).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def Check_Xpath(self, xpath, tiempo):
        def action(element, _):
            element.click()
            print(f"Click en el elemento {xpath}")
            time.sleep(tiempo)

        self._action("xpath", xpath, action, None)

    def Check_ID(self, id, tiempo):
        self.Check_Xpath(id, tiempo)

    def scroll_y_captura2(self, xpath):
        # Buscar el elemento por su XPath
        elemento = self.driver.find_element(By.XPATH, xpath)

        # Ejecutar un script de JavaScript para hacer scroll hasta el elemento
        self.driver.execute_script("arguments[0].scrollIntoView();", elemento)

        # Tomar una captura de pantalla y guardarla en un archivo
        self.driver.save_screenshot('captura_de_pantalla.png')


    def Check_Xpath_Multiples(self, tiempo, *args):
        """
        Toma múltiples xpaths y hace clic en cada uno de ellos.
        """
        for arg in args:
            self.Check_Xpath(arg, tiempo)


    #def Check_Xpath_Multiples(self, tiempo, *args):
     #   for arg in args:
      #      self.Check_Xpath(arg, tiempo)

    def Existe(self, tipo, selector, tiempo):
        # Se decide el tipo de localizador basado en el tipo de selector
        locator = None
        if tipo == "xpath":
            locator = (By.XPATH, selector)
        elif tipo == "id":
            locator = (By.ID, selector)
        else:
            print(f"Tipo {tipo} no soportado.")
            return "No Existe"

        # Ahora, independientemente del tipo de selector, realizamos las operaciones
        try:
            # Esperar hasta que el elemento sea visible
            element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
            # Desplazarse hasta el elemento (esto puede ser opcional dependiendo de tus necesidades)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            # Verificar que el elemento existe
            self.driver.find_element(*locator)
            # Mensaje de éxito
            print(f"El elemento {tipo} -> {selector} existe.")
            time.sleep(tiempo)
            return "Existe"
        except TimeoutException as ex:
            print(ex.msg)
            print(f"No se encontró el Elemento {selector}")
            return "No Existe"
