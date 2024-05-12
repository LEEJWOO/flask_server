/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sl8ismhmv20za2l")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "zmkuk4lc",
    "name": "label",
    "type": "relation",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "collectionId": "ezw2yfojbzclypo",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": null,
      "displayFields": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sl8ismhmv20za2l")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "zmkuk4lc",
    "name": "labe",
    "type": "relation",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "collectionId": "ezw2yfojbzclypo",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": null,
      "displayFields": null
    }
  }))

  return dao.saveCollection(collection)
})
