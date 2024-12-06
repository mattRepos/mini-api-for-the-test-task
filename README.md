# Возможные запросы 
## Для users 
POST /api/users/ — создание пользователя.
GET /api/users/ — получение всех пользователей.
PUT /api/users/1/ — изменение данных пользователя с ID=1.
DELETE /api/users/1/ — удаление пользователя с ID=1.
## Для movies
POST /api/movies/ — добавление фильма.
GET /api/movies/ — получение списка всех фильмов.
PUT /api/movies/1/ — изменение данных фильма с ID=1.
DELETE /api/movies/1/ — удаление фильма с ID=1.
## Для favorites 
POST /api/favorites/ — добавление фильма в избранное.
GET /api/favorites/user/1/ — получение списка избранных фильмов пользователя с ID=1.
POST /api/favorites/remove/ — удаление фильма из избранного пользователя.
