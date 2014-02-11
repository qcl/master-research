db = db.getSiblingDB('projizz')
var result = db.runCommand({"distinct":"patty.yago.relation","key":"relation"});
var relations = result["values"]
printjson(relations);
