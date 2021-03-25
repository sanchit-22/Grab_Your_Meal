console.log("sss")
function san(){
    return 8
}
function load() {
    var list = [];
    var keyArray = ["one","two"];
  for (var i = 0; i < keyArray.length; i++) {
        var item = localStorage.getItem(keyArray[i]);
       if (item.charAt(0) == "+") {
            item = parseFloat(item.substring(1));
      }
        list.push(item);
  }
    return list;
}
var itemArray = [];
var abc=san()
console.log(abc)
myArray = load();
console.log(myArray[0],myArray[1])
console.log("sdfds")
var result = sessionStorage.getItem('sessionName');
console.log(result)