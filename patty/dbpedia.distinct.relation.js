//db = db.getSiblingDB('projizz')
var result = db.runCommand({"distinct":"patty.dbpedia.relation","key":"relation"});
var relations = result["values"]
printjson(relations);
