var it = db.result.patty.instances.find()

while(it.hasNext()){
    var instance = it.next();
    var features = [];

    var qid = db.dbpedia.wikiId.find({"resource":instance._id});
    if(!qid.hasNext()){
        continue;
    }

    var qrevid = db.dbpedia.wikiRevId.find({"resource":instance._id});
    if(!qrevid.hasNext()){
        continue;
    }
    var id = qid.next().id;
    var revid = qrevid.next().revid;
    var resourceName = instance._id;

    if(instance.value.count==undefined){
        //不正常的case

        //printjson(instance);
        var feature = instance.value.slice(28);
        if(features.indexOf(feature)<0){
            features.push(feature);
        }else{
            //nothing to do
        }
    }else{
        for(var i = 0 ; i<instance.value.features.length; i++){
            if(typeof(instance.value.features[i])!=typeof("jizz")){
                for(var j = 0 ; j<instance.value.features[i].features.length; j++){
                    var feature = instance.value.features[i].features[j].slice(28);
                    if(features.indexOf(feature)<0){
                        features.push(feature);
                    }
                }
            }else{
                var feature = instance.value.features[i].slice(28);
                if(features.indexOf(feature)<0){
                    features.push(feature);
                }   
            }
        }
    }

    db.result.data.instance.insert({
        "_id":resourceName,
        "id":id,
        "revid":revid,
        "features":features,
        "count":features.length
    });

    print(resourceName+", id="+id+", revid="+revid+", count="+features.length);
}

