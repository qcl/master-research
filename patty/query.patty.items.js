// Try to find all instance name in PATTY.

var mapper = function(){
    emit(this.arg1,1);
    emit(this.arg2,1);
}

var reducer = function(key,values){
    return values.length;
}

db.patty.wiki.instance.mapReduce(
    mapper,
    reducer,
    {
        out: "result.patty.items"
    });

