/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("iwdfirb6ssntcvy")

  collection.name = "stars_webtoon"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("iwdfirb6ssntcvy")

  collection.name = "star_webtoon"

  return dao.saveCollection(collection)
})
