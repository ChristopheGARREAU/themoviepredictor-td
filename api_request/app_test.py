from omdb import OMDB

film = "joker"

nouveau_film = OMDB(film)

print(nouveau_film.title)
print(nouveau_film.duration)
print(nouveau_film.release_date)