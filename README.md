# Prueba tecnica - Sopa de letras

### Cómo iniciar el proyecto.

Ingresar el comando docker `docker compose up --build`para iniciar por primera vez el proyecto. Las siguientes veces ingresar `docker compose up`.

### API

En postman ingresar la ruta `/api/word-search/` para enviar una petición `POST`.


```bash
{
	"letters": "a,b,s,g,a,q,t",
	"words": "Mango, perro, gato"
}

```
> [!IMPORTANT]
>  Tomar en cuenta que el dato `letters` solo puede recibir `196` caracteres en total. Además, el campo `words` no puede tener espacios en medio de las palabras.

### Tecnologías

- Python
- Django Rest Framework
- Docker
- Postman


