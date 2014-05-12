/*
 *  2014.05.12, rebuild the anwser set.
 * */
var it = db.old.result.data.instance.find();

//pattyR
load("../patty/patty.dbpedia.Relations.json");

while(it.hasNext()){
    var instance = it.next();
    var features = [];
    
    var mprIt = db.dbpedia.map.property.find({"resource":instance._id})
    while(mprIt.hasNext()){
        var property = mprIt.next();
        var feature = property.property.slice(28);
        if(pattyR.indexOf(feature)>=0 && features.indexOf(feature)<0){
            features.push(feature)
        }
    }

    var id = instance.id;
    var revid = instance.revid;
    var resourceName = instance._id;

    db.result.data.instance.insert({
        "_id":resourceName,
        "id":id,
        "revid":revid,
        "features":features,
        "count":features.length
    });

    print(resourceName+", id="+id+", revid="+revid+", count="+features.length);
}
