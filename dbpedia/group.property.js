var result = db.dbpedia.map.property.group({
    key: { property:1},
    reduce: function(curr,result){
        result.count++;  //Do count!
    },
    initial: { count:0 }
});
printjson(result);
