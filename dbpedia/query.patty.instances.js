//pattyR
load("../patty/patty.dbpedia.Relations.json");

var queries = [];

for(var i=0;i<pattyR.length;i++){
    if(pattyR[i]=="headquarters"){
        var target = "http://dbpedia.org/ontology/headquarter";
    }else{
        var target = "http://dbpedia.org/ontology/"+pattyR[i];
    }
    queries.push(target);
}

var mapper = function(){
    if(queries.indexOf(this.property)>0){
        emit(this.resource,this.property);
    }
}

var reducer = function(key,values){
    return {features:values,count:values.length};
}

db.dbpedia.map.property.mapReduce(
    mapper,
    reducer,
    {
        out: "result.patty.instances",
        scope: {
            queries: queries
        }
    });

//var it = db.dbpedia.mapresult.property.targets.number.find({_id:{ $in: queries}}).sort({"value":-1});
//
//while(it.hasNext()){
//    var obj = it.next();
//    print(obj._id+"\t"+obj.value);
//}
