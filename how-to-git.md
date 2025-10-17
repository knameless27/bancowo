# Flujo básico para trabajar con Git

1. Cambiar a la rama `master`

   ```bash
   git checkout master
   ```

2. Actualizar la rama `master` con los últimos cambios

   ```bash
   git pull origin master
   ```

3. Crear una nueva rama desde `master` a por ejemplo feature/making-user-login

   ```bash
   git checkout -b feature/making-user-login
   ```

4. Hacer tus cambios y confirmar

   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   ```

5. Subir tu rama al repositorio remoto

   ```bash
   git push origin nombre-de-tu-rama
   ```

6. Crear un Pull Request (PR) desde `feature/making-user-login` hacia `master`
   (Esto se hace usualmente desde la interfaz web de GitHub, GitLab o Bitbucket)
