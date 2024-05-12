/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "ezw2yfojbzclypo",
    "created": "2024-05-09 02:01:22.524Z",
    "updated": "2024-05-09 02:01:22.524Z",
    "name": "label_webtoon",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "ypamxgvq",
        "name": "label",
        "type": "select",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSelect": 1,
          "values": [
            "작화",
            "스토리",
            "캐릭터",
            "기타"
          ]
        }
      },
      {
        "system": false,
        "id": "hhbuy0xj",
        "name": "positive_count",
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
        "id": "j3ypsx5v",
        "name": "positive_summary",
        "type": "text",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
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
  const collection = dao.findCollectionByNameOrId("ezw2yfojbzclypo");

  return dao.deleteCollection(collection);
})
