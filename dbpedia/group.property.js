/* using mongodb map-reduce framework 
 * object: { resource:"", property: "", value: ""  }
 * */

/* do count */
var mapper = function(){
    emit(this.property, 1);
};

var reducer = function(key,values){
    return Array.sum(values);
};

db.dbpedia.map.property.mapReduce(mapper,reducer,{out: "result.property.targets.number"});


