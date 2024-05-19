/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sl8ismhmv20za2l")

  // remove
  collection.schema.removeField("bbrpty6q")

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sl8ismhmv20za2l")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "bbrpty6q",
    "name": "field",
    "type": "url",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "exceptDomains": [],
      "onlyDomains": []
    }
  }))

  return dao.saveCollection(collection)
})
