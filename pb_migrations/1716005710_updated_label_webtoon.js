/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ezw2yfojbzclypo")

  // remove
  collection.schema.removeField("j3ypsx5v")

  // update
  collection.schema.addField(new SchemaField({
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
        "분량",
        "기타"
      ]
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ezw2yfojbzclypo")

  // add
  collection.schema.addField(new SchemaField({
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
  }))

  // update
  collection.schema.addField(new SchemaField({
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
  }))

  return dao.saveCollection(collection)
})
