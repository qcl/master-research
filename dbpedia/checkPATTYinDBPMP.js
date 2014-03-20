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

//print(queries);

var it = db.result.property.targets.number.find({_id:{ $in: queries}}).sort({"value":-1});

while(it.hasNext()){
    var obj = it.next();
    print(obj._id+"\t"+obj.value);
}
