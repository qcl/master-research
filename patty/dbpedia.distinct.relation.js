db = db.getSiblingDB('projizz')
var result = db.runCommand({"distinct":"patty.dbpedia.relation","key":"relation"});
var relations = result["values"];
for(var index in relations){
    var rela = relations[index];
    print(rela);
    var f = db.patty.dbpedia.relation.findOne({"relation":rela});
    printjson(f);
}
