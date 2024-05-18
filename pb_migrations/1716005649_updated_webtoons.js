/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sl8ismhmv20za2l")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qsiq56xt",
    "name": "label_summary",
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

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "no8bdj4n",
    "name": "total_summary",
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

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sl8ismhmv20za2l")

  // remove
  collection.schema.removeField("qsiq56xt")

  // remove
  collection.schema.removeField("no8bdj4n")

  return dao.saveCollection(collection)
})
