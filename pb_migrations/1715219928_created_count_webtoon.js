/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "vsg5nppvbo2qyk2",
    "created": "2024-05-09 01:58:48.345Z",
    "updated": "2024-05-09 01:58:48.345Z",
    "name": "count_webtoon",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "4f9ygrzh",
        "name": "total_p",
        "type": "number",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "noDecimal": false
        }
      },
      {
        "system": false,
        "id": "ltb7qxk2",
        "name": "total_n",
        "type": "number",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "noDecimal": false
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
  const collection = dao.findCollectionByNameOrId("vsg5nppvbo2qyk2");

  return dao.deleteCollection(collection);
})
