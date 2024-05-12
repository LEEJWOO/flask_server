/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "iwdfirb6ssntcvy",
    "created": "2024-05-09 02:00:04.688Z",
    "updated": "2024-05-09 02:00:04.688Z",
    "name": "star_webtoon",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "bqlx8eoa",
        "name": "star_list",
        "type": "json",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSize": 2000000
        }
      }
    ],
    "indexes": [],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("iwdfirb6ssntcvy");

  return dao.deleteCollection(collection);
})
