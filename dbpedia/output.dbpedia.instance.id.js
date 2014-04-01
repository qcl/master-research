var it = db.dbpedia.wikiId.find();

while(it.hasNext()){
    var resource = it.next();
    var q = db.result.patty.instances.find({"_id":resource.resource});
    if(q.hasNext()){
        print(resource.id);
    }
}

