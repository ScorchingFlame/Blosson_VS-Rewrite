function sort_object(obj) {
  items = Object.keys(obj).map(function(key) {
      return [key, obj[key]];
  });
  items.sort(function(first, second) {
      return second[1] - first[1];
  });
  sorted_obj={}
  items.forEach(items, function(k, v) {
      use_key = v[0]
      use_value = v[1]
      sorted_obj[use_key] = use_value
  })
  return(sorted_obj)
} 


dict = {
  "x" : 1,
  "y" : 6,
  "z" : 9,
  "a" : 5,
  "b" : 7,
  "c" : 11,
  "d" : 17,
  "t" : 3
};

sort_object(dict)
