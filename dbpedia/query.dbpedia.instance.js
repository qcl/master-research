// build _id: resourceName, value: wiki link and wiki id 

var mapper = function(){
    emit(this._id,1);
}

var reducer = function(key,values){
    var linkData = db.dbpedia.link.find({"resource":key});
    var idData   = db.dbpedia.wikiId.find({"resource":key});
    
    if(linkData.count()*idData.count()>0){
        var link = linkData[0].link;
        var id   = idData[0].id;
        return {link:link,id:id};
    }

}

db.result.patty.instance.mapReduce(
    mapper,
    reducer,
    {
        out: "result.dbpedia.instance",
        verbose: true
    });

