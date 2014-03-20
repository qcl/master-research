/*
 * result.target.properties.number
 * */

for(var i=0;i<=2410;i+=10){
    var count = db.result.target.properties.number.find({"value":{ $gte:i, $lt: i+10}}).count();
    print(i+"\t"+count);
}
