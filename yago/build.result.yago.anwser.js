/*
 *  2014.05.24, build the yago anwser set.
 * */

var yagoRelations = db.patty.yago.relation.distinct("relation");

print(yagoRelations);

var it = db.yago.map.dbpedia.find();

while(it.hasNext()){
    var instance = it.next();

    var yagoInstance = instance.yago;
    var dbpediaInstanceName = instance.dbpedia;

    var subjectItr = db.yago.facts.find({"subject":yagoInstance});
    var objectItr  = db.yago.facts.find({"object":yagoInstance});
    var dbpediaItr = db.result.data.instance.find({"_id":dbpediaInstanceName});

    var properties = [];
    var references = [];

    //Get the properties
    while(subjectItr.hasNext()){
        var fact = subjectItr.next();
        var property = fact.property;
        if(yagoRelations.indexOf(property)>=0 && properties.indexOf(property) < 0){
            properties.push(property);
        }
    }

    //Get referenced properties
    while(objectItr.hasNext()){
        var fact = objectItr.next();
        var property = fact.property;
        if(yagoRelations.indexOf(property)>=0 && references.indexOf(property) < 0){
            references.push(property);
        }
    }

    if((properties.length>0 || references.length>0)&&dbpediaItr.hasNext()){
        var dbpediaInstance = dbpediaItr.next();

        var id = dbpediaInstance.id;
        var revid = dbpediaInstance.revid;

        db.result.yago.anwser.insert({
            "_id": yagoInstance,
            "id": id,
            "revid": revid,
            "dbpedia": dbpediaInstanceName,
            "properties": properties,
            "references": references
        });
        print(yagoInstance+", id="+id+", revid="+revid+", count="+properties.length);

    }

}
