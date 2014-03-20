/*
 * result.property.targets.number
 * */

var it = db.result.property.targets.number.find().sort({"value":-1});

while(it.hasNext()){
    var obj = it.next();
    print(obj._id+"\t"+obj.value);
}
