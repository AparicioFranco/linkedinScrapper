# LinkedinScrapper
Aclaraciones del Scrapper

1. El algortimo esta hecho en python y con selenium ya que permite manipular facilmente todos los datos de la web.
2. Exclui los mensajes que son Sponsors o Special Offers de Linkedin por que no vi importancia en cargarlos a una base de datos. Se podria modificar el codigo para tener en cuenta estos datos ya que estas conversaciones tienen un layout distinto a las conversaciones normales. Pueden existir otro tipos de mensajes que no son sponsors, special offers ni mensajes normales, que podria romper el algortimo por que no estan contemplados ya que esos son los unicos tipo de mensajes que encontre en mi Linkedin.
3. La base de datos esta compuesta por 3 tablas, chat, chat_user y chat_line. Chat son las distintas conversaciones de Linkedin. Chat_user son los distintos usuarios que se encuentran en las conversaciones. Chat_line son los distintos mensajes que hay en las conversaciones, y tiene, line_text, que es el mensaje que se envio, chat_user_id, que es el usuario que lo envio, y chat_id, que es a que conversaciones que pertenece ese mensaje.
4. Se podria optimizar el codigo en el ultimo for loop, que carga los mensajes a la base de datos. Se deberian guardar los usuarios en dos variables distintas, asi se evita tener que hacer tantos llamados a la base de datos, ya que cada vez que se lee una tupla nueva de mensaje, se llama a la base de datos para encontrar el usuario.
5. Las credenciales se guardaron en el config.py para no estar expuestas y ahi esta la conexion a la base de datos y para probar el algortimo se deberian poner el user y contraseña de Linkedin.
6. Los delays estan puestos para que le de tiempo a cargar a Linkedin, asi cuando el algoritmo quiere clickear un objeto, lo encuentre y no tire error y se pare el algortimo.

Modelo base de datos
![Linkedin Message Scrapper](https://github.com/AparicioFranco/linkedinScrapper/assets/38363271/488d64d0-0f09-43d7-89b5-24352c1c96e8)


