/* using mongodb map-reduce framework 
 * object: { resource:"", property: "", value: ""  }
 * */

/* do count */
var mapper = function(){
    emit(this.resource, 1);
};

var reducer = function(key,values){
    return Array.sum(values);
};

db.dbpedia.map.property.mapReduce(mapper,reducer,{out: "result.target.properties.number"});


